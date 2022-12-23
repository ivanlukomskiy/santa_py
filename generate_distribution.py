import csv
import itertools
import random

from sortedcontainers import SortedDict


def get_participants():
    with open('participants.csv', encoding="utf-8") as f:
        return [{k: v for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True, delimiter=';')]


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

        if score > best_score:
            best_order = order
            best_score = score

    print('Scores distribution')
    for k in scores_map.keys():
        v = scores_map.get(k)
        print(f'{k} -> {v}')

    return best_order


if __name__ == '__main__':
    participants = get_participants()
    participants = order(participants)
    with open("dist.txt", 'w') as file:
        for i, participant in enumerate(participants):
            target_idx = i + 1 if i < len(participants) - 1 else 0
            sender_tg = participant['telegram'].replace('https://t.me/', '')
            receiver_tg = participants[target_idx]['telegram'].replace('https://t.me/', '')
            file.write(f'{sender_tg},{receiver_tg}\n')
