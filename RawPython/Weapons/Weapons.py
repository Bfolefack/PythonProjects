import random

def generateWeapon(dice: int, die: int, crit_range: int, crit: int, reload=0, misfire=0, loading=False):
    weapon = {
        "dice": dice,
        "die": die,
        "crit_range": crit_range,
        "crit": crit,
        "reload": reload,
        "loading": loading,
        "misfire": misfire
    }
    return weapon

def rollWeapon(AC: int, attacks: int, weapon: dict):
    total = 0
    if(weapon["loading"]):
        attacks = 1
    for i in range(attacks):
        if(weapon["reload"] > 0):
            if(random.randint(1, weapon["reload"] + 1) == 1):
                total += 0
                return 0
    for i in range(attacks):
        total += rollWeaponOnce(AC, weapon)
    return total
    
def rollWeaponOnce(AC: int, weapon: dict):
    attack_roll = random.randint(1, 20)
    if(attack_roll >= AC or attack_roll >= weapon["crit_range"]):
        roll = 0
        crit = 1
        if(attack_roll >= weapon["crit_range"]):
            crit = weapon["crit"]
        for c in range (crit):
            for i in range (weapon["dice"]):
                roll += random.randint(1, weapon["die"])
        return roll
    if(weapon["misfire"] > 0):
        if(attack_roll <= weapon["misfire"]):
            roll = 0
            for i in range (weapon["dice"]):
                roll += random.randint(1, weapon["die"])
            return -roll
    
    return 0

def averageDamage(AC: int, attacks: int, weapon: dict):
    average = 0
    for i in range(50000):
        average += rollWeapon(AC, attacks, weapon)
    return average / 50000

weapons = {
    
    "Simple Melee Weapons": {
        #"Knuckleduster": generateWeapon(2, 1, 20, 3),
        "Club": generateWeapon(1, 4, 20, 2),
        "Dagger": generateWeapon(1, 4, 20, 2),
        "Gauntlet": generateWeapon(1, 4, 20, 2),
        "Greatclub": generateWeapon(2, 4, 20, 2),
        "Handaxe": generateWeapon(1, 6, 20, 3),
        "Javelin": generateWeapon(1, 6, 20, 3),
        "Light Hammer": generateWeapon(1, 4, 20, 2),
        "Mace": generateWeapon(1, 6, 20, 3),
        "Poisoner's Dagger": generateWeapon(1, 4, 20, 2),
        "Shortspear": generateWeapon(1, 6, 20, 2),
        "Sickle": generateWeapon(1, 4, 20, 2),
        "Switchblade": generateWeapon(1, 4, 19, 2),
    },
    
    "Simple Ranged Weapons": {
        "Boomerang": generateWeapon(1, 4, 19, 2),
        "Dart": generateWeapon(1, 4, 21, 1),
        "Grenade": generateWeapon(2, 8, 21, 1, misfire=1),
        "Handgone": generateWeapon(2, 8, 19, 8, misfire=5,loading=True),
        "Light Crossbow": generateWeapon(1, 8, 20, 2, loading=True),
        "Shortbow": generateWeapon(1, 6, 20, 2),
        "Sling": generateWeapon(1, 4, 20, 2),
    },
    
    "Martial Melee Weapons": {
        "Battleaxe": generateWeapon(1, 8, 20, 3),
        "Bostaff": generateWeapon(1, 6, 20, 3),
        "Broadsword": generateWeapon(1, 10, 19, 2),
        "Chain Blade": generateWeapon(1, 6, 20, 3),
        "Clawed Gauntlet": generateWeapon(1, 6, 20, 3),
        "Flail": generateWeapon(1, 8, 20, 2),
        "Gauche": generateWeapon(1, 4, 20, 2),
        "Glaive": generateWeapon(1, 10, 19, 2),
        "Great Trident": generateWeapon(1, 10, 19, 2),
        "Greataxe": generateWeapon(1, 12, 20, 3),
        "Greatsword": generateWeapon(2, 6, 19, 2),
        "Harpoon": generateWeapon(1, 10, 20, 2),
        "Hook Sword": generateWeapon(1, 6, 20, 3),
        "Khopesh": generateWeapon(1, 6, 20, 3),
        "Lance": generateWeapon(1, 10, 20, 2),
        "Longspear": generateWeapon(1, 8, 20, 2),
        "Longsword": generateWeapon(1, 8, 19, 2),
        "Maul": generateWeapon(3, 4, 20, 2),
        "Morningstar": generateWeapon(1, 8, 20, 3),
        "Pike": generateWeapon(2, 8, 20, 2),
        "Rapier": generateWeapon(1, 8, 19, 3),
        "Scimitar": generateWeapon(1, 6, 19, 3),
        "Scythe": generateWeapon(2, 4, 20, 3),
        "Shortsword": generateWeapon(1, 6, 19, 2),
        "Trident": generateWeapon(1, 8, 19, 2),
        "War Pick": generateWeapon(1, 8, 20, 2),
        "Warclub": generateWeapon(1, 12, 20, 3),
        "Warhammer": generateWeapon(1, 8, 20, 3),
        "Whip": generateWeapon(1, 6, 20, 2),
    }, 
    
    "Martial Ranged Weapons": {
        "Blowgun": generateWeapon(1, 4, 20, 2, loading=True),
        "Firestarter": generateWeapon(3, 6, 21, 1, misfire=3, loading=True),
        "Grappling Hook": generateWeapon(1, 4, 20, 2),
        "Hand Crossbow": generateWeapon(1, 6, 20, 3, loading=True),
        "Harpoon Gun": generateWeapon(2, 6, 20, 3),
        "Heavy Crossbow": generateWeapon(1, 10, 20, 3, loading=True),
        "Longbow": generateWeapon(1, 8, 20, 2),
        "Pistol": generateWeapon(1, 10, 20, 3, 8),
        "Recurve Bow": generateWeapon(1, 10, 20, 3),
        "Revolver": generateWeapon(1, 8, 20, 2, 6, 1),
        "Rifle": generateWeapon(2, 10, 20, 2, 5, 3),
        "Shotgun": generateWeapon(2, 8, 20, 4, 2),
        "Throwing Knife": generateWeapon(1, 6, 20, 3),
        "Throwing Star": generateWeapon(1, 8, 20, 2),
        "Wrist Crossbow": generateWeapon(1, 4, 20, 2, loading=True),
    },
    
    
    "Advanced Melee Weapons": {
        "Ankle Blade": generateWeapon(1, 6, 19, 3),
        "Chain Gauntlet": generateWeapon(1, 6, 20, 2),
        "Chain Sword": generateWeapon(2, 6, 19, 3),
        "Dwarven Warhammer": generateWeapon(3, 6, 20, 3),
        "Giant's Club": generateWeapon(2, 12, 20, 4),
        "Great Pike": generateWeapon(2, 8, 20, 3),
        "Halberd": generateWeapon(3, 6, 18, 2),
        "Nerfed Halberd": generateWeapon(2, 8, 18, 2),
        "Warwhip": generateWeapon(1, 8, 20, 3),
        "Wrist Blade": generateWeapon(1, 8, 20, 3),
    },
    
    "Advanced Ranged Weapons": {
        "Chakram": generateWeapon(1, 8, 18, 3),
        "Edged Card": generateWeapon(1, 8, 19, 3),
        "Portable Ballista": generateWeapon(3, 6, 20, 3, loading=True),
        "Repeating Crossbow": generateWeapon(1, 8, 20, 3, misfire=1),
        "Sniper Rifle": generateWeapon(4, 10, 20, 4, 1, misfire=1),
    }
}

simple_melees = weapons["Simple Melee Weapons"]
simple_rangeds = weapons["Simple Ranged Weapons"]
martial_melees = weapons["Martial Melee Weapons"]
martial_rangeds = weapons["Martial Ranged Weapons"]
advanced_melees = weapons["Advanced Melee Weapons"]
advanced_rangeds = weapons["Advanced Ranged Weapons"]

AC = 15
attacks = 2

# print("Simple Melee Weapons: ")
# for i in weapons["Simple Melee Weapons"]:
#     print(i + ": " + str(averageDamage(AC, attacks, simple_melees[i])))
# print()

# print("Simple Ranged Weapons: ")
# for i in weapons["Simple Ranged Weapons"]:
#     print(i + ": " + str(averageDamage(AC, attacks, simple_rangeds[i])))
# print()

# print("Martial Melee Weapons: ")
# for i in weapons["Martial Melee Weapons"]:
#     print(i + ": " + str(averageDamage(AC, attacks, martial_melees[i])))
# print()

# print("Martial Ranged Weapons: ")
# for i in weapons["Martial Ranged Weapons"]:
#     print(i + ": " + str(averageDamage(AC, attacks, martial_rangeds[i])))
# print()

print("Advanced Melee Weapons: ")
for i in weapons["Advanced Melee Weapons"]:
    print(i + ": " + str(averageDamage(AC, attacks, advanced_melees[i])))
print()

# print("Advanced Ranged Weapons: ")
# for i in weapons["Advanced Ranged Weapons"]:
#     print(i + ": " + str(averageDamage(AC, attacks, advanced_rangeds[i])))
# print()