# World Cup winner prediction
import csv
from itertools import combinations

# --- Groups ---

groups = {
    "A": ["Mexico", "South Korea", "Czech Republic", "South Africa"],
    "B": ["Switzerland", "Canada", "Qatar", "Bosnia & Herzegovina"],
    "C": ["Scotland", "Morocco", "Brazil", "Haiti"],
    "D": ["United States", "Australia", "Türkiye", "Paraguay"],
    "E": ["Germany", "Ivory Coast", "Ecuador", "Curaçao"],
    "F": ["Sweden", "Japan", "Netherlands", "Tunisia"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cabo Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Iraq", "Norway"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
    "L": ["England", "Croatia", "Ghana", "Panama"],
}

# --- Scoring model ---

lower_is_better = {"FIFA ranking", "Coach ranking", "Number of injuries"}

weights = {
    "Team strength": 3, "Team form": 2, "FIFA ranking": 2,
    "Keeper ranking": 1.5, "Defender ranking": 1.5,
    "Midfielder ranking": 1.5, "Forward ranking": 1.5,
    "Continental Cups": 1, "Coach ranking": 1, "Fan support": 1,
    "Players with World Cup experience": 1, "Number of injuries": 1,
    "Players in EPL": 1, "Players in La Liga": 0.5, "Players in Serie A": 0.5,
    "Players in Bundesliga": 0.5, "Players in Ligue 1": 0.5,
    "Players in other leagues": 0.1,
    "GOAT effect": 3,
}

def load_teams(filename):
    teams = {}
    with open(filename, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            name = row["Team"]
            teams[name] = {k: float(v) if v else 0.0 for k, v in row.items() if k != "Team"}
    return teams

teams = load_teams("teams.csv")

def matchup_score(team, opponent):
    total = 0
    for stat, weight in weights.items():
        a = team[stat]
        b = opponent[stat]
        if stat in lower_is_better:
            a = 1 / a if a else 0
            b = 1 / b if b else 0
        combined = a + b
        share = a / combined if combined else 0.5
        total += weight * share
    return total

def play(a, b):
    return a if matchup_score(teams[a], teams[b]) >= matchup_score(teams[b], teams[a]) else b

# --- Group stage ---

def group_standings(group):
    points      = {name: 0   for name in group}
    total_score = {name: 0.0 for name in group}
    for home, away in combinations(group, 2):
        s_home = matchup_score(teams[home], teams[away])
        s_away = matchup_score(teams[away], teams[home])
        total_score[home] += s_home
        total_score[away] += s_away
        if s_home > s_away:
            points[home] += 3
        elif s_away > s_home:
            points[away] += 3
        else:
            points[home] += 1
            points[away] += 1
    standings = sorted(group, key=lambda n: (points[n], total_score[n]), reverse=True)
    return standings, points, total_score

# Single pass: compute standings, print results, collect qualifiers and thirds
group_results = {}
for letter, group in groups.items():
    standings, points, total_score = group_standings(group)
    group_results[letter] = {"standings": standings, "points": points, "score": total_score}

print("=== Group Stage ===")
for letter, res in group_results.items():
    print(f"\n--- Group {letter} ---")
    for rank, name in enumerate(res["standings"], start=1):
        marker = " (qualifies)" if rank <= 2 else ""
        print(f"  {rank}. {name} - {res['points'][name]} pts{marker}")

winners = {g: r["standings"][0] for g, r in group_results.items()}
runners = {g: r["standings"][1] for g, r in group_results.items()}

# --- Best 8 third-placed teams ---

third_placed = []
for letter, res in group_results.items():
    third = res["standings"][2]
    third_placed.append({
        "team": third, "group": letter,
        "points": res["points"][third], "score": res["score"][third],
    })

third_placed.sort(key=lambda t: (t["points"], t["score"]), reverse=True)
best_eight = third_placed[:8]
eliminated = third_placed[8:]

print("\n=== Third-Placed Teams ===")
print("Qualifying:")
for rank, t in enumerate(best_eight, start=1):
    print(f"  {rank}. {t['team']} (Group {t['group']}) - {t['points']} pts, score {t['score']:.1f}")
print("Eliminated:")
for t in eliminated:
    print(f"  {t['team']} (Group {t['group']})")

third_by_group        = {t["group"]: t["team"] for t in best_eight}
qualified_third_groups = set(third_by_group)

# --- Assign thirds to winner slots ---
# Each slot can face a third from any group except its own (no same-group rematch).

_all_groups = list("ABCDEFGHIJKL")
_slot_names = ["A", "B", "C", "D", "E", "F", "I", "J"]
third_slots = {s: [g for g in _all_groups if g != s] for s in _slot_names}

def assign_thirds(slots, available_groups):
    slot_names = list(slots)
    assignment, used = {}, set()

    def backtrack(i):
        if i == len(slot_names):
            return True
        slot = slot_names[i]
        for g in slots[slot]:
            if g in available_groups and g not in used:
                assignment[slot] = g
                used.add(g)
                if backtrack(i + 1):
                    return True
                used.remove(g)
                del assignment[slot]
        return False

    if not backtrack(0):
        raise ValueError("No valid third-placed assignment for these qualifiers")
    return assignment

third_assignment = assign_thirds(third_slots, qualified_third_groups)

# --- Round of 32 ---

r32 = {}
for slot, third_group in third_assignment.items():
    r32[f"W{slot}"] = (winners[slot], third_by_group[third_group])

r32["GvH"] = (winners["G"], runners["H"])
r32["HvG"] = (winners["H"], runners["G"])
r32["KvL"] = (winners["K"], runners["L"])
r32["LvK"] = (winners["L"], runners["K"])
r32["AB"]  = (runners["A"], runners["B"])
r32["CD"]  = (runners["C"], runners["D"])
r32["EF"]  = (runners["E"], runners["F"])
r32["IJ"]  = (runners["I"], runners["J"])

print("\n=== Round of 32 ===")
r32_win = {}
for label, (a, b) in r32.items():
    r32_win[label] = play(a, b)
    print(f"  [{label}] {a} vs {b}  ->  {r32_win[label]}")

# --- Round of 16 ---

r16_bracket = [
    ("WA", "CD"),
    ("WB", "AB"),
    ("WC", "GvH"),
    ("WD", "EF"),
    ("WE", "HvG"),
    ("WF", "KvL"),
    ("WI", "IJ"),
    ("WJ", "LvK"),
]

print("\n=== Round of 16 ===")
r16_win = []
for l1, l2 in r16_bracket:
    a, b = r32_win[l1], r32_win[l2]
    w = play(a, b)
    r16_win.append(w)
    print(f"  {a} vs {b}  ->  {w}")

# --- Quarterfinals ---

def play_round(teams_in, round_name):
    print(f"\n=== {round_name} ===")
    out = []
    for i in range(0, len(teams_in), 2):
        a, b = teams_in[i], teams_in[i + 1]
        w = play(a, b)
        out.append(w)
        print(f"  {a} vs {b}  ->  {w}")
    return out

quarter_win = play_round(r16_win, "Quarterfinals")

# --- Semifinals (losers go to bronze match) ---

print("\n=== Semifinals ===")
finalists, bronze_match = [], []
for i in range(0, len(quarter_win), 2):
    a, b = quarter_win[i], quarter_win[i + 1]
    w = play(a, b)
    finalists.append(w)
    bronze_match.append(b if w == a else a)
    print(f"  {a} vs {b}  ->  {w}")

# --- Third-place playoff ---

print("\n=== Third-Place Playoff ===")
a, b = bronze_match
third_place = play(a, b)
print(f"  {a} vs {b}  ->  {third_place}")

# --- Final ---

print("\n=== Final ===")
a, b = finalists
champion = play(a, b)
runner_up = b if champion == a else a
print(f"  {a} vs {b}  ->  {champion}")

# --- Podium ---

print("\n========== FINAL STANDINGS ==========")
print(f"1st - Champion:    {champion}")
print(f"2nd - Runner-up:   {runner_up}")
print(f"3rd - Third place: {third_place}")
