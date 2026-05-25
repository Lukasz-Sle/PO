from ursina import *
from board import Board 
from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from game_manager import manager

# Inicjalizacja aplikacji
app = Ursina()
window.color = color.rgb(0, 0, 153) 

# Szachownica
game_board = Board()
manager.board = game_board

#Ustawienie figur
def setup_board():
    # Pętla od pionów
    for i in range(8):
        Pawn(i, 1, color.white)  
        Pawn(i, 6, color.black)  

    # Białe figury
    Rook(0, 0, color.white); Rook(7, 0, color.white)
    Knight(1, 0, color.white); Knight(6, 0, color.white)
    Bishop(2, 0, color.white); Bishop(5, 0, color.white)
    Queen(3, 0, color.white)
    King(4, 0, color.white)

    # Czarne figury
    Rook(0, 7, color.black); Rook(7, 7, color.black)
    Knight(1, 7, color.black); Knight(6, 7, color.black)
    Bishop(2, 7, color.black); Bishop(5, 7, color.black)
    Queen(3, 7, color.black)
    King(4, 7, color.black)

manager.setup_ui()
setup_board()

# Pozycja statywu
camera_pivot = Entity(position=(3.5, 0, 3.5))

# Przyczepiamy kamerę do statywu
camera.parent = camera_pivot

# Pozycja kamery względem statywu
camera.position = (0, 10, -12.5) 
camera.rotation_x = 40

from game_manager import manager
manager.camera_pivot = camera_pivot        

# Start
app.run()