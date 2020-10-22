
import AI_Module.AI_Transformer
from gameplay.game_manager import GameManager
import numpy as np
import db.game_database

class Environment:

    def __init__(self):
        self.ai_transformer = AI_Module.AI_Transformer.AI_Transformer()
        self.state_space_dim = self.ai_transformer.state_space_dim
        self.action_space_dim = self.ai_transformer.action_space_dim

        db_root = db.game_database.calculate_root_dir()
        game_db = db.game_database.GameDatabase(db_root)
        self.game_manager = GameManager(game_db.game_app_data)
        self.action_cards_played = {}
        self.win_count = 0
        self.win_int = 0

        #reward values
        self.win_reward = 3
        self.unplayable_card_pun = -1
        self.loss_pun = -0.75

    def Reset(self):
        self.game_manager.init_game()
        self.game_manager.start_player_turn()
        current_state = self.ai_transformer.GetAIStateSpace(self.game_manager.game_state, self.game_manager.get_current_playable_cards())
        self.win_int = 0
        # TODO: function to reset environment
        # if game is currently executing, stop it
        # start the game execution
        # return the game state (flat list with neuron values)
        # use self.ai_transformer.GetAIStateSpace(game_state, playable_cards) to convert to flat list
        return current_state

    def IsCardPlayable(self, action_neuron_number):
        #end turn is always doable
        # if(action_neuron_number == 0):
        #     return True

        action_card = self.ai_transformer.GetGameAction(action_neuron_number)
        isPlayable = action_card in self.game_manager.get_current_playable_cards()
        return isPlayable

    def IsAnyCardPlayable(self):
        #return true is ANY card can be played from the deck. False if no card is playable.
        is_any_playable = False
        if(len(self.game_manager.get_current_playable_cards()) > 0):
            is_any_playable = True
        return is_any_playable


    def Step(self, action_space_vec,  isRandomTurn = False):
        self.game_manager.print_cards_info_on_hand()
        
        reward = 0
        isTurnEnd = False
        unplayableCardSelected = False

        #action_card contains string of card name
        old_player_hp = self.game_manager.game_state.player.current_hp
        old_player_block = self.game_manager.game_state.player.block
        old_player_buffs = self.game_manager.game_state.player.buff_dict.copy()
        old_player_energy = self.game_manager.game_state.player_energy
        old_boss_hp = self.game_manager.game_state.boss.current_hp
        old_boss_block = self.game_manager.game_state.boss.block
        old_boss_buffs = self.game_manager.game_state.boss.buff_dict.copy()
        

        #TODO: play the action card in the environment
        # new_state = state in flat list after playing card
        if(not self.IsAnyCardPlayable()): 
            isTurnEnd = True
            self.ExecutePlayerEndFunctions()
            #Ending turn hence -1
            action_neuron_number = -1
            print("Player ended turn")
        else:

            #Get the index with the maximum q-value
            if(not isRandomTurn):
                action_neuron_number = np.argmax(action_space_vec)
                print("Took Action :" + str(action_neuron_number))
            else:                
                action_neuron_number = self.ChoosePossibleActionWithMaxQVal(action_space_vec)
                print("Took Random Action :" + str(action_neuron_number))
                

            action_card = self.ai_transformer.GetGameAction(action_neuron_number)

            if self.IsCardPlayable(action_neuron_number):
                # NOTICE: game_manager doesn't expose card_play_manager anymore, use execute_play_card() instead
                # PREVIOUS:
                # self.game_manager.card_play_manager.PlayCard(action_card)
                # CURRENT:
                self.game_manager.execute_play_card(action_card)

                print("Player took action : " + action_card)
            else:
                #negative reward for trying to play a card that is not playable
                #Player loses if wrong move is made
                unplayableCardSelected = True
                self.game_manager.game_state.player.current_hp = 0

            if action_card in self.action_cards_played:
                self.action_cards_played[action_card] += 1
            else:
                self.action_cards_played[action_card] = 1

        new_state = self.ai_transformer.GetAIStateSpace(self.game_manager.game_state, self.game_manager.get_current_playable_cards())

        new_player_hp = self.game_manager.game_state.player.current_hp
        new_player_block = self.game_manager.game_state.player.block
        new_player_buffs = self.game_manager.game_state.player.buff_dict
        new_player_energy = self.game_manager.game_state.player_energy
        new_boss_hp = self.game_manager.game_state.boss.current_hp
        new_boss_block = self.game_manager.game_state.boss.block
        new_boss_buffs = self.game_manager.game_state.boss.buff_dict

        #calculate isTerminal
        # isTerminal = true if the game has ended by taking action 
        isTerminal = self.game_manager.is_game_end()
        isPlayerWin = self.game_manager.is_player_win() if isTerminal else False 

        #reward calculation
        # reward by transitioning from current state to new state

        reward = 0

        old_player_info = (old_player_hp, old_player_block, old_player_buffs, old_player_energy)
        new_player_info = (new_player_hp, new_player_block, new_player_buffs, new_player_energy)
        old_boss_info = (old_boss_hp, old_boss_block, old_boss_buffs)
        new_boss_info = (new_boss_hp, new_boss_block, new_boss_buffs)

        pac_state = (old_player_info, new_player_info, old_boss_info, new_boss_info)

        if (isTerminal and isPlayerWin) : 
            reward += self.win_reward
            self.win_count += 1
            self.win_int = 1
        elif (isTerminal and not isPlayerWin) : 
            if unplayableCardSelected:
                #higher negative reward for choosing wrong card
                reward += self.unplayable_card_pun
                self.win_int = -2
            else:
                reward += self.loss_pun
                self.win_int = -1

        return new_state, int(action_neuron_number), reward, isTerminal, pac_state, isTurnEnd


    def ExecutePlayerEndFunctions(self):
        self.game_manager.end_player_turn()
        self.game_manager.start_enemy_turn()

        if(not self.game_manager.is_game_end()):
            self.game_manager.execute_enemy_intent()
        
        self.game_manager.start_player_turn()


    def ChoosePossibleActionWithMaxQVal(self, action_space_vec):
        action_space_vec_dec = np.sort(action_space_vec)[::-1].tolist()
        action_space_vec = action_space_vec.tolist()

        for i in range(len(action_space_vec_dec)):
            index = action_space_vec.index(action_space_vec_dec[i])
            if self.IsCardPlayable(index):
                return index
        
        return -1