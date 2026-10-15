# numberGuess

A terminal-based number guessing game with difficulty levels and a scoring system.

## How It Works

The program picks a random number between 1 and the upper limit of the difficulty level you choose. You try to guess the number before you run out of attempts. After each wrong guess, you're told whether the number is bigger or smaller than your guess.

## Difficulty Levels

| Level  | Range    | Attempts |
|--------|----------|----------|
| Easy   | 1-50     | 10       |
| Medium | 1-100    | 7        |
| Hard   | 1-1000   | 10       |

## Scoring

The score is calculated with the following formula:

```
score = (remaining_attempts * 100 + time_bonus) * level_multiplier
```

- **Time bonus:** `300 - elapsed_time` (capped at 300, 0 if negative)
- **Level multiplier:** Easy = 1, Medium = 2, Hard = 3

The highest score for each difficulty level is stored separately in `high_scores.json`.

## Running the Game

```bash
python number_guessing_game.py
```

**Requirements:** Python 3.x (no extra libraries needed)

## Files

- `number_guessing_game.py` — the game's source code
- `high_scores.json` — stores the high scores (created automatically, not included in the repo)
