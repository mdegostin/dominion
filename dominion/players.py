"""The players module defines the Dominion player classes.

The abstract base class Player defines many of the common
methods and attributes that both human and CPU players need.
The Human class defines how a human player players the game,
including getting input from the player via command line.
The CPU class is currently not implemented. 

"""

from containers import CardContainer, CardDeck
from utilities import transfer, get_parent_classes, Info
from errors import DominionError, DominionPassError, DominionQuitError


class Player():
    """Abstract base class for Dominion player.

    """

    def __init__(self, name):
        """Initialize a player at the beginning of the game.

        Parameters
        ----------
        name: str
            The string by which the player will be referred
            to.

        """

        # The player's name.
        self.name = name

        # Initial deck for each player contains 7 Copper and 3 Estate.
        self.deck = CardContainer(CardDeck('Copper', 7).cards + CardDeck('Estate', 3).cards)
        self.deck.shuffle()

        # Empty card containers for the hand, discard pile and play mat.
        self.hand = CardContainer()
        self.discard_pile = CardContainer()
        self.play_mat = CardContainer()

        # Draw the initial hand for the player.
        self.draw_hand()

        # How many turns the player has taken.
        self.turns = 0

        # Number of action points and buy points.
        self.actions = 0
        self.buys = 0

        # The number of coins is a sum of coins they accumulate during
        # their turn and based on the Treasure cards in their hand.
        self.turn_coins = 0
        self.hand_coins = 0
        self.coins = 0

        # Number of victory points accumulated, mostly used for end game.
        self.victory_points = 0

        # Reset actions, buys, and coins to prepare for the first turn.
        self.reset_points()
        self.set_coins()

    def draw(self, num_cards=1):
        """Generic method to draw cards from the deck to the hand.

        num_cards: int (default 1)
            The number of cards to draw from the deck. If the
            deck is empty, place the discard pile in the deck
            and shuffle it.

        """

        # Raise an error if you're trying to draw more cards than are available.
        if num_cards > (self.deck.num_cards + self.discard_pile.num_cards):
            raise DominionError(f"Cannot draw {num_cards} cards.")

        # Loop for however many cards you want to draw.
        for _ in range(num_cards):
            try:
                # Transfer from the deck to the hand.
                transfer(self.deck, self.hand, [0])
            except DominionError:
                # If not enough cards, shuffle and draw again.
                transfer(self.discard_pile, self.deck)
                self.deck.shuffle()
                transfer(self.deck, self.hand, [0])

    def draw_hand(self):
        """Simple method to draw 5 cards.

        """

        self.draw(num_cards=5)

    def reset_points(self):
        """Method to reset actions, buys, and coins prior to every turn.

        """

        # Each player starts their turn with 1 action & 1 buy. 
        self.actions = 1
        self.buys = 1

        # Start with 0 accumulated coins in each turn.
        self.turn_coins = 0

    def increment_actions(self, increment):
        """Simple method to add to the number of action points.

        Parameters
        ----------
        increment: int
            Number by which to change action points.

        """

        # This can be negative as well.
        self.actions += increment

    def increment_buys(self, increment):
        """Simple method to add to the number of buy points.

        Parameters
        ----------
        increment: int
            Number by which to change buy points.

        """

        # This can be negative as well.
        self.buys += increment

    def increment_coins(self, increment):
        """Simple method to add to the number of accumulated coins.

        Parameters
        ----------
        increment: int
            Number by which to change coins.

        """

        # This can be negative as well.
        self.turn_coins += increment

    def count_coins(self):
        """Method to add up the number of coins in one's hand.

        """

        # Get a list of the number of coins represented in player's hand.
        card_coins = [card.coin for card in self.hand.cards if 'Treasure' in get_parent_classes(card)]

        # Sum up the number of coins.
        self.hand_coins = sum(card_coins)

    def set_coins(self):
        """Method to calculate and set the number of coins a player has.

        """

        # First count the number of coins in your hand.
        self.count_coins()

        # Then add to the number of coins accumulated during the turn.
        self.coins = self.turn_coins + self.hand_coins

    def discard(self):
        """Abstract method for how a player discards a card.

        """

        raise NotImplementedError("Must implement a discard method.")

    def trash(self):
        """Abstract method for how a player trashes a card.

        """

        raise NotImplementedError("Must implement a trash method.")

    def turn(self):
        """Abstract method for how a player proceeds through their turn.

        """

        raise NotImplementedError("Must implement a turn method.")

    def action(self):
        """Abstract method for how a player plays an action.

        """

        raise NotImplementedError("Must implement an action method.")

    def buy(self):
        """Abstract method for how a player buys a card.

        """

        raise NotImplementedError("Must implement a buy method.")

    def free_buy(self):
        """Abstract method for how a player free buys a card.

        """

        raise NotImplementedError("Must implement a free buy method.")

    def cleanup(self):
        """Method to perform post-turn cleanup.

        """

        # First transfer all cards from the play mat and hand to the discard pile.
        transfer(self.play_mat, self.discard_pile)
        transfer(self.hand, self.discard_pile)

        # Next draw a fresh hand.
        self.draw_hand()

        # Finally reset actions, buys, and coins for the next turn.
        self.reset_points()
        self.set_coins()

    def end_game(self):
        """Method to perform end game actions and count victory points.

        """

        # Transfer all cards to the player's deck.
        transfer(self.play_mat, self.discard_pile)
        transfer(self.hand, self.discard_pile)
        transfer(self.discard_pile, self.deck)

        # Now add up the number of victory points in the deck.
        card_victory_pts = 0
        for card in self.deck.cards:
            card_victory_pts += getattr(card, "victory", 0)

        # Make sure to keep any victory points accumulated during the game.
        self.victory_points += card_victory_pts

    def display_hand(self):
        """Method to display the contents of one's hand to screen.

        """

        # Print a nice multiline string showing the contents.
        return_str = f"\n{self.name}'s Hand\n" + "-" * (len(self.name) + 7) + "\n"
        return_str += str(self.hand) + "\n"
        print(return_str)

    def display_totals(self):
        """Method to display the number of action points, buy points, and coins.

        """

        print(f"Totals: {self.actions} Action(s), {self.buys} Buy(s), {self.coins} Coin(s)")

    def __str__(self):
        """Custom str representation of the player.

        """

        return self.name

    def __repr__(self):
        """Custom obj representation for the player.

        """

        return self.__str__()


class Human(Player):
    """Class defining a human player of Dominion.

    """

    def __init__(self, name):
        """Initialize a human player here.

        Parameters
        ----------
        name: str
            The name of the player as a string.

        """

        # Call parent class initializer.
        super().__init__(name)

    def discard(self, config):
        """Human discard method.

        Notes: This method makes extensive use of the
        input function to get input from the user.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First display the contents of the player's hand.
        self.display_hand()

        # Loop until we get a valid response.
        while True:

            # Ask the use what card they want to discard.
            response = input(f"{self.name}, what card would you like to discard? ").lower()

            # Player can pass here.
            if response == 'pass':
                raise DominionPassError("pass")

            # Player can also quit here.
            elif response == 'quit':
                raise DominionQuitError(f"Game quit by {self.name}.")

            # Player can ask for help, this is context sensitive.
            elif 'help' in response:
                if response == 'help':
                    Info(config, topic="discard")
                else:
                    Info(config, response=response)
                continue

            # Now check to see if the response is an integer.
            try:
                response = int(response)
            except:
                print("Invalid card identifier. Specify an integer.")
                continue

            # Now check to see that the response defines a valid identifier for a card.
            # If it is, transfer from the hand to discard pile. If not, try again.
            if response in self.hand.identifiers:
                print(f"{self.name} discards {self.hand.cards[response].name}.")
                transfer(self.hand, self.discard_pile, [response])
                break
            else:
                print("Invalid card identifier.")

    def trash(self, config, card_type=None):
        """Human trash method.

        Notes: This method makes extensive use of the
        input function to get input from the user.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First display the player's hand.
        self.display_hand()

        # Loop until we get a valid response.
        while True:

            # We can ask for a specific type of card to trash.
            if card_type is None:
                response = input(f"{self.name}, select a card to trash: ").lower()
            else:
                response = input(f"{self.name}, select a {card_type} card to trash: ").lower()

            # The player can pass here.
            if response == 'pass':
                raise DominionPassError("pass")

            # The player can also quit here.
            elif response == 'quit':
                raise DominionQuitError(f"Game quit by {self.name}.")

            # The player can ask for help, which is optionally context sensitive.
            elif 'help' in response:
                if response == 'help':
                    Info(config, topic="trash")
                else:
                    Info(config, response=response)
                continue

            # Check to see if the response is an integer.
            try:
                response = int(response)
            except:
                print("Invalid card identifier. Specify an integer.")
                continue

            # If the response denotes a valid identifier for a card, proceed.
            if response in self.hand.identifiers:

                # If we don't care what type of card it is.
                if card_type is None:

                    # Trash the card and return the cost of the card.
                    print(f"{self.name} trashes {self.hand.cards[response].name}.")
                    card_cost = self.hand.cards[response].cost
                    transfer(self.hand, config.trash, [response])
                    return card_cost

                # If we do care what type of card it is.
                elif card_type in get_parent_classes(self.hand.cards[response]):

                    # Trash the card and return the cost of the card.
                    print(f"{self.name} trashes {self.hand.cards[response].name}.")
                    card_cost = self.hand.cards[response].cost
                    transfer(self.hand, config.trash, [response])
                    return card_cost

                # If the player selects an invalid card type.
                else:
                    print(f"Cannot trash that type of card.")
                    continue

            # Try again.
            else:
                print("Invalid card identifier.")

    def turn(self, config):
        """Human turn method.

        Notes: This method can probably live in the parent
        class since the CPU will eventually have to use
        this exact same logic.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First increment the number of turns.
        self.turns += 1

        # Print the key and the current supply.
        Info(config).info_key()
        print(str(config.supply) + "\n")

        # Now tell the player it's their turn.
        print_str = f"{self.name}'s Turn"
        print("-" * len(print_str) + f"\n{print_str}\n" + "-" * len(print_str))

        # The action phase
        self.action_phase(config)

        # The buy phase
        self.buy_phase(config)

        # The clean-up phase
        self.cleanup()

    def action_phase(self, config):
        """The action phase for the human player.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # Only do this if they have enough action points.
        if self.actions > 0:

            # Calculate the number of coins the user has.
            print("\n***** Action Phase *****")
            self.set_coins()

            # Until we run out of action points, perform an action or pass.
            while self.actions > 0:
                try:
                    self.action(config)
                except DominionPassError:
                    self.actions = 0
                    break

    def buy_phase(self, config):
        """The buy phase for the human player.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # Only do this if they have enough buy points.
        if self.buys > 0:

            # Calculate the number of coins the user has.
            print("\n***** Buy Phase *****")
            self.set_coins()

            # Loop until they run out of buy points or pass.
            while self.buys > 0:
                try:
                    self.buy(config)
                except DominionPassError:
                    self.buys = 0
                    break

    def action(self, config):
        """Human action method.

        Notes: This method makes extensive use of the
        input function to get input from the user.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First calculate the number of coins and display the player's hand.
        self.set_coins()
        self.display_hand()
        self.display_totals()

        # If somehow we make it here but don't have enough action points.
        if self.actions < 1:
            print(f"{self.name} cannot perform an action, no action points left.")
            return

        # Loop until we get a valid response.
        while True:

            # Ask the user what card they want to play.
            response = input(f"{self.name}, what action card would you like to play? ").lower()

            # The player can pass here.
            if response == 'pass':
                raise DominionPassError("pass")

            # The player can quit here.
            elif response == 'quit':
                raise DominionQuitError(f"Game quit by {self.name}.")

            # The player can ask for help here. This is context sensitive.
            elif 'help' in response:
                if response == 'help':
                    Info(config, topic="action")
                else:
                    Info(config, response=response)
                continue

            # Check that the response is an integer.
            try:
                response = int(response)
            except:
                print("Invalid card identifier. Specify an integer.")
                continue

            # Check that the response is a valid identifier for a card in hand.
            if response in self.hand.identifiers:

                # Make sure the card is an action card.
                if 'Action' not in get_parent_classes(self.hand.cards[response]):
                    print("Not an action card.")
                    continue

                # If valid, play the card and enter its action method.
                else:
                    self.actions -= 1
                    transfer(self.hand, self.play_mat, [response])
                    self.play_mat.cards[-1].action(config)
                    transfer(self.play_mat, self.discard_pile, [-1])
                    break

            # Try again.
            else:
                print("Invalid card identifier.")

    def buy(self, config):
        """Human buy method.

        Notes: This method makes extensive use of the
        input function to get input from the user.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.

        """

        # First calculate the number of coins and display the player's hand.
        self.set_coins()
        self.display_hand()
        self.display_totals()

        # If we made it here but don't have buy points, return.
        if self.buys < 1:
            print(f"{self.name} cannot buy anything, no buy points left.")
            return

        # Loop until we get a valid response.
        while True:

            # Ask the user what they would like to buy.
            response = input(f"{self.name}, what card would you like to buy? ").lower()

            # The player can pass here.
            if response == 'pass':
                raise DominionPassError("pass")

            # The player can quit here.
            elif response == 'quit':
                raise DominionQuitError(f"Game quit by {self.name}.")

            # The player can ask for help here. This is context sensitive.
            elif 'help' in response:
                if response == 'help':
                    Info(config, topic="buy")
                else:
                    Info(config, response=response)
                continue

            # Check that the response is an integer.
            try:
                response = int(response)
            except:
                print("Invalid card identifier. Specify an integer.")
                continue

            # If the identifier is in the base supply.
            if response in config.supply.base_supply.identifiers:

                # Check that there is enough inventory.
                if config.supply.base_supply.decks[response].num_cards < 1:
                    print("Cannot buy, not enough inventory.")
                    continue

                # Ok now we can proceeds.
                else:

                    # Check if the player has enough coin to buy it.
                    if config.supply.base_supply.decks[response].cards[0].cost > self.coins:
                        print("Cannot buy, not enough coin.")
                        continue

                    # Buy the card, put it in the discard pile, decrement the coins and buy points.
                    else:
                        self.turn_coins -= config.supply.base_supply.decks[response].cards[0].cost
                        self.buys -= 1
                        print(f"{self.name} buys {config.supply.base_supply.decks[response].cards[0].name}.")
                        transfer(config.supply.base_supply.decks[response], self.discard_pile, [0])
                        break

            # If the identifier is in the kingdom supply.
            elif response in config.supply.kingdom_supply.identifiers:

                # Modify the identifier to account for it being after the base supply.
                local_id = response - config.supply.kingdom_supply.id_start

                # Check if there is enough inventory to buy.
                if config.supply.kingdom_supply.decks[local_id].num_cards < 1:
                    print("Cannot buy, not enough inventory.")
                    continue

                # Proceed now.
                else:

                    # Check if the player has enough coin to buy the card.
                    if config.supply.kingdom_supply.decks[local_id].cards[0].cost > self.coins:
                        print("Cannot buy, not enough coin.")
                        continue

                    # If they can buy, buy the card, decrement buy points and coins.
                    else:
                        self.turn_coins -= config.supply.kingdom_supply.decks[local_id].cards[0].cost
                        self.buys -= 1
                        print(f"{self.name} buys {config.supply.kingdom_supply.decks[local_id].cards[0].name}.")
                        transfer(config.supply.kingdom_supply.decks[local_id], self.discard_pile, [0])
                        break

            # Try again.
            else:
                print("Invalid card identifier.")
                continue

    def free_buy(self, config, max_cost, card_type=None, destination='discard'):
        """Human free buy method.

        Notes: This method makes extensive use of the
        input function to get input from the user. This function
        is typically called after playing an action card,
        where the card says to purchase a card worth up to
        a certain amount, but it shouldn't detract from the
        player's coins. In the real Dominion game, this is
        typically referred to as 'gaining' a card.

        Parameters
        ----------
        config: dominion.Config type
            The configuration object for the current game.
        max_cost: int
            The max allowable cost of the card you are buying.
        card_type: str (default None)
            The type of card specified as a string. If None, the
            player can free buy any type of card.
        destination: str (default 'discard')
            Valid options are 'hand' or 'discard'. This
            is where the gained card will end up.

        """

        # Set the destination for the card based on the input.
        if destination == 'hand':
            dest_pile = self.hand
        elif destination == 'discard':
            dest_pile = self.discard_pile
        else:
            raise DominionError(f"Cannot gain a card to {destination} location.")

        # Loop until we get a valid response.
        while True:

            # Prompt the user to play an action card.
            response = input(f"{self.name}, what card up to {max_cost} coin would you like to buy? ").lower()

            # The player can pass here.
            if response == 'pass':
                raise DominionPassError("pass")

            # The player can quit here.
            elif response == 'quit':
                raise DominionQuitError(f"Game quit by {self.name}.")

            # The player can ask for help, which is context sensitive.
            elif 'help' in response:
                if response == 'help':
                    Info(config, topic="buy")
                else:
                    Info(config, response=response)
                continue

            # Check that the response is an integer.
            try:
                response = int(response)
            except:
                print("Invalid card identifier. Specify an integer.")
                continue

            # If the specified card is in the base supply, enter here.
            if response in config.supply.base_supply.identifiers:

                # Check that there's enough inventory.
                if config.supply.base_supply.decks[response].num_cards < 1:
                    print("Cannot buy, not enough inventory.")
                    continue

                # Check that the card type is valid.
                if card_type is not None:
                    if card_type not in get_parent_classes(config.supply.base_supply.decks[response].cards[0]):
                        print(f"Cannot buy that type of card. Can only buy a {card_type} card.")
                        continue

                # Check that the card costs less than the max allowable cost.
                if config.supply.base_supply.decks[response].cards[0].cost > max_cost:
                    print("Cannot buy, not enough coin.")
                    continue

                # Finally we can purchase the card!
                else:
                    print(f"{self.name} gains {config.supply.base_supply.decks[response].cards[0].name}.")
                    transfer(config.supply.base_supply.decks[response], dest_pile, [0])
                    break

            # If the specified card is in the kingdom supply, enter here.
            elif response in config.supply.kingdom_supply.identifiers:

                # Get the identifier for the card in the kingdom supply.
                local_id = response - config.supply.kingdom_supply.id_start

                # Check if there's enough inventory to buy.
                if config.supply.kingdom_supply.decks[local_id].num_cards < 1:
                    print("Cannot buy, not enough inventory.")
                    continue

                # Check that the card is the right type.
                if card_type is not None:
                    if card_type not in get_parent_classes(config.supply.kingdom_supply.decks[local_id].cards[0]):
                        print(f"Cannot buy that type of card. Can only buy a {card_type} card.")
                        continue

                # Check that the cost is less than the max allowable.
                if config.supply.kingdom_supply.decks[local_id].cards[0].cost > max_cost:
                    print("Cannot buy, not enough coin.")
                    continue

                # Finally we can gain the card.
                else:
                    print(f"{self.name} gains {config.supply.kingdom_supply.decks[local_id].cards[0].name}.")
                    transfer(config.supply.kingdom_supply.decks[local_id], dest_pile, [0])
                    break

            # Try again.
            else:
                print("Invalid card identifier.")
                continue


class CPU(Player):
    """The placeholder CPU class.

    """

    def __init__(self, name, strategy="big_money", difficulty="easy"):
        """Initialize a CPU here. NOT IMPLEMENTED.

        Parameters
        ----------
        NOT SURE IT COULD CHANGE.

        """

        # Not implemented!
        raise NotImplementedError("No CPU players allowed.")
