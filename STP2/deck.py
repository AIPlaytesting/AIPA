import Pile
import json
from db.game_app_data import GameAppData

class CardInstance:
    def __init__(self,card_name,game_unique_id):
        self.card_name = card_name
        self.game_unique_id = game_unique_id
    def __str__(self):
        return self.card_name 

# all cards are stored as CardInstance
class Deck:
    def __init__(self,deck_config):
        super().__init__()
        self.internal_id_counter = 0
        self.__draw_pile = Pile.Pile()# CardInstance[]  
        self.__discard_pile = Pile.Pile()# CardInstance[]  
        self.__cards_on_hand = [] # CardInstance[]  
        self.reset_deck(deck_config)

    def reset_deck(self,deck_config):
        self.__draw_pile.resetPile()
        self.__discard_pile.resetPile()
        print(deck_config)
        cards_in_deck = []
        for card_name,card_number in deck_config.items():
            for i in range(card_number):
                guid = self.__assign_game_uniqe_id(card_name)
                card_instance = CardInstance(card_name,guid)
                cards_in_deck.append(card_instance)

        print("deck: ", [str(card_instance) for card_instance in cards_in_deck])
        self.__draw_pile.addCards(cards_in_deck)

    def get_card_names_on_hand(self):
        return [card_instance.card_name for card_instance in self.__cards_on_hand]

    def get_card_instances_on_hand(self):
        return self.__cards_on_hand

    def draw_cards(self,num):
        for i in range(num):
            if self.__draw_pile.cardsLeft() <= 0:
                # shuffle discard pile into draw pile
               self. __draw_pile.addCards(self.__discard_pile.cards)
               self. __discard_pile.resetPile()

            self.__cards_on_hand.append(self.__draw_pile.draw())

    def discard_card(self,card_name,number_added_to_discard_pile):
        for card_instance in self.__cards_on_hand:
            if card_name == card_instance.card_name:
                guid = card_instance.game_unique_id
                self.__cards_on_hand.remove(card_instance)
                # add coppies accroding to the given number
                for i in range(number_added_to_discard_pile):
                     # if not first copy, get new id
                    new_card_guid = guid if i == 0  else self.__assign_game_uniqe_id(card_name)
                    self.__discard_pile.addCards([CardInstance(card_name,new_card_guid)])
                break

    # remove all cards from hand to discard pile
    def discard_all_cards(self):
            self.__discard_pile.addCards(self.__cards_on_hand)
            self.__cards_on_hand.clear()

    def get_card_names_in_discard_pile(self):
        return [card_instance.card_name for card_instance in self.__discard_pile.cards]

    def get_discard_pile(self):
        return self.__discard_pile

    def get_card_names_in_draw_pile(self):
        return [card_instance.card_name for card_instance in self.__draw_pile.cards]
        
    def get_draw_pile(self):
        return self.__draw_pile

    def __assign_game_uniqe_id(self,card_name)->str:
        guid = card_name + str(self.internal_id_counter)
        self.internal_id_counter+=1
        return guid