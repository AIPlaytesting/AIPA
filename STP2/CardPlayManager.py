import CardBase
import game_manager
import CardEffectManager


class CardPlayManager:
    #this class creates and manages instances of the cards

    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.card_effects_manager = CardEffectManager.CardEffectManager(game_manager)
        self.CreateCardInstances()
        
    def CreateCardInstances(self):
        self.cards_dict = {}
        self.cards_dict['Anger'] = CardBase.Card('Anger')

    
    def PlayCard(self, cardName):

        if not cardName in self.cards_dict:
            print(cardName + ' is an invalid card name')
            return

        card = self.cards_dict[cardName]

        #Apply buffs
        for key in card.buffs:

            if(card.buffs[key]['target'] == 'enemy'):
                buff_target = self.game_manager.game_state.boss
            else:
                buff_target = self.game_manager.game_state.player

            buff_value = card.buffs[key]['value']

            self.card_effects_manager.ApplyBuff(buff_target, key, buff_value)

        #Create Block
        self.card_effects_manager.AddBlock(self.game_manager.game_state.player, card.damage_block['block'])

        #Deal Damage 
        for i in range(0, card.damage_block['damage_instances']):
            self.card_effects_manager.DealDamage(self.game_manager.game_state.player, self.game_manager.game_state.boss, card.damage_block['damage'], card.special_mod['strength_multiplier'])

        # TODO : Draw card (pile.py)

        # TODO : Add to discard pile (pile.py) [add functionality for removing card from hand]

        #Reduce player energy
        self.card_effects_manager.ReducePlayerEnergy(card.energy_cost)


    def GetEmptyBuffDict(self):
        buff_dict = self.cards_dict['Anger'].buffs

        empty_buff_dict = {}

        for key in buff_dict:
            empty_buff_dict[key] = 0

        return empty_buff_dict
        

        