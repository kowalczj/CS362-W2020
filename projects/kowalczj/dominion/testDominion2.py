# -*- coding: utf-8 -*-
"""
Refactored on Sun Jan 12 14:10:39 2020

@author: kowalczj

original author: tfleck
"""

from testUtility import get_supply
from testUtility import get_supply_order
from testUtility import get_trash
from testUtility import get_players
from testUtility import play


def main():
    """ Function to get game data structures from utility functions
        and play the game
    """
    player_names = ["Susan", "*Annie", "*Roger", "*Ben", "*Carla"]
    players = get_players(player_names)
    supply = get_supply(num_players=len(player_names) - 1)
    supply_order = get_supply_order()
    trash = get_trash()
    play(supply, supply_order, players, trash)


if __name__ == "__main__":
    main()
