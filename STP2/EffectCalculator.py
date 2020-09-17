import game_manager
import buff_type

class EffectCalculator:

    def __init__(self, game_manager):
        self.game_manager = game_manager

    def ApplyBuff(self, source, target, buff_key, buff_value):
        target.buff_dict[buff_key] += buff_value
        self.LogBuffApplication(source, target, buff_key, buff_value)

    def AddBlock(self, target, value):
        target.block += value
        self.LogAddBlock(target, value)

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
        self.LogDamage(source, target, damage_value)
        self.ThornDamage(source, target)

        
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
    

    def ThornDamage(self, source, target):
        #thorn damage is different because it does not get affected by modifiers
        thorn_damage_value = source.buff_dict['Thorns']

        if not thorn_damage_value > 0:
            return

        thorn_damage_value = self.BlockDamage(target, thorn_damage_value)
        target.current_hp -= thorn_damage_value
        self.LogThornDamage(source, target, thorn_damage_value)
        
    
    def ReducePlayerEnergy(self, energy):
        self.game_manager.game_state.player_energy -= energy

    def LogAddBlock(self, target, block_val):
        print("[" + target.name + "]" + "[GAINS BLOCK =" + str(block_val) + "]")

    def LogBlock (self, target, block_val):
        print("[" + target.name + "]" + "[BLOCK DMG = " + str(block_val) + "]  |  " + "[" + target.name + " hp]" + " = " + str(target.hp) + "," + "[" + target.name + " block]" + " = " + str(target.block))

    def LogDamage (self, source, target, damage_val):
        print("[" + source.name + "]" + " [HIT] " + "[" + target.name + "]" + " [DMG = " + str(damage_val) + "]  |  " + "[" + target.name + " hp]" + " = " + str(target.hp) + "," + "[" + target.name + " block]" + " = " + str(target.block))

    def LogThornDamage(self, source, target, damage_val):
        print("[" + source.name + "]" + " [THORN HIT] " + "[" + target.name + "]" + " [DMG = " + str(damage_val) + "]  |  " + "[" + target.name + " hp]" + " = " + str(target.hp) + "," + "[" + target.name + " block]" + " = " + str(target.block))

    def LogBuffApplication(self, source, target, buff_name, buff_value):
        print("[" + source.name + "]" + " [APPLIES BUFF] " + "[" + str(buff_value) +"]" + "[" + buff_name + "]" + "[" + target.name + "]")