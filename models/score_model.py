# models/score_model.py
import boto3
from models.dynamo_client import dynamodb
from config import SCORES_TABLE_NAME
from datetime import datetime

scores_table = dynamodb.Table(SCORES_TABLE_NAME)

def save_score(performance_id, judge_id, category_scores):

    # response = scores_table.get_item(
    #         Key={
    #             'performance_id': performance_id,
    #             'user_id': judge_id
    #         }
    #     )
    # if 'Item' in response:
    #     per = response.get('Items',[])[0]
    #     final_category_scores = per['category_scores'].append(category_scores)
    #     scores_table.update_item(
    #     Key={'performance_id': performance_id},
    #     UpdateExpression="SET category_scores = :s",
    #     ExpressionAttributeValues={
    #         ':s': final_category_scores
    #     }
    # )

    # else:
    scores_table.put_item(
        Item={
            "performance_id": performance_id,
            "user_id": judge_id,
            "category_scores": category_scores,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

def get_scores_for_performance(performance_id):
    response = scores_table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('performance_id').eq(performance_id)
    )
    # performances_scores = response.get('Items', [])[0]
    # cumulative_scores = {f"Category_{i}": 0 for i in range(1, 6)}
    # for p in performances_scores:
    #     for k,v in p.items():
    #         cumulative_scores[k] += v

    return response.get('Items', [])

