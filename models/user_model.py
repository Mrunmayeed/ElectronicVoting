# models/user_model.py
from models.dynamo_client import dynamodb
from config import USERS_TABLE_NAME
import boto3

users_table = dynamodb.Table(USERS_TABLE_NAME)

def get_user(email):
    response = users_table.get_item(Key={'email': email})
    return response.get('Item')

def verify_user(email, password):
    user = get_user(email)
    return user if user and user['password'] == password else None

def get_weightage(user_id):
    response = users_table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('user_id').eq(user_id)
    )
    weightage = response.get('Items',[])[0].get('weightage',1)
    print(weightage)
    return weightage

