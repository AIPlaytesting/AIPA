import CardBase
import game_manager
import EffectCalculator
from game_event import GameEvent

class CardPlayManager:
    # this class creates and manages instances of the cards

    def __init__(self, game_manager, effect_calculator):
        self.game_manager = game_manager
        self.card_effects_manager = effect_calculator
        self.CreateCardInstances()
        self.next_attack_count = 1

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

    # return GameEvent[] which happens AFATER played this card
    def PlayCard(self, cardName):

        if not cardName in self.cards_dict:
            print(cardName + ' is an invalid card name')
            return []

        game_events = []

        card = self.cards_dict[cardName]

        card_play_count = self.next_attack_count if card.type == 'Attack' else 1

        for i in range(0, card_play_count):
            # Apply buffs
            for key in card.buffs:
                if(card.buffs[key]['target'] == 'enemy'):
                    buff_target = self.game_manager.game_state.boss
                else:
                    buff_target = self.game_manager.game_state.player

                # TODO: should be += card.buffs[key]['value'], however becuase of thron bug in Guardien, will fix in future
                buff_value = card.buffs[key]['value']
                self.card_effects_manager.ApplyBuff(self.game_manager.game_state.player, buff_target, key, buff_value)
                
                # TODO: should record buff only it change
                if buff_value != 0:
                    # record game event
                    buff_change_event = GameEvent.create_buff_change_event(buff_target.game_unique_id,key,buff_value)
                    game_events.append(buff_change_event)

            # Create Block
            self.card_effects_manager.AddBlock(self.game_manager.game_state.player, card.damage_block['block'])
            # record bock change event
            block_diff  = card.damage_block['block']
            if block_diff != 0:
                block_change_event = GameEvent.create_block_change_event(
                    self.game_manager.game_state.player.game_unique_id,
                    self.game_manager.game_state.player.block)
                game_events.append(block_change_event)

            # Deal Damage
            for i in range(0, card.damage_block['damage_instances']):
                
                if card.special_mod['unique_damage'] == 'none':
                    damage_value = card.damage_block['damage']
                elif card.special_mod['unique_damage'] == 'block':
                    damage_value = self.game_manager.game_state.player.block

                damage_events = self.card_effects_manager.DealDamage(self.game_manager.game_state.player, self.game_manager.game_state.boss,
                    damage_value, card.special_mod['strength_multiplier'])
                # record damage events 
                game_events.extend(damage_events)

            #Draw card
            self.game_manager.game_state.deck.draw_cards(card.card_life_cycle['draw_card'])

        # Add to discard pile
        self.game_manager.game_state.deck.discard_card(cardName,card.card_life_cycle["copies_in_discard_pile_when_played"])

        # Reduce player energy
        self.card_effects_manager.ReducePlayerEnergy(card.energy_cost)

        # Modify the next_attack_count variable. [Attack card always resets it to 1]. 
        self.next_attack_count = 1 if card.type == 'Attack' else self.next_attack_count
        self.next_attack_count = card.special_mod['next_attack_count'] if cardName == 'Double Tap' else self.next_attack_count

        return game_events

    def GetEmptyBuffDict(self):
        buff_dict = self.cards_dict['Anger'].buffs
        empty_buff_dict = {}
        for key in buff_dict:
            empty_buff_dict[key] = 0
        return empty_buff_dict
