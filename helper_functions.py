import random

def shuffle_and_pick(group, count):
    random.shuffle(group)
    return group[:count]

def roll_dice(sides=6, times=1):
    return [random.randint(1, sides) for _ in range(times)]
