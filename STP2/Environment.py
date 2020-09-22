
import AI_Module.AI_Transformer
import game_manager
import numpy as np

class Environment:

    def __init__(self):
        self.ai_transformer = AI_Module.AI_Transformer.AI_Transformer()
        self.game_manager = game_manager.GameManager()

    def Reset(self):
        self.game_manager.init_game()
        self.game_manager.start_player_turn()
        current_state = self.ai_transformer.GetAIStateSpace(self.game_manager.game_state, self.game_manager.get_current_playable_cards())
        # TODO: function to reset environment
        # if game is currently executing, stop it
        # start the game execution
        # return the game state (flat list with neuron values)
        # use self.ai_transformer.GetAIStateSpace(game_state, playable_cards) to convert to flat list
        return current_state

    def IsCardPlayable(self, action_neuron_number):
        #end turn is always doable
        if(action_neuron_number == 0):
            return True

        action_card = self.ai_transformer.GetGameAction(action_neuron_number)
        isPlayable = action_card in self.game_manager.get_current_playable_cards()
        return isPlayable


    def Step(self, action_space_vec):

        action_neuron_number = self.ChoosePossibleActionWithMaxQVal(action_space_vec)
        action_card = self.ai_transformer.GetGameAction(action_neuron_number)
        reward = 0

        #action_card contains string of card name
        old_player_hp = self.game_manager.game_state.player.current_hp
        old_boss_hp = self.game_manager.game_state.boss.current_hp

        #TODO: play the action card in the environment
        # new_state = state in flat list after playing card
        if(action_card == 'end_turn'): 
            self.ExecutePlayerEndFunctions()
            print("Player ended turn")
        else:
            self.game_manager.card_play_manager.PlayCard(action_card)
            print("Player took action : " + action_card)

        new_state = self.ai_transformer.GetAIStateSpace(self.game_manager.game_state, self.game_manager.get_current_playable_cards())
        new_player_hp = self.game_manager.game_state.player.current_hp
        new_boss_hp = self.game_manager.game_state.boss.current_hp

        #TODO: calculate isTerminal
        # isTerminal = true if the game has ended by taking action 
        isTerminal = self.game_manager.is_game_end()
        isPlayerWin = self.game_manager.is_player_win() if isTerminal else False 

        #TODO: reward calculation
        # reward by transitioning from current state to new state
        if (isTerminal and isPlayerWin) : 
            reward = 1
        elif (isTerminal and not isPlayerWin) : 
            reward = -1
        elif (not isTerminal):
            #{negative reward to player for losing hp}
            reward += (new_player_hp - old_player_hp) * 0.01  
            #{positive reward to player for boss losing hp}
            reward += -(new_boss_hp - old_boss_hp) * 0.01  

        return new_state, int(action_neuron_number), reward, isTerminal


    def ExecutePlayerEndFunctions(self):
        self.game_manager.end_player_turn()

        self.game_manager.start_enemy_turn()

        if(not self.game_manager.is_game_end()):
            self.game_manager.execute_enemy_intent()
        
        self.game_manager.start_player_turn()


    def ChoosePossibleActionWithMaxQVal(self, action_space_vec):
        action_space_vec_dec = np.sort(action_space_vec)[::-1].tolist()
        action_space_vec = action_space_vec.tolist()

        print(action_space_vec)
        print(action_space_vec_dec)

        for i in range(len(action_space_vec_dec)):
            index = action_space_vec.index(action_space_vec_dec[i])
            if self.IsCardPlayable(index):
                return index
        
        return 0
