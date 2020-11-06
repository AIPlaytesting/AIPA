from .effect_calculator import EffectCalculator
from .game_event import GameEvent

class CardPlayManager:
    # this class creates and manages instances of the cards

    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.card_effects_manager = EffectCalculator(game_manager)
        self.CreateCardInstances(game_manager.game_app_data)
        self.next_attack_count = 1

    def CreateCardInstances(self,game_app_data):
        self.cards_dict = game_app_data.cards_dict.copy()
        
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

                buff_value = card.buffs[key]['value']
                self.card_effects_manager.ApplyBuff(self.game_manager.game_state.player, buff_target, key, buff_value)
                
                # TODO: should record buff only it change
                if buff_value != 0:
                    # record game event
                    buff_change_event = GameEvent.create_buff_change_event(buff_target.game_unique_id,key,buff_value)
                    game_events.append(buff_change_event)

            # Create Block
            block_events  = self.card_effects_manager.AddBlock(self.game_manager.game_state.player, card.damage_block['block'])
            # record bock change event
            game_events.extend(block_events)

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

        if card.type == 'Attack':
            self.next_attack_count = 1
            self.game_manager.game_state.player.buff_dict['DoubleTapActive'] = 0

        if self.game_manager.game_state.player.buff_dict['DoubleTapActive'] > 0:
            self.next_attack_count = self.game_manager.game_state.player.buff_dict['DoubleTapActive'] + 1

        return game_events
