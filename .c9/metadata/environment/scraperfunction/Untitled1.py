{"filter":false,"title":"Untitled1.py","tooltip":"/scraperfunction/Untitled1.py","undoManager":{"mark":7,"position":7,"stack":[[{"start":{"row":3,"column":0},"end":{"row":3,"column":1},"action":"insert","lines":["i"],"id":1},{"start":{"row":3,"column":1},"end":{"row":3,"column":2},"action":"insert","lines":["m"]},{"start":{"row":3,"column":2},"end":{"row":3,"column":3},"action":"insert","lines":["p"]},{"start":{"row":3,"column":3},"end":{"row":3,"column":4},"action":"insert","lines":["o"]},{"start":{"row":3,"column":4},"end":{"row":3,"column":5},"action":"insert","lines":["r"]},{"start":{"row":3,"column":5},"end":{"row":3,"column":6},"action":"insert","lines":["t"]},{"start":{"row":3,"column":6},"end":{"row":3,"column":7},"action":"insert","lines":[" "]},{"start":{"row":3,"column":7},"end":{"row":3,"column":8},"action":"insert","lines":["n"]}],[{"start":{"row":3,"column":7},"end":{"row":3,"column":8},"action":"remove","lines":["n"],"id":2}],[{"start":{"row":3,"column":7},"end":{"row":3,"column":8},"action":"insert","lines":["b"],"id":3},{"start":{"row":3,"column":8},"end":{"row":3,"column":9},"action":"insert","lines":["o"]},{"start":{"row":3,"column":9},"end":{"row":3,"column":10},"action":"insert","lines":["t"]}],[{"start":{"row":3,"column":7},"end":{"row":3,"column":10},"action":"remove","lines":["bot"],"id":4},{"start":{"row":3,"column":7},"end":{"row":3,"column":12},"action":"insert","lines":["boto3"]}],[{"start":{"row":3,"column":12},"end":{"row":4,"column":0},"action":"insert","lines":["",""],"id":5},{"start":{"row":4,"column":0},"end":{"row":5,"column":0},"action":"insert","lines":["",""]},{"start":{"row":5,"column":0},"end":{"row":5,"column":1},"action":"insert","lines":["d"]},{"start":{"row":5,"column":1},"end":{"row":5,"column":2},"action":"insert","lines":["u"]}],[{"start":{"row":5,"column":1},"end":{"row":5,"column":2},"action":"remove","lines":["u"],"id":6}],[{"start":{"row":5,"column":0},"end":{"row":5,"column":1},"action":"remove","lines":["d"],"id":7},{"start":{"row":5,"column":0},"end":{"row":40,"column":68},"action":"insert","lines":["import boto3","","# Get the service resource.","dynamodb = boto3.resource('dynamodb')","","# Create the DynamoDB table.","table = dynamodb.create_table(","    TableName='users',","    KeySchema=[","        {","            'AttributeName': 'username',","            'KeyType': 'HASH'","        },","        {","            'AttributeName': 'last_name',","            'KeyType': 'RANGE'","        }","    ],","    AttributeDefinitions=[","        {","            'AttributeName': 'username',","            'AttributeType': 'S'","        },","        {","            'AttributeName': 'last_name',","            'AttributeType': 'S'","        },","    ],","    ProvisionedThroughput={","        'ReadCapacityUnits': 5,","        'WriteCapacityUnits': 5","    }",")","","# Wait until the table exists.","table.meta.client.get_waiter('table_exists').wait(TableName='users')"]}],[{"start":{"row":3,"column":0},"end":{"row":3,"column":12},"action":"remove","lines":["import boto3"],"id":8},{"start":{"row":2,"column":3},"end":{"row":3,"column":0},"action":"remove","lines":["",""]}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":38,"column":27},"end":{"row":38,"column":27},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1605811040871,"hash":"2d4149213193c0c1464d8b16cb617e511dc0fe66"}