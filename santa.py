import itertools
import time

import yaml
import csv
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sortedcontainers import SortedDict

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


def order(participants):
    def count_score(order):
        score = 0
        for i, participant in enumerate(order):
            next = order[i + 1 if i + 1 < len(order) else 0]
            if participant['sex'] and next['sex'] and participant['sex'] != next['sex']:
                score += len(order)
            if participant['group'] and next['group'] and participant['group'] == next['group']:
                score -= len(order) ** 2 + 1
        return score

    def offer_order():
        copy = participants.copy()
        random.shuffle(copy)
        return copy

    scores_map = SortedDict()

    best_order = participants
    best_score = 0

    for _ in itertools.repeat(None, 100000):
        order = offer_order()
        score = count_score(order)

        scores_map[score] = scores_map.get(score, 0) + 1

        # names = [p['name'] for p in order]
        # print(score, names)

        if score > best_score:
            best_order = order
            best_score = score

    print('Scores distribution')
    for k in scores_map.keys():
        v = scores_map.get(k)
        print(f'{k} -> {v}')

    return best_order


config = yaml.safe_load(open("smtp.yaml", "r"))['mail']['smtp']
template = open("template.html", "r", encoding="utf-8").read()
participants = get_participants()
participants = order(participants)
for participant in participants:
    print(participant)

send_multiple(participants)
