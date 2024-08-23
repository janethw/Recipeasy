# class represents a game module that initiates game play
# not yet developed, placeholders only

class GameModule:
    # class method creates a GameModule instance and starts the game play
    @classmethod
    def start(cls):
        game = cls()
        game.play_game()

    # constructor for GameModule
    def __init__(self):
        pass

    # initiate game play
    def play_game(self):
        pass
