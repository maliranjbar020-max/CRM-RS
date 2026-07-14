import json
from melipayamak import Api


class PanelSender:

    def __init__(self):

        with open("config/settings.json", "r", encoding="utf-8") as f:
            config = json.load(f)

        self.username = config["melipayamak"]["username"]
        self.password = config["melipayamak"]["password"]
        self.sender = config["melipayamak"]["from"]

        api = Api(self.username, self.password)
        self.sms = api.sms()

    def send(self, numbers, text):

        if isinstance(numbers, str):
            numbers = [numbers]

        results = []

        for number in numbers:

            try:

                response = self.sms.send(
                    number,
                    self.sender,
                    text
                )

                print("RESPONSE:", response)
                results.append(response)

            except Exception as e:

                print("ERROR:", e)
                results.append(str(e))

        return results