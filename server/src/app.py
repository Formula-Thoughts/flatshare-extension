import json
import uuid
import boto3
from botocore.exceptions import ClientError

BUCKET = 'flatini-blob-db'


def lambda_handler(event, context):
    route = event['routeKey']

    s3_client = boto3.client('s3')

    default_headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Methods': '*'
    }

    routes = {
        'POST /groups': lambda data_client, x: create_group(data_client, x),
        'GET /groups/{group_id}': lambda data_client, x: get_group(data_client, x),
        'POST /groups/{group_id}/flats': lambda data_client, x: create_flat(data_client, x),
        'DELETE /groups/{group_id}/flats/{flat_id}': lambda data_client, x: delete_flat(data_client, x)
    }

    try:
        (response, status) = routes[route](s3_client, event)
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


def create_group(data_client, event) -> (dict, int):
    if not is_body_valid_json(event['body']):
        return ({'message': 'body is invalid json'}, 400)

    body = json.loads(event['body'])
    if not validate_group_body(body):
        return {'message': 'required fields missing from body'}, 400
    id, code = generate_group_id_and_code(data_client)
    group = {
        'id': str(id),
        'name': body['name'],
        'code': code,
        'flats': []
    }
    data_client.put_object(Bucket=BUCKET,
                           Key=f'groups/{str(id)}',
                           Body=json.dumps(group),
                           ContentType='application/json', )

    return {'id': str(id)}, 201


def create_flat(data_client, event) -> (dict, int):
    if not is_body_valid_json(event['body']):
        return ({'message': 'body is invalid json'}, 400)

    body = json.loads(event['body'])
    if not validate_flat_body(body):
        return {'message': 'required fields missing from body'}, 400
    (get_group_response, status) = get_group(data_client, event)
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


def delete_flat(data_client, event) -> (dict, int):
    (get_group_response, get_group_status) = get_group(data_client, event)
    if get_group_status == 404:
        return get_group_response, get_group_status

    (get_flat_response, get_flat_status) = get_flat(data_client, event)
    if get_flat_status == 404:
        return get_flat_response, get_flat_status

    get_group_response['flats'] = list(filter(lambda x: x['id'] != event['pathParameters']['flat_id'], get_group_response['flats']))
    data_client.put_object(Bucket=BUCKET,
                           Key=f'groups/{get_group_response["id"]}',
                           Body=json.dumps(get_group_response),
                           ContentType='application/json', )

    return None, 204


def get_group(data_client, event) -> (dict, int):
    group_id = event['pathParameters']['group_id']
    try:
        group = data_client.get_object(Bucket=BUCKET,
                                       Key=f'groups/{str(group_id)}')['Body'].read()
        return json.loads(group), 200
    except ClientError:
        return {'message': f'group {group_id} not found'}, 404


def get_flat(data_client, event) -> (dict, int):
    (group, _) = get_group(data_client, event)
    results = list(filter(lambda x: x['id'] == event['pathParameters']['flat_id'], group['flats']))
    if len(results) == 0:
        return {'message': f'flat with id {event["pathParameters"]["flat_id"]} does not exist'}, 404
    else:
        return ({}, 200)


def is_body_valid_json(body) -> bool:
    try:
        json.loads(body)
        return True
    except:
        return False


def validate_group_body(body) -> bool:
    if 'name' in body:
        return True
    else:
        return False


def validate_flat_body(body) -> bool:
    if 'url' in body and 'price' in body and 'title' in body:
        return True
    else:
        return False
