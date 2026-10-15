import random
import json
import os
import time

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
SCORES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_scores.json")


def read_records():
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_records(records):
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=4)


def show_record(upper_limit):
    record = read_records().get(str(upper_limit))
    if record:
        print(f"Record: {record['score']} points ({record['name']})")
    else:
        print("No record yet for this level")


def check_record(upper_limit, name, score):
    records = read_records()
    key = str(upper_limit)
    old_record = records.get(key)

    if old_record is None or score < old_record["score"]:
        records[key] = {"name": name, "score": score}
        save_records(records)
        print(GREEN, "New Record!", RESET)


def calculate_score(remaining_attempts, duration, upper_limit):
    multipliers = {50: 1, 100: 2, 1000: 3}
    multiplier = multipliers[upper_limit]
    time_bonus = max(0, 300 - int(duration))
    return (remaining_attempts * 100 + time_bonus) * multiplier


def choose_difficulty():
    print(YELLOW, "\nChoose a difficulty level!", RESET)
    print("1 - Easy (1-50, 10 attempts)")
    print("2 - Medium (1-100, 7 attempts)")
    print("3 - Hard (1-1000, 10 attempts)")

    while True:
        choice = input("Your choice (1/2/3): ")
        if choice == "1":
            return 50, 10
        elif choice == "2":
            return 100, 7
        elif choice == "3":
            return 1000, 10
        print(RED, "Please enter 1, 2 or 3!", RESET)


def get_guess(previous_guesses, upper_limit):
    while True:
        raw_value = input("Your guess: ")

        try:
            guess = int(raw_value)
        except ValueError:
            print(RED, "Please enter a valid number!", RESET)
            continue
        if guess < 1 or guess > upper_limit:
            print(RED, f"The number must be between 1 and {upper_limit}!", RESET)
            continue
        if guess in previous_guesses:
            print(RED, "You already tried this number!", RESET)
            continue

        return guess


def play_game(name):
    upper_limit, attempts = choose_difficulty()
    show_record(upper_limit)
    number = random.randint(1, upper_limit)
    guesses = []

    print(CYAN, f"\nI picked a number between 1 and {upper_limit}. Guess it:", RESET)
    start_time = time.time()
    while attempts > 0:
        guess = get_guess(guesses, upper_limit)
        guesses.append(guess)
        if guess == number:
            duration = time.time() - start_time
            score = calculate_score(attempts, duration, upper_limit)
            print(GREEN, f"Congratulations {name}, you guessed it in {len(guesses)} tries and {duration:.1f} seconds",
                  RESET)
            print(CYAN, f"Your score: {score}", RESET)
            check_record(upper_limit, name, score)
            return
        elif guess < number:
            print(YELLOW, "Try a bigger number", RESET)
        else:
            print(YELLOW, "Try a smaller number", RESET)

        attempts -= 1

    print(RED, f"Out of attempts. The number I picked was {number}.", RESET)


name = input("What's your name? ").strip()
if name == "":
    name = "Player"
print(f"Hello {name}!")

while True:
    play_game(name)
    answer = input("\nWould you like to play again? (y/n) ").strip().lower()
    if answer != "y":
        print(CYAN, "Goodbye", RESET)
        break
