from ursina import color, Text, Entity, Button, camera, Func, destroy, curve, time, Audio, Quad

class GameManager(Entity):
    def __init__(self):
        super().__init__() 
        
        self.selected_piece = None
        self.board = None
        self.highlighted_tiles = []
        self.current_turn = color.white
        self.whose_turn = None
        self.camera_pivot = None 
        self.promotion_menu = None
        self.pawn_to_promote = None
        self.en_passant_target = None  
        self.en_passant_victim = None
        self.game_over_text = None 
        
        # Dźwięki
        self.sound_move = Audio('assets/sounds/move.wav', autoplay=False)
        self.sound_capture = Audio('assets/sounds/capture.wav', autoplay=False)

        # Wybór zestawu figur
        self.model_pack = 'normalnefigury'

        # Menu
        self.main_menu_panel = None
        self.play_again_btn = None
        self.game_ui_panel = None

        # Zegary
        self.time_limit = 600
        self.time_white = self.time_limit
        self.time_black = self.time_limit
        self.timer_text_white = None
        self.timer_text_black = None
        
        # Historia
        self.move_history = []
        self.history_text = None

    def setup_ui(self):
        # Menu
        self.game_ui_panel = Entity(parent=camera.ui, enabled=False)

        # Ramki
        
        # Ramka pod Historię ruchów
        Entity(
            parent=self.game_ui_panel,
            model=Quad(radius=0.05),
            color=color.azure,
            scale=(0.266, 0.506),
            position=(-0.73, 0.19),
            z=0.02  # Obwódka jest GŁĘBIEJ
        )
        self.history_bg = Entity(
            parent=self.game_ui_panel,
            model=Quad(radius=0.05),
            color=color.black66,
            scale=(0.26, 0.50),
            position=(-0.73, 0.19),
            z=0.01  # Czarne tło jest BLIŻEJ NAS
        )
        
        # Ramka górna (Kogo kolej)
        Entity(
            parent=self.game_ui_panel,
            model=Quad(radius=0.05),
            color=color.azure,
            scale=(0.406, 0.066),
            position=(0, 0.47),
            z=0.02
        )
        self.top_bg = Entity(
            parent=self.game_ui_panel,
            model=Quad(radius=0.05),
            color=color.black66,
            scale=(0.4, 0.06),
            position=(0, 0.47),
            z=0.01
        )

        # Ramka pod Zegar czarnych 
        Entity(
            parent=self.game_ui_panel,
            model=Quad(radius=0.05),
            color=color.azure,
            scale=(0.306, 0.106),
            position=(0.7, 0.45),
            z=0.02
        )
        self.timer_b_bg = Entity(
            parent=self.game_ui_panel,
            model=Quad(radius=0.05),
            color=color.black66,
            scale=(0.3, 0.1),
            position=(0.7, 0.45),
            z=0.01
        )

        # Ramka pod Zegar białych 
        Entity(
            parent=self.game_ui_panel,
            model=Quad(radius=0.05),
            color=color.azure,
            scale=(0.306, 0.106),
            position=(0.7, -0.45),
            z=0.02
        )
        self.timer_w_bg = Entity(
            parent=self.game_ui_panel,
            model=Quad(radius=0.05),
            color=color.black66,
            scale=(0.3, 0.1),
            position=(0.7, -0.45),
            z=0.01
        )

        # Kogo kolej 
        self.whose_turn = Text(
            parent=self.game_ui_panel, 
            text="Kolej: Białe", 
            position=(0, 0.47), 
            origin=(0, 0), 
            scale=1.2, 
            color=color.white
        )

        # Zegary
        self.timer_text_black = Text(
            parent=self.game_ui_panel, 
            text="Czarne: 10:00", 
            position=(0.7, 0.45), 
            origin=(0, 0), 
            scale=1.5, 
            color=color.light_gray
        )
        self.timer_text_white = Text(
            parent=self.game_ui_panel, 
            text="Białe: 10:00", 
            position=(0.7, -0.45), 
            origin=(0, 0), 
            scale=1.5, 
            color=color.white
        )

        # Historia 
        self.history_text = Text(
            parent=self.game_ui_panel, 
            text="Historia ruchów:\n", 
            position=(-0.84, 0.42), 
            origin=(-0.5, 0.5), 
            scale=1.1, 
            color=color.white
        )

        # Promocja piona
        self.promotion_menu = Entity(
            parent=camera.ui, 
            enabled=False
        )
        
        # 1. Ramka - OUTLINE
        Entity(
            parent=self.promotion_menu, 
            model=Quad(radius=0.05), 
            color=color.azure, 
            scale=(0.506, 0.306), 
            position=(0, 0), 
            z=0.02
        )
        
        # 2. Ramka - TŁO
        Entity(
            parent=self.promotion_menu, 
            model=Quad(radius=0.05), 
            color=color.black66, 
            scale=(0.5, 0.3), 
            position=(0, 0), 
            z=0.01,
            collider='box'  
        )
        
        Text(
            parent=self.promotion_menu, 
            text="Wybierz figure do promocji:", 
            position=(0, 0.1), 
            origin=(0, 0), 
            scale=1.5
        )

        Button(
            parent=self.promotion_menu, 
            text='Hetman', 
            position=(-0.18, -0.05), 
            scale=(0.11, 0.08), 
            color=color.azure, 
            on_click=Func(self.promote, 'Queen')
        )
        Button(
            parent=self.promotion_menu, 
            text='Wieza',  
            position=(-0.06, -0.05), 
            scale=(0.11, 0.08), 
            color=color.azure, 
            on_click=Func(self.promote, 'Rook')
        )
        Button(
            parent=self.promotion_menu, 
            text='Skoczek',
            position=(0.06, -0.05),  
            scale=(0.11, 0.08), 
            color=color.azure, 
            on_click=Func(self.promote, 'Knight')
        )
        Button(
            parent=self.promotion_menu, 
            text='Goniec', 
            position=(0.18, -0.05),  
            scale=(0.11, 0.08), 
            color=color.azure, 
            on_click=Func(self.promote, 'Bishop')
        )

        # Panel końca gry
        self.game_over_panel = Entity(
            parent=camera.ui, 
            enabled=False
        )

        Entity(
            parent=self.game_over_panel,
            model=Quad(radius=0.05),
            color=color.red,        
            scale=(0.806, 0.306),   
            position=(0, 0.25),     
            z=0.02
        )
        
        Entity(
            parent=self.game_over_panel,
            model=Quad(radius=0.05),
            color=color.rgba(20/255, 5/255, 5/255, 200/255), 
            scale=(0.8, 0.3),
            position=(0, 0.25),
            z=0.01
        )

        self.game_over_text = Text(
            parent=self.game_over_panel, 
            text="", 
            position=(0, 0.25),     
            origin=(0, 0), 
            scale=3, 
            color=color.white       
        )

        self.play_again_btn = Button(
            parent=self.game_over_panel, 
            text="Zagraj ponownie", 
            position=(0, -0.05),    
            scale=(0.3, 0.1), 
            color=color.azure, 
            on_click=self.reset_and_start
        )

        # Budowa Menu Głównego
        self.main_menu_panel = Entity(
            parent=camera.ui,
            enabled=False
        )
        Entity(
            parent=self.main_menu_panel,
            model='quad',
            color=color.black90,
            scale=(2, 2),
            z=0.1,
            collider='box'
        )
        Text(
            parent=self.main_menu_panel,
            text="SZACHY 3D",
            position=(0, 0.25),
            origin=(0, 0),
            scale=5,
            color=color.white
        )
        # Panel wyboru zestawu figur (styl jak historia ruchów)
        Entity(
            parent=self.main_menu_panel,
            model=Quad(radius=0.05),
            color=color.azure,
            scale=(0.56, 0.196),
            position=(0, -0.3),
            z=0.02
        )
        Entity(
            parent=self.main_menu_panel,
            model=Quad(radius=0.05),
            color=color.black66,
            scale=(0.55, 0.19),
            position=(0, -0.3),
            z=0.01
        )
        Text(
            parent=self.main_menu_panel,
            text="Zestaw figur",
            position=(0, -0.25),
            origin=(0, 0),
            scale=1.2,
            color=color.azure
        )

        # Kółka radio
        self._radio_normal_dot = Entity(parent=self.main_menu_panel, model='circle', color=color.azure,      scale=0.018, position=(-0.22, -0.3),  z=-0.01)
        self._radio_cosmic_dot = Entity(parent=self.main_menu_panel, model='circle', color=color.light_gray, scale=0.018, position=(-0.22, -0.355), z=-0.01)

        Text(parent=self.main_menu_panel, text="Normalne figury",  position=(-0.195, -0.3),   origin=(-0.5, 0), scale=1.2, color=color.white)
        Text(parent=self.main_menu_panel, text="Kosmiczne figury", position=(-0.195, -0.355), origin=(-0.5, 0), scale=1.2, color=color.white)

        def select_normal():
            self.model_pack = 'normalnefigury'
            self._radio_normal_dot.color = color.azure
            self._radio_cosmic_dot.color = color.light_gray

        def select_cosmic():
            self.model_pack = 'kosmicznefigury'
            self._radio_normal_dot.color = color.light_gray
            self._radio_cosmic_dot.color = color.azure

        Button(
            parent=self.main_menu_panel,
            model=Quad(radius=0.03),
            text="",
            position=(0, -0.3),
            scale=(0.55, 0.042),
            color=color.clear,
            highlight_color=color.clear,
            pressed_color=color.clear,
            on_click=select_normal
        )
        Button(
            parent=self.main_menu_panel,
            model=Quad(radius=0.03),
            text="",
            position=(0, -0.355),
            scale=(0.55, 0.042),
            color=color.clear,
            highlight_color=color.clear,
            pressed_color=color.clear,
            on_click=select_cosmic
        )

        Button(
            parent=self.main_menu_panel,
            text="GRAJ",
            position=(0, -0.10),
            scale=(0.4, 0.13),
            color=color.green,
            on_click=self.start_game
        )
 
    def show_main_menu(self):
        self.main_menu_panel.enabled = True
        self.game_ui_panel.enabled = False

    def start_game(self):
        self.main_menu_panel.enabled = False
        self.game_ui_panel.enabled = True
        self.setup_pieces()
    
    # Przywrócenie stanu początkowego gry
    def reset_and_start(self):
        for x in range(8):
            for z in range(8):
                tile = self.board.tiles[(x, z)]
                if tile.occupying_piece:
                    destroy(tile.occupying_piece)
                    tile.occupying_piece = None
                    
        self.current_turn = color.white
        self.whose_turn.text = "Kolej: Białe"
        self.whose_turn.color = color.white
        self.camera_pivot.rotation_y = 0
        self.game_over_panel.enabled = False
        self.selected_piece = None
        self.en_passant_target = None  
        self.en_passant_victim = None
        self.highlighted_tiles.clear()
        
        self.time_white = self.time_limit
        self.time_black = self.time_limit
        
        self.move_history.clear()
        self.history_text.text = "Historia ruchów:\n"
        
        self.start_game()

    def setup_pieces(self):
        from pieces import Pawn, Rook, Knight, Bishop, Queen, King
        for i in range(8):
            Pawn(i, 1, color.white)  
            Pawn(i, 6, color.black)  

        Rook(0, 0, color.white); Rook(7, 0, color.white)
        Knight(1, 0, color.white); Knight(6, 0, color.white)
        Bishop(2, 0, color.white); Bishop(5, 0, color.white)
        Queen(3, 0, color.white)
        King(4, 0, color.white)

        Rook(0, 7, color.black); Rook(7, 7, color.black)
        Knight(1, 7, color.black); Knight(6, 7, color.black)
        Bishop(2, 7, color.black); Bishop(5, 7, color.black)
        Queen(3, 7, color.black)
        King(4, 7, color.black)

    # Historia ruchów (tłumacznenie na język szachowy)
    def log_move(self, piece, start_x, start_z, target_x, target_z, is_capture=False, special=None):
        cols = "ABCDEFGH"
        rows = "12345678"
        start_pos = f"{cols[start_x]}{rows[start_z]}"
        end_pos = f"{cols[target_x]}{rows[target_z]}"
        
        piece_names = {'Pawn': 'Pion', 'Rook': 'Wieża', 'Knight': 'Skoczek', 'Bishop': 'Goniec', 'Queen': 'Hetman', 'King': 'Król'}
        p_name = piece_names.get(piece.__class__.__name__, 'Figura')
        c_name = "B" if piece.piece_color == color.white else "C"
        
        if special == "Krótka roszada":
            move_str = f"{c_name}: 0-0 (Roszada)"
        elif special == "Długa roszada":
            move_str = f"{c_name}: 0-0-0 (Roszada)"
        elif special == "En Passant":
            move_str = f"{c_name} {p_name}: {start_pos}x{end_pos} (e.p.)"
        else:
            action = "x" if is_capture else "-"
            move_str = f"{c_name} {p_name}: {start_pos}{action}{end_pos}"
            
        self.move_history.append(move_str)
        
        # Ograniczenie historii do ostatnich 15 ruchów
        if len(self.move_history) > 15:
            self.move_history.pop(0)
            
        self.history_text.text = "Historia ruchów:\n\n" + "\n".join(self.move_history)

    # Promocja piona
    def promote(self, piece_type):
        pawn = self.pawn_to_promote
        x, z, c = pawn.x_pos, pawn.z_pos, pawn.piece_color
        destroy(pawn)
        from pieces import Queen, Rook, Knight, Bishop
        
        if piece_type == 'Queen': new_piece = Queen(x, z, c)
        elif piece_type == 'Rook': new_piece = Rook(x, z, c)
        elif piece_type == 'Knight': new_piece = Knight(x, z, c)
        elif piece_type == 'Bishop': new_piece = Bishop(x, z, c)
            
        self.board.tiles[(x, z)].occupying_piece = new_piece
        self.promotion_menu.enabled = False
        self.pawn_to_promote = None
        self.switch_turn()

    # Zmiana tury
    def switch_turn(self):
        if self.current_turn == color.white:
            self.current_turn = color.black
            print("--> Tura Czarnych")
            self.whose_turn.text = "Kolej: Czarne"
            self.whose_turn.color = color.light_gray
            self.camera_pivot.animate_rotation_y(180, duration=0.8, curve=curve.in_out_sine)
        else:
            self.current_turn = color.white
            print("--> Tura Białych")
            self.whose_turn.text = "Kolej: Białe"
            self.whose_turn.color = color.white
            self.camera_pivot.animate_rotation_y(0, duration=0.8, curve=curve.in_out_sine)

        self.check_game_over()

    # Koniec gry?
    def check_game_over(self):
        king_pos = None
        for x in range(8):
            for z in range(8):
                p = self.board.tiles[(x, z)].occupying_piece
                if p and p.piece_color == self.current_turn and p.__class__.__name__ == 'King':
                    king_pos = (x, z)
                    break
            if king_pos: break
            
        enemy_color = color.black if self.current_turn == color.white else color.white
        is_in_check = False
        if king_pos:
            is_in_check = self.is_square_under_attack(king_pos[0], king_pos[1], enemy_color)
            
        moves_available = False
        
        for x in range(8):
            for z in range(8):
                piece = self.board.tiles[(x, z)].occupying_piece
                if piece and piece.piece_color == self.current_turn:
                    piece.show_valid_moves()
                    if len(self.highlighted_tiles) > 0: moves_available = True
                    for t in self.highlighted_tiles: t.color = t.original_color
                    self.highlighted_tiles.clear()
                    if moves_available: break
            if moves_available: break
                
        if not moves_available:
            self.game_over_panel.enabled = True 
            if is_in_check:
                zwyciezca = "BIAŁE" if enemy_color == color.white else "CZARNE"
                self.game_over_text.text = "SZACH-MAT!\nWygrywaja {}".format(zwyciezca)
            else:
                self.game_over_text.text = "PAT!\nGra konczy sie remisem"
            self.current_turn = None
        elif is_in_check:
            side = "Białe" if self.current_turn == color.white else "Czarne"
            self.whose_turn.text = f"Kolej: {side} — SZACH!"

    # Zegary
    def update(self):
        if not self.game_ui_panel.enabled or self.current_turn is None:
            return

        if self.current_turn == color.white:
            self.time_white -= time.dt
            if self.time_white <= 0:
                self.time_white = 0
                self.time_out(color.black) 
        else:
            self.time_black -= time.dt
            if self.time_black <= 0:
                self.time_black = 0
                self.time_out(color.white)

        # Zmiana sekund na minuty i sekundy
        mins_w, secs_w = divmod(int(self.time_white), 60)
        self.timer_text_white.text = f"Białe: {mins_w:02d}:{secs_w:02d}"

        mins_b, secs_b = divmod(int(self.time_black), 60)
        self.timer_text_black.text = f"Czarne: {mins_b:02d}:{secs_b:02d}"

    def time_out(self, winner_color):
        self.game_over_text.enabled = True
        self.play_again_btn.enabled = True
        zwyciezca = "BIAŁE" if winner_color == color.white else "CZARNE"
        self.game_over_text.text = f"CZAS MINĄŁ!\nWygrywają {zwyciezca}"
        self.current_turn = None

    # Radar zagrożeń
    def is_square_under_attack(self, x, z, enemy_color):
        pawn_dir = 1 if enemy_color == color.white else -1
        for dx in [-1, 1]:
            px, pz = x + dx, z - pawn_dir 
            if 0 <= px <= 7 and 0 <= pz <= 7:
                piece = self.board.tiles[(px, pz)].occupying_piece
                if piece and piece.piece_color == enemy_color and piece.__class__.__name__ == 'Pawn':
                    return True

        knight_moves = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
        for dx, dz in knight_moves:
            kx, kz = x + dx, z + dz
            if 0 <= kx <= 7 and 0 <= kz <= 7:
                piece = self.board.tiles[(kx, kz)].occupying_piece
                if piece and piece.piece_color == enemy_color and piece.__class__.__name__ == 'Knight':
                    return True

        king_moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dz in king_moves:
            kx, kz = x + dx, z + dz
            if 0 <= kx <= 7 and 0 <= kz <= 7:
                piece = self.board.tiles[(kx, kz)].occupying_piece
                if piece and piece.piece_color == enemy_color and piece.__class__.__name__ == 'King':
                    return True

        straight_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dz in straight_dirs:
            step = 1
            while True:
                cx, cz = x + (dx * step), z + (dz * step)
                if 0 <= cx <= 7 and 0 <= cz <= 7:
                    piece = self.board.tiles[(cx, cz)].occupying_piece
                    if piece:
                        if piece.piece_color == enemy_color and piece.__class__.__name__ in ['Rook', 'Queen']:
                            return True
                        break 
                else:
                    break
                step += 1

        diag_dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dz in diag_dirs:
            step = 1
            while True:
                cx, cz = x + (dx * step), z + (dz * step)
                if 0 <= cx <= 7 and 0 <= cz <= 7:
                    piece = self.board.tiles[(cx, cz)].occupying_piece
                    if piece:
                        if piece.piece_color == enemy_color and piece.__class__.__name__ in ['Bishop', 'Queen']:
                            return True
                        break 
                else:
                    break
                step += 1

        return False

    def is_move_safe(self, piece, target_x, target_z):
        original_x = piece.x_pos
        original_z = piece.z_pos
        target_tile = self.board.tiles.get((target_x, target_z))
        
        if not target_tile:
            return False
            
        original_occupant = target_tile.occupying_piece

        self.board.tiles[(original_x, original_z)].occupying_piece = None
        target_tile.occupying_piece = piece
        piece.x_pos = target_x
        piece.z_pos = target_z

        king_pos = None
        for x in range(8):
            for z in range(8):
                p = self.board.tiles[(x, z)].occupying_piece
                if p and p.piece_color == piece.piece_color and p.__class__.__name__ == 'King':
                    king_pos = (x, z)
                    break
            if king_pos:
                break

        is_safe = True
        if king_pos:
            enemy_color = color.black if piece.piece_color == color.white else color.white
            if self.is_square_under_attack(king_pos[0], king_pos[1], enemy_color):
                is_safe = False

        piece.x_pos = original_x
        piece.z_pos = original_z
        self.board.tiles[(original_x, original_z)].occupying_piece = piece
        target_tile.occupying_piece = original_occupant

        return is_safe

manager = GameManager()