import requests

class BrewersTeam:
    def __init__(self, sport_id, team_id, date):
        self.sport_id = sport_id
        self.team_id = team_id
        self.date = date
        self.data = None
        self.live_data = None

        url = "https://statsapi.mlb.com/api/v1/schedule"
        params = {
            "sportId": self.sport_id,
            "teamId": self.team_id,
            "date": self.date
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Request failed with status {response.status_code}")
        else:
            data = response.json()
            if data["totalGames"] == 0:
                print("No Brewers game today.")
            else:
                self.data = data

    def getscores(self):
        game = self.data["dates"][0]["games"][0]

        away_team = game["teams"]["away"]["team"]["name"]
        home_team = game["teams"]["home"]["team"]["name"]
        away_score = game["teams"]["away"].get("score", 0)
        home_score = game["teams"]["home"].get("score", 0)
        status = game["status"]["detailedState"]
        venue = game["venue"]["name"]

        print(f"{away_team} @ {home_team}")
        print(f"Venue: {venue}")
        print(f"Status: {status}")
        print(f"Score: {away_score} - {home_score}")
        if self.fetch_live_data():
            self.print_current_state()

    def __str__(self):
        return f"BrewersTeam tracker on {self.date}"

    def fetch_live_data(self):
        """Fetches the live feed once and stores it. Call this before using any get_current_* methods."""
        game = self.data["dates"][0]["games"][0]
        game_pk = game["gamePk"]

        live_url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
        live_response = requests.get(live_url)

        if live_response.status_code != 200:
            print(f"Live feed request failed with status {live_response.status_code}")
            return False

        self.live_data = live_response.json()
        return True

    def get_current_pitcher(self):
        linescore = self.live_data["liveData"]["linescore"]
        return linescore["defense"]["pitcher"]["fullName"]

    def get_current_batter(self):
        linescore = self.live_data["liveData"]["linescore"]
        return linescore["offense"]["batter"]["fullName"]

    def get_count(self):
        linescore = self.live_data["liveData"]["linescore"]
        return linescore["balls"], linescore["strikes"], linescore["outs"]

    def get_pitch_count(self):
        linescore = self.live_data["liveData"]["linescore"]
        pitcher_id = linescore["defense"]["pitcher"]["id"]
        defense_team_id = linescore["defense"]["team"]["id"]
        defense_side = "home" if self.live_data["gameData"]["teams"]["home"]["id"] == defense_team_id else "away"
        return self.live_data["liveData"]["boxscore"]["teams"][defense_side]["players"][f"ID{pitcher_id}"]["stats"][
            "pitching"]["numberOfPitches"]

    def print_current_state(self):
        """The formatter — calls the small getters and displays everything together."""
        status = self.data["dates"][0]["games"][0]["status"]["detailedState"]
        if status in ("Scheduled", "Pre-Game", "Warmup"):
            print(f"Game hasn't started yet ({status}).")
            return

        pitcher = self.get_current_pitcher()
        batter = self.get_current_batter()
        balls, strikes, outs = self.get_count()
        pitch_count = self.get_pitch_count()

        print(f"{pitcher} pitching to {batter} ({pitch_count} pitches)")
        print(f"Count: {balls}-{strikes}, {outs} out(s)")
        self.print_diamond()
        if status == "Final":
            event, description = self.get_final_play()
            print(f"Final play: {event} — {description}")
            return

    def get_final_play(self):
        plays = self.live_data["liveData"]["plays"]["allPlays"]
        last_play = plays[-1]
        return last_play["result"]["event"], last_play["result"]["description"]

    def get_runners(self):
        """Returns a list of occupied bases, e.g. ['2B'] or ['1B', '3B']"""
        offense = self.live_data["liveData"]["linescore"]["offense"]
        runners = []
        if "first" in offense:
            runners.append("1B")
        if "second" in offense:
            runners.append("2B")
        if "third" in offense:
            runners.append("3B")
        return runners

    def print_diamond(self):
        runners = self.get_runners()
        print(f"        {'[2B]' if '2B' in runners else ' -- '}")
        print(f"  {'[3B]' if '3B' in runners else ' -- '}       {'[1B]' if '1B' in runners else ' -- '}")
        print(f"        {'[H] '}")