"""This module defines the card classes required for Dominion.

This module defines a series of abstract classes used to
represent the different card types used in the game. Then,
the individual card types are defined.

"""

import textwrap
from collections import OrderedDict

from errors import DominionPassError, DominionQuitError


class Card():
    """Abstract base class for all cards.

    """

    def __init__(self, cost=0, name=None):
        """The constructor for card base class.

        Parameters
        ----------
        cost: int (default 0)
            The cost of the card. All cards in the
            game cost a certain amount of coin.
        name: str (default None)
            The name of a card. Redundant information
            with the name of the child classes.

        """

        self.cost = cost
        self.name = name

    def info(self):
        """Abstract method for the information about a given card.

        The implemented info methods in child classes will be called
        from the utilities.Info class to help players learn what each
        card is.

        """

        # Raise an exception if the method is not defined in child class.
        raise NotImplementedError("Must define info method for card class.")

    def _print_formatted(self, msg):
        """Method to print a formatted message using textwrap.

        The primary usage of this method is to wrap long info
        messages to multiple lines in a consistent manner. This
        method prints the formatted message.

        Parameters
        ----------
        msg: str
            The message to format in a particular way.

        """

        # Use the textwrap fill function to convert a single string
        # to a multi-line formatted string.
        msg_formatted = textwrap.fill(msg)
        print("\n" + msg_formatted + "\n")


class Treasure(Card):
    """Abstract class for all Treasure-type cards.

    """

    def __init__(self, cost=0, name=None, coin=0):
        """Constructor for all Treasure type cards.

        Parameters
        ----------
        cost: see Card class
        name: see Card class
        coin: int (default 0)
            The amount that a given treasure card is worth
            in coin (currency).

        """

        # Call the parent constructor method.
        super().__init__(cost, name)

        # Set the coin attribute for the Treasure card.
        self.coin = coin

    def info(self):
        """Method defines and prints the information for all Treasure cards.

        """

        # Prints the name of the card and the amount of coin it is worth.
        info = f"{self.name}. This card is worth {self.coin} coin."
        self._print_formatted(info)

    def __str__(self):
        """Custom str representation used for the game's CLI.

        """

        # Return a string that succinctly describes the treasure card.
        return_str = f"{self.name}".ljust(12) + f"(Type T, Cost {self.cost}, +{self.coin} C)"
        return return_str.ljust(56)

    def __repr__(self):
        """Custom object representation used for the game's CLI.

        """

        return self.__str__()


class Victory(Card):
    """Abstract class for all Victory-type cards.

    """

    def __init__(self, cost=0, name=None, victory=0):
        """Constructor for all Victory type cards.

        Parameters
        ----------
        cost: see Card class
        name: see Card class
        victory: int (default 0)
            The amount that a given victory card is worth
            in victory points (territory).

        """

        # Call the parent constructor method.
        super().__init__(cost, name)

        # Set the victory points attribute.
        self.victory = victory

    def info(self):
        """Method defines and prints the information for all Victory cards.

        """

        # Prints the name of the card and the amount of victory it is worth.
        info = f"{self.name}. This card is worth {self.victory} victory points."
        self._print_formatted(info)

    def __str__(self):
        """Custom str representation used for the game's CLI.

        """

        # Return a string that succinctly describes the victory card.
        return_str = f"{self.name}".ljust(12) + f"(Type V, Cost {self.cost}, +{self.victory} V)"
        return return_str.ljust(56)

    def __repr__(self):
        """Custom object representation used for the game's CLI.

        """

        return self.__str__()


class Action(Card):
    """Abstract class for all Victory-type cards.

    """

    def __init__(self, cost=0, name=None, **kwargs):
        """Constructor for all Action type cards.

        Parameters
        ----------
        cost: see Card class
        name: see Card class
        **kwargs:
            Arbitrary keyword arguments.

        """

        # First call the parent constructor
        super().__init__(cost, name)

        # Now define three properties about the card.
        # First, does the card only affect the current player?
        self.single_player = kwargs['single_player']

        # Next, is the card an attack card?
        self.attack = kwargs['attack']

        # Finally, is the card a reaction card?
        self.reaction = kwargs['reaction']

        # The effects dictionary defines all other attributes for action cards.
        # These effects take place when this card is played during a turn.
        self.effects = OrderedDict([('A', 0),  # Added action points
                                    ('B', 0),  # Added buy points
                                    ('Ca', 0),  # Number of cards to draw
                                    ('C', 0),  # Added coin
                                    ('Effect', None),  # Arbitrary effect (containing logic)
                                    ])

    def info(self):
        """Method defines and prints the information for all Victory cards.

        """

        # First print the name of the card.
        info = f"{self.name} card."

        # Get a list of all non-zero effects from the card.
        str_list = []
        for key, value in self.effects.items():
            if key != 'Effect':
                if value > 0:
                    str_list.append(f"+{value} {key}")

        # If there are effects, print them.
        if len(str_list) > 0:
            info += " Playing this card results in the following: "
            info += ", ".join(str_list) + "."

        # If there is an arbitrary effect, print it.
        if self.effects['Effect'] is not None:
            info += " This card has the following effect: "
            info += self.effects['Effect']

        # Print the formatted result.
        self._print_formatted(info)

    def action(self):
        """Abstract method for all action cards defining their action.

        The logic in the child action method should dictate the flow of
        the control of the program when the card is played.

        """

        # Raise an exception if not defined in child class.
        raise NotImplementedError("Must define action method for card class.")

    def __str__(self):
        """Custom str representation used for the game's CLI.

        """

        # Return a string that succinctly describes the action card.
        type_str = "A"
        if self.attack:
            type_str += "A"
        elif self.reaction:
            type_str += "R"

        str_repr = f"{self.name}".ljust(12) + f"(Type {type_str}, Cost {self.cost}, "
        str_list = []
        for key, value in self.effects.items():
            if key != 'Effect':
                if value > 0:
                    str_list.append(f"+{value} {key}")
        str_repr += ", ".join(str_list)

        # If the card has an artbitrary effect, use an * to denote.
        if self.effects['Effect'] is not None:
            if len(str_list) > 0:
                str_repr += ", *"
            else:
                str_repr += "*"

        str_repr += ")"

        return str_repr.ljust(56)

    def __repr__(self):
        """Custom object representation used for the game's CLI.

        """
        return self.__str__()


class Copper(Treasure):
    """The Copper card. The most basic Treasure type card in the game.

    """

    def __init__(self):
        """Constructor for the Copper card.

        """

        # Copper costs 0 and is worth 1 coin.
        super().__init__(cost=0, name="Copper", coin=1)


class Silver(Treasure):
    """The Silver card. The intermediate Treasure type card.

    """

    def __init__(self):
        """Constructor for the Silver card.

        """

        # Silver costs 3 and is worth 2 coin.
        super().__init__(cost=3, name="Silver", coin=2)


class Gold(Treasure):
    """The Gold card. The highest Treasure type card.

    """

    def __init__(self):
        """Constructor for the Gold card.

        """

        # Gold costs 6 and is worth 3 coin.
        super().__init__(cost=6, name="Gold", coin=3)


class Estate(Victory):
    """The Estate card. The most basic Victory card.

    """

    def __init__(self):
        """Constructor for the Estate card.

        """

        # Estate costs 2 and is worth 1 victory point.
        super().__init__(cost=2, name="Estate", victory=1)


class Duchy(Victory):
    """The Duchy card. The intermediate Victory card.

    """

    def __init__(self):
        """Constructor for the Duchy card.

        """

        # Duchy costs 5 and is worth 3 victory points.
        super().__init__(cost=5, name="Duchy", victory=3)


class Province(Victory):
    """The Province card. The highest Victory card (in this implementation).

    """

    def __init__(self):
        """Constructor for the Province card.

        """

        # Province costs 8 and is worth 6 victory point.
        super().__init__(cost=8, name="Province", victory=6)


class Cellar(Action):
    """The Cellar action card.

    """

    def __init__(self):
        """Constructor for the Cellar card.

        """

        # Cellar costs 2 coin and only impacts the current player.
        # It is not an attack or reaction card.
        super().__init__(cost=2,
                         name="Cellar",
                         single_player=True,
                         attack=False,
                         reaction=False
                         )

        # Cellar yields 1 additional action point when played.
        # Cellar has the added effect listed below.
        self.effects['A'] = 1
        self.effects['Effect'] = ("Discard any number of cards, then "
                                  "draw that many.")

    def action(self, config):
        """The action for the Cellar card.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First print the info of the card.
        self.info()

        # Increment the player's action points by 1.
        config.current_player.increment_actions(1)

        # Now let the player discard as many cards as they want.
        num_discards = 0
        while config.current_player.hand.num_cards > 0:
            try:
                config.current_player.discard(config)
                num_discards += 1

            # ...unless they pass.
            except DominionPassError:
                break

        # Now draw to replace the cards that were discarded.
        config.current_player.draw(num_discards)


class Market(Action):
    """The Market action card.

    """

    def __init__(self):
        """Constructor for the Market card.

        """

        # Market costs 5 coin and only impacts the current player.
        # It is not an attack or reaction card.
        super().__init__(cost=5,
                         name="Market",
                         single_player=True,
                         attack=False,
                         reaction=False
                         )

        # Effects when played, no arbitrary effect.
        self.effects['Ca'] = 1
        self.effects['A'] = 1
        self.effects['B'] = 1
        self.effects['C'] = 1

    def action(self, config):
        """The action for the Market card.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First print the info of the card.
        self.info()

        # Let the payer draw one card first.
        config.current_player.draw(1)

        # Increment the player's action points by 1.
        config.current_player.increment_actions(1)

        # Increment the player's buy points by 1.
        config.current_player.increment_buys(1)

        # Increment the player's number of coins this turn by 1.
        config.current_player.increment_coins(1)


class Merchant(Action):
    """The Merchant action card.

    """

    def __init__(self):
        """Constructor for the Merchant card.

        """

        # Merchant costs 3 coin and only impacts the current player.
        # It is not an attack or reaction card.
        super().__init__(cost=3,
                         name="Merchant",
                         single_player=True,
                         attack=False,
                         reaction=False
                         )

        # Merchant has the following effects and an arbitrary effect.
        self.effects['Ca'] = 1
        self.effects['A'] = 1
        self.effects['Effect'] = ("The first time you play a silver this turn, "
                                  "+1 C.")

    def action(self, config):
        """The action for the Merchant card.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First print the info of the card.
        self.info()

        # The player gets to draw 1 card.
        config.current_player.draw(1)

        # Increment player's action points by 1.
        config.current_player.increment_actions(1)

        # Now check if the player has a Silver in their hand.
        # If they do, they get 1 extra coin to use this turn.
        # This is SLIGHTLY different from the real usage.
        has_silver = False
        for card in config.current_player.hand.cards:
            if card.name == 'Silver':
                has_silver = True

        if has_silver:
            config.current_player.increment_coins(1)


class Militia(Action):
    """The Militia action card.

    """

    def __init__(self):
        """Constructor for the Militia card.

        """

        # Militia costs 4 coin and impacts all players.
        # It is an attack card.
        super().__init__(cost=4,
                         name="Militia",
                         single_player=False,
                         attack=True,
                         reaction=False
                         )

        # Effects and arbitrary effect of this card.
        self.effects['C'] = 2
        self.effects['Effect'] = ("Each other player discards down to 3 cards "
                                  "in hand.")

    def action(self, config):
        """The action for the Militia card.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First print the info of the card.
        self.info()

        # Increment the player's coins this turn by 2.
        config.current_player.increment_coins(2)

        # Iterate through all other players at the table.
        for player in config.other_players:

            # Get the cards in each player's hand (secretly)
            player_cards = [card.name for card in player.hand.cards]

            # If any player has Moat, they are unaffected by Militia.
            if 'Moat' in player_cards:
                print(f"{player.name} reveals Moat. They are unaffected.")
                continue

            # If the player does not have Moat, force them to discard down to 3 cards.
            else:
                print(f"{player.name} must discard down to 3 cards.")
                while len(player.hand.cards) > 3:
                    print(f"{len(player.hand.cards) - 3} card(s) remain.")
                    try:
                        player.discard(config)
                    except DominionPassError:
                        pass


class Mine(Action):
    """The Mine action card.

    """

    def __init__(self):
        """Constructor for the Mine card.

        """

        # Mine costs 5 coin and impacts only the current player.
        # It is not an attack or reaction card.
        super().__init__(cost=5,
                         name="Mine",
                         single_player=True,
                         attack=False,
                         reaction=False
                         )

        # Arbitrary effect of the Mine card.
        self.effects['Effect'] = ("You may trash a Treasure from your hand. "
                                  "Gain a Treasure to your hand costing up to "
                                  "3 C more than it.")

    def action(self, config):
        """The action for the Mine card.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First print the info of the card.
        self.info()

        # Let the player trash a Treasure type card.
        # If they do, let them free buy a new Treasure costing over 3 coin more.
        try:
            card_cost = config.current_player.trash(config, card_type="Treasure")
            max_cost = card_cost + 3
            config.current_player.free_buy(config, max_cost, card_type="Treasure", destination='hand')
        except DominionPassError:
            pass


class Moat(Action):
    """The Moat action card.

    """

    def __init__(self):
        """Constructor for the Moat card.

        """

        # Moat costs 2 coin and does not only impact the current player.
        # It is a reaction card.
        super().__init__(cost=2,
                         name="Moat",
                         single_player=False,
                         attack=False,
                         reaction=True
                         )

        # Effect and reaction effect of Moat.
        self.effects['Ca'] = 2
        self.effects['Effect'] = ("When another player plays an Attack card, "
                                  "you may first reveal this from your hand, "
                                  "to be unaffected by it.")

    def action(self, config):
        """The action for the Moat card.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First print the info of the card.
        self.info()

        # Let the player draw 2 cards.
        config.current_player.draw(2)

        # In the future, we could implement a reaction method which defines
        # the reaction when using this card. Right now, the check for existence
        # of Moat and playing Moat is performed in Militia's action method.
        # This will need to change if more reaction cards are added.


class Remodel(Action):
    """The Remodel action card.

    """

    def __init__(self):
        """Constructor for the Remodel card.

        """

        # Remodel costs 4 coin and only impacts the current player.
        # It is not an attack or reaction card.
        super().__init__(cost=4,
                         name="Remodel",
                         single_player=True,
                         attack=False,
                         reaction=False
                         )

        # Arbitrary effect of playing the card.
        self.effects['Effect'] = ("Trash a card from your hand. Gain a card "
                                  "costing up to 2 C more than it.")

    def action(self, config):
        """The action for the Remodel card.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First print the info of the card.
        self.info()

        # Let the player trash any card.
        # If they do, let the player free buy a card costing up to 2 coin more.
        try:
            card_cost = config.current_player.trash(config)
            max_cost = card_cost + 2
            config.current_player.free_buy(config, max_cost)
        except DominionPassError:
            pass


class Smithy(Action):
    """The Smithy action card.

    """

    def __init__(self):
        """Constructor for the Smithy card.

        """

        # Smithy costs 4 coin and only impacts the current player.
        # It is not an attack or reaction card.
        super().__init__(cost=4,
                         name="Smithy",
                         single_player=True,
                         attack=False,
                         reaction=False
                         )

        # The effect of the Smithy card.
        self.effects['Ca'] = 3

    def action(self, config):
        """The action for the Smithy card.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First print the info of the card.
        self.info()

        # The player draws 3 cards when this card is played.
        config.current_player.draw(3)


class Village(Action):
    """The Village action card.

    """

    def __init__(self):
        """Constructor for the Village card.

        """

        # Village costs 3 coin and only impacts the current player.
        # It is not an attack or reaction card.
        super().__init__(cost=3,
                         name="Village",
                         single_player=True,
                         attack=False,
                         reaction=False
                         )

        # The effects of the Village card.
        self.effects['Ca'] = 1
        self.effects['A'] = 2

    def action(self, config):
        """The action for the Village card.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First print the info of the card.
        self.info()

        # The player first draws 1 card.
        config.current_player.draw(1)

        # Then increment the player's action points by 2.
        config.current_player.increment_actions(2)


class Workshop(Action):
    """The Workshop action card.

    """

    def __init__(self):
        """Constructor for the Workshop card.

        """

        # Workshop costs 3 coin and only impacts the current player.
        # It is not an attack or reaction card.
        super().__init__(cost=3,
                         name="Workshop",
                         single_player=True,
                         attack=False,
                         reaction=False
                         )

        # The arbitrary effect of the card.
        self.effects['Effect'] = ("Gain a card costing up to 4 coin.")

    def action(self, config):
        """The action for the Workshop card.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First print the info of the card.
        self.info()

        # Le the player free buy any card worth up to 4 coin.
        config.current_player.free_buy(config, 4)


class Festival(Action):
    """The Festival action card.

    """

    def __init__(self):
        """Constructor for the Festival card.

        """

        # Festival costs 5 coin and only impacts the current player.
        # It is not an attack or reaction card.
        super().__init__(cost=5,
                         name="Festival",
                         single_player=True,
                         attack=False,
                         reaction=False
                         )

        self.effects['A'] = 2
        self.effects['B'] = 1
        self.effects['C'] = 2

    def action(self, config):
        """The action for the Festival card.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First print the info of the card.
        self.info()

        # Increment the player's action points by 2.
        config.current_player.increment_actions(2)

        # Increment the player's buy points by 1.
        config.current_player.increment_buys(1)

        # Increment the player's coins this turn by 2.
        config.current_player.increment_coins(2)


class Laboratory(Action):
    """The Laboratory action card.

    """

    def __init__(self):
        """Constructor for the Laboratory card.

        """

        # Laboratory costs 5 coin and only impacts the current player.
        # It is not an attack or reaction card.
        super().__init__(cost=5,
                         name="Laboratory",
                         single_player=True,
                         attack=False,
                         reaction=False
                         )

        # Effects of the Laboratory card.
        self.effects['Ca'] = 2
        self.effects['A'] = 1

    def action(self, config):
        """The action for the Laboratory card.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First print the info of the card.
        self.info()

        # Let the player draw 2 cards.
        config.current_player.draw(2)

        # Then increment the player's action points by 1.
        config.current_player.increment_actions(1)
