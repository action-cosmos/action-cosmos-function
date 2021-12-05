from .redis_client import redis_client
import logging
import azure.functions as func

MESSAGE_TYPE_KEY = "user:{}:options:message_type"
SLACK_WEBHOOK_URL_KEY = "user:{}:options:slack:webhook_url"
KAKAO_APP_KEY = "user:{}:options:kakaowork:app_key"
KAKAO_CHANNEL_ID_KEY = "user:{}:options:kakaowork:channel_id"

def main(req: func.HttpRequest) -> func.HttpResponse:
    request_body = req.get_json()

    message_type = request_body.get('message_type')
    user_token = req.headers.get('Authorization')

    if (message_type is None) or (user_token is None):
        return func.HttpResponse(status_code=400)

    validate_message_params(user_token, message_type, request_body)
    set_message_params(user_token, message_type, request_body)

    return func.HttpResponse(
        "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
        status_code=200
    )

def validate_message_params(user_token, message_type, data):
    if message_type == 'slack':
        slack_webhook_url = data['webhook_url']
        if slack_webhook_url is None:
            raise ValidateError
        redis_client.set(MESSAGE_TYPE_KEY.format(user_token), slack_webhook_url)
        redis_client.set(SLACK_WEBHOOK_URL_KEY.format(user_token), slack_webhook_url)

    elif message_type == 'kakaowork':
        kakao_app_key = data['app_key']
        kakao_channel_id = data['channel_id']

        if (kakao_app_key is None) or (kakao_channel_id is None):
            raise ValidateError
    else:
        raise ValidateError

def set_message_params(user_token, message_type, data):
    if message_type == 'slack':
        slack_webhook_url = data['webhook_url']

        redis_client.set(MESSAGE_TYPE_KEY.format(user_token), 'slack')
        redis_client.set(SLACK_WEBHOOK_URL_KEY.format(user_token), slack_webhook_url) 

    elif message_type == 'kakaowork':
        kakao_app_key = data['app_key']
        kakao_channel_id = data['channel_id']

        redis_client.set(MESSAGE_TYPE_KEY.format(user_token), 'kakaowork')
        redis_client.set(KAKAO_APP_KEY.format(user_token), kakao_app_key)
        redis_client.set(KAKAO_CHANNEL_ID_KEY.format(user_token), kakao_channel_id)

class ValidateError:
    pass
