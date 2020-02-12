import requests
import telebot
from time import sleep
#

TOKEN = '893266500:AAGFqFnbc74XdOi2TCDq7I5kV9S7SgTJ-og'

HEADERS = {"Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJjdG0iLCJleHAiOjE1ODA3NzU3Nzgs"
                            "Im9yaWdJYXQiOjE1ODA3NzU0Nzh9.HvbDshnMaAk3t-lEe5kMtY0Od_xG1PuJjZ9agO3FZis"}

EMPTY_TEXT = "Nada que mostrar..."


def run_api(query):
    request = requests.post('https://server.novadmin.dynu.net/', json={'query': query}, headers=HEADERS)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


nodes_query = """
query{
  nodes{
    edges{
      node{
        pk
        address
        nombre
        online
        rtt
      }
    }
  }
}
"""


def nodetext(node):
    text = "{address} ({rtt}) {nombre}".format(
        address=node['node']['address'], rtt=node['node']['rtt'],
        nombre=node['node']['nombre']
    )
    return text


def listener(messages):
    result = run_api(nodes_query)
    nodes = result['data']['nodes']['edges']

    for m in messages:
        chatid = m.chat.id
        if m.content_type == 'text':
            text = m.text
            text = text.lower()

            try:
                if text == "u":
                    data = [obj for obj in nodes if(obj['node']['online'])]
                    for node in data:
                        tb.send_message(chatid, text=nodetext(node=node))
                    if not data:
                        tb.send_message(chatid, text=EMPTY_TEXT)

                elif text == "d":
                    data = [obj for obj in nodes if (not obj['node']['online'])]
                    for node in data:
                        tb.send_message(chatid, text=nodetext(node=node))
                    if not data:
                        tb.send_message(chatid, text=EMPTY_TEXT)

                else:
                    tb.send_message(chatid, "No se reconoce el comando")

            except Exception as listener_ex:
                print(listener_ex)
                tb.send_message(chatid, listener_ex)


while True:
    try:
        tb = telebot.TeleBot(TOKEN, True, 4)
        tb.set_update_listener(listener)

        print("CONNECT OK")
        tb.polling()
        tb.polling(none_stop=True)
        tb.polling(interval=3)

        while True:
            sleep(1)

    except Exception as e:
        print(e)
        break
