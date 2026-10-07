class CricketMatch:
    def __init__(self, batting_team, bowling_team):
        self.batting_team = batting_team
        self.bowling_team = bowling_team
        self.total_runs = 0
        self.wickets = 0
        self.balls_bowled = 0
        self.batsmen = {}  # {name: [runs, balls, 4s, 6s, is_out, wicket_type]}
        self.ball_history = []

    def add_batsman_if_not_exists(self, name):
        if name not in self.batsmen:
            # [runs, balls, 4s, 6s, is_out, wicket_type]
            self.batsmen[name] = [0, 0, 0, 0, False, ""]

    def play_match(self):
        print("\n" + "=" * 55)
        print(f" 🏏  LIVE CRICKET SCORER: {self.batting_team} vs {self.bowling_team}")
        print("=" * 55)
        print("Instructions: Enter ball-by-ball details. Type 'exit' to finish the match early.\n")

        while True:
            overs = self.balls_bowled // 6
            balls = self.balls_bowled % 6
            print(f"\n--------------------------------------------------")
            print(f" Current Score: {self.total_runs}/{self.wickets}  (Overs: {overs}.{balls})")
            print(f"--------------------------------------------------")

            striker = input("Enter Batsman Name: ").strip()
            if striker.lower() == 'exit':
                break
            if not striker:
                print("Please enter a valid name!")
                continue

            self.add_batsman_if_not_exists(striker)

            # Check if the batsman is already out
            if self.batsmen[striker][4]:
                print(f"⚠️ {striker} is already out! Please choose another batsman.")
                continue

            runs_input = input(f"Runs scored by {striker} (0, 1, 2, 3, 4, 6): ").strip()
            if not runs_input.isdigit():
                print("Please enter a valid number for runs!")
                continue
            
            runs = int(runs_input)
            if runs not in [0, 1, 2, 3, 4, 6]:
                print("Only 0, 1, 2, 3, 4, or 6 are allowed!")
                continue

            is_out_input = input("Is the batsman out? (yes / no): ").strip().lower()
            is_wicket = False
            wicket_type = ""

            if is_out_input in ['yes', 'y']:
                is_wicket = True
                wicket_type = input("How was he out? (e.g., Caught, Bowled, Run Out): ").strip()
                if not wicket_type:
                    wicket_type = "Out"

            # Update match data
            self.balls_bowled += 1
            self.total_runs += runs
            
            self.batsmen[striker][0] += runs
            self.batsmen[striker][1] += 1
            
            if runs == 4:
                self.batsmen[striker][2] += 1
            elif runs == 6:
                self.batsmen[striker][3] += 1
                
            ball_desc = f"{runs} Run(s)"
            if is_wicket:
                self.wickets += 1
                self.batsmen[striker][4] = True
                self.batsmen[striker][5] = wicket_type
                ball_desc = f"OUT! ({wicket_type})"

            self.ball_history.append({
                "ball_no": self.balls_bowled,
                "striker": striker,
                "description": ball_desc
            })

            # Stop if all 10 wickets are down
            if self.wickets >= 10:
                print("\n⚠️ All 10 wickets are down! Innings over.")
                break

        # Display scorecard when the match ends
        self.display_scorecard()

    def display_scorecard(self):
        overs = self.balls_bowled // 6
        balls = self.balls_bowled % 6
        
        print("\n" + "=" * 75)
        print(f" 🏆  MATCH SCORECARD: {self.batting_team} vs {self.bowling_team}")
        print("=" * 75)
        print(f" Total Score : {self.total_runs} / {self.wickets}")
        print(f" Total Overs : {overs}.{balls} Overs")
        print("-" * 75)
        print(f" {'Batsman':<15} | {'R':<4} | {'B':<4} | {'4s':<4} | {'6s':<4} | {'Status':<25}")
        print("-" * 75)
        
        for name, data in self.batsmen.items():
            runs, balls_faced, fours, sixes, is_out, w_type = data
            status = f"OUT ({w_type})" if is_out else "Not Out"
            print(f" {name:<15} | {runs:<4} | {balls_faced:<4} | {fours:<4} | {sixes:<4} | {status:<25}")
            
        print("-" * 75)
        print(" 📌 Ball-by-Ball History:")
        for b in self.ball_history:
            ov = (b['ball_no'] - 1) // 6
            bl = (b['ball_no'] - 1) % 6 + 1
            print(f" Over {ov}.{bl} -> {b['striker']} scored {b['description']}")
        print("=" * 75)


if __name__ == "__main__":
    b_team = input("Enter Batting Team Name: ")
    bow_team = input("Enter Bowling Team Name: ")
    
    match = CricketMatch(b_team, bow_team)
    match.play_match()
