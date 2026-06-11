from ursina import *
from game_manager import manager
from ursina.shaders import lit_with_shadows_shader

class Tile(Entity):
    def __init__(self, x, z, tile_color):
        super().__init__(
            model='cube',
            color=tile_color,
            position=(x, 0, z),
            scale=(1, 0.1, 1),
            collider='box',
            shader=lit_with_shadows_shader
            
        )
        wireframe = Entity(
            parent=self,
            model='wireframe_cube',
            color=color.black,
            scale=(1, 1.05, 1),
            collider=None,
        )
        wireframe.model.setRenderModeThickness(5)
        self.x_pos = x
        self.z_pos = z
        self.original_color = tile_color
        self.occupying_piece = None 

    def input(self, key):
        if self.hovered and key == 'left mouse down':
            if self in manager.highlighted_tiles:
                self.perform_move() # Wywołujemy ruch klikając w płytkę

    # Ruch
    def perform_move(self):
        piece = manager.selected_piece
        
        # Historia ruchu (stan przed ruchem)
        start_x = piece.x_pos
        start_z = piece.z_pos
        is_capture = False
        special_move = None
        
        # Bicie
        if self.occupying_piece is not None:
            enemy = self.occupying_piece
            enemy.is_alive = False
            
            # Animacja bicia
            enemy.animate_scale((0, 0, 0), duration=0.2)
            invoke(destroy, enemy, delay=0.25)
            
            is_capture = True 
            print(f"Zlikwidowano figurę na X:{self.x_pos} Z:{self.z_pos}!")
        
        # Zwolnienie pola
        old_tile = manager.board.tiles.get((piece.x_pos, piece.z_pos))
        if old_tile:
            old_tile.occupying_piece = None
        
        # Roszada
        if piece.__class__.__name__ == 'King' and abs(self.x_pos - piece.x_pos) == 2:
            # Krótka roszada 
            if self.x_pos == 6:
                special_move = "Krótka roszada" 
                rook = manager.board.tiles[(7, piece.z_pos)].occupying_piece
                manager.board.tiles[(7, piece.z_pos)].occupying_piece = None
                manager.board.tiles[(5, piece.z_pos)].occupying_piece = rook
                rook.x_pos = 5
                
                # Animacja roszady
                rook.animate_position((5, 0, rook.z_pos), duration=0.3, curve=curve.in_out_sine)
                
                rook.has_moved = True
                
            # Długa roszada 
            elif self.x_pos == 2:
                special_move = "Długa roszada" 
                rook = manager.board.tiles[(0, piece.z_pos)].occupying_piece
                manager.board.tiles[(0, piece.z_pos)].occupying_piece = None
                manager.board.tiles[(3, piece.z_pos)].occupying_piece = rook
                rook.x_pos = 3
                
                # Animacja roszady
                rook.animate_position((3, 0, rook.z_pos), duration=0.3, curve=curve.in_out_sine)
                
                rook.has_moved = True
        
        # Bicie w przelocie
        if piece.__class__.__name__ == 'Pawn' and (self.x_pos, self.z_pos) == manager.en_passant_target:
            # Animacja bicia w przelocie
            manager.en_passant_victim.animate_scale((0, 0, 0), duration=0.2)
            invoke(destroy, manager.en_passant_victim, delay=0.25)
            
            manager.board.tiles[(manager.en_passant_victim.x_pos, manager.en_passant_victim.z_pos)].occupying_piece = None
            is_capture = True 
            special_move = "En Passant" 
            print("Bicie w przelocie wykonane!")

        new_target = None
        new_victim = None

        # Wykrycie ruchu piona o 2 pola
        if piece.__class__.__name__ == 'Pawn' and abs(self.z_pos - piece.z_pos) == 2:
            ghost_z = (self.z_pos + piece.z_pos) // 2
            new_target = (self.x_pos, ghost_z)
            new_victim = piece
        manager.en_passant_target = new_target
        manager.en_passant_victim = new_victim
        
        piece.has_moved = True

        # Ruch figury
        piece.x_pos = self.x_pos
        piece.z_pos = self.z_pos
        
        # Animacja ruchu
        piece.animate_position((self.x_pos, 0, self.z_pos), duration=0.3, curve=curve.in_out_sine)

        # Dźwięki
        if is_capture:
            manager.sound_capture.play()
        else:
            manager.sound_move.play()
        
        print(f"Wykonano ruch na X:{self.x_pos} Z:{self.z_pos}")
        
        self.occupying_piece = piece
        
        # Historia ruchu (stan po ruchu)
        manager.log_move(piece, start_x, start_z, self.x_pos, self.z_pos, is_capture, special_move)
        
        # Reset po ruchu
        piece.color = piece.original_color
        for t in manager.highlighted_tiles:
            t.color = t.original_color
        manager.highlighted_tiles.clear()
        manager.selected_piece = None

        # Czy promocja piona?
        is_promotion = False
        
        if piece.__class__.__name__ == 'Pawn':
            if (piece.piece_color == color.white and piece.z_pos == 7) or \
               (piece.piece_color == color.black and piece.z_pos == 0):
                
                is_promotion = True
                manager.pawn_to_promote = piece      
                manager.promotion_menu.enabled = True 
        if not is_promotion:
            manager.switch_turn()

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