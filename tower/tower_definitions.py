from typing import NamedTuple

#################
# region Models #
#################


class TowerLevelDefinition(NamedTuple):
    range_radius: int
    reload_time_milliseconds: int
    damage_per_shot: int
    slows_enemy: bool
    sees_invisible: bool


class TowerDefinition(NamedTuple):
    tower_name: str
    tower_human_readable_name: str

    description_line_1: str
    description_line_2: str
    description_line_3: str

    level_one: TowerLevelDefinition
    level_one_price: int

    level_two: TowerLevelDefinition
    level_two_price: int

    level_three: TowerLevelDefinition
    level_three_price: int

    level_four: TowerLevelDefinition
    level_four_price: int

    level_five: TowerLevelDefinition
    level_five_price: int

    def get_level_definition(self, level: int) -> TowerLevelDefinition:
        return {
            1: self.level_one,
            2: self.level_two,
            3: self.level_three,
            4: self.level_four,
            5: self.level_five
        }[level]

    def get_upgrade_price(self, current_level: int) -> int:
        return {
            1: self.level_two_price,
            2: self.level_three_price,
            3: self.level_four_price,
            4: self.level_five_price,
            5: -1
        }[current_level]

######################
# region Definitions #
######################

# Basic Tower #
###############


basic_level_one = TowerLevelDefinition(
    range_radius=60,
    reload_time_milliseconds=550,
    damage_per_shot=10,
    slows_enemy=False,
    sees_invisible=False
)

basic_level_two = TowerLevelDefinition(
    range_radius=63,
    reload_time_milliseconds=520,
    damage_per_shot=12,
    slows_enemy=False,
    sees_invisible=False
)

basic_level_three = TowerLevelDefinition(
    range_radius=68,
    reload_time_milliseconds=480,
    damage_per_shot=14,
    slows_enemy=False,
    sees_invisible=False
)

basic_level_four = TowerLevelDefinition(
    range_radius=75,
    reload_time_milliseconds=440,
    damage_per_shot=16,
    slows_enemy=False,
    sees_invisible=False
)

basic_level_five = TowerLevelDefinition(
    range_radius=80,
    reload_time_milliseconds=420,
    damage_per_shot=19,
    slows_enemy=False,
    sees_invisible=False
)

basic_tower = TowerDefinition(
    tower_name='basic',
    tower_human_readable_name='Basic',

    description_line_1='Average damage, fire rate, range',
    description_line_2='No special abilities',
    description_line_3='Good for base & resistant critters',

    level_one=basic_level_one,
    level_one_price=30,

    level_two=basic_level_two,
    level_two_price=6,

    level_three=basic_level_three,
    level_three_price=12,

    level_four=basic_level_four,
    level_four_price=18,

    level_five=basic_level_five,
    level_five_price=24
)

# Machine Gun Tower #
#####################

machine_gun_level_one = TowerLevelDefinition(
    range_radius=45,
    reload_time_milliseconds=200,
    damage_per_shot=5,
    slows_enemy=False,
    sees_invisible=False
)

machine_gun_level_two = TowerLevelDefinition(
    range_radius=49,
    reload_time_milliseconds=180,
    damage_per_shot=8,
    slows_enemy=False,
    sees_invisible=False
)

machine_gun_level_three = TowerLevelDefinition(
    range_radius=55,
    reload_time_milliseconds=180,
    damage_per_shot=10,
    slows_enemy=False,
    sees_invisible=False
)

machine_gun_level_four = TowerLevelDefinition(
    range_radius=60,
    reload_time_milliseconds=140,
    damage_per_shot=13,
    slows_enemy=False,
    sees_invisible=False
)

machine_gun_level_five = TowerLevelDefinition(
    range_radius=65,
    reload_time_milliseconds=120,
    damage_per_shot=15,
    slows_enemy=False,
    sees_invisible=False
)

machine_gun_tower = TowerDefinition(
    tower_name='machine_gun',
    tower_human_readable_name='Rapid',

    description_line_1='Low damage, range.',
    description_line_2='Fast fire rate. Good for speeders',
    description_line_3='No special abilities',

    level_one=machine_gun_level_one,
    level_one_price=35,

    level_two=machine_gun_level_two,
    level_two_price=7,

    level_three=machine_gun_level_three,
    level_three_price=14,

    level_four=machine_gun_level_four,
    level_four_price=21,

    level_five=machine_gun_level_five,
    level_five_price=28
)

# Sniper Tower #
################

sniper_level_one = TowerLevelDefinition(
    range_radius=120,
    reload_time_milliseconds=1000,
    damage_per_shot=50,
    slows_enemy=False,
    sees_invisible=True
)

sniper_level_two = TowerLevelDefinition(
    range_radius=130,
    reload_time_milliseconds=950,
    damage_per_shot=60,
    slows_enemy=False,
    sees_invisible=True
)

sniper_level_three = TowerLevelDefinition(
    range_radius=140,
    reload_time_milliseconds=900,
    damage_per_shot=70,
    slows_enemy=False,
    sees_invisible=True
)

sniper_level_four = TowerLevelDefinition(
    range_radius=150,
    reload_time_milliseconds=850,
    damage_per_shot=75,
    slows_enemy=False,
    sees_invisible=True
)

sniper_level_five = TowerLevelDefinition(
    range_radius=160,
    reload_time_milliseconds=800,
    damage_per_shot=85,
    slows_enemy=False,
    sees_invisible=True
)

sniper_tower = TowerDefinition(
    tower_name='sniper',
    tower_human_readable_name='Snipe',

    description_line_1='Great range, damage',
    description_line_2='Slow fire rate.',
    description_line_3='Sees invisible critters',

    level_one=sniper_level_one,
    level_one_price=55,

    level_two=sniper_level_two,
    level_two_price=11,

    level_three=sniper_level_three,
    level_three_price=22,

    level_four=sniper_level_four,
    level_four_price=33,

    level_five=sniper_level_five,
    level_five_price=44
)

# Glue Tower #
##############

glue_level_one = TowerLevelDefinition(
    range_radius=60,
    reload_time_milliseconds=750,
    damage_per_shot=1,
    slows_enemy=True,
    sees_invisible=False
)

glue_level_two = TowerLevelDefinition(
    range_radius=68,
    reload_time_milliseconds=730,
    damage_per_shot=1,
    slows_enemy=True,
    sees_invisible=False
)

glue_level_three = TowerLevelDefinition(
    range_radius=75,
    reload_time_milliseconds=710,
    damage_per_shot=2,
    slows_enemy=True,
    sees_invisible=False
)

glue_level_four = TowerLevelDefinition(
    range_radius=80,
    reload_time_milliseconds=690,
    damage_per_shot=4,
    slows_enemy=True,
    sees_invisible=False
)

glue_level_five = TowerLevelDefinition(
    range_radius=90,
    reload_time_milliseconds=670,
    damage_per_shot=8,
    slows_enemy=True,
    sees_invisible=False
)

glue_tower = TowerDefinition(
    tower_name='glue',
    tower_human_readable_name='Glue',

    description_line_1='Slows down enemies',
    description_line_2='Moderate fire rate, range',
    description_line_3='No effect on resistant critters',

    level_one=glue_level_one,
    level_one_price=25,

    level_two=glue_level_two,
    level_two_price=5,

    level_three=glue_level_three,
    level_three_price=10,

    level_four=glue_level_four,
    level_four_price=15,

    level_five=glue_level_five,
    level_five_price=20
)