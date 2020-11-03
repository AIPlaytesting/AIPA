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
    # hp and block
    player_markup = gamestate_markup['player']
    print('current hp',player_markup['currentHP'])
    gamestate.player.current_hp = player_markup['currentHP']
    print('block',player_markup['block'])
    gamestate.player.block = player_markup['block']
    # buffs
    reversed_buffdict = {}
    for buff in player_markup['buffs']:
        reversed_buffdict[buff['buffName']] = buff['buffValue']
        print('buff:',buff['buffName'],'value',buff['buffValue'])
    for buffname in gamestate.player.buff_dict.keys():
        if buffname in reversed_buffdict:
            gamestate.player.buff_dict[buffname] = reversed_buffdict[buffname]
        else:
            gamestate.player.buff_dict[buffname] = 0

    print('reverse boss info -------------------------------')
    # hp and block
    boss_markup = gamestate_markup['enemies'][0]
    print('current hp',boss_markup['currentHP'])
    gamestate.boss.current_hp = boss_markup['currentHP']
    print('block',boss_markup['block'])
    gamestate.boss.block = boss_markup['block']
    # buffs
    reversed_buffdict = {}
    for buff in boss_markup['buffs']:
        reversed_buffdict[buff['buffName']] = buff['buffValue']
        print('buff:',buff['buffName'],'value',buff['buffValue'])
    for buffname in gamestate.boss.buff_dict.keys():
        if buffname in reversed_buffdict:
            gamestate.boss.buff_dict[buffname] = reversed_buffdict[buffname]
        else:
            gamestate.boss.buff_dict[buffname] = 0