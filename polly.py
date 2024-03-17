import boto3
import os
import sys
from tempfile import gettempdir
from contextlib import closing

# Initialize S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Retrieve text from the event
    text = event['text']

    # Initialize AWS Polly client with the specified profile
    aws_mag_con = boto3.session.Session()
    polly_client = aws_mag_con.client(service_name="polly", region_name="us-east-1")

    # Synthesize speech
    response = polly_client.synthesize_speech(VoiceId='Joanna', OutputFormat='mp3', Text=text, Engine='neural')

    if "AudioStream" in response:
        with closing(response['AudioStream']) as stream:
            # Generate a unique S3 key
            s3_key = f"audio/{text[:20].replace(' ', '_')}.mp3"  # Example key generation

            # Upload the audio stream to S3
            try:
                s3.put_object(Body=stream.read(), Bucket='t2converter', Key=s3_key)
            except Exception as e:
                print("Error uploading audio to S3:", e)
                return {"statusCode": 500, "body": "Error uploading audio to S3"}
    else:
        print("Could not find the stream!")
        return {"statusCode": 500, "body": "Audio stream not found"}

    # Return S3 key of the uploaded audio file
    return {"statusCode": 200, "body": s3_key}
