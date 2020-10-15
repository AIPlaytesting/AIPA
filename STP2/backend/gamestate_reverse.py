from gameplay.game_state import GameState

def reverse_markup_to_gamestate(gamestate_markup:dict,gamestate:GameState):
    print('reverse -------------------------------')
    cards_on_hand = gamestate_markup['cardsOnHand']
    print('cards to reverse -------------------------------')
    new_cardnames_on_hand = []
    for cardmarkup in cards_on_hand:
        print("name",cardmarkup['name'],"guid",cardmarkup['gameUniqueID'])
        new_cardnames_on_hand.append(cardmarkup['name'])
    gamestate.deck.reset_cards_on_hand(new_cardnames_on_hand)
    print('reverse player info -------------------------------')
    player_markup = gamestate_markup['player']
    print('current hp',player_markup['currentHP'])
    gamestate.player.current_hp = player_markup['currentHP']
    print('block',player_markup['block'])
    gamestate.player.block = player_markup['block']