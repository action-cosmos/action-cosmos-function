from client.redis_client import redis_client
import json
import logging
import requests
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Complete forwarding requested')

    option = req.get_json()['option']
    message_type = req.get_json()['message_type']

    if not message_type:
        return func.HttpResponse("필수 값이 없습니다", status_code=400)
    
