import random
from Objects import Sanitise, Power, Fuel
from PIL import Image
import os
num_modules = 17
module = 1
last_module = 0
possible_moves = []
alive = True
won = False
power = Power(100)
fuel = Fuel(500)
#flamethrower
locked = 0
queen = 0
vent_shafts = []
info_panels = []
workers = []
locked_modules = []
power_supplies = []

def menu():
    while True:
        start = options()
        if start == True:
            break

def options():
    while True:
        print("""1) Start
2) Rules
3) Quit""")
        option = input(">")
        option = option.strip()
        if option == "1":
            return True
        elif option == "2":
            rules()
            return False
        elif option == "3":
            exit(0)
        else:
            print("Invalid input.")

def rules():
    print("""The aim of the game is to defeat the alien queen.

To defeat the alien queen you need to lock her out of any escape routes and then attack her with your flamethrower.
Most actions will cost you power if you run out of power you die.
You can move between modules using the move command.
You can lock modules using the lock command.
The scanner opens a sub menu where you can access the map and check power as well as search for aliens.""")
    
def fight():
    global fuel, alive, won
    print()
    print("For maximum immersion imagine boss fight music")
    print()
    print("This is it the final battle if you lose it's all over.")
    print("You whack the Queen with the flame thrower")
    if fuel.get_fuel() < 100:
        print("Your flamethrower tickles the Queen. ACHOOO !!! The queen sneezes, her sneeze puts out your flame thrower.")
        print("The Queen absorbs you into the hive mind")
        alive = False
    else:
        print("Your flamethrower tickles the Queen. ACHOOO !!! The queen sneezes and the flames engulf her body, and they burn her to a crisp.")
        won = True
              
def load_module():
    global module, possible_moves
    possible_moves = get_modules_from(module)

def get_modules_from(module):
    moves = []
    text_file = open("Charles_Darwin\m" + str(module) + ".txt", "r")
    for counter in range(0, 4):
        move_read = text_file.readline()
        move_read = int(move_read.strip())
        if move_read != 0:
            moves.append(move_read)
    text_file.close()
    return moves

def find_npcs():
    queen = npcs["queen"]
    vents = npcs["ventilation shafts"]
    panel = npcs["information panel"]
    worker = npcs["alien worker"]
    empty = npcs["empty"]
    
    
    if queen == module:
        print("The queen is in this module.")

    for mod in vents:
        if mod == module:
            print("There is a ventilation shaft in this module.")

    for mod in panel:
        if mod == module:
            print("There is an information panel in this module.")

    for mod in worker:
        if mod == module:
            print("There is an alien worker in this module.")

    for mod in empty:
        if mod == module:
            print("This is and empty module")
    
def output_module():
    global module
    print()
    print("-----------------------------------------------------------------")
    print()
    print("You are in module", module)
    print()

def output_moves():
    global possible_moves
    print()
    print("You are in module {}".format(module))
    find_npcs()
    for move in possible_moves:
        print(move, '| ', end = '')
    print()

def get_action():
    global module, last_module, possible_moves, power, alive, npcs
    options = "(MOVE, SCANNER"
    if module in npcs["information panel"]:
        options += ", INFO"
    options += ")"
    valid_action = False
    while valid_action == False:
        print("Power: {}".format(power.get_power()))
        print("What do you want to do next ?", options)
        action = input(">")
        action = action.upper()
        al = action.split(" ")
        if len(al) == 2 and (al[0] == "MOVE" or al[0] == "M"):
            action = al[0]
            try:
                move = int(al[1])
            except ValueError:
                print("Invalid module")
        else:
            check = Sanitise(action)
            al = check.sanitise()
            action = al[0]
            move = al[1]
        if action == "MOVE" or action == "M":
            while True and str(move).isdigit() == False:
                try:
                    move = int(input("Enter the module to move to: "))
                    break
                except ValueError:
                    print("INTEGERS!!!!!")
            if move in possible_moves:
                valid_action = True
                last_module = module
                module = move
                newPower = power.get_power() - 1
                power.update_power(newPower)
            else:
                print("The module must be connected to the current module.")
        elif action == "LOCK" or action == "L":
            lock(move)
        elif action == "SCANNER" or action == "S":
            command = input("Scanner ready. Enter command (LOCK, POWER, MAP, ALIENS): ")
            command = command.upper()
            if command == "LOCK" or command == "L":
                lock(move)
            elif command == "POWER" or command == "P":
                print("Power remaining:", power.get_power())
            elif command == "MAP" or command == "M":
                mapImage = Image.open("map.jpg")
                mapImage.show()
            elif command == "ALIENS" or command == "A":
                totalAliens = 1 + len(npcs["alien worker"])
                print("There is a total of {} aliens on the ship.".format(totalAliens))
        elif action == "INFO" or action == "I" and module in npcs["information panel"]:
            if power.get_power() <= 50:
                print("Not enough power :(")
            else:
                print("The Queen is in module {}".format(npcs["queen"]))
                newPower = power.get_power() - 50
                power.update_power(newPower)
                
def spawn_npcs():
    global num_modules, queen, vent_shafts, greedy_info_panels, workers, module_set, npcs
    module_set = []
    npcs = {"queen": [], "ventilation shafts": [], "information panel": [],
            "alien worker": [], "power supply": [], "empty": []}
    for counter in range(2, num_modules + 1):
        module_set.append(counter)
    random.shuffle(module_set)
    i = 0
    queen = module_set[i]
    npcs["queen"] = module_set[i]
    for counter in range(0, 3):
        i = i + 1
        vent_shafts.append(module_set[i])
        npcs["ventilation shafts"].append(module_set[i])

    for counter in range(0, 2):
        i = i + 1
        info_panels.append(module_set[i])
        npcs["information panel"].append(module_set[i])

    for counter in range(0, 3):
        i = i + 1
        workers.append(module_set[i])
        npcs["alien worker"].append(module_set[i])

    for counter in range(0, 4):
        i = i + 1
        power_supplies.append(module_set[i])
        npcs["power supply"].append(module_set[i])
        
    j = i
    for counter in range(j, len(module_set) - 1):
        i = i + 1
        npcs["empty"].append(module_set[i])
    npcs["empty"].append(1)

def check_vent_shafts():
    global num_modules, module, vent_shafts, fuel
    global module
    if module in npcs["ventilation shafts"]:
        print("There is a bank of fuel cells here.")
        print("You load one in to your flamethrower.")
        fuel_gained = random.randint(2,5)*10
        newFuel = fuel.get_fuel() + fuel_gained
        print("Fuel was", fuel.get_fuel(), "now reading:", newFuel)
        fuel.update_fuel(newFuel)
        print("The doors suddenly lock shut.")
        print("What is happening to the station?")
        print("Our only escape is to climb the ventilation shaft.")
        print("We have no idea where we are going.")
        print("We follow the passages and find ourselves sliding down.")
        last_module = module
        while True:
            module = random.randint(1, num_modules)
            if module != last_module:
                break
        load_module()

def lock(mod = None):
    global num_modules, locked, power
    validInput = False
    if mod is not None:
        try:
            new_lock = int(mod)
            validInput = True
        except:
            print("Invalid module input.")
    while validInput == False:
        try:
            new_lock = int(input("Enter module to lock: "))
            validInput = True
        except ValueError:
            print("No number entered")
    if new_lock < 0 or new_lock > num_modules:
        print("Invalid modules. Operation failed.")
    elif new_lock == npcs["queen"]:
        print("Operation failed. Unable to lock module.")
    elif new_lock in locked_modules:
        print("Module already locked")
    else:
        locked = new_lock
        print("Aliens cannot get into module", locked)
        locked_modules.append(new_lock)
    power_used = 25 + 5*random.randint(0, 5)
    newPower = power.get_power() - power_used
    power.update_power(newPower)
    print("Power:", power.get_power())

def move_queen():
    global num_modules, module, last_module, locked, queen, won, vent_shafts
    if module == npcs["queen"]:
        print("There it is! The queen alien is in this module...")
        moves_to_make = random.randint(1, 3)
        can_move_to_last_module = False
        while moves_to_make > 0:
            escapes = get_modules_from(npcs["queen"])
            if module in escapes:
                escapes.remove(module)
            if last_module in escapes and can_move_to_last_module == False:
                escapes.remove(last_module)
            for locky in locked_modules:
                for escape in escapes:
                    if escape == locky:
                        escapes.remove(locky)
            if len(escapes) == 0:
                fight()
                moves_to_make = 0
            else:
                npcs["queen"] = random.choice(escapes)
                moves_to_make = 0
                can_move_to_last_module = True
                if npcs["queen"] not in npcs["ventilation shafts"]:
                    print("...and has escaped")
                while npcs["queen"] in npcs["ventilation shafts"]:
                    valid_move = False
                    while valid_move == False:
                        valid_move = True
                        npcs["queen"] = random.randint(1, num_modules)
                        if npcs["queen"] in npcs["ventilation shafts"]:
                            valid_move = False
                        if valid_move == True:
                            print("...and has escaped.")
                            print("We can hear scuttling in the ventialtion shafts.")
                    moves_to_make = 0
                    
def intuition():
    global possible_moves, workers, vent_shafts
    for connected_module in possible_moves:
        if connected_module in npcs["alien worker"]:
            print("I can hear something scuttling!")
        if connected_module in npcs["ventilation shafts"]:
            print("I can feel cold air!")
        if connected_module == npcs["queen"]:
            print("Listen! Did you hear that?")

def worker_aliens():
    global module, workers, fuel, alive, npcs, last_module
    if module in npcs["alien worker"]:
        print("Startled, a young alien scuttles across the floor.")
        print("It turns and leaps towards us.")
        successful_attack = False
        while (successful_attack == False) and alive == True:
            print("You can:")
            print()
            print("- Short blast your flamethrower to frighten it away.")
            print("- Long blast your flamethrower to try to kill it.")
            print("- RUN")
            print()
            print("How will you react? (S, L, R)")
            action = 0
            while action not in ("S", "L", "R"):
                action = input("Pick an action: ")
                action = action.upper()
            enoughFuel = False
            if action == "R":
                chance = random.randint(1, 100)
                if chance <= 10:
                    print("FAIL")
                    alive = False
                else:
                    module = last_module
                successful_attack = True
            if action in ("S", "L"):
                while enoughFuel == False: 
                    try:
                        fuel_used = int(input("How much fuel will you use? ..."))
                        correctInput = True
                    except ValueError:
                        print("ENTER AN INTEGER VALUE")
                        correctInput = False
                    if correctInput == True:
                        enoughFuel = fuel.compare_fuel(fuel_used)
                        if enoughFuel == False:
                            print("ERROR not enough fuel, please enter a valid amount.")
                if fuel.get_fuel() == 0:
                    print("You were about to attack the alien with a lot of force but nothing happened. Sad times. So the alien worker bit your face off.")
                    alive = False
                else:
                    newFuel = fuel.get_fuel() - fuel_used
                    fuel.update_fuel(newFuel)
                    if action == "S":
                        fuel_needed = 30 + 10*random.randint(0, 5)
                    if action == "L":
                        fuel_needed = 90 + 10*random.randint(0, 5)
                    if fuel_used >= fuel_needed:
                        successful_attack = True
                    else:
                        print("The alien squeals but it is not dead. It's angry.")
        if action == "S" and alive == True:
            print("The alien scuttles away into the corner of the room.")
        if action == "L" and alive == True:
            print("The alien has been destroyed.")
            npcs["alien worker"].remove(module)

def power_supply():
    global power, module, npcs
    if module in npcs["power supply"]:
        newPower = 10*random.randint(1, 10)
        print("You found a power supply you gain {} power.".format(newPower))
        totalPower = power.get_power() + newPower
        power.update_power(totalPower)
        npcs["power supply"].remove(module)

menu()
spawn_npcs()
print("Queen alien is located in module:", queen)
print("Ventilation shafts are located in modules:", vent_shafts)
print("Information panels are located in modules:", info_panels)
print("Worker aliens are located in modules:", workers)

while alive and not won:
    load_module()
    check_vent_shafts()
    move_queen()
    worker_aliens()
    power_supply()
    fuel.check_fuel()
    if alive == True:
        alive = power.check_power()
    if won == False and alive == True:
        intuition()
        output_moves()
        get_action()
        
if won == True:
    print("You win! :)")
elif alive == False and power.check_power() == False:
    print("The station has run out of power. Unable to sustain life support, you die.")
else:
    print("Game Over :(")
