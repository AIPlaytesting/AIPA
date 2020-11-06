import json
class SingleBattleData:
    def __init__(self):
        self.fragments = []

    def encode_to_json(self):
        json_obj = {}
        json_obj["fragments"] = [f.to_serilizable_obj() for f in self.fragments]
        return json.dumps(json_obj,indent=1)

class FragmentRecord:
    def __init__(self,start_state):
        self.start_state = start_state
        self.game_events = []

    # use c# naming style here
    def to_serilizable_obj(self):
        serializable = {}
        serializable["startState"] = self.start_state
        serializable["gameEvents"] = self.game_events
        return serializable