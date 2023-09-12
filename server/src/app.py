def lambda_handler(event, context):
    return {
            "statusCode": 200,
            "body": "{\"field\": 2}",
            "headers": {"Content-Type": "application/json",
                        'Access-Control-Allow-Origin': "*",
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Methods": "*"}
    }