"""
Your module description
"""

import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='deals',
    KeySchema=[
        {
            'AttributeName': 'brandname',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'posttime',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'brandname',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'posttime',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='deals')

# print out some data about the table.
print(table.item_count)