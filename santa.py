import time

import yaml
import csv
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SUBJECT = 'Тайный Санта'


def get_participants():
    with open('participants.csv', encoding="utf-8") as f:
        return [{k: v for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True, delimiter=';')]


def send_multiple(participants):
    session = smtplib.SMTP(config['host'], config['port'])
    session.starttls()
    session.login(config['user'], config['password'])

    def send(email, name, target):
        print(f"send: sent message to ${name} to email ${email}, your target is ${target}")
        message = MIMEMultipart()
        message['From'] = config['user']
        message['To'] = email
        message['Subject'] = SUBJECT

        replaced = template.replace('$name', name).replace('$target', target)
        message.attach(MIMEText(replaced, 'html'))

        text = message.as_string()

        session.sendmail(config['user'], email, text)
        time.sleep(3)

    for i, participant in enumerate(participants):
        target_idx = i + 1 if i < len(participants) - 1 else 0
        send(participant['email'], participant['name'], participants[target_idx]['name'])

    session.quit()


config = yaml.safe_load(open("smtp.yaml", "r"))['mail']['smtp']
template = open("template.html", "r", encoding="utf-8").read()
participants = get_participants()
random.shuffle(participants)
send_multiple(participants)
