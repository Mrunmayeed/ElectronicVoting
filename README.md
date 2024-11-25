# ElectronicVoting
CS218 Midterm

pip install -r requirements.txt

export FLASK_APP=app.py
export FLASK_ENV=development
flask run
1. Create tables in DynamoDB (bill by usage)
    Users - email, user_id, password, role, weightage(optional)
    Scores - performance_id, user_id
        Also category_scores, timestamp
    Performers - performance_id
        Also cumulative_scores, is_voting_active

2. Create a user DynamoDBUser, give it access to policy: AmazonDynamoDBFullAccess

3. Create .env file:
FLASK_APP=app.py
FLASK_ENV=development
AWS_ACCESS_KEY="<your-aws-key>"
AWS_SECRET_KEY="<your-aws-secret>"
