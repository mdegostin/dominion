"""This module defines the container classes required for Dominion.

This module defines a series of containers used to house
the cards used to play a game of Dominion. This includes a
generic CardContainer class and the most basic methods for a
given container, such as adding and removing cards. In addition,
herein we define the concept of a card deck which is a collection
of some number of the same type of card. Finally, the supply piles
for the game are defined here, including the Base Supply, the
Kingdom supply (both of which are groups of card decks), and the
overall Supply which houses both the Kingdom and Base supplies.

"""

import random
from pprint import pprint
from copy import deepcopy

import cards
from errors import DominionError


class CardContainer():
    """A container class for all collections of cards.

    """

    def __init__(self, card_list=[], id_start=0):
        """This class houses cards and associated information.

        Parameters
        ----------
        card_list: list of Card type (default [])
            A list of cards.Card() objects. By default
            this is an empty list.
        id_start: int (default 0)
            The initial identifier for the cards in the
            container. The identifiers are used to help
            a player determine which card to interact with.

        """

        # The container houses a deep copied list of cards.
        self.cards = deepcopy(card_list)

        # num_cards attribute is hte number of cards in the container.
        self.num_cards = len(self.cards)

        # The initial identifier for the cards.
        self.id_start = id_start

        # The identifiers are the list of unique IDs for each card.
        self.identifiers = []
        self.set_identifiers()

    def count_cards(self):
        """Method to count the cards currently in the container.

        """

        # Simply get the length of the card list.
        self.num_cards = len(self.cards)

    def set_identifiers(self):
        """Reset the identifiers for the cards in the container.
        
        """

        # Initialize as an empty list.
        self.identifiers = []

        # For each card, give the card a unique ID.
        for num, _ in enumerate(self.cards):
            self.identifiers.append(num + self.id_start)

    def shuffle(self):
        """A method to shuffle the cards in the container.

        """

        # Utilize random module to shuffle the card list.
        random.shuffle(self.cards)

        # Need to reset the card identifiers once they are shuffled.
        self.set_identifiers()

    def add_cards(self, cards):
        """Method to add given cards to this container.

        Parameters
        ----------
        cards: list of cards.Cards type
            The list of cards to add to this container.
        
        """

        # First, append the new cards to the existing container.
        self.cards += cards

        # Reset the identifiers for the modified container.
        self.set_identifiers()

        # Now count the cards once cards were added.
        self.count_cards()

    def remove_cards(self, identifiers):
        """Method to remove specified cards from the container.

        Parameters
        ----------
        identifiers: list of int
            The list of identifiers defining which cards
            to remove from the container.
        
        """

        removed = []

        # First check to see that the identifiers do not specify
        # to remove more cards than are contained herein.
        if len(identifiers) > len(self.cards):
            msg = (f"Cannot remove {len(identifiers)} cards from "
                   f"a container with {len(self.cards)} cards.")
            raise DominionError(msg)

        # If valid, pop cards from the card container and store them in a new list.
        for index in sorted(identifiers, reverse=True):
            removed.append(self.cards.pop(index - self.id_start))

        # Now reset the identifiers for the modified container.
        self.set_identifiers()

        # Count the remaining cards.
        self.count_cards()

        # Remove the list of cards which were removed from the container.
        return removed

    def __str__(self):
        """Custom str representation of the card container.
        
        """

        # Empty str if the container is empty.
        return_str = ""

        # List out the identifier for each card and the individual cards.
        for num, card in enumerate(self.cards):
            return_str += f"{self.identifiers[num]}".ljust(3) + ": " + str(card) + "\n"

        # Return the multiline string.
        if self.num_cards > 0:
            return return_str[:-1]
        else:
            return return_str

    def __repr__(self):
        """Custom object representation for the container.

        """

        # Return the string representation.
        return self.__str__()


class CardDeck(CardContainer):
    """A child of card container defining a standard card deck.
    
    Notes: This class is used to represent a collection of cards
    of the SAME type. Not to be confused with a player's deck, which
    is just a regular card container and can contain different
    types of cards.
    
    """

    def __init__(self, card_type, num_cards=10):
        """The constructor for a card deck.

        Parameters
        ----------
        card_type: str
            The string name of the card type which should
            be used to populate the deck. Must be an attribute
            of the cards module.
        
        """

        # Find the card class defined by card_type.
        card_class_ = getattr(cards, card_type)

        # Create a list of card instances of that type.
        card_list = [card_class_() for num in range(num_cards)]

        # Initialize a card container with this card list.
        super().__init__(card_list, id_start=0)


class Base():
    """Base class defines the group of base card decks for the game.

    The Base is referred to as the Base Supply in traditional
    Dominion game. This contains decks of the Treasure types,
    and decks of the Victory type cards. This also will typically
    contain Curse cards as well, but not in this implementation.

    """

    def __init__(self, num_players):
        """The constructor for the Base Supply class.

        Parameters
        ----------
        num_players: int
            The number of players for a game. This
            determines the number of cards in the base.

        """

        # If more than 2 players are playing, use 12 V cards.
        # Otherwise, use 8 V cards.
        if num_players > 2:
            num_victory = 12
        else:
            num_victory = 8

        # Initialize the list of decks
        self.decks = []

        # Populate the list of decks with Treasure cards.
        self.decks.append(CardDeck('Copper', 60 - num_players * 7))
        self.decks.append(CardDeck('Silver', 40))
        self.decks.append(CardDeck('Gold', 30))

        # Populate the list of decks with Victory cards.
        self.decks.append(CardDeck('Estate', num_victory))
        self.decks.append(CardDeck('Duchy', num_victory))
        self.decks.append(CardDeck('Province', num_victory))

        # Set identifiers for the decks in the Base.
        self.identifiers = [i for i in range(len(self.decks))]

        # Keep a card object of each deck for printing.
        self._decks_ref = [deck.cards[0] for deck in self.decks]

    def __str__(self):
        """Custom str representation of the Base supply.

        """

        return_str = "Base Card Supply\n" + "-" * 16 + "\n"

        # Return a multiline string with the card representation.
        for num, deck in enumerate(self.decks):
            return_str += (f"{self.identifiers[num]}".ljust(3)
                           + ": "
                           + str(self._decks_ref[num])
                           + "x"
                           + str(deck.num_cards)
                           + "\n")

        return return_str[:-1]

    def __repr__(self):
        """Custom object representation.

        """
        return self.__str__()


class Kingdom():
    """Kingdom class defines the group of action card decks for the game.

    The Kingdom is referred to as the Kingdom Supply in traditional
    Dominion game. This contains decks of the action types. There are
    many different Kingdom configurations that are used in Dominion.
    In this implementation, we focus on the 'First Game' setup, and
    a solo setup which only contains single player cards. Finally,
    we implement the kingdom randomizer which can be used as more cards
    are added to the game.

    """

    def __init__(self, num_players, kingdom='first_game', id_start=0):
        """The constructor for the kingdom supply.

        Parameters
        ----------
        num_players: int
            The number of players playing.
        kingdom: str (default first_game)
            The name of the kingdom setup to use
            for the game. If one player is playing,
            use solo. Can also choose to use the
            randomizer for varied experiences.
        id_start: int (default 0)
            The initial identifier for the decks in this
            kingdom supply. This is required because the
            base supply will start from 0, so this
            differentiates between base and kingdom supplies.
        
        """

        # A dictionary of the possible kingdoms. Each entry
        # should have a corresponding method.
        kingdoms = {'first_game': self.first_game(),
                    'solo': self.solo(),
                    'random': self.random(),
                    }

        # If one player, use solo. Else construct input kingdom.
        if num_players == 1:
            self.decks = kingdoms['solo']
        else:
            self.decks = kingdoms[kingdom]

        # Set the identifiers for the deck
        self.id_start = id_start
        self.identifiers = [i + id_start for i in range(len(self.decks))]

        # Keep a reference card from each deck for printing.
        self._decks_ref = [deck.cards[0] for deck in self.decks]

    def first_game(self):
        """The method to construct the first_game kingdom.
        
        """

        decks = []
        decks.append(CardDeck('Cellar', 10))
        decks.append(CardDeck('Market', 10))
        decks.append(CardDeck('Merchant', 10))
        decks.append(CardDeck('Militia', 10))
        decks.append(CardDeck('Mine', 10))
        decks.append(CardDeck('Moat', 10))
        decks.append(CardDeck('Remodel', 10))
        decks.append(CardDeck('Smithy', 10))
        decks.append(CardDeck('Village', 10))
        decks.append(CardDeck('Workshop', 10))

        return decks

    def solo(self):
        """The method to construct the solo kingdom.
        
        """

        decks = []
        decks.append(CardDeck('Cellar', 10))
        decks.append(CardDeck('Market', 10))
        decks.append(CardDeck('Merchant', 10))
        decks.append(CardDeck('Mine', 10))
        decks.append(CardDeck('Remodel', 10))
        decks.append(CardDeck('Smithy', 10))
        decks.append(CardDeck('Village', 10))
        decks.append(CardDeck('Workshop', 10))
        decks.append(CardDeck('Festival', 10))
        decks.append(CardDeck('Laboratory', 10))

        return decks

    def random(self):
        """The method to construct a random kingdom.

        This method sifts through all available action
        cards and randomly selects 10 of them.
        
        """

        # Find alld efined action cards in the cards module.
        all_action_cards = [cls.__name__ for cls in cards.Action.__subclasses__()]

        # Get a random sample of 10 of the action card types.
        action_cards = random.sample(all_action_cards, 10)

        # Construct the card decks for this kingdom.
        decks = [CardDeck(action_card, 10) for action_card in action_cards]

        return decks

    def __str__(self):
        """Custom str representation for the kingdom supply.

        """

        return_str = "Kingdom Card Supply\n" + "-" * 19 + "\n"

        # Return a multiline string with the card representation.
        for num, deck in enumerate(self.decks):
            return_str += (f"{self.identifiers[num]}".ljust(3)
                           + ": "
                           + str(self._decks_ref[num])
                           + "x"
                           + str(deck.num_cards)
                           + "\n")

        return return_str[:-1]

    def __repr__(self):
        """Custom object representation for the kingdom supply.

        """

        return self.__str__()


class Supply():
    """The Supply class defines the overall supply for a game.

    The supply consists of the base supply and the kingdom supply. 
    
    """

    def __init__(self, num_players, kingdom='first_game'):
        """Constructor for the Supply class.

        Parameters
        ----------
        num_players: int
            The number of players of the game.
        kingdom: str
            The name of the kingdom to use.
        
        """

        # Initialize the base supply.
        self.base_supply = Base(num_players)

        # Initialize the kingdom supply.
        self.kingdom_supply = Kingdom(num_players,
                                      kingdom=kingdom,
                                      id_start=len(self.base_supply.decks))

    def check_end_game(self):
        """All end game criteria are determined by the supply.

        Therefore this method checks whether or not the game
        is over dependent on which cards are left in the supply.
        
        """

        # End game criteria #1
        # If three supply piles are empty, return True
        num_empty_piles = 0
        for deck in self.base_supply.decks + self.kingdom_supply.decks:
            if deck.num_cards == 0:
                num_empty_piles += 1
        if num_empty_piles > 2:
            return True

        # End game criteria #2
        # If the Province pile is empty, return True
        num_province = self.base_supply.decks[5].num_cards
        if num_province == 0:
            return True

        # If the game hasn't ended, return False
        return False

    def __str__(self):
        """Custom str representation for the Supply.

        Simply returns the string representation of the
        Base and the Kingdom supplies.

        """

        return_str = str(self.base_supply) + "\n\n" + str(self.kingdom_supply)

        return return_str

    def __repr__(self):
        """Custom object representation for the Supply.
        
        """
        
        return self.__str__()
