# config.py
import os

AWS_REGION = "us-west-1"
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
USERS_TABLE_NAME = "Users"
SCORES_TABLE_NAME = "Scores"
PERFORMERS_TABLE_NAME = "Performers"
