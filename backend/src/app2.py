import json

try:
    from backend.src.core import Group
except Exception:
    from src.core import Group

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps(Group(price_limit=154.5, location="UK").__dict__)
    }
