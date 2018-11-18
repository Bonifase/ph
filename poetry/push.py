import os
import logging

from pywebpush import webpush, WebPushException


logger = logging.getLogger(__name__)

VAPID_CLAIMS = {
    "sub": "mailto:youremail"
}


def send_web_push(subscription_information, message_body):
    try:
        webpush(
            subscription_info=subscription_information,
            data=message_body,
            vapid_private_key=os.getenv("VAPID_PRIVATE_KEY"),
            vapid_claims=VAPID_CLAIMS
        )
    except WebPushException as exception:
        logger.error(exception)
