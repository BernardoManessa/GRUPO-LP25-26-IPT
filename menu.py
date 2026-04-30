import sys
import tkinter as tk

from constantes import TITULO_MENU



def mostrar_menu_grafico(callback_iniciar):
    """Mostra o menu inicial e chama a função de arranque com a opção escolhida."""
    raiz = tk.Tk()
    raiz.title(TITULO_MENU)
    raiz.geometry("300x250")
    raiz.resizable(False, False)

    largura_ecra = raiz.winfo_screenwidth()
    altura_ecra = raiz.winfo_screenheight()
    posicao_x = (largura_ecra // 2) - (300 // 2)
    posicao_y = (altura_ecra // 2) - (250 // 2)
    raiz.geometry(f"300x250+{posicao_x}+{posicao_y}")

    moldura_principal = tk.Frame(raiz, padx=20, pady=20)
    moldura_principal.pack(expand=True)

    tk.Label(moldura_principal, text="Damas Portuguesas", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(moldura_principal, text="Escolha quem começa:", font=("Arial", 10)).pack(pady=5)

    def processar_escolha(escolha):
        raiz.destroy()
        if escolha == 0:
            sys.exit(0)
        callback_iniciar(escolha)

    tk.Button(moldura_principal, text="Branco Começa", width=25, command=lambda: processar_escolha(1)).pack(pady=5)
    tk.Button(moldura_principal, text="Preta Começa", width=25, command=lambda: processar_escolha(2)).pack(pady=5)
    tk.Button(moldura_principal, text="Sair", width=25, command=lambda: processar_escolha(0)).pack(pady=5)

    raiz.mainloop()
