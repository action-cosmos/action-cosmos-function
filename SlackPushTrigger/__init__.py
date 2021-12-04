from client.redis_client import redis_client
import json
import logging
import requests
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Slack push requested')

    user_token = req.get_json()['user_token']
    message = req.get_json()['message']

    if not user_token:
        return func.HttpResponse("필수 값이 없습니다", status_code=400)

    slack_webhook_url = redis_client().get("user:{}:options:slack:webhook_url".format(user_token))
    if slack_webhook_url is None:
        return func.HttpResponse(status_code=400)

    slack_webhook_url = slack_webhook_url.decode('utf-8')
    message_data = {
        "text": message
    }

    response = requests.post(slack_webhook_url, data = json.dumps(message_data))
    logging.info("1 response_code={} body={}".format(response.status_code, response.text))
    logging.info("message_data={}".format(message_data))
    if response.status_code != 200:
        logging.warn("response_code={} body={}".format(response.status_code, response.text))
        return func.HttpResponse(status_code=500)

    logging.info('Slack push done')
    data = {"message": "ok"}

    return func.HttpResponse(
        json.dumps(data), status_code=200
    )
