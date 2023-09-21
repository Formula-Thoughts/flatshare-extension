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
        'DELETE /groups/{group_id}/flats': lambda data_client, x: create_flat(data_client, x)
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


def create_group(data_client, event) -> (dict, int):
    body = json.loads(event['body'])
    if not validate_group_body(body):
        return {'message': 'required fields missing from body'}, 400
    id = uuid.uuid4()
    group = {
        'id': str(id),
        'name': body['name'],
        'code': body['code'],
        'flats': []
    }
    data_client.put_object(Bucket=BUCKET,
                           Key=f'groups/{str(id)}',
                           Body=json.dumps(group),
                           ContentType='application/json', )

    return group, 200


def create_flat(data_client, event) -> (dict, int):
    body = json.loads(event['body'])
    if not validate_flat_body(body):
        return {'message': 'required fields missing from body'}, 400
    (get_group_response, status) = get_group(data_client, event)
    if status == 404:
        return get_group_response, status
    get_group_response['flats'].append(body['flatUrl'])
    data_client.put_object(Bucket=BUCKET,
                           Key=f'groups/{get_group_response["id"]}',
                           Body=json.dumps(get_group_response),
                           ContentType='application/json', )

    return None, 201


def delete_flat(data_client, event) -> (dict, int):
    body = json.loads(event['body'])
    if not validate_flat_body(body):
        return {'message': 'required fields missing from body'}, 400
    (get_group_response, get_group_status) = get_group(data_client, event)
    if get_group_status == 404:
        return get_group_response, get_group_status
    (get_flat_response, get_flat_status) = get_flat(data_client, event)
    if get_flat_status == 404:
        return get_flat_response, get_flat_status

    get_group_response['flats'].remove(body['flatUrl'])
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
        return group, 200
    except ClientError:
        return {'message': f'group {group_id} not found'}, 404


def get_flat(data_client, event) -> (dict, int):
    (group, status) = get_group(data_client, event)
    body = json.loads(event['body'])
    results = list(filter(lambda x: x == body['flatUrl'], group['flats']))
    if len(results) == 0:
        return {'message': f'flat with url {body["flatUrl"]} does not exist'}, 404


def validate_group_body(body) -> bool:
    if 'code' in body and 'name' in body:
        return True
    else:
        return False


def validate_flat_body(body) -> bool:
    if 'flatUrl' in body:
        return True
    else:
        return False
