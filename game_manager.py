from ursina import color, Text

class GameManager:
    def __init__(self):
        self.selected_piece = None
        self.board = None
        self.highlighted_tiles = []
        self.current_turn = color.white
        self.whose_turn = None 

    def setup_ui(self):
        self.whose_turn = Text(
            text="Kolej: Białe", 
            position=(0, 0.45), 
            origin=(0, 0),      
            scale=1.2,          
            color=color.white
        )

manager = GameManager()