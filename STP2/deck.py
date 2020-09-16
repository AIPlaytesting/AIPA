import Pile

# all cards are stored as names(str)
class Deck:
    def __init__(self,all_cards_names):
        super().__init__()
        self.__draw_pile = Pile.Pile()
        self.__discard_pile = Pile.Pile()
        self.__cards_on_hand = [] # string[]  each item is the name of the card
        self.reset_deck(all_cards_names)

    def reset_deck(self,all_cards_names):
        print("deck reset as: ", all_cards_names)
        self.__draw_pile.resetPile()
        self.__discard_pile.resetPile()
        self.__draw_pile.addCards(all_cards_names)

    def get_card_names_on_hand(self):
        return self.__cards_on_hand

    def draw_cards(self,num):
        for i in range(num):
            if self.__draw_pile.cardsLeft() <= 0:
                # shuffle discard pile into draw pile
               self. __draw_pile.addCards(self.__discard_pile.cards)
               self. __discard_pile.resetPile()

            self.__cards_on_hand.append(self.__draw_pile.draw())

    def discard_card(self,card_name,number_added_to_discard_pile):
        if card_name in self.__cards_on_hand:
            self.__cards_on_hand.remove(card_name)
            for i in range(number_added_to_discard_pile):
                self.__discard_pile.addCards([card_name])
        else:
            print("[ERROR]-Deck.discard_card(): discard a card which is not in hand")

    # remove all cards from hand to discard pile
    def discard_all_cards(self):
            self.__discard_pile.addCards(self.__cards_on_hand)
            self.__cards_on_hand.clear()

