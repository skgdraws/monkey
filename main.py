import tkinter as tk
import pathlib

def main():

    # Window settings
    window = tk.Tk()
    window.title("Taller de Interfaz Gráfica")
    window.geometry("448x512")
    #window.iconbitmap( str(pathlib.Path().resolve()) + "\icon.ico")
    window.resizable(False, False)

    #Canvases and stuff like that
    menu_canvas = tk.Canvas(window, width=448, height=512, borderwidth=0, highlightthickness=0, bg="#000000")
    menu_canvas.place(x=0, y=0)

    # The window we are working with must be selected as the main loop
    window.mainloop()

main()