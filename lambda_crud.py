import boto3
import json

dynamodb = boto3.resource("dynamodb")


def lambda_handler(event, context):
    table = dynamodb.Table("table-esame-AnassBenzanzoun")

    # UPDATE
    if (
        event.get("httpMethod") == "PUT"
        and "body" in event
        and "pathParameters" in event
    ):
        item = json.loads(event["body"])
        pk = event["pathParameters"]["pk"]
        expression = "SET " + ", ".join(f"{k}=:{k}" for k in item.keys())
        table.update_item(
            Key={"pk": pk},
            UpdateExpression=expression,
            ExpressionAttributeValues={f":{k}": v for k, v in item.items()},
            ReturnValues="UPDATED_NEW",
        )
        return {"statusCode": 200, "body": json.dumps("Item updated.")}

    else:
        return {"statusCode": 400, "body": json.dumps("Invalid request.")}


import boto3
import json
import uuid

dynamodb = boto3.resource("dynamodb")


def lambda_handler(event, context):
    table = dynamodb.Table("table-esame-AnassBenzanzoun")

    # CREATE
    print(event["httpMethod"])
    print(event["body"])
    if event.get("httpMethod") == "POST" and event.get("body"):
        print(event)
        item = json.loads(event["body"])
        item["pk"] = str(uuid.uuid4())
        table.put_item(Item=item)
        return {"statusCode": 200, "body": json.dumps("Item created.")}

    else:
        return {"statusCode": 400, "body": json.dumps("Invalid request.")}


import boto3
import json

dynamodb = boto3.resource("dynamodb")


def lambda_handler(event, context):
    table = dynamodb.Table("table-esame-AnassBenzanzoun")

    pk = event["queryStringParameters"]["pk"]
    table.delete_item(Key={"pk": pk})
    return {"statusCode": 200, "body": json.dumps("Item deleted.")}


import boto3
import json
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")


def lambda_handler(event, context):
    table = dynamodb.Table("table-esame-AnassBenzanzoun")

    # SCAN
    if "queryStringParameters" not in event or not event["queryStringParameters"]:
        response = table.scan()
        return {"statusCode": 200, "body": json.dumps(response["Items"])}

    # READ GET ITEM
    elif "Service" in event["queryStringParameters"]:
        Service = event["queryStringParameters"]["Service"]
        response = table.scan(FilterExpression=Attr("Service").eq(Service))

        items = response["Items"]
        return {"statusCode": 200, "body": json.dumps(items)}

    else:
        return {"statusCode": 400, "body": json.dumps("Invalid request.")}
