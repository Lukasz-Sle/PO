from ursina import *
from game_manager import manager

class Piece(Entity):
    def __init__(self, x, z, piece_color, **kwargs):
        super().__init__(
            model='cube',                 # Narazie kostki (później bedzie lepszy model)
            color=piece_color,            
            position=(x, 0.5, z),         
            scale=(0.4, 0.8, 0.4),        
            collider='box',               
            **kwargs
        )
        
        self.x_pos = x
        self.z_pos = z
        self.piece_color = piece_color
        self.is_alive = True
        self.original_color = piece_color 
        self.has_moved = False
        starting_tile = manager.board.tiles.get((self.x_pos, self.z_pos))
        if starting_tile:
            starting_tile.occupying_piece = self

    def input(self, key):
        if self.hovered and key == 'left mouse down':
            # Pilnowanie tury 
            if self.piece_color != manager.current_turn:
                print("To nie jest twoja tura!")
                return
            # Odznaczanie figury
            if manager.selected_piece == self:
                self.color = self.original_color
                manager.selected_piece = None
                print("Odznaczono figurę.")
                
                for tile in manager.highlighted_tiles:
                    tile.color = tile.original_color
                manager.highlighted_tiles.clear()
            #Zaznaczamy nową figurę
            else:
                # Reset wcześniej klikniętej figury
                if manager.selected_piece is not None:
                    manager.selected_piece.color = manager.selected_piece.original_color
                    
                    for tile in manager.highlighted_tiles:
                        tile.color = tile.original_color
                    manager.highlighted_tiles.clear()
                
                self.color = color.red
                manager.selected_piece = self
                
                # Pokazanie dostępnych ruchów
                if hasattr(self, 'show_valid_moves'):
                    self.show_valid_moves()

class Pawn(Piece): #Pionek
    def __init__(self, x, z, piece_color):
        super().__init__(x, z, piece_color)
        self.scale = (0.4, 0.6, 0.4)

    def show_valid_moves(self):
        # Kierunek ruchu
        if self.piece_color == color.white:
            direction = 1
        else:
            direction = -1
        
        # Ruch o jedno pole
        forward_z = self.z_pos + direction
        
        if 0 <= forward_z <= 7:
            tile_1 = manager.board.tiles.get((self.x_pos, forward_z))
            
            if tile_1 and tile_1.occupying_piece is None:
                # Sprawdzenie czy król bezpieczny po ruchu
                if manager.is_move_safe(self, self.x_pos, forward_z):
                    tile_1.color = color.green
                    manager.highlighted_tiles.append(tile_1)
                    
                    # Ruch o dwa pola
                    if (self.piece_color == color.white and self.z_pos == 1) or (self.piece_color == color.black and self.z_pos == 6):
                        
                        double_forward_z = self.z_pos + (direction * 2)
                        tile_2 = manager.board.tiles.get((self.x_pos, double_forward_z))
                        
                        if tile_2 and tile_2.occupying_piece is None:
                            # Sprawdzenie czy król bezpieczny po ruchu
                            if manager.is_move_safe(self, self.x_pos, double_forward_z):
                                tile_2.color = color.green
                                manager.highlighted_tiles.append(tile_2)

        # Atak
        for dx in [-1, 1]:
            attack_x = self.x_pos + dx
            attack_z = self.z_pos + direction
            
            if 0 <= attack_x <= 7 and 0 <= attack_z <= 7:
                attack_tile = manager.board.tiles.get((attack_x, attack_z))
                
                if attack_tile:
                    # Zwykłe bicie
                    if attack_tile.occupying_piece is not None:
                        if attack_tile.occupying_piece.piece_color != self.piece_color:
                            # Sprawdzenie czy król bezpieczny po ruchu
                            if manager.is_move_safe(self, attack_x, attack_z):
                                attack_tile.color = color.red
                                manager.highlighted_tiles.append(attack_tile)
                            
                    # Bicie w przelocie
                    elif (attack_x, attack_z) == manager.en_passant_target:
                        if manager.en_passant_victim.piece_color != self.piece_color:
                            # Sprawdzenie czy król bezpieczny po ruchu
                            if manager.is_move_safe(self, attack_x, attack_z):
                                attack_tile.color = color.red
                                manager.highlighted_tiles.append(attack_tile)                
                        
class Rook(Piece): # Wieża
    def __init__(self, x, z, piece_color):
        super().__init__(x, z, piece_color)
        self.scale = (0.5, 0.7, 0.5)

    def show_valid_moves(self):
        # (0, 1) - góra
        # (0, -1) - doł
        # (1, 0) - prawo
        # (-1, 0) - lewo 
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dz in directions:
            step = 1 
            
            while True:
                check_x = self.x_pos + (dx * step)
                check_z = self.z_pos + (dz * step)

                if 0 <= check_x <= 7 and 0 <= check_z <= 7:
                    tile = manager.board.tiles.get((check_x, check_z))

                    if tile:
                        # Puste pole
                        if tile.occupying_piece is None:
                            # Sprawdzenie czy król bezpieczny po ruchu
                            if manager.is_move_safe(self, check_x, check_z):
                                tile.color = color.green
                                manager.highlighted_tiles.append(tile)
                            
                        # Zajęte pole
                        else:
                            # Wróg
                            if tile.occupying_piece.piece_color != self.piece_color:
                                # Sprawdzenie czy król bezpieczny po ruchu
                                if manager.is_move_safe(self, check_x, check_z):
                                    tile.color = color.red
                                    manager.highlighted_tiles.append(tile)
                            break
                else:
                    break
                step += 1 

class Knight(Piece): # Koń
    def __init__(self, x, z, piece_color):
        super().__init__(x, z, piece_color)
        self.scale = (0.45, 0.75, 0.45)
    def show_valid_moves(self):
        moves = [
            (1, 2), (2, 1), (-1, 2), (-2, 1),
            (1, -2), (2, -1), (-1, -2), (-2, -1)
        ]

        for dx, dz in moves:
            jump_x = self.x_pos + dx
            jump_z = self.z_pos + dz

            if 0 <= jump_x <= 7 and 0 <= jump_z <= 7:
                tile = manager.board.tiles.get((jump_x, jump_z))

                if tile:
                    # Puste pole
                    if tile.occupying_piece is None:
                        # Sprawdzenie czy król bezpieczny po ruchu
                        if manager.is_move_safe(self, jump_x, jump_z):
                            tile.color = color.green
                            manager.highlighted_tiles.append(tile)
                        
                    # Zajęte pole
                    else:
                        # Wróg
                        if tile.occupying_piece.piece_color != self.piece_color:
                            # Sprawdzenie czy król bezpieczny po ruchu
                            if manager.is_move_safe(self, jump_x, jump_z):
                                tile.color = color.red
                                manager.highlighted_tiles.append(tile)

class Bishop(Piece): # Goniec
    def __init__(self, x, z, piece_color):
        super().__init__(x, z, piece_color)
        self.scale = (0.4, 0.85, 0.4)
    def show_valid_moves(self):
        # (1, 1) - góra, prawo
        # (1, -1) - góra, lewo
        # (-1, 1) - dół, prawo
        # (-1, -1) - dół, lewo 
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dz in directions:
            step = 1 
            
            while True:
                check_x = self.x_pos + (dx * step)
                check_z = self.z_pos + (dz * step)

                if 0 <= check_x <= 7 and 0 <= check_z <= 7:
                    tile = manager.board.tiles.get((check_x, check_z))

                    if tile:
                        # Puste pole
                        if tile.occupying_piece is None:
                            # Sprawdzenie czy król bezpieczny po ruchu
                            if manager.is_move_safe(self, check_x, check_z):
                                tile.color = color.green
                                manager.highlighted_tiles.append(tile)
                            
                        # Zajęte pole
                        else:
                            # Wróg
                            if tile.occupying_piece.piece_color != self.piece_color:
                                # Sprawdzenie czy król bezpieczny po ruchu
                                if manager.is_move_safe(self, check_x, check_z):
                                    tile.color = color.red
                                    manager.highlighted_tiles.append(tile)
                            break
                else:
                    break
                step += 1 

class Queen(Piece): # Królowa
    def __init__(self, x, z, piece_color):
        super().__init__(x, z, piece_color)
        self.scale = (0.45, 0.9, 0.45)
    def show_valid_moves(self):
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),    # Prosto i na boki
            (1, 1), (1, -1), (-1, 1), (-1, -1)   # Skosy
        ]

        for dx, dz in directions:
            step = 1 
            
            while True:
                check_x = self.x_pos + (dx * step)
                check_z = self.z_pos + (dz * step)

                if 0 <= check_x <= 7 and 0 <= check_z <= 7:
                    tile = manager.board.tiles.get((check_x, check_z))

                    if tile:
                        # Puste pole
                        if tile.occupying_piece is None:
                            # Sprawdzenie czy król bezpieczny po ruchu
                            if manager.is_move_safe(self, check_x, check_z):
                                tile.color = color.green
                                manager.highlighted_tiles.append(tile)
                 
                        # Zajęte pole
                        else:
                            # Wróg
                            if tile.occupying_piece.piece_color != self.piece_color:
                                # Sprawdzenie czy król bezpieczny po ruchu
                                if manager.is_move_safe(self, check_x, check_z):
                                    tile.color = color.red
                                    manager.highlighted_tiles.append(tile)
                            break
                else:
                    break
                step += 1 

class King(Piece): # Król
    def __init__(self, x, z, piece_color):
        super().__init__(x, z, piece_color)
        self.scale = (0.5, 1.0, 0.5)  
    def show_valid_moves(self):
        moves = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for dx, dz in moves:
            move_x = self.x_pos + dx
            move_z = self.z_pos + dz

            if 0 <= move_x <= 7 and 0 <= move_z <= 7:
                tile = manager.board.tiles.get((move_x, move_z))

                if tile:
                    # Puste pole
                    if tile.occupying_piece is None:
                        # Sprawdzenie czy król bezpieczny po ruchu
                        if manager.is_move_safe(self, move_x, move_z):
                            tile.color = color.green
                            manager.highlighted_tiles.append(tile)
                        
                    # Zajęte pole
                    else:
                        # Wróg
                        if tile.occupying_piece.piece_color != self.piece_color:
                            # Sprawdzenie czy król bezpieczny po ruchu
                            if manager.is_move_safe(self, move_x, move_z):
                                tile.color = color.red
                                manager.highlighted_tiles.append(tile)
        
        # Roszada

        if not self.has_moved:
            enemy_color = color.black if self.piece_color == color.white else color.white
            
            # Król w szachu, nie może roszady
            if not manager.is_square_under_attack(self.x_pos, self.z_pos, enemy_color):
                
                # Krótka roszada (w prawo)
                tile_rook_right = manager.board.tiles.get((7, self.z_pos))
                if tile_rook_right and tile_rook_right.occupying_piece:
                    rook = tile_rook_right.occupying_piece
                    # Sprawdzamy czy to jest wieża, która się nie ruszyła
                    if rook.__class__.__name__ == 'Rook' and not rook.has_moved:
                        # Sprawdzamy czy pola pomiędzy są puste
                        if manager.board.tiles[(5, self.z_pos)].occupying_piece is None and manager.board.tiles[(6, self.z_pos)].occupying_piece is None:
                            if not manager.is_square_under_attack(5, self.z_pos, enemy_color) and not manager.is_square_under_attack(6, self.z_pos, enemy_color):
                                tile = manager.board.tiles[(6, self.z_pos)]
                                tile.color = color.cyan  
                                manager.highlighted_tiles.append(tile)

                # Długa roszada (w lewo)
                tile_rook_left = manager.board.tiles.get((0, self.z_pos))
                if tile_rook_left and tile_rook_left.occupying_piece:
                    rook = tile_rook_left.occupying_piece
                    # Sprawdzamy czy to jest wieża, która się nie ruszyła
                    if rook.__class__.__name__ == 'Rook' and not rook.has_moved:
                        # Sprawdzamy czy pola pomiędzy są puste
                        if manager.board.tiles[(1, self.z_pos)].occupying_piece is None and manager.board.tiles[(2, self.z_pos)].occupying_piece is None and manager.board.tiles[(3, self.z_pos)].occupying_piece is None:
                            if not manager.is_square_under_attack(2, self.z_pos, enemy_color) and not manager.is_square_under_attack(3, self.z_pos, enemy_color):
                                tile = manager.board.tiles[(2, self.z_pos)]
                                tile.color = color.cyan
                                manager.highlighted_tiles.append(tile)