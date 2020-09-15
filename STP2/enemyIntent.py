from STP2.buffType import BuffType
from STP2.gameManager import GameState
from STP2.combatUnit import CombatUnit

class EnemyIntent:
    def __init__(self):
        self.isAttack = False
        self.attackValue = 0
        self.isDebuff = False
        self.debuffType = BuffType.Empty
        self.debuffValue = 1
        self.isEnbuff = False
        self.enbuffType = BuffType.Empty
        self.enbuffValue = 1

    def apply_to(self, gameState: GameState):
        if self.isAttack :
            gameState.player.currentHP -= self.attackValue
        elif self.isDebuff:
            gameState.player.add_new_buff(self.debuffType,self.debuffValue)