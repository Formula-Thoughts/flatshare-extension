import json
import uuid

import boto3
from botocore.client import BaseClient


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
        'GET /groups': lambda data_client, x: get_all_groups(data_client, x)
    }

    try:
        (response, status) = routes[route](s3_client, event)
        return {
            'statusCode': status,
            'body': json.dumps(response),
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
    id = uuid.uuid4()
    body = json.loads(event['body'])
    group = {
        'id': id,
        'name': body['name'],
        'code': body['code']
    }
    data_client.put_object(Bucket='flatini-blob-db',
                           Key=f'groups/{id}',
                           Body=json.dumps(group),
                           ContentType='application/json',)

    return group


def get_all_groups(data_client, event) -> (dict, int):
    return [
        {
            'id': uuid.uuid4(),
            'name': 'test1',
            'code': 12345
        },
        {
            'id': uuid.uuid4(),
            'name': 'test2',
            'code': 12346
        }
    ]
