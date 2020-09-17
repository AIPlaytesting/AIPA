import CardBase
import game_manager
import EffectCalculator

class CardPlayManager:
    # this class creates and manages instances of the cards

    def __init__(self, game_manager, effect_calculator):
        self.game_manager = game_manager
        self.card_effects_manager = effect_calculator
        self.CreateCardInstances()

    def CreateCardInstances(self):
        self.cards_dict = {}
        self.cards_dict['Anger'] = CardBase.Card('Anger')
        self.cards_dict['Body Slam'] = CardBase.Card('Body Slam')
        self.cards_dict['Clothesline'] = CardBase.Card('Clothesline')
        self.cards_dict['Defend'] = CardBase.Card('Defend')
        self.cards_dict['Double Tap'] = CardBase.Card('Double Tap')
        self.cards_dict['Flex'] = CardBase.Card('Flex')
        self.cards_dict['Heavy Blade'] = CardBase.Card('Heavy Blade')
        self.cards_dict['Iron Wave'] = CardBase.Card('Iron Wave')
        self.cards_dict['Pommel Strike'] = CardBase.Card('Pommel Strike')
        self.cards_dict['Shrug It Off'] = CardBase.Card('Shrug It Off')
        self.cards_dict['Sword Boomerang'] = CardBase.Card('Sword Boomerang')

    def PlayCard(self, cardName):

        if not cardName in self.cards_dict:
            print(cardName + ' is an invalid card name')
            return

        card = self.cards_dict[cardName]

        # Apply buffs
        for key in card.buffs:

            if(card.buffs[key]['target'] == 'enemy'):
                buff_target = self.game_manager.game_state.boss
            else:
                buff_target = self.game_manager.game_state.player

            buff_value = card.buffs[key]['value']

            self.card_effects_manager.ApplyBuff(self.game_manager.game_state.player, buff_target, key, buff_value)

        # Create Block
        self.card_effects_manager.AddBlock(
            self.game_manager.game_state.player, card.damage_block['block'])

        # Deal Damage
        for i in range(0, card.damage_block['damage_instances']):
            self.card_effects_manager.DealDamage(self.game_manager.game_state.player, self.game_manager.game_state.boss,
                card.damage_block['damage'], card.special_mod['strength_multiplier'])

        #Draw card
        self.game_manager.game_state.deck.draw_cards(card.card_life_cycle['draw_card'])

        # TODO : Add to discard pile (pile.py) [add functionality for removing card from hand]
        self.game_manager.game_state.deck.discard_card(cardName,card.card_life_cycle["copies_in_discard_pile_when_played"])

        # Reduce player energy
        self.card_effects_manager.ReducePlayerEnergy(card.energy_cost)

    def GetEmptyBuffDict(self):
        buff_dict = self.cards_dict['Anger'].buffs

        empty_buff_dict = {}

        for key in buff_dict:
            empty_buff_dict[key] = 0

        return empty_buff_dict
