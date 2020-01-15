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
import random
from collections import defaultdict


def get_supply(num_players):
    """ Function to create card supply
        Requires number of players for
        The data interface to the game uses supply
        Refactoring includes:
        - num_players instead of len(player_names)
        Parameterization is desired in future refactoring
    """

    # number of curses and victory cards
    if num_players > 2:
        nV = 12
    else:
        nV = 8
    nC = -10 + 10 * num_players

    # Define box
    box = {}
    box["Woodcutter"] = [Dominion.Woodcutter()] * 10
    box["Smithy"] = [Dominion.Smithy()] * 10
    box["Laboratory"] = [Dominion.Laboratory()] * 10
    box["Village"] = [Dominion.Village()] * 10
    box["Festival"] = [Dominion.Festival()] * 10
    box["Market"] = [Dominion.Market()] * 10
    box["Chancellor"] = [Dominion.Chancellor()] * 10
    box["Workshop"] = [Dominion.Workshop()] * 10
    box["Moneylender"] = [Dominion.Moneylender()] * 10
    box["Chapel"] = [Dominion.Chapel()] * 10
    box["Cellar"] = [Dominion.Cellar()] * 10
    box["Remodel"] = [Dominion.Remodel()] * 10
    box["Adventurer"] = [Dominion.Adventurer()] * 10
    box["Feast"] = [Dominion.Feast()] * 10
    box["Mine"] = [Dominion.Mine()] * 10
    box["Library"] = [Dominion.Library()] * 10
    box["Gardens"] = [Dominion.Gardens()] * nV
    box["Moat"] = [Dominion.Moat()] * 10
    box["Council Room"] = [Dominion.Council_Room()] * 10
    box["Witch"] = [Dominion.Witch()] * 10
    box["Bureaucrat"] = [Dominion.Bureaucrat()] * 10
    box["Militia"] = [Dominion.Militia()] * 10
    box["Spy"] = [Dominion.Spy()] * 10
    box["Thief"] = [Dominion.Thief()] * 10
    box["Throne Room"] = [Dominion.Throne_Room()] * 10

    # Pick 10 cards from box to be in the supply.
    boxlist = [k for k in box]
    random.shuffle(boxlist)
    random10 = boxlist[:10]
    supply = defaultdict(list, [(k, box[k]) for k in random10])

    # The supply always has these cards
    supply["Copper"] = [Dominion.Copper()] * (60 - num_players * 7)
    supply["Silver"] = [Dominion.Silver()] * 40
    supply["Gold"] = [Dominion.Gold()] * 30
    supply["Estate"] = [Dominion.Estate()] * nV
    supply["Duchy"] = [Dominion.Duchy()] * nV
    supply["Province"] = [Dominion.Province()] * nV
    supply["Curse"] = [Dominion.Curse()] * nC

    # the data interface to the game uses only supply
    # intermediate data such as box are not needed by external functions
    # paramaterization is desired in future refactoring
    return supply


def get_supply_order():
    """ Function to create card supply_order
        The data interface to the game uses supply_order
        Parameterization is desired in future refactoring
    """
    supply_order = {
        0: ["Curse", "Copper"],
        2: ["Estate", "Cellar", "Chapel", "Moat"],
        3: ["Silver", "Chancellor", "Village", "Woodcutter", "Workshop"],
        4: [
            "Gardens",
            "Bureaucrat",
            "Feast",
            "Militia",
            "Moneylender",
            "Remodel",
            "Smithy",
            "Spy",
            "Thief",
            "Throne Room",
        ],
        5: [
            "Duchy",
            "Market",
            "Council Room",
            "Festival",
            "Laboratory",
            "Library",
            "Mine",
            "Witch",
        ],
        6: ["Gold", "Adventurer"],
        8: ["Province"],
    }
    return supply_order


def get_trash():
    """ Function to create trash list
        The data interface to the game uses trash
        Parameterization is desired in future refactoring
    """
    trash = []
    return trash


def get_players(player_names):
    """ Function to add create players list
        and add players to Dominion object
        The data interface to the game uses players
        Parameterization is desired in future refactoring
    """
    # Costruct the Player objects
    players = []
    for name in player_names:
        if name[0] == "*":
            players.append(Dominion.ComputerPlayer(name[1:]))
        elif name[0] == "^":
            players.append(Dominion.TablePlayer(name[1:]))
        else:
            players.append(Dominion.Player(name))
    return players


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
