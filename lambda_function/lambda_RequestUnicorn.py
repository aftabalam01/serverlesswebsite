import json
import boto3
import secrets
from datetime import datetime 
import random
import string
import urllib.parse


randomBytes=secrets.token_urlsafe(16)

awsclient = boto3.client('dynamodb')

fleet = [
    {
        "Name": 'Bucephalus',
        "Color": 'Golden',
        "Gender": 'Male',
    },
    {
        "Name": 'Shadowfax',
        "Color": 'White',
        "Gender": 'Male',
    },
    {
        "Name": 'Rocinante',
        "Color": 'Yellow',
        "Gender": 'Female',
    },
]
def recordRide(rideId, username, unicorn):
    res = awsclient.put_item(
        TableName ='Rides',
        Item = {
            'RideId': {'S':rideId},
            'User': {'S':username},
            'Unicorn': {'M':{"Name":{"S":unicorn['Name']},"Color":{"S":unicorn['Color']},"Gender":{"S":unicorn['Gender']}}},
            'UnicornName': {'S':unicorn['Name']},
            'RequestTime': {'S':datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')},
        }) 
    return res
def errorResponse(errormessage,awsRequestId):
    return {
    "statusCode": 500,
    "body": json.dumps({
      "Error": errormessage,
      "Reference": awsRequestId,
    }),
    "headers": {
      'Access-Control-Allow-Origin': '*',
    },
  }

def findUnicorn(pickupLocation):
    print(f"Finding unicorn for {pickupLocation['Latitude']}, {pickupLocation['Longitude']}")
    return random.choice(fleet)

def lambda_handler(event, context):
    if (not event.get('requestContext').get('authorizer')):
        errorResponse('Authorization not configured', context.get('awsRequestId'))
        return
    rideId = randomBytes
    print(f'Received event (, {rideId}, ): , {event}')
  
    username = event['requestContext']['authorizer']['claims']['cognito:username']
    requestBody = event['body']
    pickupLocation = requestBody['PickupLocation']
    unicorn = findUnicorn(pickupLocation)
    res = recordRide(rideId, username, unicorn)
    responseCode = res['ResponseMetadata']['HTTPStatusCode']
    if responseCode !=200:
        errorResponse(res['code not save recordRide','ResponseMetadata']['RequestId'])
        
    return {
            "statusCode": 201,
            "body": json.dumps({
                "RideId": rideId,
                "Unicorn": unicorn,
                "UnicornName": unicorn['Name'],
                "ETA": '30 seconds',
                "Rider": username,
            }),
            "headers": {
                'Access-Control-Allow-Origin': '*',
            },
        }
    