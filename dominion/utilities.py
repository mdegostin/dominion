"""The utilities module defines various Dominion utilities.

"""

import textwrap

from errors import DominionError
import cards


class Info():
    """The Info class describes rules and is the game's help menu.

    This class is mainly interacted with via player typing help during
    gameplay. They can specify a topic or get a context-sensitive help.

    """

    def __init__(self, config, response=None, topic=None):
        """Initialize the Info class and print help messages.

        Parameters
        ----------
        config: dominion.Config type
            The current game's config object.
        response: str (default None)
            The user's help query captured via input().
        topic: str (default None)
            The user's topic when they call help.

        """

        # This dictionary of pointers helps return the right help info
        # depending on which topic is asked about.
        info_funcs = {'buy': self.info_buy,
                      'action': self.info_action,
                      'discard': self.info_discard,
                      'trash': self.info_trash,
                      'key': self.info_key,
                      'supply': self.info_supply,
                      'rules': self.info_rules,
                      }

        # Context-sensitive help menu. A topic is passed in.
        if response is None:
            if topic is not None:

                # Call the correct help function to return a helpful message.
                info_funcs[topic](config=config)

        # Non-context-sensitive help menu.
        else:

            # Split the response string to determine the topic.
            help_strs = response.split()
            if len(help_strs) != 2:
                print("Not a valid help topic.")
            else:
                topic = help_strs[1]

            # Get a list of all card classes and names in the cards module.
            cls_list = (cards.Treasure.__subclasses__()
                        + cards.Victory.__subclasses__()
                        + cards.Action.__subclasses__())
            card_names = [cls.__name__.lower() for cls in cls_list]

            # If the user asks about a specific card type.
            if topic in card_names:
                num = card_names.index(topic)
                cls_list[num]().info()

            # Otherwise the topic is maybe defined in this class.
            else:
                try:
                    info_funcs[topic](config=config)
                except (AttributeError, KeyError):
                    print("Not a valid help topic.")

    def info_buy(self, **kwargs):
        """Method prints a formatted description of the buy phase.

        """

        msg = ("Select a card from the supply to purchase by specifying the "
               "card identifier (# next to the card). To view the available "
               "cards again, type help supply. You must have 1 or more buy points "
               "to make a purchase, in addition to the requisite number of coins. "
               "If either of these conditions are not met or you do not want to "
               "purchase a card, you may continue by typing pass.")
        self._print_formatted(msg)

    def info_action(self, **kwargs):
        """Method prints a formatted description of the action phase.

        """

        msg = ("Select an action card from your hand to play by specifying the "
               "card identifier (# next to the card). If your hand does not "
               "contain any action cards, you may continue to the buy phase by "
               "typing pass.")
        self._print_formatted(msg)

    def info_discard(self, **kwargs):
        """Method prints a formatted description of the discard action.

        """

        msg = ("Select a card from your hand to discard by specifying the "
               "card identifier (# next to the card). If you choose to not "
               "discard, you may continue by typing pass.")
        self._print_formatted(msg)

    def info_trash(self, **kwargs):
        """Method prints a formatted description of the trash action.

        """

        msg = ("Select a card from your hand to trash (remove from the game) "
               "by specifying the card identifier (# next to the card). If the "
               "instructions specify a specific type of card to trash, you must "
               "choose a card of that type from your hand. You can also choose to "
               "not trash a card by typing pass.")
        self._print_formatted(msg)

    def info_supply(self, **kwargs):
        """Method prints the current supply.

        """

        print("\n" + str(kwargs['config'].supply) + "\n")

    def info_key(self, **kwargs):
        """Method prints the key defining actions the user can take.

        This helps the user determine what they can type in the command
        line interface.

        """

        print("\nEffect Key: (C=Coin) (V=Victory) (A=Action) (Ca=Cards) (B=Buy)\n"
              "Card Type Key: (T=Treasure) (V=Victory) (A*=Action) (AA=Attack) (AR=Reaction)\n"
              "User Actions: (# = No. of Card) (pass = Pass to Next Phase)\n"
              "User Actions: (quit = Quit Game) (help or help <topic> = Get help)\n"
              "Help Menu Topics: rules, action, buy, discard, trash, key, supply, "
              "and any card name.\n")

    def info_rules(self, **kwargs):
        """Method prints a formatted description of the game's rules.

        """

        msg = ("\nWelcome to Dominion! Provided below is a brief summary of the rules\n"
               "of the game. There are many more detailed rules in the complete game,\n"
               "however this should give you a basic overview. If you wish to learn\n"
               "more, it is recommended to read the Dominion wiki page or the\n"
               "Dominion_Project_Overview.pdf file accompanying this source code.\n\n"
               "In a game of Dominion, each player is given a starting deck of 10 cards,\n"
               "and they play around a Supply of card piles that they can buy from over\n"
               "the game.\n\nOn their turn, a player goes through three turn phases:\n\n1) "
               "Action (A) - They may play one Action card from their hand. Some Action\n"
               "cards are non-terminal, meaning they provide the player with additional\n"
               "action points that the player can use to play additional action cards.\n"
               "Action cards in general contain instructions to follow when the card\n"
               "is played; for example, a card might tell the player to draw three additional\n"
               "cards into their hand. An Action card might also be an Attack card, where\n"
               "it forces other players to be at a disadvantage. An Action card might also\n"
               "be a Reaction card, which can be used to counter or react to Attack cards.\n\n"
               "2) Buy (B) - They may play their Treasure cards and buy one card that they\n"
               "can afford, putting that card in their discard pile. If an Action card played\n"
               "this turn gives the player additional buy points, the player can use them to\n"
               "purchase multiple cards in one turn. Some Action cards also let the player\n"
               "'gain' a card from the Supply. In these cases, the player may choose a card\n"
               "meeting certain constraints to buy without affecting their buy points or coins.\n\n"
               "3) Clean-up (C) - They take all cards they've played, and all cards remaining\n"
               "in their hand, and put them in their discard pile. They then draw a fresh hand\n"
               "of 5 cards from their deck, and end their turn. When any player needs to draw\n"
               "cards from their deck and there are not enough cards left to do so, the\n"
               "player's discard pile is used to replace the deck and then shuffled. In\n"
               "this way, cards bought in earlier turns will become playable in later turns.\n\n"
               "The game ends when either 3 Supply piles are empty, or when the Province\n"
               "pile specifically empties. At the end of the game, the player with the most\n"
               "victory points wins.\n\n"
               "At any point while playing, the player can ask for help via typing 'help'\n"
               "(without quotes) at the prompt. 'help key' is particularly useful at it\n"
               "gives the player a list of things they can type during gameplay, including\n"
               "'quit' to quit the game. Enjoy!\n")

        print(msg)

    def _print_formatted(self, msg):
        """Method to wrap a long string into a nicely formatted multiline.

        """

        # Use the textwrap module to do this.
        msg_formatted = textwrap.fill(msg)
        print("\n" + msg_formatted + "\n")

    def __str__(self, **kwargs):
        """Custom str representation of the help menu.

        """

        # I'm not quite sure why this is here, but I don't want to break anything.

        return ""

    def __repr__(self, **kwargs):
        """Custom obj representation of the help menu.

        """

        # I'm not quite sure why this is here, but I don't want to break anything.
        return ""


def transfer(source, target, identifiers=None):
    """Transfer method transfers a group of cards from one container to another.

    Parameters
    ----------
    source: containers.CardContainer type
        The source card container.
    target: containers.CardContainer type
        The target card container.
    identifiers: list of int or None (default None)
        The list of identifiers to transfer. If None
        this will transfer all possible cards from
        the source to the target.

    """

    # If no identifiers are provided, use all of the cards in the source.
    if identifiers is None:
        transferred = source.remove_cards(source.identifiers)

    # Otherwise use the identifiers specified.
    else:
        transferred = source.remove_cards(identifiers)

    # Add the removed cards from the source to the target.
    target.add_cards(transferred)


def get_parent_classes(item):
    """A helper function to get a list of the parent class names of a class.

    Parameters
    ----------
    item: object
        Any object!
    
    """

    # Returns a list of parent class names.
    list_of_parents = [class_type.__name__ for class_type in item.__class__.mro()]

    return list_of_parents
