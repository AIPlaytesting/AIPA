from . game_state import GameState
from . enemy_intent import EnemyIntent
from . combat_unit import CombatUnit
from . game_event import GameEvent
from db.game_app_data import Card,GameAppData

class EventManager:
    def __init__(self,game_app_data:GameAppData):
        # self.cards_dict: cardname:str,Card:game_app_data.Card
        self.cards_dict = game_app_data.cards_dict.copy()
        # TODO: remove this flag variabl, use buff to indicate!
        self.next_attack_count = 1

    # return GameEvent[]
    def execute_card(self,game_state:GameState,cardname:str)->[]:
        if not cardname in self.cards_dict:
            print(cardname + ' is an invalid card name')
            return []

        game_events = []
        card = self.cards_dict[cardname]
        card_play_count = self.next_attack_count if card.type == 'Attack' else 1
        for i in range(0, card_play_count):
            # apply buffs
            buff_events = self.__execute_card_buffs(game_state,card)
            # TODO:extentd buff_events
            # game_events.extend(buff_events)

            # apply block
            block_events = self.__on_change_block_value(card.damage_block['block'],game_state.player)
            game_events.extend(block_events)

            # apply attack
            attack_events = self.__execute_card_attack(game_state,card)
            game_events.extend(attack_events)

            # TODO: remove this draw card to buff system
            # apply draw card
            game_state.deck.draw_cards(card.card_life_cycle['draw_card'])

        # discard card after played
        self.__on_discard_card(game_state,card)

        # reduce player energy after played the card
        self.__on_change_energy(game_state,-card.energy_cost) 

        # TODO: move this together with  self.next_attack_count into buff system
        # Modify the next_attack_count variable. [Attack card always resets it to 1]. 
        self.next_attack_count = 1 if card.type == 'Attack' else self.next_attack_count
        if card.type == 'Attack':
            self.next_attack_count = 1
            game_state.player.buff_dict['DoubleTapActive'] = 0

        if game_state.player.buff_dict['DoubleTapActive'] > 0:
            self.next_attack_count = game_state.player.buff_dict['DoubleTapActive'] + 1

        return game_events

    # return GameEvent[]
    def execute_enemy_intent(self,game_state:GameState,intent:EnemyIntent)->[]:
        pass
  
    # return GameEvent[]
    def __execute_card_buffs(self,game_state:GameState,card:Card)->[]:
        game_events = []
        for buffname in card.buffs:
            # decide buff target
            if(card.buffs[buffname]['target'] == 'enemy'):
                buff_target = game_state.boss
            else:
                buff_target = game_state.player

            buff_value = card.buffs[buffname]['value']

            # apply buff
            self.__on_apply_buff_to(buffname,buff_value,buff_target)

            # create game event for it
            if buff_value != 0:
                buff_change_event = GameEvent.create_buff_change_event(buff_target.game_unique_id,buffname,buff_value)
                game_events.append(buff_change_event)

        return game_events

    # return GameEvent[]
    def __execute_card_attack(self,game_state:GameState,card:Card)->[]:
        game_events = []
        for i in range(0, card.damage_block['damage_instances']):       
            if card.special_mod['unique_damage'] == 'none':
                damage_value = card.damage_block['damage']
            elif card.special_mod['unique_damage'] == 'block':
                damage_value = self.game_manager.game_state.player.block
            
            # apply attack
            damage_events = self.__on_attack(game_state.boss_AI, game_state.player,game_state.boss,damage_value)
            game_events.extend(damage_events)

            # damage_events = self.card_effects_manager.DealDamage(self.game_manager.game_state.player, self.game_manager.game_state.boss,
            #     damage_value, card.special_mod['strength_multiplier'])

        return game_events

    # return GameEvent[]
    def __on_change_block_value(self,incremental_val:int,target:CombatUnit):
        target.block += incremental_val
        if incremental_val != 0:
            return [GameEvent.create_block_change_event(target.game_unique_id,target.block)]
        else:
            return []


    # difference between "on_attack" and "on_take_damage" is:
    #       "on_attack" will apply all buff effects such as throns, weaken,etc.
    #       "on_take_damage" just basiclly take the final damage result, only consider block
    # TODO：remove BOSSAI from paras
    # TODO: heavy blade,strength_multiplier
    # return GameEvent[]
    def __on_attack(self,boss_AI,attack_source:CombatUnit, attack_target:CombatUnit, attack_value:int):
        game_events = []
       
        # condider buffs 
        attack_value =+ attack_source.buff_dict['Strength'] 
        if attack_source.buff_dict['Weakened'] > 0 :
            attack_value *= 0.75
        if attack_target.buff_dict['Vulnerable'] > 0 :
            attack_value *= 1.5
        if attack_target.buff_dict['Thorns'] > 0 :
           thron_damage_events = self.__on_take_damage(boss_AI,attack_source,attack_target.buff_dict['Thorns'])
           game_events.extend(thron_damage_events)
        attack_value = int(attack_value)

        # apply real damage
        damage_events = self.__on_take_damage(boss_AI,attack_source,attack_target,attack_value)
        game_events.extend(damage_events)
        return game_events
    
    # return GameEvent[]
    # TODO: remove BOSS AI in parameter list
    def __on_take_damage(self,boss_AI,damage_source:CombatUnit, damage_target:CombatUnit, damage_value:int):
        game_events = []
        # consider block
        blocked_value = 0
        target_block = damage_target.block
        # blocked value
        if target_block  >= damage_value :
            blocked_value = damage_value
        else:
            blocked_value = target_block     
        # get real damage after block
        damage_value -= blocked_value      
        # change block
        block_events = self.__on_change_block_value(blocked_value,damage_target)
        game_events.extend(block_events)

        # apply damage
        damage_target.current_hp -= damage_value
        game_events.append( GameEvent.create_get_hurt_event(damage_target.game_unique_id,damage_value))

        # TODO remove this part into other place!
        # print remaining number to trigger mode shift
        # if boss is in offensive mode, charge accumulator and turn to defensive if over 30
        if damage_target.game_unique_id == 'boss' and boss_AI.mode == 'Offensive':
            boss_AI.accumulator += damage_value

            if boss_AI.accumulator >= boss_AI.transformTriggerPoint:
                boss_AI.transformTriggerPoint += 10
                boss_AI.mode = 'Defensive'
                boss_AI.boss.block += 20
                boss_AI.curStateIndex = 0
                # refresh current intent on game state
                self.game_manager.game_state.boss_intent = boss_AI.make_intent()
                print('Transform to Defensive mode')
            else:
                print("Boss will switch mode in", boss_AI.transformTriggerPoint - boss_AI.accumulator, "damages")
        return game_events

    def __on_discard_card(self,game_state:GameState,card:Card):
        game_state.deck.discard_card(card.name ,card.card_life_cycle["copies_in_discard_pile_when_played"])

    def __on_change_energy(self,game_state:GameState, incremental_val:int):
        game_state.player_energy += incremental_val

    def __on_apply_buff_to(self,buffname:str,incremental_val:int,target:CombatUnit):
        target.buff_dict[buffname] += incremental_val
