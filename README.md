# Brewers Live Score & Stats Tracker

A Python command-line tool that pulls live game data for the Milwaukee Brewers using the MLB Stats API and the Live Game Feed API.  
It will display the score, current pitcher/batter, pitch count, at-bat count, number of outs, base runners and how the game ended.

## Features

- Fetches desired Brewers game (User can change date in main.py when the Class is called)
- Handles game states (Scheduled, Pre-Game, In-Progress, Final)
- Shows live at-bat details
- Displays base runners on a simple ASCII diamond
- Reports the final play when a game ends

## Tech

-Python 3.12
- [`requests`](https://pypi.org/project/requests/) for API calls
- MLB Stats API:
  - Schedule endpoint (`/api/v1/schedule`) — game info, teams, score
  - Live Game Feed endpoint (`/api/v1.1/game/{gamePk}/feed/live`) — real-time
    pitcher/batter, count, outs, base runners, and play-by-play

## Setup

\```
git clone https://github.com/Omgnoob1/project_brewers_tracker.git
cd project_brewers_tracker
pip install -r requirements.txt
\```

## Usage

my_team = BrewersTeam(sport_id=1, team_id=158, date="**2026-07-04**")
Change date to what you want, use YYYY-MM-DD Format.  Team_ID is set to Milwaukee Brewers (158), but can be changed if you know other Team #'s.
Sport ID should not be changed.

## Sample Output

```
BrewersTeam tracker on 2026-07-03
Milwaukee Brewers @ Arizona Diamondbacks
Venue: Chase Field
Status: Final
Score: 7 - 4
Grant Anderson pitching to Tommy Troy (20 pitches)
Count: 2-3, 3 out(s)
        --
  --         --
        [H]
Final play: Strikeout — Tommy Troy strikes out swinging.
```

## What I learned

Built my first python project, practiced working with real nested JSON APIs, class design & functions, handling real-world edge cases
like games that haven't started yet or have already ended.
