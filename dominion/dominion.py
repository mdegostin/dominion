"""This module defines and controls the Dominion game.

This module contains two classes, the game Config and
the Game itself. The Config class holds all of the data
required to play a game of Dominion. The Game class
defines the overall high level game logic.

"""

import os
import sys
from random import shuffle
from copy import copy

from players import Human, CPU
from containers import Supply, CardContainer
from errors import DominionError, DominionQuitError
from utilities import Info


class Config():
    """Config class houses the data required for a game.

    """

    def __init__(self):
        """Sets up the game configuration for a new game.

        """

        os.system('cls' if os.name == 'nt' else 'clear')

        # Print a nice welcome message.
        print("*" * 50)
        print(f"{'Welcome to Dominion!':^50}")
        print("*" * 50 + "\n")

        # Ask if the user wants to view the rules
        while True:
            response = input("Would you like to view the rules (y or n)? ")
            if response == 'y':
                Info(self).info_rules()
                break
            elif response == 'n':
                break
            else:
                continue

        # Use input to ask how many humans are playing.
        # Only allow between 1 and 4.
        while True:
            try:
                num_humans = int(input("How many human players are playing? "))
                if num_humans < 1 or num_humans > 4:
                    raise DominionError
                break
            except:
                print("Invalid response. Please enter an integer between 1 and 4.")
                continue
        self.num_humans = num_humans

        # In the future, include CPU players also, for now there are none.
        self.num_CPUs = 0

        # Initialize the human player objects given their names.
        self.players = []

        # First we need to ask for each player's name.
        for player in range(self.num_humans):
            while True:
                try:
                    name = input(f"Please enter a name for Player {player + 1}: ")
                    break
                except:
                    print("Invalid name.")
                    continue
            # Now we initialize each player.
            self.players.append(Human(name))

        # Initialize the computer players here (not implemented).

        # Count how many total players there are.
        self.num_players = len(self.players)

        # Initialize the supply and trash for the game.
        self.supply = Supply(num_players=self.num_players)

        # The trash is an empty card container to begin with.
        self.trash = CardContainer()

        # Determine the game type. If solo, the objective might
        # be to win in the fewest number of turns. If normal,
        # the player with the most victory points wins.
        if self.num_players == 1:
            self.game_type = "solo"
        else:
            self.game_type = "normal"

        # Once the players are set, shuffle their order.
        shuffle(self.players)
        self.current_player = None
        self.other_players = None

        # Set the current and other_player objects.
        self.set_current_player(0)

    def set_current_player(self, index):
        """Method to set who the current player is.

        Notes: This method is mainly used to help the action
        cards determine who used the card and who else is
        in the game that might be affected.
        
        Parameters
        ----------
        index: int
            The index of the current player in the players
            list.
        
        """

        # Set the current player.
        self.current_player = self.players[index]

        # Set the list of other players in the game.
        self.other_players = copy(self.players)

        # A shallow copy is required so when we pop out the
        # current player, we don't modify the overall list of players.
        self.other_players.pop(index)


class Game():
    """The Game class defines the Dominion game and control logic.
    
    """

    def __init__(self):
        """Initialize and play a Dominion game!
        
        """

        # First initialize the config for the game.
        self.config = Config()

        # Now play the game with the play_game method.
        self.play_game()

    def play_game(self):
        """This method plays the Dominion game.
        
        """

        os.system('cls' if os.name == 'nt' else 'clear')

        # Print the beginning game message.
        print("\nBeginning " + str(self))

        # It is the initial turn.
        turn = 0

        # This is the game loop. When the game ends we will exit this loop.
        has_ended = False
        while not has_ended:

            # Increment the turn number.
            turn += 1

            # Iterate through each player that is playing.
            for player_num, player in enumerate(self.config.players):
                
                # Set the current player.
                self.config.set_current_player(player_num)
                
                # Before each player's turn, check to see if the game ended.
                if self.config.supply.check_end_game():
                    has_ended = True
                    break
                
                # The player's turn starts here.
                try:
                    print(f"\n********** Turn #{turn} **********")
                    player.turn(self.config)
                    os.system('cls' if os.name == 'nt' else 'clear')
                
                # Here we catch unexpected errors while playing the game.
                except DominionError as e:
                    print("Encountered an error while playing. " + e)
                    return

                # If anyone quits, exit the game here.
                except DominionQuitError:
                    print(f"Game quit by {player.name}")
                    return

        # Once the game has ended, run the end_game method.
        self.end_game(turn)

    def end_game(self, turn):
        """The end_game method ends the game and determines the winner.

        Parameters
        ----------
        turn: int
            The turn number during which the game ended.

        """

        # First let the players know the game ended.
        print(f"The game has ended in {turn} turns.\n")

        # The list of victory points and objects for each player.
        end_game_victory = []
        end_game_players = []

        # Iterate through each player and end the game for them.
        for player in self.config.players:

            # Run the player end_game method to count their points.
            player.end_game()
            end_game_players.append(player)
            end_game_victory.append(player.victory_points)

        # Now sort the list of players by their number of points.
        end_game_victory, end_game_players = (list(tup) for tup in
                                              zip(*sorted(zip(end_game_victory, end_game_players), reverse=True)))

        # Now print the results.
        print("********** Results **********\n")

        # Give players their places by their points.
        # If two players tie, they get the same placement.
        places = []
        for num, player in enumerate(end_game_players):

            # First place!
            if num == 0:
                place = 1
                places.append(place)
                # Print the place, name, and points for each player.
                print(f"{place} - {player.name} with {end_game_victory[num]} points")
            
            # Others places.
            else:
                # Here check to see if anyone tied.
                if end_game_victory[num] != end_game_victory[num - 1]:
                    place += 1
                places.append(place)
                # Print the place, name, and points for each player.
                print(f"{place} - {player.name} with {end_game_victory[num]} points")

        # Write a congrats message for the winner(s)
        for num, place in enumerate(places):
            if place == 1:
                print(f"\nCongrats {end_game_players[num]}, you win!!")

    def __str__(self):
        """Custom str representation for the Dominion game.

        """

        # Just describes the game and who's playing.
        return f"Dominion game with {', '.join([str(player) for player in self.config.players])}"

    def __repr__(self):
        """Custom obj representation of the game.

        """

        return self.__str__()


if __name__ == "__main__":

    # Play a new Dominion game!!
    Game()
