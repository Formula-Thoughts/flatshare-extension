import json
import uuid
import boto3


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
        'id': str(id),
        'name': body['name'],
        'code': body['code']
    }
    data_client.put_object(Bucket='flatini-blob-db',
                           Key=f'groups/{str(id)}',
                           Body=json.dumps(group),
                           ContentType='application/json',)

    return (group, 200)


def get_all_groups(data_client, event) -> (dict, int):
    response = data_client.list_objects_v2(Bucket='flatini-blob-db',
                                           Prefix='groups/')

    groups = []
    for obj in response['Contents']:
        groups.append(json.loads(data_client.get_object(Bucket='flatini-blob-db',
                                             Key=obj['Key'])['Body'].read()))

    print(groups)

    return (groups, 200)
