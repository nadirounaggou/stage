import json

print('Loading function')

#3 operation possible : +, -, *
def lambda_handler(event, context):
    elem1 = int(event['queryStringParameters']['a'])
    elem2 = int(event['queryStringParameters']['b'])
    op = event['queryStringParameters']['op']
    if op == ' ':
        result = elem1 + elem2
    elif op == '-':
        result = elem1 - elem2
    else:
        result = elem1 * elem2
    result = 'le resultat est :' + str(result)
    return {
        "statusCode": 200,
        "body": json.dumps(result),
    }
