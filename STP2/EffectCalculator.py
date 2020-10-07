import game_manager
import buff_type
from game_event import GameEvent

class EffectCalculator:

    def __init__(self, game_manager):
        self.game_manager = game_manager

    # TODO:return GameEvent[]
    def ApplyBuff(self, source, target, buff_key, buff_value):
        target.buff_dict[buff_key] += buff_value
        self.LogBuffApplication(source, target, buff_key, buff_value)
        return []

    def AddBlock(self, target, value):
        target.block += value
        self.LogAddBlock(target, value)

        if value != 0:
            block_change_event = GameEvent.create_block_change_event(target.game_unique_id,target.block)
            return [block_change_event]
        else:
            return []

    # return GameEvent[]
    def DealDamage(self, source, target, value, strength_multiplier):
        damage_game_events = []
        #calculate damage modifications
        # strength -> add (strength value * special_mod.strength_multiplier) to damage
        # player weakened -> (damage + str bonus) * 0.75
        # enemy vulnerable -> (damage) * 1.5
        damage_value = value + (source.buff_dict['Strength'] * strength_multiplier)

        if source.buff_dict['Weakened'] > 0 :
            damage_value *= 0.75

        if target.buff_dict['Vulnerable'] > 0 :
            damage_value *= 1.5

        damage_value = int(damage_value)
        damage_value = self.BlockDamage(target, damage_value)
        target.current_hp -= damage_value
        # print remaining number to trigger mode shift
        # if boss is in offensive mode, charge accumulator and turn to defensive if over 30
        boss_AI = self.game_manager.boss_AI 
        if target.game_unique_id == 'boss' and \
            boss_AI.mode == 'Offensive':
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


        # record damge event
        damage_game_events.append(GameEvent.create_get_hurt_event(target.game_unique_id,damage_value))

        self.LogDamage(source, target, damage_value)
        thron_damage_event = self.ThornDamage(target,source)
        # record thoron demage event
        if thron_damage_event != None:
            damage_game_events.append(thron_damage_event)
        return damage_game_events

    def BlockDamage(self, target, damage):
        damage_value = damage
        #calculate damage reduction from block
        if target.block > damage_value:
            target.block -= damage_value
            damage_value = 0
            self.LogBlock(target, damage_value)
        elif damage_value > target.block:
            damage_value -= target.block
            target.block = 0
            self.LogBlock(target, target.block)
        else:
            damage_value = 0
            target.block = 0
            self.LogBlock(target, target.block)
        
        return damage_value
    
    # return demage event
    def ThornDamage(self, source, target):
        #thorn damage is different because it does not get affected by modifiers
        thorn_damage_value = source.buff_dict['Thorns']

        if not thorn_damage_value > 0:
            return None

        thorn_damage_value = self.BlockDamage(target, thorn_damage_value)
        target.current_hp -= thorn_damage_value
        self.LogThornDamage(source, target, thorn_damage_value)
        
        return GameEvent.create_get_hurt_event(target.game_unique_id,thorn_damage_value)
    
    def ReducePlayerEnergy(self, energy):
        self.game_manager.game_state.player_energy -= energy

    def LogAddBlock(self, target, block_val):
        if block_val != 0 and self.game_manager.isLoggingEnabled:
            print("[" + target.name + "]" + "[GAINS BLOCK =" + str(block_val) + "]")

    def LogBlock (self, target, block_val):
        if block_val != 0 and self.game_manager.isLoggingEnabled:
            print("[" + target.name + "]" + "[BLOCK DMG = " + str(block_val) + "]  |  " + "[" + target.name + " hp]" + " = " + str(target.current_hp) + "," + "[" + target.name + " block]" + " = " + str(target.block))

    def LogDamage (self, source, target, damage_val):
        if damage_val != 0 and self.game_manager.isLoggingEnabled:
            print("[" + source.name + "]" + " [HIT] " + "[" + target.name + "]" + " [DMG = " + str(damage_val) + "]  |  " + "[" + target.name + " hp]" + " = " + str(target.current_hp) + "," + "[" + target.name + " block]" + " = " + str(target.block))

    def LogThornDamage(self, source, target, damage_val):
        if damage_val != 0 and self.game_manager.isLoggingEnabled:
            print("[" + source.name + "]" + " [THORN HIT] " + "[" + target.name + "]" + " [DMG = " + str(damage_val) + "]  |  " + "[" + target.name + " hp]" + " = " + str(target.current_hp) + "," + "[" + target.name + " block]" + " = " + str(target.block))

    def LogBuffApplication(self, source, target, buff_name, buff_value):
        if buff_value != 0 and self.game_manager.isLoggingEnabled:
            print("[" + source.name + "]" + " [APPLIES BUFF] " + "[" + str(buff_value) +"]" + "[" + buff_name + "]" + "[" + target.name + "]")