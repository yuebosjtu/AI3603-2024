"""
This module contains functions to run and simulate games of Chinese Checkers using different agents.

Functions:
    runGame(ccgame, agents):
        Runs a single game of Chinese Checkers.
        Args:
            ccgame (ChineseChecker): The game instance.
            agents (dict): A dictionary mapping player numbers to their respective agents.
        Returns:
            int: The winner of the game (1 for player 1, 2 for player 2, 0 for a tie).

    simulateMultipleGames(agents_dict, simulation_times, ccgame):
        Simulates multiple games of Chinese Checkers and tracks the results.
        Args:
            agents_dict (dict): A dictionary mapping player numbers to their respective agents.
            simulation_times (int): The number of games to simulate.
            ccgame (ChineseChecker): The game instance.
        Returns:
            None

    callback(ccgame):
        Callback function to start the game simulation when the button is pressed.
        Args:
            ccgame (ChineseChecker): The game instance.
        Returns:
            None

Usage:
    The script initializes a Chinese Checkers game and a Tkinter GUI. It sets up a button to start the game simulation.
"""

from agent import *
from game import ChineseChecker
import datetime
import tkinter as tk
from UI import GameBoard
import time

result_list = []


def runGame(ccgame, agents: dict):
    state = ccgame.startState()
    print(state)
    max_iter = 200  # deal with some stuck situations
    iter = 0
    start = datetime.datetime.now()
    while (not ccgame.isEnd(state, iter)) and iter < max_iter:
        iter += 1
        board.board = state[1]
        board.draw()
        board.update_idletasks()
        board.update()

        player = ccgame.player(state)
        agent: Agent = agents[player]
        # function agent.getAction() modify class member action
        agent.getAction(state)
        legal_actions = ccgame.actions(state)
        if agent.action not in legal_actions:
            agent.action = random.choice(legal_actions)
        state = ccgame.succ(state, agent.action)
        if state[-1]:
            print("opp step")
            print(agent.action)
            agent.oppAction(state)
            legal_actions = ccgame.opp_actions(state)
            if agent.opp_action not in legal_actions:
                agent.opp_action = random.choice(legal_actions)
            state = ccgame.opp_succ(state, agent.opp_action, agent.action[1])

    board.board = state[1]
    # board.draw()
    board.update_idletasks()
    board.update()
    time.sleep(0.1)

    end = datetime.datetime.now()
    if ccgame.isEnd(state, iter):
        return state[1].isEnd(iter)[1], iter  # return winner
    else:  # stuck situation
        print('stuck!')
        return 0, iter


def simulateMultipleGames(agents_dict, simulation_times, ccgame):
    win_times_P1 = 0
    win_times_P2 = 0
    tie_times = 0
    utility_sum = 0
    for i in range(simulation_times):
        run_result = runGame(ccgame, agents_dict)
        print(run_result)
        if run_result == 1:
            win_times_P1 += 1
        elif run_result == 2:
            win_times_P2 += 1
        elif run_result == 0:
            tie_times += 1
        result_list.append(run_result)
        print('game', i + 1, 'finished', 'winner is player ', run_result)
    print('In', simulation_times, 'simulations:')
    print('winning times: for player 1 is ', win_times_P1)
    print('winning times: for player 2 is ', win_times_P2)
    print('Tie times:', tie_times)


def callback(ccgame):
    B.destroy()
    simpleGreedyAgent = SimpleGreedyAgent(ccgame)
    simpleGreedyAgent1 = SimpleGreedyAgent(ccgame)
    randomAgent = RandomAgent(ccgame)
    teamAgent = YourAgent(ccgame)
    teamAgent1 = YourAgent(ccgame)

    # Player 1 first move, Player 2 second move
    # YourAgent need to test as both player 1 and player 2
    # simulateMultipleGames({1: simpleGreedyAgent1, 2:simpleGreedyAgent}, 1, ccgame)
    # simulateMultipleGames({1: simpleGreedyAgent, 2: teamAgent}, 30, ccgame)
    # simulateMultipleGames({1: teamAgent, 2: simpleGreedyAgent}, 30, ccgame)
    simulateMultipleGames({1: teamAgent, 2: teamAgent1}, 2, ccgame)


if __name__ == '__main__':
    ccgame = ChineseChecker(10, 4)
    root = tk.Tk()
    board = GameBoard(root, ccgame.size, ccgame.size * 2 - 1, ccgame.board)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    B = tk.Button(board, text="Start", command=lambda: callback(ccgame=ccgame))
    B.pack()
    root.mainloop()
    print(result_list)
