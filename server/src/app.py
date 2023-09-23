import json
import uuid
import boto3
from botocore.exceptions import ClientError

BUCKET = 'flatini-blob-db'
DELETE_FLAT_MESSAGE_TYPE = 'DELETE_FLAT'
CREATE_FLAT_MESSAGE_TYPE = 'CREATE_FLAT'
CREATE_GROUP_MESSAGE_TYPE = 'DELETE_GROUP'


def create_flat_event_handler(msg, data_client):
    group = data_client.get_object(Bucket=BUCKET,
                                   Key=f'groups/{str(msg["group_id"])}')['Body'].read()
    group['flats'].append({
        'id': msg['id'],
        'url': msg['url'],
        'title': msg['title'],
        'price': msg['price']
    })
    data_client.put_object(Bucket=BUCKET,
                           Key=f'groups/{msg["group_id"]}',
                           Body=json.dumps(group),
                           ContentType='application/json', )


def create_group_event_handler(msg, data_client):
    data_client.put_object(Bucket=BUCKET,
                           Key=f'groups/{msg["id"]}',
                           Body=json.dumps(msg),
                           ContentType='application/json')


def delete_flat_event_handler(msg, data_client):
    group = data_client.get_object(Bucket=BUCKET,
                                   Key=f'groups/{str(msg["group_id"])}')['Body'].read()
    group['flats'] = list(filter(lambda x: x['id'] != msg['id'], group['flats']))
    data_client.put_object(Bucket=BUCKET,
                           Key=f'groups/{msg["group_id"]}',
                           Body=json.dumps(group),
                           ContentType='application/json', )


def lambda_event_handler(event, context):
    handler_id = uuid.uuid4()
    # aws spins up multiple lambdas with batches of events
    for record in event['Records']:
        print(f"logging from handler {handler_id}")

        try:
            s3_client = boto3.client("s3")

            message_body = json.loads(record["body"])
            message_type = message_body['message_type']
            payload = message_body['payload']

            handlers = {
                CREATE_FLAT_MESSAGE_TYPE: lambda msg, data_client: create_flat_event_handler(msg, data_client),
                CREATE_GROUP_MESSAGE_TYPE: lambda msg, data_client: create_group_event_handler(msg, data_client),
                DELETE_FLAT_MESSAGE_TYPE: lambda msg, data_client: delete_flat_event_handler(msg, data_client)
            }

            handlers[message_type](message_body, s3_client)

            print(str(payload))
        except Exception as e:
            print(f"error occured in handler {handler_id} {str(e)}")


def lambda_api_handler(event, context):
    route = event['routeKey']

    s3_client = boto3.client('s3')
    sqs_client = boto3.client('sqs')
    flatini_queue = sqs_client.get_queue_url(QueueName='flatini-queue.fifo')

    default_headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Methods': '*'
    }

    routes = {
        'POST /groups': lambda data_client, queue_client, queue, x: api_create_group(data_client, queue_client, queue, x),
        'GET /groups/{group_id}': lambda data_client, queue_client, queue, x: api_get_group(data_client, queue_client,
                                                                                            queue, x),
        'POST /groups/{group_id}/flats': lambda data_client, queue_client, queue, x: api_create_flat(data_client,
                                                                                                     queue_client, queue,
                                                                                                     x),
        'DELETE /groups/{group_id}/flats/{flat_id}': lambda data_client, queue_client, queue, x: api_delete_flat(
            data_client, queue_client, queue, x)
    }

    try:
        (response, status) = routes[route](s3_client, sqs_client, flatini_queue, event)
        return {
            'statusCode': status,
            'body': json.dumps(response) if response is not None else "",
            'headers': default_headers
        }
    except Exception as e:
        print(f'error occured {str(e)}')

        return {
            'statusCode': 500,
            'body': '{\'message\': \'internal server error :(\'}',
            'headers': default_headers
        }


def lambda_handler(event, context):
    if 'routeKey' in event:
        return lambda_api_handler(event, context)

    if 'Records' in event:
        return lambda_event_handler(event, context)


def does_group_code_exist(data_client, group_id: str) -> bool:
    object_list_response = data_client.list_objects_v2(Bucket=BUCKET,
                                                       Prefix=f'groups/{group_id}')
    return object_list_response['KeyCount'] != 0


def generate_group_id_and_code(data_client) -> (uuid, str):
    id_has_been_generated = False
    (id, code) = (None, None)
    while not id_has_been_generated:
        group_id = uuid.uuid4()
        id_substring = str(group_id)[0:8]
        if not does_group_code_exist(data_client, id_substring):
            (id, code) = (group_id, id_substring.upper())
            id_has_been_generated = True
    return id, code


def api_create_group(data_client, queue_client, queue, event) -> (dict, int):
    if not is_body_valid_json(event['body']):
        return {'message': 'body is invalid json'}, 400

    id, code = generate_group_id_and_code(data_client)
    group = {
        'id': str(id),
        'code': code,
        'flats': []
    }
    send_create_group_message(group, queue_client, queue)

    return {'id': str(id)}, 201


def api_create_flat(data_client, queue_client, queue, event) -> (dict, int):
    if not is_body_valid_json(event['body']):
        return ({'message': 'body is invalid json'}, 400)

    body = json.loads(event['body'])
    if not validate_flat_body(body):
        return {'message': 'required fields missing from body'}, 400
    (get_group_response, status) = api_get_group(data_client, queue_client, queue, event)
    if status == 404:
        return get_group_response, status
    id = uuid.uuid4()
    get_group_response['flats'].append({
        'id': str(id),
        'url': body['url'],
        'title': body['title'],
        'price': body['price']
    })
    data_client.put_object(Bucket=BUCKET,
                           Key=f'groups/{get_group_response["id"]}',
                           Body=json.dumps(get_group_response),
                           ContentType='application/json', )

    return {'id': str(id)}, 201


def api_delete_flat(data_client, queue_client, queue, event) -> (dict, int):
    (get_group_response, get_group_status) = api_get_group(data_client, queue_client, queue, event)
    if get_group_status == 404:
        return get_group_response, get_group_status

    (get_flat_response, get_flat_status) = get_flat(get_group_response, data_client, queue_client, queue, event)
    if get_flat_status == 404:
        return get_flat_response, get_flat_status

    get_group_response['flats'] = list(
        filter(lambda x: x['id'] != event['pathParameters']['flat_id'], get_group_response['flats']))
    data_client.put_object(Bucket=BUCKET,
                           Key=f'groups/{get_group_response["id"]}',
                           Body=json.dumps(get_group_response),
                           ContentType='application/json', )

    return None, 204


def api_get_group(data_client, queue_client, queue, event) -> (dict, int):
    group_id = event['pathParameters']['group_id']
    try:
        group = data_client.get_object(Bucket=BUCKET,
                                       Key=f'groups/{str(group_id)}')['Body'].read()
        return json.loads(group), 200
    except ClientError:
        return {'message': f'group {group_id} not found'}, 404


def get_flat(group, data_client, queue_client, queue, event) -> (dict, int):
    results = list(filter(lambda x: x['id'] == event['pathParameters']['flat_id'], group['flats']))
    if len(results) == 0:
        return {'message': f'flat with id {event["pathParameters"]["flat_id"]} does not exist'}, 404
    else:
        return ({}, 200)


def send_sqs_message(message_group_id, payload: dict, queue_client, queue):
    queue_client.send_message(
        QueueUrl=queue['QueueUrl'],
        MessageBody=json.dumps(payload),
        MessageGroupId=message_group_id,
        MessageDeduplicationId=str(uuid.uuid4())
    )


def send_delete_flat_message(id, group_id, queue_client, queue):
    send_sqs_message(group_id, {
        'message_type': DELETE_FLAT_MESSAGE_TYPE,
        'payload': {
            'id': id
        }
    }, queue_client, queue)


def send_create_flat_message(flat_payload, group_id, queue_client, queue):
    send_sqs_message(group_id, {
        'message_type': CREATE_FLAT_MESSAGE_TYPE,
        'payload': flat_payload
    }, queue_client, queue)


def send_create_group_message(group_payload, queue_client, queue):
    send_sqs_message(group_payload['id'], {
        'message_type': CREATE_GROUP_MESSAGE_TYPE,
        'payload': group_payload
    }, queue_client, queue)


def is_body_valid_json(body) -> bool:
    try:
        json.loads(body)
        return True
    except:
        return False


def validate_flat_body(body) -> bool:
    if 'url' in body and 'price' in body and 'title' in body:
        return True
    else:
        return False
