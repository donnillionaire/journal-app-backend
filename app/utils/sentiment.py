
import os
import boto3
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# Initialize AWS Comprehend client
comprehend = boto3.client(
    "comprehend",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_S3_REGION_NAME")
)


def get_sentiment(text):
    """
    Analyze sentiment using AWS Comprehend.

    Args:
        text (str): The input text.

    Returns:
        str: The predicted sentiment (POSITIVE, NEGATIVE, NEUTRAL, or MIXED).
    """
    if not text:
        raise ValueError("Text input is required")

    response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    return response["Sentiment"]