from enemy_intent import EnemyIntent
import random
import buff_type


class EnemyAI:
    def __init__(self, boss):
        self.boss = boss
        self.intents_offensive = ['Charging Up',
                                  'Fierce Bash', 'Vent Steam', 'Whirlwind']
        self.intents_defensive = ['Defensive Mode', 'Roll Attack', 'Twin slam']
        self.curStateIndex = 0
        self.mode = 'Offensive'
        self.prev_hp = self.boss.max_hP

    # Check whether to change mode

    def onEnemyTurnStart(self,game_state):
        # change from Offensive to Defensive
        if self.prev_hp - self.boss.current_hp >= 30 and self.mode == 'Offensive':
            self.mode = 'Defensive'
            self.boss.block += 20
            self.curStateIndex = 0
            # refresh current intent on game state
            game_state.boss_intent = self.make_intent()
            print('Transfer to Defensive mode')

        # change from Defensive to Offensive
        # if defensive mode and on the stage of using Twin slam skill, boss will turn back to offensive mode
        if self.mode == 'Defensive' and self.curStateIndex == 0:
            self.mode = 'Offensive'
            self.boss.buff_dict['Thorns'] = 0
            self.curStateIndex = len(self.intents_offensive) - 1
            # refresh current intent on game state
            game_state.boss_intent = self.make_intent()
            print('Transfer to Offensive mode')

    # Offensive AI
    def make_intent(self) -> EnemyIntent:
        intent = EnemyIntent()
        if self.mode == 'Offensive':
            curState = self.intents_offensive[self.curStateIndex]
            if curState == 'Charging Up':
                intent.name = 'Charging Up'
                intent.is_block = True
                intent.block_value = 9
                print('BOSS intent: -[block]-', intent.block_value)
            elif curState == 'Fierce Bash':
                intent.name = 'Fierce Bash'
                intent.is_attack = True
                intent.attack_value = 32
                print("BOSS intent: -[attack]-", intent.attack_value)
            elif curState == 'Vent Steam':
                intent.name = 'Vent Steam'
                intent.is_debuff = True
                intent.debuff_type = 'Weakened'
                intent.debuff_value = 2
                print("BOSS intent: -[debuff]-", intent.debuff_type)
            elif curState == 'Whirlwind':
                intent.name = 'Whirlwind'
                intent.is_attack = True
                intent.attack_value = 20
                print("BOSS intent: -[attack]-", intent.attack_value)

            # move to the next intent
            self.curStateIndex = (self.curStateIndex +
                                  1) % len(self.intents_offensive)

        else:
            curState = self.intents_defensive[self.curStateIndex]
            if curState == 'Defensive Mode':
                intent.name = 'Defensive Mode'
                intent.is_enbuff = True
                intent.enbuff_type = 'Thorns'
                intent.enbuff_value = 3
                print('BOSS intent: -[enbuff]-', intent.enbuff_type)

            elif curState == 'Roll Attack':
                intent.name = 'Roll Attack'
                intent.is_attack = True
                intent.attack_value = 9
                print("BOSS intent: -[attack]-", intent.attack_value)
            elif curState == 'Twin slam':
                intent.name = 'Twin slam'
                intent.is_attack = True
                intent.attack_value = 18
                print("BOSS intent: -[attack]-", intent.attack_value)
            else:
                intent.name = 'none'
                print('error on defensive mode')

            # move to the next intent
            self.curStateIndex = (self.curStateIndex +
                                  1) % len(self.intents_defensive)

        return intent

    # whirlwind makes 4 attack, return a list of Enemy Intent?
    # 1 Enemy Intent for now

    # every time boss got hit and its offensive mode, it will calculate whether modeShiftValue < 0.
    # if yes, then turn to defensive mode.
    #
