import boto3

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Retrieve text from the event
    text = event['text']

    # Initialize AWS Comprehend client
    comprehend = boto3.client('comprehend')

    # Detect sentiment
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')

    # Save the response to DynamoDB
    dynamodb.put_item(
        TableName='sentimentAnalysis',
        Item={
            'Text': {'S': text},
            'Sentiment': {'S': response['Sentiment']},
            'SentimentScore': {'M': response['SentimentScore']}
        }
    )

    # Return the response
    return response