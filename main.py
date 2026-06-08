from ursina import *
from board import Board 
from game_manager import manager

# Inicjalizacja aplikacji
app = Ursina()
window.color = color.rgb(0, 0, 153) 

# Szachownica
game_board = Board()
manager.board = game_board

# Pozycja statywu
camera_pivot = Entity(position=(3.5, 0, 3.5))

# Przyczepiamy kamerę do statywu
camera.parent = camera_pivot

# Pozycja kamery względem statywu
camera.position = (0, 10, -12.5) 
camera.rotation_x = 40

manager.camera_pivot = camera_pivot        

manager.setup_ui()

manager.show_main_menu()

# Start
app.run()