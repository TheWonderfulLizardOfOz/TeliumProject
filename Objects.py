class Sanitise():
    def __init__(self, phrase):
        self.phrase = phrase.upper()

    def sanitise(self):
        poss_v = False
        for i in range(len(self.phrase)):
            if self.phrase[i].isdigit() == True:
                poss_v = True
                action = self.phrase[0:i].strip(" ")
                poss_module = self.phrase[i::].strip(" ")
                break
            
        if poss_v == False:
            action = self.phrase
            poss_module = "No Module"
        else:
            try:
                poss_module = int(poss_module)
            except:
                poss_module = "No Module"

        return [action, poss_module]

class Power():
    def __init__(self, power):
        self.power = power

    def check_power(self):
        if self.power <= 0:
            print("The is no power so you died :/")
            return False
        elif self.power <= 10:
            print("WARNING: Power is very low !!!!")
            return True
        elif self.power <= 20:
            print("Power levels running low please limit use of power")
            return True
        else:
            return True

    def update_power(self, newPower):
        self.power = newPower

    def get_power(self):
        return self.power

class Fuel():
    def __init__(self, fuel):
        self.fuel = fuel

    def update_fuel(self, newFuel):
        if newFuel < 0:
            self.fuel = 0
        else:
            self.fuel = newFuel

    def get_fuel(self):
        return self.fuel

    def compare_fuel(self, amountOfFuelNeeded):
        if self.fuel < amountOfFuelNeeded:
            return False
        else:
            return True

    def check_fuel(self):
        if self.fuel < 100:
            print("WARNING: fuel level running low.")
