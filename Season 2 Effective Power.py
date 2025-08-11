import math

verbose = True

# Inputs:
# What is your current resistance?
current_resistance = 6750

# What is your current power?
current_power = 23980000

# What is the resistance of the target?
target_resistance = 8100

# What is the reccomended power of the target?
reccomended_power = 14300000

# Are you attacking with the right kind of squad? (I.e. attacking tank with air, air with missile, missile with tank)
advantage = False


# This section helps convert back and forth between resistance and furance level
def furnace_level_to_resistance(level: int) -> int:
    return LEVEL_TO_RESISTANCE.get(level)


def resistance_to_furnace_level(resistance: int) -> int:
    return RESISTANCE_TO_LEVEL.get(resistance)


LEVEL_TO_RESISTANCE = {
    1: 100,
    2: 200,
    3: 300,
    4: 400,
    5: 500,
    6: 750,
    7: 1000,
    8: 1250,
    9: 1500,
    10: 1750,
    11: 2000,
    12: 2250,
    13: 2500,
    14: 2750,
    15: 3000,
    16: 3400,
    17: 3800,
    18: 4200,
    19: 4600,
    20: 5000,
    21: 5500,
    22: 6000,
    23: 6500,
    24: 7000,
    25: 7500,
    26: 8000,
    27: 8500,
    28: 9000,
    29: 9500,
    30: 10000,
}

RESISTANCE_TO_LEVEL = {v: k for k, v in LEVEL_TO_RESISTANCE.items()}


# This function runs the calculations based off of furnace level and whether you have the season pass
def calc(base_level, season_pass):
    # This converts furnace level and season pass back to resistance
    resistance = furnace_level_to_resistance(base_level)
    if season_pass:
        resistance += 250

    # All percentages are based off the difference between your resistance and the enemy resistance divided by the enemy resistance
    missing_raw = target_resistance - resistance
    missing_proportion = missing_raw / target_resistance

    # This calculation determines the "Your troop's damage will be reduced by" percentage
    a = 1 - ((math.ceil(missing_proportion * 100) / 100) * 2)

    if a > 0:
        damage_actual = a * 100
    else:
        damage_actual = max(((a / 20) + 0.01), 0.001) * 100

    # this calcluation determines the "enemy damage will be increased by" percentage
    if missing_proportion <= 0.25:
        enemy_increase = 10 * math.ceil(missing_proportion * 100)
    elif missing_proportion > 0.25 and missing_proportion < 0.5:
        enemy_increase = 25 * math.ceil(missing_proportion * 100) - 375
    elif missing_proportion >= 0.5:
        enemy_increase = 50 * math.ceil(missing_proportion * 100) - 1600

    # This determines your "effective power," that is, your squad power decreased by the "Your troop's damange will be reduced by" percentage
    # The x1.25 on the end is to account for in battle bonuses such as lineup and tech
    effective_personal_power = damage_actual / 100 * current_power * 1.25

    # Having a type advantage against the enemy is another force multiplier
    if advantage:
        effective_personal_power = effective_personal_power * 1.2

    # This determines the "effective enemy power," that is, the reccomended power of the enemy increased by the "enemy damage will be increased by" percentage
    effective_enemy_power = (enemy_increase + 100) / 100 * reccomended_power

    print("\nResistance: " + str(resistance))
    if verbose:
        print(f"Effective Squad Power:{round(effective_personal_power):,}")
        print(f"Effective Enemy Power:{round(effective_enemy_power):,}")

    return effective_personal_power, effective_enemy_power, resistance


# This takes in your resistance and figures out your furnace level and whether you have the season pass
# This does not work below 3000 resistance because it is impossible to determine the difference between furnace level and having the season pass
if current_resistance > 3000:
    season_pass = False
    if current_resistance not in RESISTANCE_TO_LEVEL:
        current_resistance = current_resistance - 250
        season_pass = True
    current_furnace_level = resistance_to_furnace_level(current_resistance)
else:
    print("Does not work under 3000 resistance")
    exit()

# This calculates data for your current power
effective_personal_power, effective_enemy_power, resistance = calc(
    current_furnace_level, season_pass
)
damage_proprtion = effective_personal_power / (effective_enemy_power) * 100
print(f"% of Enemy Power: {str(round(damage_proprtion, 1))}%")
# Power does not always determine whether and attack will succeed - I found that if your power is within 85%ish of your opponent, your attacks might work
if damage_proprtion > 85 and damage_proprtion <= 90:
    print("Decent change of success at this resistance - try an attack!")
if damage_proprtion > 90 and damage_proprtion < 100:
    print("High change of success at this resistance - try an attack!")

# This loops the calculation until your effective power is above the enemy's effective power
while effective_personal_power <= effective_enemy_power:
    current_furnace_level = current_furnace_level + 1
    effective_personal_power, effective_enemy_power, resistance = calc(
        current_furnace_level, season_pass
    )
    damage_proprtion = effective_personal_power / (effective_enemy_power) * 100
    print(f"% of Enemy Power: {str(round(damage_proprtion, 1))}%")
    if damage_proprtion > 85 and damage_proprtion <= 90:
        print("Decent change of success at this resistance - try an attack!")
    if damage_proprtion > 90 and damage_proprtion < 100:
        print("High change of success at this resistance - try an attack!")

# Once the loop is done, print out the last resistance
print(f"\nResistance needed: {str(resistance)}\n")
