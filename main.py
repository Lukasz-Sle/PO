from ursina import *
from board import Board 
from game_manager import manager

# Inicjalizacja aplikacji
app = Ursina()
window.color = color.rgb32(10, 100, 10) 

# Szachownica
game_board = Board()
manager.board = game_board

# Pozycja statywu
camera_pivot = Entity(position=(3.5, 0, 3.5))

# Przyczepiamy kamerę do statywu
camera.parent = camera_pivot

# Pozycja kamery względem statywu
camera.position = (0, 12, -12) 
camera.rotation_x = 45

# Proste oświetlenie, żeby tekstury lepiej widać
DirectionalLight(y=2, x=1, z=1)
AmbientLight(color=color.rgba(150, 150, 150, 0.5))

manager.camera_pivot = camera_pivot        

manager.setup_ui()

manager.show_main_menu()

# Start
app.run()