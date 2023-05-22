import aiohttp
import json
from flask import current_app
async def send_message(data):
  headers = {
    "Content-type": "application/json",
    "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }
  async with aiohttp.ClientSession() as session:
    url = 'https://graph.facebook.com' + f"/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"
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

def get_text_message_input(recipient, text):
  return json.dumps({
    "messaging_product": "whatsapp",
    "preview_url": False,
    "recipient_type": "individual",
    "to": recipient,
    "type": "text",
    "text": {
        "body": text
    },

  })

def get_templated_message_input(recipient, resources):
  return json.dumps({
    "messaging_product": "whatsapp",
    "to": recipient,
    "type": "template",
    "template": {
      "name": "resources",
      "language": {
        "code": "en_US"
      },
      "components": [
        {
          "type": "header",
          "parameters": [
            {
              "type": "document",
              "document": {
                "filename": "data structures c programming.pdf",
                "link": resources['document']
              }
            }
          ]
        },
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "text": resources['author']
            },
            {
              "type": "text",
              "text": resources['topic']
            },
            {
              "type": "text",
              "text": resources['Rating']
            }
          ]
        }
      ]
    }
  })