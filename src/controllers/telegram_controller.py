import requests
import logging
import json
from flask import request
from typing import Dict

from src.utils import getenv
from src.blueprints.telegram import telegram_bp
from src.services.job_application_service import JobApplicationService


@telegram_bp.route('/{}'.format(getenv('TELEGRAM_BOT_TOKEN')), methods=['POST'])
def respond(jas: JobApplicationService):
    content = request.json

    logging.info(content)

    chat_id = content['message']['chat']['id']
    message_id = content['message']['message_id']
    message_text = content['message']['text']

    job_description_json = jas._minimize_job_description(message_text)

    _send_code(
        chat_id=chat_id,
        title=f'Job Description as JSON: {message_text}',
        data=job_description_json,
        reply_to=message_id
    )

    cover_letter = jas.generate_cover_letter(job_description_json)

    logging.info(cover_letter)

    return _send_message(
        chat_id=chat_id,
        text=cover_letter[1],
        reply_to=message_id
    )


@telegram_bp.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    response = _execute_method('setWebhook', {
        'url': getenv('TELEGRAM_HOST_URL') + getenv('TELEGRAM_BOT_TOKEN')
    })
    return response


def _execute_method(method, data=None):
    base_api_url = getenv('TELEGRAM_API_BASE_URL') + getenv('TELEGRAM_BOT_TOKEN')
    api_url = f'{base_api_url}/{method}'

    if data is None:
        response = requests.get(api_url)
    else:
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(api_url, headers=headers, json=data)

    return response.json()


def _send_message(chat_id: int, text: str, reply_to: int = None):
    return _execute_method(
        method='sendMessage',
        data={
            'chat_id': chat_id,
            'text': text,
            'reply_to_message_id': reply_to,
        }
    )


def _send_code(chat_id: int, data: Dict, title: str = None, reply_to: int = None):
    json_str = json.dumps(data, indent=2)

    text = f'{title}\n```{json_str}```' if title else f'```{json_str}```'

    return _execute_method(
        method='sendMessage',
        data={
            'chat_id': chat_id,
            'text': text,  # Use the text with the title (if provided) and the code
            'parse_mode': 'MarkdownV2',  # Use Markdown parse mode
            'reply_to_message_id': reply_to,
        }
    )
