from client.redis_client import redis_client
import json
import logging
import requests
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Complete forwarding requested')

    user_token = req.get_json()['user_token']

    if not user_token:
        return func.HttpResponse("필수 값이 없습니다", status_code=400)

    message_type = redis_client().get("user:{}:options:message_type".format(user_token)).decode('utf-8')

    message_type_data = {
        "user_token": user_token,
        "message": user_token
    }
    
    url_slack = 'https://functionapp-slacktrigger-westus3.azurewebsites.net/api/SlackPushTrigger'
    # url_kakaowork = 


    if message_type == 'slack':
        response = requests.post(url_slack, data = json.dumps(message_type_data))
    # elif message_type == 'kakaowork':
    #     response = requests.post(url_kakaowork, data = json.dumps(message_type_data))

    if response.status_code != 200:
        logging.warn("response_code={} body={}".format(response.status_code, response.text))
        return func.HttpResponse(status_code=500)

    logging.info('Complete forwarding done')
    data = {"message": "ok"}

    return func.HttpResponse(
        json.dumps(data), status_code=200
    )