import json
import boto3
import random
client = boto3.client('dynamodb')

def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    rNat = event['routeKey']
    listAll = client.scan(TableName = 'TODOs')['Items']
    user = event['headers']['user']
    if rNat == 'GET /todos':
        res = 'les tâches de: ' + user + '\n'
        for elem in listAll:
            if elem['user']['S'] == user:
                res += elem['taskId']['N'] + ' ' + elem['task']['S'] + '\n'
    elif rNat == 'DELETE /todos/{id}':
        taskNb = event['pathParameters']['id']
        res = 'vous ne pouvez pas supprimer la tâche.'
        for elem in listAll:
            if int(elem['taskId']['N']) == int(taskNb) and elem['user']['S'] == user:
                res = 'la tâche à supprimer est: ' + elem['taskId']['N'] + ' ' + elem['task']['S']
                client.delete_item( TableName='TODOs', Key={ 'taskId': { 'N': str(taskNb)}})
                break
    elif rNat == 'POST /todos':
        randId = random.getrandbits(15)
        client.put_item( Item={ 'taskId': { 'N': str(randId)}, 'user': { 'S': user}, 'task': { 'S': event['body']}}, TableName='TODOs')
        res = 'ajout de la tâche: ' + str(randId) + ' \'' + event['body'] + '\' s\'est fait avec succes.'
    return res
