import tkinter as tk

from jogo import JogoDamas
from menu import mostrar_menu_grafico



def iniciar_jogo(quem_comeca):
    raiz = tk.Tk()
    JogoDamas(raiz, quem_comeca)
    raiz.mainloop()


if __name__ == "__main__":
    mostrar_menu_grafico(iniciar_jogo)
