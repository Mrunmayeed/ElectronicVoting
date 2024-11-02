# models/performer_model.py
from models.dynamo_client import dynamodb
from datetime import datetime
from config import PERFORMERS_TABLE_NAME
import boto3

performers_table = dynamodb.Table(PERFORMERS_TABLE_NAME)

def create_performer(performance_id):
    """Creates a new performer entry with voting inactive by default."""
    performers_table.put_item(
        Item={
            "performance_id": performance_id,
            "is_voting_active": False,
            "cumulative_scores": {f"Category_{i}": 0 for i in range(1, 6)},
            "performance_date": datetime.utcnow().isoformat()
        }
    )
    per = get_performer(performance_id)
    print(f'per::{per}')
    return per

def update_voting_status(performance_id, is_voting_active):
    """Updates the voting status for a performer."""
    performers_table.update_item(
        Key={'performance_id': performance_id},
        UpdateExpression="SET is_voting_active = :v",
        ExpressionAttributeValues={':v': is_voting_active}
    )
    print(f'updating status for {performance_id}')

def update_cumulative_scores(performance_id, cumulative_scores):
    """Stores the cumulative scores after voting ends."""
    performers_table.update_item(
        Key={'performance_id': performance_id},
        UpdateExpression="SET cumulative_scores = :s, is_voting_active = :v",
        ExpressionAttributeValues={
            ':s': cumulative_scores,
            ':v': False
        }
    )
    print('updated_cumulative')

def get_performer(performance_id):
    """Retrieves a performer by ID."""
    response = performers_table.get_item(Key={'performance_id': performance_id})
    return response.get('Item')

def get_active_performers():
    """Fetch all performers with voting active."""
    response = performers_table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('is_voting_active').eq(True),
        ProjectionExpression="performance_id"
    )
    active_performers = [i['performance_id'] for i in response.get('Items', [])]
    return active_performers



