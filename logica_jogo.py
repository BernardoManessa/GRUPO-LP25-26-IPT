from constantes import (
    JOGADOR_BRANCO,
    JOGADOR_PRETO,
    LINHAS_INICIAIS_BRANCO,
    LINHAS_INICIAIS_PRETO,
    TAMANHO_TABULEIRO,
)


def criar_tabuleiro_vazio():
    """Cria um tabuleiro 8x8 vazio."""
    return [[None for _ in range(TAMANHO_TABULEIRO)] for _ in range(TAMANHO_TABULEIRO)]



def inicializar_tabuleiro():
    """Coloca as peças nas posições iniciais."""
    tabuleiro = criar_tabuleiro_vazio()

    for linha in range(TAMANHO_TABULEIRO):
        for coluna in range(TAMANHO_TABULEIRO):
            if (linha + coluna) % 2 == 1:
                if linha in LINHAS_INICIAIS_PRETO:
                    tabuleiro[linha][coluna] = JOGADOR_PRETO
                elif linha in LINHAS_INICIAIS_BRANCO:
                    tabuleiro[linha][coluna] = JOGADOR_BRANCO

    return tabuleiro



def obter_cor_peca(peca):
    """Devolve a cor da peça, quer seja normal ou dama."""
    if peca is None:
        return None
    if isinstance(peca, tuple):
        return peca[0]
    return peca



def eh_dama(peca):
    """Indica se a peça é uma dama."""
    return isinstance(peca, tuple) and peca[1] is True



def eh_casa_escura(linha, coluna):
    return (linha + coluna) % 2 == 1



def movimento_valido(tabuleiro, linha_origem, coluna_origem, linha_destino, coluna_destino):
    """Valida o movimento conforme a lógica original do programa."""
    peca = tabuleiro[linha_origem][coluna_origem]
    if peca is None:
        return False

    cor_peca = obter_cor_peca(peca)
    dama = eh_dama(peca)

    if tabuleiro[linha_destino][coluna_destino] is not None:
        return False

    if not eh_casa_escura(linha_destino, coluna_destino):
        return False

    diferenca_linhas = linha_destino - linha_origem
    diferenca_colunas = coluna_destino - coluna_origem

    if abs(diferenca_linhas) != abs(diferenca_colunas):
        return False

    if not dama:
        if cor_peca == JOGADOR_BRANCO and diferenca_linhas >= 0:
            return False
        if cor_peca == JOGADOR_PRETO and diferenca_linhas <= 0:
            return False

    if abs(diferenca_linhas) == 1:
        return True

    if abs(diferenca_linhas) == 2:
        linha_meio = (linha_origem + linha_destino) // 2
        coluna_meio = (coluna_origem + coluna_destino) // 2
        peca_meio = tabuleiro[linha_meio][coluna_meio]

        if peca_meio is None:
            return False

        return obter_cor_peca(peca_meio) != cor_peca

    return False



def promover_se_necessario(tabuleiro, linha, coluna):
    """Transforma uma peça em dama quando atinge a última linha."""
    peca = tabuleiro[linha][coluna]
    if peca is None or eh_dama(peca):
        return

    cor_peca = obter_cor_peca(peca)

    if cor_peca == JOGADOR_BRANCO and linha == 0:
        tabuleiro[linha][coluna] = (cor_peca, True)
    elif cor_peca == JOGADOR_PRETO and linha == TAMANHO_TABULEIRO - 1:
        tabuleiro[linha][coluna] = (cor_peca, True)



def executar_movimento(tabuleiro, linha_origem, coluna_origem, linha_destino, coluna_destino):
    """Executa um movimento já validado."""
    peca = tabuleiro[linha_origem][coluna_origem]

    if abs(linha_destino - linha_origem) == 2:
        linha_meio = (linha_origem + linha_destino) // 2
        coluna_meio = (coluna_origem + coluna_destino) // 2
        tabuleiro[linha_meio][coluna_meio] = None

    tabuleiro[linha_destino][coluna_destino] = peca
    tabuleiro[linha_origem][coluna_origem] = None
    promover_se_necessario(tabuleiro, linha_destino, coluna_destino)



def contar_pecas(tabuleiro):
    """Conta quantas peças brancas e pretas existem no tabuleiro."""
    total_brancas = 0
    total_pretas = 0

    for linha in tabuleiro:
        for peca in linha:
            cor_peca = obter_cor_peca(peca)
            if cor_peca == JOGADOR_BRANCO:
                total_brancas += 1
            elif cor_peca == JOGADOR_PRETO:
                total_pretas += 1

    return total_brancas, total_pretas



def obter_vencedor(tabuleiro):
    """Verifica se algum jogador ficou sem peças."""
    total_brancas, total_pretas = contar_pecas(tabuleiro)

    if total_brancas == 0:
        return JOGADOR_PRETO
    if total_pretas == 0:
        return JOGADOR_BRANCO
    return None
