import json

from sms.phone_sender import PhoneSender
from sms.panel_sender import PanelSender


class SMSManager:

    def __init__(self):

        self.phone = PhoneSender()
        self.panel = PanelSender()

    def get_method(self):

        with open(
            "config/settings.json",
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        return data["sms_method"]

    def save_method(self, method):

        with open(
            "config/settings.json",
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        data["sms_method"] = method

        with open(
            "config/settings.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

    def send_sms(self, numbers, text):

        if self.get_method() == "panel":

            return self.panel.send(
                numbers,
                text
            )

        return self.phone.send(
            numbers,
            text
        )