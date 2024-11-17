from matplotlib import pyplot as pp
from os import listdir, getcwd


def gerando_grafico():
    """
    Descrição:
        Função responsável por, sozinha, pegar o último arquivo de dados
        e gerar um gráfico padrão sobre ele.
    """

    # Devemos descobrir qual é o último arquivo de dados primeiro.
    arquivo_de_dados = "dados.txt"
    caract_divisor = ","

    # Vamos abri-lo e criar os arquivos

    valores_tempo = []
    valores_posicao = []
    valores_velocidade = []
    valores_altura = []
    with open(arquivo_de_dados, "r") as base:
        for linha in base:
            linha = linha.replace("\n", "")
            lista_de_dados = [float(numero) for numero in linha.split(
                caract_divisor
            )]

            valores_tempo.append(
                lista_de_dados[0]
            )
            valores_posicao.append(
                lista_de_dados[1]
            )
            valores_velocidade.append(
                lista_de_dados[2]
            )
            valores_altura.append(
                lista_de_dados[3]
            )

    pp.subplot(1, 3, 1)
    pp.plot(
        valores_tempo,
        valores_posicao
    )
    pp.xlabel("Tempo(s)")
    pp.ylabel("Posição(m)")
    pp.grid(True)

    pp.subplot(1, 3, 2)
    pp.plot(
        valores_tempo,
        valores_velocidade
    )
    pp.xlabel("Tempo(s)")
    pp.ylabel("Velocidade(m/s)")
    pp.grid(True)

    pp.subplot(1, 3, 3)
    pp.plot(
        valores_tempo,
        valores_altura
    )
    pp.xlabel("Tempo(s)")
    pp.ylabel("Altura Líquido(m)")
    pp.grid(True)
    pp.show()


if __name__ == '__main__':
    gerando_grafico()
