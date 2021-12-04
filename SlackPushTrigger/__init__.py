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

    slack_webhook_url = ""
    # TODO: DB에서 user_token에 맞는 slack_webhook_url을 가져온다

    message_data = {
        "text": message
    }

    response = requests.post(slack_webhook_url, data = json.dumps(message_data))
    logging.info("reponse_code={} body={}".format(response.status_code, response.text))
    logging.info("message_data={}".format(message_data))
    if response.status_code != 200:
        logging.warn("reponse_code={} body={}".format(response.status_code, response.text))
        return func.HttpResponse(status_code=500)

    data = {"message": "ok"}
    return func.HttpResponse(
        json.dumps(data), status_code=200
    )
