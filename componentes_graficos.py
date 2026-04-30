import tkinter as tk

from constantes import (
    COR_BORDA,
    COR_BORDA_DESTINO_POSSIVEL,
    COR_BORDA_PECA_BRANCA,
    COR_BORDA_PECA_PRETA,
    COR_CASA_CLARA,
    COR_CASA_ESCURA,
    COR_DESTINO_POSSIVEL,
    COR_PECA_BRANCA,
    COR_PECA_PRETA,
    COR_SELECAO,
    JOGADOR_BRANCO,
    RAIO_PECA,
    TAMANHO_CASA,
    TAMANHO_TABULEIRO,
)
from logica_jogo import eh_dama, obter_cor_peca


class VistaJogo:
    """Trata apenas da parte visual da janela do jogo."""

    def __init__(self, raiz, ao_mover_peca, ao_reiniciar_jogo, jogador_atual):
        self.raiz = raiz
        self.ao_mover_peca = ao_mover_peca
        self.ao_reiniciar_jogo = ao_reiniciar_jogo
        self.jogador_atual = jogador_atual

        self.canvas = None
        self.etiqueta_estado = None
        self.entrada_origem_linha = None
        self.entrada_origem_coluna = None
        self.entrada_destino_linha = None
        self.entrada_destino_coluna = None

        self._criar_interface()

    def _criar_interface(self):
        moldura_principal = tk.Frame(self.raiz)
        moldura_principal.pack(padx=10, pady=10)

        self.canvas = tk.Canvas(
            moldura_principal,
            width=TAMANHO_CASA * TAMANHO_TABULEIRO,
            height=TAMANHO_CASA * TAMANHO_TABULEIRO,
            bg="white",
        )
        self.canvas.pack(side=tk.LEFT)

        moldura_controlo = tk.Frame(moldura_principal)
        moldura_controlo.pack(side=tk.LEFT, padx=10)

        tk.Label(moldura_controlo, text="Coordenadas de origem:", font=("Arial", 10, "bold")).pack(pady=5)

        tk.Label(moldura_controlo, text="Linha (1-8):").pack()
        self.entrada_origem_linha = tk.Entry(moldura_controlo, width=10)
        self.entrada_origem_linha.pack(pady=2)

        tk.Label(moldura_controlo, text="Coluna (1-8):").pack()
        self.entrada_origem_coluna = tk.Entry(moldura_controlo, width=10)
        self.entrada_origem_coluna.pack(pady=2)

        tk.Label(moldura_controlo, text="Coordenadas de destino:", font=("Arial", 10, "bold")).pack(pady=5)

        tk.Label(moldura_controlo, text="Linha (1-8):").pack()
        self.entrada_destino_linha = tk.Entry(moldura_controlo, width=10)
        self.entrada_destino_linha.pack(pady=2)

        tk.Label(moldura_controlo, text="Coluna (1-8):").pack()
        self.entrada_destino_coluna = tk.Entry(moldura_controlo, width=10)
        self.entrada_destino_coluna.pack(pady=2)

        tk.Button(
            moldura_controlo,
            text="Mover Peça",
            command=self.ao_mover_peca,
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5,
        ).pack(pady=10)

        tk.Button(
            moldura_controlo,
            text="Reiniciar Jogo",
            command=self.ao_reiniciar_jogo,
            bg="#f44336",
            fg="white",
            padx=20,
            pady=5,
        ).pack(pady=5)

        cor_texto = "grey" if self.jogador_atual == JOGADOR_BRANCO else "black"
        self.etiqueta_estado = tk.Label(
            moldura_controlo,
            text=f"Vez do jogador: {self.jogador_atual.upper()}",
            font=("Arial", 10, "bold"),
            fg=cor_texto,
        )
        self.etiqueta_estado.pack(pady=10)

        quadro_instrucoes = tk.LabelFrame(moldura_controlo, text="Instruções", padx=5, pady=5)
        quadro_instrucoes.pack(pady=10)
        tk.Label(quadro_instrucoes, text="• Linhas e colunas de 1 a 8", justify=tk.LEFT).pack()
        tk.Label(quadro_instrucoes, text="• Movimento diagonal para frente", justify=tk.LEFT).pack()
        tk.Label(quadro_instrucoes, text="• Captura pulando por cima", justify=tk.LEFT).pack()
        tk.Label(quadro_instrucoes, text="• Dama move-se para trás/frente", justify=tk.LEFT).pack()

    def desenhar_tabuleiro(self, tabuleiro, peca_selecionada=None, movimentos_possiveis=None):
        self.canvas.delete("all")
        movimentos_possiveis = movimentos_possiveis or []

        for linha in range(TAMANHO_TABULEIRO):
            for coluna in range(TAMANHO_TABULEIRO):
                x1 = coluna * TAMANHO_CASA
                y1 = linha * TAMANHO_CASA
                x2 = x1 + TAMANHO_CASA
                y2 = y1 + TAMANHO_CASA

                cor_casa = COR_CASA_CLARA if (linha + coluna) % 2 == 0 else COR_CASA_ESCURA
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor_casa, outline=COR_BORDA)

                if (linha + coluna) % 2 == 1:
                    self.canvas.create_text(
                        x1 + 10,
                        y1 + 10,
                        text=f"{linha + 1},{coluna + 1}",
                        font=("Arial", 8),
                        fill="white",
                    )

        for linha in range(TAMANHO_TABULEIRO):
            for coluna in range(TAMANHO_TABULEIRO):
                peca = tabuleiro[linha][coluna]
                if peca is not None:
                    self._desenhar_peca(linha, coluna, peca)

        if peca_selecionada:
            self._destacar_peca_selecionada(*peca_selecionada)

        for linha, coluna in movimentos_possiveis:
            self._destacar_movimento_possivel(linha, coluna)

    def _desenhar_peca(self, linha, coluna, peca):
        centro_x = coluna * TAMANHO_CASA + TAMANHO_CASA // 2
        centro_y = linha * TAMANHO_CASA + TAMANHO_CASA // 2
        cor_peca = obter_cor_peca(peca)

        preenchimento = COR_PECA_BRANCA if cor_peca == JOGADOR_BRANCO else COR_PECA_PRETA
        contorno = COR_BORDA_PECA_BRANCA if cor_peca == JOGADOR_BRANCO else COR_BORDA_PECA_PRETA

        self.canvas.create_oval(
            centro_x - RAIO_PECA,
            centro_y - RAIO_PECA,
            centro_x + RAIO_PECA,
            centro_y + RAIO_PECA,
            fill=preenchimento,
            outline=contorno,
            width=2,
        )

        self.canvas.create_oval(
            centro_x - RAIO_PECA + 5,
            centro_y - RAIO_PECA + 5,
            centro_x - RAIO_PECA + 15,
            centro_y - RAIO_PECA + 15,
            fill="white",
            outline="",
            stipple="gray50",
        )

        if eh_dama(peca):
            self.canvas.create_text(
                centro_x,
                centro_y,
                text="♕",
                font=("Arial", 16, "bold"),
                fill="gold",
            )

    def _destacar_peca_selecionada(self, linha, coluna):
        centro_x = coluna * TAMANHO_CASA + TAMANHO_CASA // 2
        centro_y = linha * TAMANHO_CASA + TAMANHO_CASA // 2
        self.canvas.create_oval(
            centro_x - RAIO_PECA - 3,
            centro_y - RAIO_PECA - 3,
            centro_x + RAIO_PECA + 3,
            centro_y + RAIO_PECA + 3,
            outline=COR_SELECAO,
            width=3,
        )

    def _destacar_movimento_possivel(self, linha, coluna):
        centro_x = coluna * TAMANHO_CASA + TAMANHO_CASA // 2
        centro_y = linha * TAMANHO_CASA + TAMANHO_CASA // 2
        self.canvas.create_oval(
            centro_x - 10,
            centro_y - 10,
            centro_x + 10,
            centro_y + 10,
            fill=COR_DESTINO_POSSIVEL,
            outline=COR_BORDA_DESTINO_POSSIVEL,
            width=2,
        )

    def obter_campos_movimento(self):
        return (
            self.entrada_origem_linha.get(),
            self.entrada_origem_coluna.get(),
            self.entrada_destino_linha.get(),
            self.entrada_destino_coluna.get(),
        )

    def limpar_campos(self):
        self.entrada_origem_linha.delete(0, tk.END)
        self.entrada_origem_coluna.delete(0, tk.END)
        self.entrada_destino_linha.delete(0, tk.END)
        self.entrada_destino_coluna.delete(0, tk.END)

    def atualizar_estado(self, jogador_atual):
        self.jogador_atual = jogador_atual
        cor_texto = "grey" if jogador_atual == JOGADOR_BRANCO else "black"
        self.etiqueta_estado.config(text=f"Vez do jogador: {jogador_atual.upper()}", fg=cor_texto)
