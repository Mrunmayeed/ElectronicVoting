# Test connection by listing tables
import boto3
from config import AWS_REGION, AWS_ACCESS_KEY, AWS_SECRET_KEY

dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)
# print(dynamodb)
def list_tables():
    try:
        tables = list(dynamodb.tables.all())
        print("Tables:", [table.name for table in tables])
    except Exception as e:
        print("Error connecting to DynamoDB:", e)


list_tables()