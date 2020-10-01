class SingleBattleData:
    def __init__(self):
        self.fragments = []

class FragmentRecord:
    def __init__(self,start_state):
        self.start_state = start_state
        self.game_events = []
