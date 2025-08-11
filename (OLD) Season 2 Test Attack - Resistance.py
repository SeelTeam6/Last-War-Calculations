import copy
import math

# Inputs go here!

# What is your current resistance?
current_resistance = 4850

# What is the resistance of the target?
target = 6000

# How much damage did you, individually, deal on an attempt?
damage = 135

# How much total Health does the target have?
total_health = 2000

# Do you want a little more info on the differences between levels?
verbose = True

# Do you want to enable experiments?
# Right now, this tries to adjust for differences due to battle length
experiments = False


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

# Create reverse mapping
RESISTANCE_TO_LEVEL = {v: k for k, v in LEVEL_TO_RESISTANCE.items()}


if verbose:
    print("Current damage:" + str(damage))


def calc(base_level, damage, total_health, season_pass):
    first_time = True
    while damage < total_health:
        resistance = furnace_level_to_resistance(base_level)

        if season_pass:
            resistance = resistance + 250

        missing_raw = target - resistance
        missing_proportion = missing_raw / target

        a = 1 - ((math.ceil(missing_proportion * 100) / 100) * 2)

        if a > 0:
            damage_actual = a * 100
        else:
            damage_actual = max(((a / 20) + 0.01), 0.001) * 100

        if missing_proportion <= 0.25:
            enemy_increase = 10 * math.ceil(missing_proportion * 100)
        elif missing_proportion > 0.25 and missing_proportion < 0.5:
            enemy_increase = 25 * math.ceil(missing_proportion * 100) - 375
        elif missing_proportion >= 0.5:
            enemy_increase = 50 * math.ceil(missing_proportion * 100) - 1600

        current_damage_proportion = damage_actual * (100 / (100 + enemy_increase))

        if verbose and first_time:
            print(
                "% of normal damage dealt: "
                + str(round(current_damage_proportion))
                + "% \n"
            )
            first_time = False

        resistance = furnace_level_to_resistance(base_level + 1)
        if season_pass:
            resistance += 250

        if resistance >= target:
            print("At next level, resistance is higher than target!")
            return base_level + 1, resistance

        missing_raw = target - resistance
        missing_proportion = missing_raw / target

        a = 1 - ((math.ceil(missing_proportion * 100) / 100) * 2)

        if a > 0:
            damage_actual = a * 100
        else:
            damage_actual = max(((a / 20) + 0.01), 0.001) * 100

        if missing_proportion <= 0.25:
            enemy_increase = 10 * math.ceil(missing_proportion * 100)
        elif missing_proportion > 0.25 and missing_proportion < 0.5:
            enemy_increase = 25 * math.ceil(missing_proportion * 100) - 375
        elif missing_proportion >= 0.5:
            enemy_increase = 50 * math.ceil(missing_proportion * 100) - 1600

        next_damage_proportion = damage_actual * (100 / (100 + enemy_increase))

        diff = next_damage_proportion / current_damage_proportion

        if experiments:
            diff = diff  # accounting for damage increase

        if verbose:
            print(
                "Damage increase at next furnace level (approx): "
                + str(round(diff * 100) / 100)
                + "x"
            )

        damage = copy.deepcopy(damage) * diff

        print(
            "Approxomate Damage at Furnace Level "
            + str(base_level + 1)
            + " ("
            + str(resistance)
            + " Resistance)"
            + ": "
            + str(round(damage))
        )

        if verbose:
            print(
                "% of normal damage dealt: "
                + str(round(next_damage_proportion))
                + "% \n"
            )

        if damage < total_health:
            base_level = base_level + 1
        else:
            if not verbose:
                print("")
            return base_level + 1, resistance


if current_resistance > 3000:
    season_pass = False
    if current_resistance not in RESISTANCE_TO_LEVEL:
        current_resistance = current_resistance - 250
        season_pass = True
    current_furnace_level = resistance_to_furnace_level(current_resistance)
else:
    print("Does not work under 3000 resistance")
    exit()

needed_level, needed_res = calc(
    current_furnace_level, damage, total_health, season_pass
)
print("Furnace level needed: " + str(needed_level))
print("Resistance Needed: " + str(needed_res))
