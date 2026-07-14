import requests

url = "https://console.melipayamak.com/api/send/simple/697e13d1fb794c1896f7f8ddbf19acca"

data = {
    "from": "50004001196405",
    "to": "09120186187",
    "text": "سلام تست CRM\nلغو11"
}

response = requests.post(url, json=data)

print("STATUS:", response.status_code)
print("BODY:", response.text)