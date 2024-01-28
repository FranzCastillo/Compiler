class StateId:
    def __init__(self):
        self.state_id = 0

    def get_state_id(self):
        self.state_id += 1
        return self.state_id
