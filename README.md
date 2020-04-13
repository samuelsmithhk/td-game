# Tower Defence
A simple tower defence game implemented in python using pygame

## Installation

Preferably within a virtual environment, requires python 3.7

```bash
pip install -r requirements.txt
```

## Play

Within the environment that you installed

```bash
python td-game.py
```

## Changelog && TODO

### Changelog

### 05/11/2020

* Switching font from Verdana to Freesan Bold, which
should be universal across OS

### 04/11/2020

* Capping FPS to 30

### 04/11/2020
Initial commit, existing features:

* 1 map with branching critter paths
* Player cash, lives
* Critter rounds and waves
* 4 critter types
    * basic
    * speeder
    * invisible - temporarily invisible to all but snipers
    * resistant - glue towers have no effect
* Each critter type has a boss equivalent
* 4 tower types - 
    * base
    * rapid - machine gun 
    * snipe - shoots invisible critters
    * glue - slows enemy
* Upgrading towers to increase range, damage, decreases reload time
* Pausing and resuming the simulation
 

### TODO

Plans for the future, not in a particular order:

* Game balancing, bug fixes
* Real win and lose states
* Performance optimization
* Difficulty levels
* Multiple maps
* New tower types:
    * fire - slowly burns critters
    * cannon - splash damage
* New critter types:
    * healers - health slowly recovers when not being damaged
    * clusters - spawns together in groups
* Menu system, level progression, profiles, saving and loading