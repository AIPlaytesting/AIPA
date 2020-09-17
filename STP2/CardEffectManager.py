import game_manager
import buff_type

class CardEffectManager:

    def __init__(self, game_manager):
        self.game_manager = game_manager

    def ApplyBuff(self, target, buff_key, buff_value):
        target.buff_dict[buff_key] += buff_value

    def AddBlock(self, target, value):
        target.block += value

    def DealDamage(self, source, target, value, strength_multiplier):
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
        self.ThornDamage(source, target)

        
    def BlockDamage(self, target, damage):
        damage_value = damage
        #calculate damage reduction from block
        if target.block > damage_value:
            target.block -= damage_value
            damage_value = 0
        elif damage_value > target.block:
            damage_value -= target.block
            target.block = 0
        else:
            damage_value = 0
            target.block = 0
        
        return damage_value
    

    def ThornDamage(self, source, target):
        #thorn damage is different because it does not get affected by modifiers

        thorn_damage_value = source.buff_dict['Thorns']

        if not thorn_damage_value > 0:
            return

        thorn_damage_value = self.BlockDamage(target, thorn_damage_value)

        target.current_hp -= thorn_damage_value
        
    
    def ReducePlayerEnergy(self, energy):
        self.game_manager.game_state.player_energy -= energy


        












        




