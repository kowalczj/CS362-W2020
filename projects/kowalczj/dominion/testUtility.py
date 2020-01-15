# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 14:19:50 2020

@author: kowalczj

Refactor the code that creates the game data by moving code here.
Creating functions that initialization dominion gameplay lists
along with any other opportunities for making common functions.
Eliminate redundant game data setup code.
"""

import Dominion


def play(supply, supply_order, players, trash):
    """ Function to play the game
        The data interface to the game uses:
        - supply
        - supply_order
        - players
        - trash
        Parameterization is desired in future refactoring
    """
    # Play the game
    turn = 0
    while not Dominion.gameover(supply):
        turn += 1
        print("\r")
        for value in supply_order:
            print(value)
            for stack in supply_order[value]:
                if stack in supply:
                    print(stack, len(supply[stack]))
        print("\r")
        for player in players:
            print(player.name, player.calcpoints())
        print("\rStart of turn " + str(turn))
        for player in players:
            if not Dominion.gameover(supply):
                print("\r")
                player.turn(players, supply, trash)

    # Final score
    dcs = Dominion.cardsummaries(players)
    vp = dcs.loc["VICTORY POINTS"]
    vpmax = vp.max()
    winners = []
    for i in vp.index:
        if vp.loc[i] == vpmax:
            winners.append(i)
    if len(winners) > 1:
        winstring = " and ".join(winners) + " win!"
    else:
        winstring = " ".join([winners[0], "wins!"])

    print("\nGAME OVER!!!\n" + winstring + "\n")
    print(dcs)
