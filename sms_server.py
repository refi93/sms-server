#!/usr/bin/env python3

import gsm_module
from sms_apps.navigator import Navigator
import config


sms_apps = [
    Navigator()
]


def handle_sms(sms_message):
    for sms_app in sms_apps:
        if (
            (sms_message["sender"] in config.senders_whitelist)
            and sms_app.should_handle(sms_message)
        ):
            gsm_module.send_sms_message(
                sms_message["sender"],
                sms_app.handle(sms_message)
            )


while True:
    sms_messages = gsm_module.get_sms_messages()

    if (len(sms_messages) > 0):
        print("new message arrived")

    for sms_message in sms_messages:
        handle_sms(sms_message)

    gsm_module.delete_all_sms_messages()
