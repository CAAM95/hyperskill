import random
import sys
import json
import datetime
from pathlib import Path
import os
import time
import shutil

class Data:
    def __init__(self,
                 player_name="",
                 temp_name="",
                 titanium_count=None,
                 locations=None,
                 shuffled_locations=None,
                 robot_count=None,
                 location_count=0,
                 current_save_dir="",
                 recorded_action="",
                 upgrades=None):

        self.player_name = player_name
        self.temp_name = temp_name
        self.locations = locations or []
        self.shuffled_locations = shuffled_locations or []
        self.location_count = location_count
        self.current_save_dir = current_save_dir
        self.recorded_action = recorded_action

        self._set_defaults(
            titanium_count=titanium_count,
            robot_count=robot_count,
            upgrades=upgrades
        )

    def _set_defaults(self, titanium_count=None, robot_count=None, upgrades=None):
        self.titanium_count = titanium_count if titanium_count is not None else 0
        self.robot_count = robot_count if robot_count is not None else 3

        self.upgrades = upgrades if upgrades is not None else {
            "titanium_scan": [False, 250],
            "enemy_encounter_scan": [False, 500],
            "new_robot": [False, 1000]
        }

    def reset_player(self,full=False):
        self._set_defaults()
        self.shuffled_locations.clear()
        self.location_count = 0

        if full:
            self.player_name = ""
            #self.locations.clear()



# Logic

def update_high_score(data):
    base_dir = BASE_DIR
    high_scores_json_path = base_dir / "high_scores.json"
    high_scores_txt_path = base_dir / "high_scores.txt"

    with open(high_scores_json_path, "r") as f:
        high_scores_json = json.load(f)

    # Update JSON only if player is valid
    if data.player_name:
        # for player in high_scores_json:
        #     if player["name"] == data.player_name:
        #         if data.titanium_count > player["titanium"]:
        #             player["titanium"] = data.titanium_count
        #             player["time"] = time.time()
        #         break
        # else:
        high_scores_json.append({
            "name": data.player_name,
            "titanium": data.titanium_count,
            "time": time.time()
        })

        high_scores_json.sort(
            key=lambda s: (-s["titanium"], s["time"])
        )
        high_scores_json = high_scores_json[:10]

        with open(high_scores_json_path, "w") as f:
            json.dump(high_scores_json, f, indent=4)

    # ALWAYS write TXT from JSON
    with open(high_scores_txt_path, "w") as f:
        if high_scores_json:
            f.write("HIGH SCORES\n\n")
            for i, player in enumerate(high_scores_json, start=1):
                f.write(f"({i}) {player['name']} {player['titanium']}\n")
        else:
            f.write("No scores")



def get_input():
    try:
        return input("Your command:\n").strip().lower()
    except EOFError:
        raise SystemExit  # terminate immediately so tests can clean up files




def gen_next_location(data):
    if len(data.shuffled_locations) >= data.location_count:
        return False

    location = random.choice(data.locations)
    titanium = random.randint(10, 100)
    encounter_rate = random.random()

    data.shuffled_locations.append({
        "name": location,
        "titanium": titanium,
        "encounter_rate": encounter_rate,
    })

    return True

def render_robots(robot, border, n: int) -> str:
    r = robot.strip("\n").splitlines()
    b = border.strip("\n").splitlines()

    robot_w = max(len(line.rstrip()) for line in r)
    border_w = max(len(line.rstrip()) for line in b)

    out_lines = []
    for rr, bb in zip(r, b):
        rr = rr.rstrip().ljust(robot_w)
        bb = bb.rstrip().ljust(border_w)

        line = ""
        for i in range(n):
            line += rr
            if i < n - 1:
                line += bb
        out_lines.append(line)

    return "\n".join(out_lines)

def create_save_slots(num_slots=3):
    base_dir = BASE_DIR

    for i in range(1, num_slots + 1):
        save_file = base_dir / f"save_file_{i}.json"
        if not save_file.exists():
            with open(save_file, "w") as f:
                json.dump([], f)

def create_high_score_txt():
    high_scores_file = BASE_DIR / "high_scores.txt"
    if not high_scores_file.exists():
        with open(high_scores_file, "w") as f:
            f.write("")

def create_high_scores_json():
    high_scores_file = BASE_DIR / "high_scores.json"
    if not high_scores_file.exists():
        with open(high_scores_file, "w") as f:
            json.dump([], f, indent=4)


def validate_dir_choice(data):
    display_saves()
    save_dir = BASE_DIR
    choice = get_input()

    if choice == "back":
        return display_main_menu

    # out of range check
    try:
        choice = int(choice)
    except ValueError:
        print("Invalid input")
        return validate_dir_choice

    if choice not in range(1, 4):
        print("Invalid input")
        return validate_dir_choice

    slot = f"save_file_{choice}.json"

    if data.recorded_action == "load":
        data.recorded_action = ""
        return load_save_slot(save_dir, slot, data)
    elif data.recorded_action == "save":
        store_save_slot(save_dir, slot, data)
        data.recorded_action = ""
        return display_log
    elif data.recorded_action == "save_exit":
        data.recorded_action = ""
        store_save_slot(save_dir, slot, data)
        return None

def store_save_slot(save_dir, slot, data):
    # if os.listdir(save_dir / slot):
    #     print("Slot not empty! are you sure you want to overwrite?\n\t[Yes] [No]")
    #     choice = get_input()
    #     if choice == "yes":
    #         pass
    #     elif choice == "no":
    #         return validate_dir_choice
    #     else:
    #         print("Invalid input")
    #         return validate_dir_choice

    json_data = create_json(data)
    with open(save_dir / slot, "w") as f:
        json.dump(json_data, f, indent=4)
    print("""
        |==============================|
        |    GAME SAVED SUCCESSFULLY   |
        |==============================|""")


def load_save_slot(save_dir, slot, data):
    # empty dir check
    with open(save_dir / slot, "r") as f:
        json_content = json.load(f)
    if not json_content:
        data.recorded_action = "load"
        print(f"Empty slot!")

        return validate_dir_choice

    save_slot = (save_dir / slot)
    json_file = json_content

    data.player_name = json_file["name"]
    data.titanium_count = json_file["titanium_balance"]
    data.robot_count = json_file["robot_count"]
    data.current_save_dir = save_slot
    data.upgrades = json_file["upgrades"]

    print("""
    |==============================|
    |    GAME LOADED SUCCESSFULLY  |
    |==============================|
    """)
    print(f"Welcome back, commander {data.player_name}!")

    return display_log

def get_json_file(path):
    if not path.exists():
        return None
    with open(path, "r") as f:
        return json.load(f)


def create_json(data):
    json_data = {
        "name": data.player_name,
        "titanium_balance": data.titanium_count,
        "robot_count": data.robot_count,
        "last_save": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "upgrades": data.upgrades
    }

    return json_data


def is_upgrade_enabled(data, upgrade_name):
    status = data.upgrades[upgrade_name][0]
    cost = data.upgrades[upgrade_name][1]
    remaining_titanium = data.titanium_count - cost
    if remaining_titanium >= 0:
        data.titanium_count -= cost
        data.upgrades[upgrade_name][0] = True
        return data.upgrades[upgrade_name][0]
    else:
        return data.upgrades[upgrade_name][0]

# UI
def display_upgrade_menu():
    print(f"""
   |================================|
   |          UPGRADE STORE         |
   |                         Price  |
   | [1] Titanium Scan         250  |
   | [2] Enemy Encounter Scan  500  |
   | [3] New Robot            1000  |
   |                                |
   | [Back]                         |
   |================================|
    """)

def display_saves():
    print("Select save slot:")
    base_dir = BASE_DIR

    save_files = sorted(base_dir.glob("save_file_*.json"))

    for i, save_file in enumerate(save_files, start=1):
        with open(save_file, "r") as f:
            json_content = json.load(f)

        if not json_content:
            print(f"[{i}] empty")
        else:
            name = json_content["name"]
            titanium = json_content["titanium_balance"]
            robots = json_content["robot_count"]
            last_save = json_content["last_save"]

            upgrades = json_content["upgrades"]
            upgrade_name = next((name for name, setting in upgrades.items() if setting[0] is True), None)
            print(f"[{i}] {name} Titanium: {titanium} Robots: {robots} Last Save: {last_save} Upgrade: {upgrade_name if upgrade_name else 'None'}")




def display_main_menu(data):
    data.recorded_action = ""
    options = ["new", "load", "high", "help", "exit"]

    intro = """+=======================================================================+
  ######*   ##*   ##*  #######*  ##*  ##*  #######*  ######*   #######*
  ##*  ##*  ##*   ##*  ##*       ##* ##*   ##*       ##*  ##*  ##*
  ##*  ##*  ##*   ##*  #######*  #####*    #####*    ######*   #######*
  ##*  ##*  ##*   ##*       ##*  ##* ##*   ##*       ##*  ##*       ##*
  ######*    ######*   #######*  ##*  ##*  #######*  ##*  ##*  #######*
                      (Survival ASCII Strategy Game)
+=======================================================================+\n"""
    print(intro)
    for i, option in enumerate(options):
        if option == "new" or option == "load":
            print(f"[{option.title()}] Game")
            continue
        if option == "high":
            print(f"[{option.title()}] Scores")
            continue
        print(f"[{option.title()}]")
    print()

    choice = get_input()

    if choice == "new":
        return handle_new_player
    elif choice == "load":
        return handle_load
    elif choice == "high":
        return handle_high_scores
    elif choice == "help":
        return handle_help
    elif choice == "exit":
        return None
    else:
        print("Invalid input")
        return display_main_menu

def display_submenu(data):
    sub_menu = """
    |==========================|
    |            MENU          |
    |                          |
    | [Back] to game           |
    | Return to [Main] Menu    |
    | [Save] and exit          |
    | [Exit] game              |
    |==========================|
    """
    print(sub_menu)
    choice = get_input()

    if choice == "back":
        return display_log
    elif choice == "main":
        return display_main_menu
    elif choice == "save":
        return handle_save_exit
    elif choice == "exit":
        return None

    print("Invalid input")
    return display_submenu


def display_log(data):
    robot = """
 $   $$$$$$$   $
 $$$$$     $$$$$
     $$$$$$$    
    $$$   $$$   
    $       $"""

    border = """
 |
 |
 |
 |
 | """

    menu = f"""
__________(LOG)__________________________________________________(LOG)__________
+==============================================================================+
{render_robots(robot, border, data.robot_count)}
+==============================================================================+
| Titanium: {data.titanium_count}                                                                 |
+==============================================================================+
|                  [Ex]plore                          [Up]grade                |
|                  [Save]                             [M]enu                   |
+==============================================================================+"""
    print(menu)
    choice = get_input()
    if choice == "ex":
        return handle_explore
    elif choice == "up":
        return handle_upgrade
    elif choice == "save":
        return handle_save
    elif choice == "m":
        return display_submenu
    else:
        print("Invalid input")
        return display_log


def display_visited_locations(data):
    print("Searching")
    for i, location in enumerate(data.shuffled_locations, start=1):
        parts = [location['name'].replace('_', ' ')]

        if data.upgrades["titanium_scan"][0]:
            parts.append(f"Titanium: {location['titanium']}")

        if data.upgrades["enemy_encounter_scan"][0]:
            parts.append(f"Encounter rate: {round(location['encounter_rate'] * 100)}%")

        print(f"[{i}] " + " ".join(parts))


    print("\n[S] Continue searching")
    return handle_explore_input


# Application
def handle_get_name(data):
    try:
        data.temp_name = input("Enter your name:\n")
    except EOFError:
        raise SystemExit
    print(f"Greetings, commander {data.temp_name}!")
    return handle_ready_check


def handle_ready_check(data):
    print("Are you ready to begin?\n\t[Yes] [No] Return to Main[Menu]")
    choice = get_input()

    if choice == "yes":
        data.reset_player(full=True)
        data.player_name = data.temp_name
        return display_log
    elif choice == "no":
        print("How about now.")
        return handle_ready_check
    elif choice == "menu":
        return display_main_menu
    else:
        print("Invalid input")
        return handle_ready_check


def handle_new_player(data):
    return handle_get_name

def handle_high_scores(data):
    high_scores_path = BASE_DIR / "high_scores.txt"
    with open(high_scores_path, "r") as f:
        print(f.read())
    print("\t[Back]")
    choice = get_input()

    if choice == "back":
        return display_main_menu
    else:
        print("Invalid input")
        return handle_high_scores


def determine_encounter_result(loc_encounter_rate):
    rand_num = random.random()
    if rand_num < loc_encounter_rate:
        return True
    return False

def handle_explore_input(data):
    while True:
        choice = get_input()

        try:
            idx = int(choice)
            if 1 <= idx <= len(data.shuffled_locations):
                print("Deploying robots...")
                entry = data.shuffled_locations[idx - 1]
                lost_robot = 0

                if determine_encounter_result(entry["encounter_rate"]):
                    print("Enemy encounter")
                    lost_robot = 1
                    data.robot_count -= lost_robot # one robot is lost

                if data.robot_count <= 0:
                    print("Game Over")
                    update_high_score(data)
                    return display_main_menu


                data.titanium_count += entry["titanium"]

                if lost_robot > 0:
                    print(f"{entry['name'].replace('_', ' ')} explored successfully, {lost_robot} robot lost..")
                else:
                    print(f"{entry['name'].replace('_', ' ')} explored successfully, with no damage taken.")
                print(f"Acquired {entry['titanium']} lumps of titanium.")

                return display_log
            else:
                print("Invalid selection.")
                continue
        except ValueError:
            pass

        if choice == "s":
            if not gen_next_location(data):
                print("Nothing more in sight.\n\t[Back]")
                continue
            return display_visited_locations
        elif choice == "back":
            return display_log
        else:
            print("Invalid input")
            continue



def handle_explore(data):
    data.location_count = random.randint(1, 9)
    data.shuffled_locations = []
    gen_next_location(data)
    return display_visited_locations

def handle_upgrade(data):
    display_upgrade_menu()
    choice = get_input()
    if choice == "back":
        return display_log
    elif choice == "1":
        if is_upgrade_enabled(data, "titanium_scan"):
            print("Purchase successful. You can now see how much titanium you can get from each found location.")
            return display_log
        else:
            print("Not enough titanium!")
            return handle_upgrade
    elif choice == "2":
        if is_upgrade_enabled(data, "enemy_encounter_scan"):
            print("Purchase successful. You will now see how likely you will encounter an enemy at each found location.")
            return display_log
        else:
            print("Not enough titanium!")
            return handle_upgrade
    elif choice == "3":
        if is_upgrade_enabled(data, "new_robot"):
            print("Purchase successful. You now have an additional robot")
            data.robot_count += 1
            data.upgrades["new_robot"][0] = False
            return display_log
        else:
            print("Not enough titanium!")
            return handle_upgrade
    else:
        print("Invalid input")
        return handle_upgrade

def handle_save(data):
    data.recorded_action = "save"
    return validate_dir_choice

def handle_save_exit(data):
    data.recorded_action = "save_exit"
    return validate_dir_choice

def handle_load(data):
    data.recorded_action = "load"
    return validate_dir_choice

def handle_help(data):
    print("WIP")
    return None

BASE_DIR = Path.cwd()
def main():

    seed = ""
    min_anim_duration = 0
    max_anim_duration = 0
    locations = "High_street,Green_park,Destroyed_Arch".split(',')

    if len(sys.argv) > 1:
        seed = sys.argv[1]
    if len(sys.argv) > 2:
        min_anim_duration = int(sys.argv[2])
    if len(sys.argv) > 3:
        max_anim_duration = int(sys.argv[3])
    if len(sys.argv) > 4:
        locations = sys.argv[4].split(',')

    if seed == "":
        random.seed()
    else:
        random.seed(seed)

    data = Data()
    data.locations = locations
    handler = display_main_menu

    create_save_slots()
    create_high_scores_json()
    create_high_score_txt()
    update_high_score(data)

    while handler:
        handler = handler(data)

    print("Goodbye.")

if __name__ == "__main__":
    main()
