import boto3
import uuid

def lambda_handler(event, context):
    # Get the text to translate from the event
    text_to_translate = event['text']
    
    # Get the source and target language codes from the event
    source_lang_code = event['source_language']
    target_lang_code = event['target_language']
    
    # Create a session and client for AWS Translate
    translate_client = boto3.client(service_name='translate', region_name='us-east-1')
    
    # Translate text using AWS Translate
    translation_response = translate_client.translate_text(
        Text=text_to_translate,
        SourceLanguageCode=source_lang_code,
        TargetLanguageCode=target_lang_code
    )
    
    # Get translated text and language codes
    translated_text = translation_response.get("TranslatedText")
    source_language_code = translation_response.get("SourceLanguageCode")
    target_language_code = translation_response.get("TargetLanguageCode")
    
    # Create a session and client for DynamoDB
    dynamodb_client = boto3.client('dynamodb')
    
    # Define the DynamoDB table name
    dynamodb_table_name = 'translate'
    
    # Generate a UUID for the ID attribute (primary key)
    id_value = str(uuid.uuid4())
    
    # Prepare item to be inserted into DynamoDB
    item = {
        'ID':{'S': id_value},
        'TextToTranslate': {'S': text_to_translate},
        'TranslatedText': {'S': translated_text},
        'SourceLanguageCode': {'S': source_language_code},
        'TargetLanguageCode': {'S': target_language_code}
    }
    
    # Put item into DynamoDB table
    dynamodb_client.put_item(
        TableName=dynamodb_table_name,
        Item=item
    )
    
    # Return the translated text and language codes
    return {
        'translated_text': translated_text,
        'source_language_code': source_language_code,
        'target_language_code': target_language_code
    }