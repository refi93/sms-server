#!/usr/bin/env python3
from time import sleep

import config
import db
from models import ReceivedMessage
from sms_apps.navigator import Navigator


sms_apps = [
    Navigator()
]


def handle(message):
    for sms_app in sms_apps:
        if (
            (message.phone_from in config.senders_whitelist)
            and sms_app.should_handle(message)
        ):
            sms_app.handle(message)


while True:
    new_messages = (
        db.query(ReceivedMessage)
        .filter(ReceivedMessage.processed_at.is_(None))
        .all()
    )

    for message in new_messages:
        handle(message)

    sleep(5)
    
