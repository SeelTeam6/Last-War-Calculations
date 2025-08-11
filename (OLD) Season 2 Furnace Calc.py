import math

verbose = True

# Inputs:
season_pass = True
current_furnace_level = 23
target = 8000


def furnace_level_to_resistance(level: int) -> int:
    resistance_table = {
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

    return resistance_table.get(level, None)


def calc(resistance, season_pass):
    if season_pass:
        resistance += 250

    missing_raw = target - resistance
    missing_proportion = missing_raw / target

    a = 1 - ((math.ceil(missing_proportion * 100) / 100) * 2)

    if a > 0:
        damage_actual = a * 100
    else:
        damage_actual = max(((a / 20) + 0.01), 0.001) * 100

    if verbose:
        print("% Damage of Original: " + str(damage_actual))

    if missing_proportion <= 0.25:
        enemy_increase = 10 * math.ceil(missing_proportion * 100)
    elif missing_proportion > 0.25 and missing_proportion < 0.5:
        enemy_increase = 25 * math.ceil(missing_proportion * 100) - 375
    elif missing_proportion >= 0.5:
        enemy_increase = 50 * math.ceil(missing_proportion * 100) - 1600

    if verbose:
        print("% Enemy Damage Increase: " + str(enemy_increase))

    final_damage = damage_actual * (100 / (enemy_increase + 100))

    return final_damage


current = furnace_level_to_resistance(current_furnace_level)
next = furnace_level_to_resistance(current_furnace_level + 1)

final_damage_now = calc(current, season_pass)
final_damage_next = calc(next, season_pass)
diff = math.ceil(final_damage_next / final_damage_now * 100) / 100

print("Increase multiplier (approx): " + str(diff) + "x")
