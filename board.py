from ursina import *
from game_manager import manager

class Tile(Entity):
    def __init__(self, x, z, tile_color):
        super().__init__(
            model='cube',
            color=tile_color,
            position=(x, 0, z),
            scale=(1, 0.1, 1),
            collider='box'
        )
        self.x_pos = x
        self.z_pos = z
        self.original_color = tile_color
        self.occupying_piece = None 

    def input(self, key):
        if self.hovered and key == 'left mouse down':
            if self in manager.highlighted_tiles:
                piece = manager.selected_piece
                
                # Bicie
                if self.occupying_piece is not None:
                    enemy = self.occupying_piece
                    enemy.is_alive = False
                    
                    destroy(enemy)
                    print(f"Zlikwidowano figurę na X:{self.x_pos} Z:{self.z_pos}!")
                
                # Zwolnienie pola
                old_tile = manager.board.tiles.get((piece.x_pos, piece.z_pos))
                if old_tile:
                    old_tile.occupying_piece = None
                
                # Ruch figury
                piece.x_pos = self.x_pos
                piece.z_pos = self.z_pos
                piece.position = (self.x_pos, 0.5, self.z_pos)
                print(f"Wykonano ruch na X:{self.x_pos} Z:{self.z_pos}")
                
                self.occupying_piece = piece
                
                # Reset po ruchu
                piece.color = piece.original_color
                for t in manager.highlighted_tiles:
                    t.color = t.original_color
                manager.highlighted_tiles.clear()
                manager.selected_piece = None

                # Zmiana tury

                if manager.current_turn == color.white:
                    manager.current_turn = color.black
                    print("--> Tura Czarnych")
                    manager.whose_turn.text = "Kolej: Czarne"
                    manager.whose_turn.color = color.light_gray
                else:
                    manager.current_turn = color.white
                    print("--> Tura Białych")
                    manager.whose_turn.text = "Kolej: Białe"
                    manager.whose_turn.color = color.white

class Board:
    def __init__(self):
        self.tiles = {}
        self.create_board()

    def create_board(self):
        for x in range(8):
            for z in range(8):
                if (x + z) % 2 == 0:
                    tile_color = color.dark_gray
                else:
                    tile_color = color.hex('#F0D9B5')

                tile = Tile(x, z, tile_color)
                self.tiles[(x, z)] = tile