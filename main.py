import socket
import time
import requests
import random
from datetime import datetime

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'brukinwagner'
token = 'oauth:91f98i9dxzjxtqfnfzwc2xqx1g0mhb'  # This should be in the format 'oauth:91f98i9dxzjxtqfnfzwc2xqx1g0mhb'
channel = '#steel'
client_id = 'gp762nuuoqcoxypju8c569th9wz7q5'
message_file = 'messages.txt'  # File containing the messages


def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"  # Specify the use of Markdown
    }
    response = requests.post(url, json=payload)
    return response.json()

# Function to check if the channel is live
def is_channel_live(client_id, token, channel_name):
    url = f'https://api.twitch.tv/helix/streams?user_login={channel_name}'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    return len(data.get('data', [])) > 0


# Function to send a message to the chat
def get_random_message(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        messages = file.readlines()
    return random.choice(messages).strip()

# Function to send a message to the chat
def send_chat_message(sock, message):
    # Encode the message as UTF-8 before sending
    sock.send(f"PRIVMSG {channel} :{message}\n".encode('utf-8'))


# Create a socket connection
sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

# Continuously check if the channel is live and send a random message
while True:
    try:
        if is_channel_live(client_id, token, channel.lstrip('#')):
            random_message = get_random_message(message_file)
            send_chat_message(sock, random_message)

            telegram_text = f"*🔴 Sent new message at {datetime.now()}:*\n\n```brukinwagner: {random_message}```"
            send_telegram_message('6815355380:AAFgWTOpdFo-4Eih-I5A3qWsI_VpT3-KUoQ', 799309399, telegram_text)

            print(f"Sent a message at {datetime.now()}")
        else:
            print(f"Channel is offline at {datetime.now()}")

        # Wait for 30 minutes before checking again
        time.sleep(1800)
    except:
        time.sleep(1800)
        pass
