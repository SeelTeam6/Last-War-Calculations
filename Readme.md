# Last War Calculations!

## Intro
Hi WRAX!

This is an accesible repository for the python scripts that  I have been writing. I'm working on a way to make these easily runnable on y'alls end as I update them. 

There's four files - any marked with "OLD" are my attempts to do a damage calculation. I've realised these have some major flaws and have abandoned them for now. (Essentially, Crit Rate causes huge swings, as well as the fact that if the battle makes it to 9ish seconds all damage calculations go out the window due to skills)

The current version is a lot simpler and hopefully more reliable, though it is a lot less precise. This version just calcaultes effective squad power and effective enemy power based on damage reduction/increase percentages. This is a lot more broad but provides a more consistent baseline, hopefully. (It also doesn't need a test attack, which is nice for calculating boss damage)

## How to use
Working on it...

You can copy these scripts into a site such as [this one](https://www.online-python.com/) for now and run them - I'll see if theres a way to provide links which live update as I make improvements.

The "Season 2 Effective Power" script, which is my current version, has descriptions on the inputs so it's easier to use - essentially, you need your resistance, your squad power, the enemy's resistance, the enemy's squad power, and whether you are attacking with the right kind of squad. 

## Details on the Calculations
When you click on a doom elite, it tells you two percentages: Damage Reduction % and Enemy Damage Increased %. Both of these values are solely based on the difference between your resistance and the enemy resistance. 

Thanks to calculations by some guy on reddit here: https://www.reddit.com/r/LastWarMobileGame/comments/1e6o122/virus_resistance_to_damage_calculation/, I already knew the formula for Damage Reduction %.

However, this doesn't account for the Enemy Damage Increase %. Through a bunch of testing using data from me and Mike (found here: https://www.desmos.com/calculator/lbp3uisfsw), I managed to reverse engineer the formulas that the game uses to calculate the Enemy Damaged Increase %. 

Both of these are present in all of the scripts, as they drive my calculations for predicting future performance without needing to see the exact percentages in game.