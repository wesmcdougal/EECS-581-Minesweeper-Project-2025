# this will manage which page the game is currently 
#i.e if its on the minesweeper or main menu
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