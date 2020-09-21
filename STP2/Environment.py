import game_runner
import AI_Module.AI_Transformer


class Environment:

    def __init__(self):
        self.ai_transformer = AI_Module.AI_Transformer.AI_Transformer()
        pass

    def Reset(self):
        # TODO: function to reset environment
        # if game is currently executing, stop it
        # start the game execution
        # return the game state (flat list with neuron values)
        # use self.ai_transformer.GetAIStateSpace(game_state, playable_cards) to convert to flat list
        pass

    def IsCardPlayable(self, action_neuron_number):
        action_card = self.ai_transformer.GetGameAction(action_neuron_number)
        #action_card contains string of card name
        
        isPlayable = True # TODO: evaluate bool to (card in playable_cards) {whether card is playable or not}
        
        return isPlayable


    def Step(self, action_neuron_number):
        action_card = self.ai_transformer.GetGameAction(action_neuron_number)
        reward = 0

        #action_card contains string of card name
        
        #TODO: play the action card in the environment
        # new_state = state in flat list after playing card

        #TODO: calculate isTerminal
        # isTerminal = true if the game has ended by taking action 
        

        #TODO: reward calculation
        # reward by transitioning from current state to new state
        # if (isTerminal and isPlayerWin) : reward = 1
        # elif (isTerminal and not isPlayerWin) : reward = 1
        # elif (not isTerminal):
        #   reward += (new_player_hp - old_player_hp) * 0.01  {negative reward to player for losing hp}
        #   reward += -(new_boss_hp - old_boss_hp) * 0.01  {positive reward to player for boss losing hp}

        #return new_state, reward, isTerminal