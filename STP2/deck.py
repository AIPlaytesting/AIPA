import Pile
import json

class CardInstance:
    def __init__(self,card_name,game_unique_id):
        self.card_name = card_name
        self.game_unique_id = game_unique_id

# all cards are stored as names(str)
class Deck:

    def __init__(self,all_cards_names):
        super().__init__()
        self.internal_id_counter = 0
        self.__draw_pile = Pile.Pile()# CardInstance[]  
        self.__discard_pile = Pile.Pile()# CardInstance[]  
        self.__cards_on_hand = [] # CardInstance[]  
        self.reset_deck(all_cards_names)

    def reset_deck(self,all_cards_names):
        self.__draw_pile.resetPile()
        self.__discard_pile.resetPile()

        card_composition = self.__load_card_composition()
        cards_in_deck = []
        for card_name in all_cards_names:
            card_count = card_composition[card_name] if  card_name in card_composition else 1
            for i in range(card_count):
                guid = self.__assign_game_uniqe_id(card_name)
                card_instance = CardInstance(card_name,guid)
                cards_in_deck.append(card_instance)

        print("deck: ", cards_in_deck)
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

    # return __discard_pile.cards [fe,2,3,4] 
    def get_discard_pile(self):
        return self.__discard_pile

    def get_draw_pile(self):
        return self.__draw_pile

    def __assign_game_uniqe_id(self,card_name)->str:
        guid = card_name + str(self.internal_id_counter)
        self.internal_id_counter+=1
        return guid

    def __load_card_composition(self):
        PATH = "Decks/" + "deck_1.0.json"
        with open(PATH, "r") as file:
            raw_json_data = file.read()
            deck_info = json.loads(raw_json_data)     
            card_composition = deck_info["Composition"]
            return card_composition