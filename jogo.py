from tkinter import messagebox

from componentes_graficos import VistaJogo
from constantes import JOGADOR_BRANCO, JOGADOR_PRETO, TITULO_JANELA
from logica_jogo import (
    executar_movimento,
    inicializar_tabuleiro,
    movimento_valido,
    obter_cor_peca,
    obter_vencedor,
)


class JogoDamas:
    """Classe principal que liga a lógica do jogo à interface gráfica."""

    def __init__(self, raiz, quem_comeca=1):
        self.raiz = raiz
        self.raiz.title(TITULO_JANELA)
        self.raiz.resizable(False, False)

        self.tabuleiro = inicializar_tabuleiro()
        self.jogador_atual = JOGADOR_BRANCO
        self.peca_selecionada = None
        self.movimentos_possiveis = []
        self.quem_comeca = quem_comeca

        self.vista = VistaJogo(
            raiz=raiz,
            ao_mover_peca=self.mover_peca_por_coordenadas,
            ao_reiniciar_jogo=self.reiniciar_jogo,
            jogador_atual=self.jogador_atual,
        )
        self.vista.desenhar_tabuleiro(self.tabuleiro, self.peca_selecionada, self.movimentos_possiveis)

    def mover_peca_por_coordenadas(self):
        """Lê as coordenadas da interface, valida o movimento e atualiza o tabuleiro."""
        try:
            linha_origem, coluna_origem, linha_destino, coluna_destino = self._ler_campos()
        except ValueError:
            messagebox.showerror("Erro", "Digite números válidos")
            return

        if not self._coordenadas_validas(linha_origem, coluna_origem, linha_destino, coluna_destino):
            messagebox.showerror("Erro", "Coordenadas devem estar entre 1 e 8")
            return

        if self.tabuleiro[linha_origem][coluna_origem] is None:
            messagebox.showerror("Erro", "Não há peça na posição de origem")
            return

        cor_peca = obter_cor_peca(self.tabuleiro[linha_origem][coluna_origem])
        if cor_peca != self.jogador_atual:
            messagebox.showerror("Erro", f"É a vez do jogador {self.jogador_atual.upper()}")
            return

        if not movimento_valido(self.tabuleiro, linha_origem, coluna_origem, linha_destino, coluna_destino):
            messagebox.showerror("Erro", "Movimento inválido!")
            return

        executar_movimento(self.tabuleiro, linha_origem, coluna_origem, linha_destino, coluna_destino)
        self._trocar_jogador()
        self.vista.limpar_campos()
        self.vista.desenhar_tabuleiro(self.tabuleiro, self.peca_selecionada, self.movimentos_possiveis)
        self._verificar_fim_jogo()

    def _ler_campos(self):
        origem_linha, origem_coluna, destino_linha, destino_coluna = self.vista.obter_campos_movimento()
        return (
            int(origem_linha) - 1,
            int(origem_coluna) - 1,
            int(destino_linha) - 1,
            int(destino_coluna) - 1,
        )

    @staticmethod
    def _coordenadas_validas(linha_origem, coluna_origem, linha_destino, coluna_destino):
        valores = [linha_origem, coluna_origem, linha_destino, coluna_destino]
        return all(0 <= valor < 8 for valor in valores)

    def _trocar_jogador(self):
        self.jogador_atual = JOGADOR_PRETO if self.jogador_atual == JOGADOR_BRANCO else JOGADOR_BRANCO
        self.vista.atualizar_estado(self.jogador_atual)

    def _verificar_fim_jogo(self):
        vencedor = obter_vencedor(self.tabuleiro)
        if vencedor == JOGADOR_PRETO:
            messagebox.showinfo("Fim de Jogo", "Jogador PRETO venceu!")
            self.reiniciar_jogo()
        elif vencedor == JOGADOR_BRANCO:
            messagebox.showinfo("Fim de Jogo", "Jogador BRANCO venceu!")
            self.reiniciar_jogo()

    def reiniciar_jogo(self):
        """Repõe o tabuleiro na posição inicial."""
        self.tabuleiro = inicializar_tabuleiro()
        self.jogador_atual = JOGADOR_BRANCO
        self.peca_selecionada = None
        self.movimentos_possiveis = []
        self.vista.limpar_campos()
        self.vista.atualizar_estado(self.jogador_atual)
        self.vista.desenhar_tabuleiro(self.tabuleiro, self.peca_selecionada, self.movimentos_possiveis)
