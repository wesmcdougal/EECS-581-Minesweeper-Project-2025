'''
File for game state management (e.g., main menu, playing, game over)
'''

class GameStateManager():
    def __init__(self, currentState):
        self.currentState = currentState
        self.params = {}

    def getState(self):
        return self.currentState
    
    def setState(self, newState, params=None):
        self.currentState = newState
        self.params = params or {}

    def getParams(self):
        return self.params
