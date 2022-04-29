import tkinter as tk
from PIL import ImageTk,Image
import pathlib
from support import save_data, import_scores

def game_over(score):

    window = tk.Tk()
    window.title("Save Your Highscore!")
    window.geometry("448x512")
    window.iconbitmap( str(pathlib.Path().resolve()) + "\icon.ico")
    window.resizable(False, False)

    #Canvases for the Background
    screen = tk.Canvas(window, width= 448, height=512, borderwidth=0, highlightthickness=0, bg="#000000")
    screen.place(x= 0, y= 0)

    #Placing the logo
    logo = ImageTk.PhotoImage(Image.open('images/Logo.png'))
    screen.create_image(10, 80, anchor = tk.NW, image= logo)

    Label1 = tk.Label(screen, text='Your Score is\n' + str(score) + 'points', font=('Kongtext', 15), bg="#000000", fg="#ffffff")
    Label1.place(x= 84, y= 230)

    var = tk.StringVar()
    entry = tk.Entry(font=("Kongtext", 15), textvariable=var, justify=tk.CENTER, width= 10)
    entry.place(x=120, y=375)

    def saving_the_funni():
        if var.get() != '':
            save_data(score, var.get())

            window.destroy()

    save_button = tk.Button(screen, text="Save Name", font=("Kongtext", "8"), fg="#ffffff", bg="#18191c", command=saving_the_funni)
    save_button.place(x = 150, y = 410)

    # The window we are working with must be selected as the main loop
    window.mainloop()


def hall_of_fame():

    window = tk.Tk()
    window.title("Hall of Fame")
    window.geometry("448x512")
    window.iconbitmap( str(pathlib.Path().resolve()) + "\icon.ico")
    window.resizable(False, False)

    #Canvases for the Background
    screen = tk.Canvas(window, width= 448, height=512, borderwidth=0, highlightthickness=0, bg="#000000")
    screen.place(x= 0, y= 0)

    #Placing the logo
    logo = ImageTk.PhotoImage(Image.open('images/Logo.png'))
    screen.create_image(10, 30, anchor = tk.NW, image= logo)

    score1 = tk.Label(text=f"1st.", font=("Kongtext", 10), fg='#ffffff', bg="#000000")
    score1.place(x= 80, y= 240)
    score2 = tk.Label(text=f"2nd.", font=("Kongtext", 10), fg='#ffffff', bg="#000000")
    score2.place(x= 80, y= 270)
    score3 = tk.Label(text=f"3rd.", font=("Kongtext", 10), fg='#ffffff', bg="#000000")
    score3.place(x= 80, y= 300)
    score4 = tk.Label(text=f"4rd.", font=("Kongtext", 10), fg='#ffffff', bg="#000000")
    score4.place(x= 80, y= 330)
    score5 = tk.Label(text=f"5th.", font=("Kongtext", 10), fg='#ffffff', bg="#000000")
    score5.place(x= 80, y= 360)

    def organize_score_list():
        lista = import_scores("data/scores.csv")
        print(lista)
        reorganize = []

        return organizar(lista, reorganize)


    def organizar(lista, reorden): 
        if lista == []: 
            return reorden
        else: 
            buscar_mayor = buscar(lista, mayor(lista), 0)
            return organizar(eliminar(lista, buscar_mayor, []), reorden + [buscar_mayor])

    def eliminar(lista, buscar_mayor, nueva_lista): 
        if lista == []: 
            return nueva_lista
        elif lista[0] == buscar_mayor: 
            return eliminar(lista[1:], buscar_mayor, nueva_lista)
        else: 
            return eliminar(lista[1:], buscar_mayor, [lista[0]] + nueva_lista)

    def buscar(lista, num, i): 
        if num == int(lista[i][0]):
            return lista[i]
        else: 
            return buscar(lista, num, i + 1)

    def mayor(lista): 
        if lista[1:] == []: 
            return int(lista[0][0])
        else: 
            return compara(int(lista[0][0]), mayor(lista[1:]))

    def compara(x, y): 
        if x > y: 
            return x
        else: 
            return y

    def set_scores(lista):

        if lista == []:
            return
        
        else:
            if lista[4][0] != '':

                score5.config(text= '5th. ' + lista[4][0] + ' - ' + lista[4][1])

            if lista[3][0] != '':

                score4.config(text= '4th. ' + lista[3][0] + ' - ' + lista[3][1])
            if lista[2][0] != '':

                score3.config(text= '3rd. ' + lista[2][0] + ' - ' + lista[2][1])

            if lista[1][0] != '':

                score2.config(text= '2nd. ' + lista[1][0] + ' - ' + lista[1][1])

            if lista[0][0] != '':

                score1.config(text= '1st. ' + lista[0][0] + ' - ' + lista[0][1])

    scores = organize_score_list()
    set_scores(scores)

    button = tk.Button(window, text="Back to Game", font=("Kongtext", "8"), fg="#ffffff", bg="#18191c", command=window.destroy)
    button.place(x=150, y=400)

    # The window we are working with must be selected as the main loop
    window.mainloop()
