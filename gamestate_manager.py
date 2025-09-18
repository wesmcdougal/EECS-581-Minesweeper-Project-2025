# this will manage which page the game is currently 
#i.e if its on the minesweeper or main menu
class GameStateManager():
    '''
    The GameStateManager is an object that can be passed between functions 
    and class. Its job is to track what the current state ("page") is.
    
    For Example a typical game will have a main menu, levels, and settings.
    The GameStateManager tracks wether you are on the main menu levels or setting page.
    This can be used in the main loop of the game as a flow control. 

    The typical scructure of how to use the GameStateManager is:

    main_loop ->  initialize GameStateManager and stores all possible states
    then get and execute the current page (typicaly first initialized to the main menu page)
    this will run the pages run loop.

    main_menu -> tracks wether the user has triggerd a page change (ie. move to levels screen)
    main_menu will set the current state to the desired state (levels for example) and return to 
    the main_loop

    main_loop -> gets the current state and exacutes the pages run loop. This cycle keeps going.

    NOTE: 
    All states need to have the same fucntion name for their run loop. They are typically names run() or draw()
    '''
    def __init__(self, currentState):
        '''
        Initializes the current state
        '''
        self.currentState = currentState
        self.params = {}

    def getState(self):
        '''
        Gets the current state
        '''
        return self.currentState
    
    def setState(self, newState, params=None):
        '''
        Returns the current state and store a parameters for 
        run loops that require a parameter to be passed in.
        '''
        self.currentState = newState
        self.params = params or {}

    def getParams(self):
        '''
        Sets the Prameters
        '''
        return self.params