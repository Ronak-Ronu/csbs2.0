import aiohttp
import json
from flask import current_app
import requests
from dotenv import load_dotenv
import os
load_dotenv()

APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
RECIPIENT_WAID = os.getenv('RECIPIENT_WAID')
VERSION = os.getenv('VERSION')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')


async def send_message(data):
  headers = {
    "Content-type": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
}
  async with aiohttp.ClientSession() as session:
    url = 'https://graph.facebook.com' + f"/{VERSION}/{PHONE_NUMBER_ID}/messages"
    try:
      async with session.post(url, data=data, headers=headers) as response:
        if response.status == 200:
          print("Status:", response.status)
          print("Content-type:", response.headers['content-type'])

          html = await response.json()
          print("Body:", html)
        else:
          print(response.status)        
          print(response)
    except aiohttp.ClientConnectorError as e:
      print('Connection Error', str(e))

def get_image_message_input(recipient,image):
  return json.dumps(
    {
  "messaging_product": "whatsapp",
  "preview_url": False,
  "recipient_type": "individual",
  "to": recipient,
  "type": "image",
  "image": {
    "link" : image
            },
  })
def get_text_message_input(recipient,text):
  return json.dumps(
  {
    "messaging_product": "whatsapp",
    "preview_url": False,
    "recipient_type": "individual",
    "to": recipient,
    "type": "text",
    "text": {
        "body": text
           }
})
