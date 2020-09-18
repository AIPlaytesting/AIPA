import Pile
import json

# all cards are stored as names(str)
class Deck:
    def __init__(self,all_cards_names):
        super().__init__()
        self.__draw_pile = Pile.Pile()
        self.__discard_pile = Pile.Pile()
        self.__cards_on_hand = [] # string[]  each item is the name of the card
        self.reset_deck(all_cards_names)

    def reset_deck(self,all_cards_names):
        self.__draw_pile.resetPile()
        self.__discard_pile.resetPile()

        card_composition = self.__load_card_composition()
        cards_in_deck = []
        for card in all_cards_names:
            card_count = card_composition[card] if  card in card_composition else 1
            for i in range(card_count):
                cards_in_deck.append(card)
        print("deck: ", cards_in_deck)
        self.__draw_pile.addCards(cards_in_deck)

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

    # return __discard_pile.cards [fe,2,3,4] 
    def getDiscardPile(self):
        return self.__discard_pile

    def getDrawPile(self):
        return self.__draw_pile

    def __load_card_composition(self):
        PATH = "Decks/" + "deck_1.0.json"
        with open(PATH, "r") as file:
            raw_json_data = file.read()
            deck_info = json.loads(raw_json_data)     
            card_composition = deck_info["Composition"]
            return card_composition