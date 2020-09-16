import Pile
class Deck:
    def __init__(self):
        super().__init__()
        self.__draw_pile = Pile.Pile()
        self.__discard_pile = Pile.Pile()
        self.__cards_on_hand = [] # string[]  each item is the name of the card
        self.reset_deck()

    def reset_deck(self):
        self.__draw_pile.resetPile()
        self.__discard_pile.resetPile()
        # TODO reset the cards from real names
        self.__draw_pile.addCards(["card1","card2","card3","card4","card5","card6","card7","card8","card9"])

    def get_card_names_on_hand(self):
        return self.__cards_on_hand

    def draw_cards(self,num):
        for i in range(num):
            if self.__draw_pile.cardsLeft() <= 0:
                # shuffle discard pile into draw pile
               self. __draw_pile.addCards(self.__discard_pile.cards)
               self. __discard_pile.resetPile()

            self.__cards_on_hand.append(self.__draw_pile.draw())

    def discard_card(self,card_name):
        if card_name in self.__cards_on_hand:
            self.__cards_on_hand.remove(card_name)
            self.discard_card.append(card_name)

    def discard_all_cards(self):
            self.__discard_pile.addCards(self.__cards_on_hand)
            self.__cards_on_hand.clear()

