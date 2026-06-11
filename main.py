from ursina import *
from board import Board 
from game_manager import manager

# Inicjalizacja aplikacji
app = Ursina()
Entity(
    parent=camera, 
    model='quad', 
    texture='assets/textures/kosmos.jpeg', 
    scale=(64, 36), 
    z=50,             
    unlit=True        
) 

# Czcionka
Text.default_font = 'assets/fonts/Quantico-Regular.ttf'

# Muzyka
bg_music = Audio('assets/sounds/muzyczka.wav', loop=True, volume=0.1)

# Szachownica
game_board = Board()
manager.board = game_board

# Pozycja statywu
camera_pivot = Entity(position=(3.5, 0, 3.5))

# Przyczepiamy kamerę do statywu
camera.parent = camera_pivot

# Pozycja kamery względem statywu
camera.position = (0, 14, -11.7) 
camera.rotation_x = 50

# Proste oświetlenie, żeby tekstury lepiej widać
sun = DirectionalLight(shadows=True)
sun.look_at(Vec3(1, -1, -1)) 
AmbientLight(color=color.rgba(150, 150, 150, 0.4)) 

manager.camera_pivot = camera_pivot        

manager.setup_ui()

manager.show_main_menu()

# Start
app.run()