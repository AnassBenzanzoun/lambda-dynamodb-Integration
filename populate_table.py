import uuid
import boto3
import csv
import json

# Read data from CSV file and convert to JSON
with open("users.csv", "r") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    json_data = json.dumps(rows)

# Parse the JSON data
data = json.loads(json_data)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("table-esame-AnassBenzanzoun")

# Iterate over the JSON data and insert each item into the table
for item in data:
    # Generate a UUID for the partition key
    user_uuid = str(uuid.uuid4())

    # Insert a new item into the table
    table.put_item(Item={"pk": user_uuid, **item})
