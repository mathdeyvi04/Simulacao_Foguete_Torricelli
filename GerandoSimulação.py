import pygame as pyg


def dicas_de_quadros(
        lista_de_textos,
        fonte,
        fps: int
):
    """
    Descrição:
        Função responsável por criar e apresentar os textos
        relativos à taxa de quadros
    """

    textos = (
        f"FPS: {fps}",
        "Q - Diminuir",
        "E - Aumentar"
    )
    posy = 0
    for frase in textos:
        texto = fonte.render(
            frase,
            True,
            (255, 255, 255)
        )
        pos = texto.get_rect(
            topleft=(0, posy)
        )
        lista_de_textos.append(
            [
                texto,
                pos
            ]
        )

        posy += 15


def desenhando_nosso_cenario(
        janela,
        comp,
        alt,
        escala,
        dados,
        index,
        img_estrada,
        estradas,
        img_propulsao
):
    """
    Descrição:
        Função responsável por apresentar toda a simulação.
    """

    # Há o fixo, que é nosso foguete safinho.
    pos_inicial = 40
    comprimento = 14
    pady = 50
    espessura = 2
    escalador = 5

    def desenhando_reservatorio():
        # |<-
        pyg.draw.line(
            janela,
            (255, 255, 255),
            (
                pos_inicial,
                alt - pady
            ),
            (
                pos_inicial,
                alt - pady - dados[2][0] * escala * escalador
            ),
            espessura
        )
        #  ->|
        pyg.draw.line(
            janela,
            (255, 255, 255),
            (
                pos_inicial + comprimento * escalador,
                alt - pady
            ),
            (
                pos_inicial + comprimento * escalador,
                alt - pady - dados[2][0] * escala * escalador
            ),
            espessura
        )
        # _
        pyg.draw.line(
            janela,
            (255, 255, 255),
            (
                pos_inicial,
                alt - pady
            ),
            (
                pos_inicial + comprimento * escalador,
                alt - pady
            ),
            espessura
        )

    desenhando_reservatorio()

    # Devemos desenhar o retângulo de líquido
    def desenhando_liquido():

        if dados[2][index] == 0:
            return None

        pyg.draw.rect(
            janela,
            (110, 233, 240),
            pyg.Rect(
                (pos_inicial + espessura, alt - pady - dados[2][index] * escala * escalador),
                (comprimento * escalador - espessura, dados[2][index] * escala * escalador + espessura / 2)
            )
        )

    desenhando_liquido()

    # Devemos desenhar a animação de propulsão
    def desenhando_propulsao():

        try:
            if dados[2][index] == 0:
                # Vamos considerar sem mais propulsão
                return None

            janela.blit(
                img_propulsao,
                img_propulsao.get_rect(
                    bottomright=(40, alt - pady + 15)
                )
            )
        except IndexError:
            pass

    desenhando_propulsao()

    # Dependendo da velocidade, devemos mudar a estrada!
    def movimentando():

        if index == 0:
            return 0

        try:
            # Devemos movimentar o foguete um dx e diminuir na estrada
            dx_percorrido = dados[1][index] - dados[1][index - 1]

            for i in (0, 1):
                estradas[i].x = estradas[i].x - dx_percorrido * 10000

                if estradas[i].x < (-comp):
                    estradas[i].x = comp

        except IndexError:
            pass

    movimentando()


def apresentando_dados(
        fonte,
        matriz_dados,
        index,
        comprimento
):
    lista_de_dados = []

    # Instante
    texto1 = fonte.render(
        f"Instante: {matriz_dados[0][index]} s",
        True,
        (255, 255, 255)
    )
    pos1 = texto1.get_rect(
        topright=(comprimento, 0)
    )
    lista_de_dados.append(
        (
            texto1,
            pos1
        )
    )

    try:
        vel = (matriz_dados[1][index] - matriz_dados[1][index - 1]) / (matriz_dados[0][index] - matriz_dados[0][index - 1])

        texto2 = fonte.render(
            f"Velocidade: {vel:.2f} m/s",
            True,
            (255, 255, 255)
        )
        pos2 = texto2.get_rect(
            topright=(comprimento, 20)
        )
        lista_de_dados.append(
            (
                texto2,
                pos2
            )
        )
    except ZeroDivisionError:
        # Evitar o inicio
        pass

    texto3 = fonte.render(
        f"Altura Combustível: {matriz_dados[2][index]: .2f} m",
        True,
        (255, 255, 255)
    )
    pos3 = texto3.get_rect(
        topright=(comprimento, 40)
    )
    lista_de_dados.append(
        (
            texto3,
            pos3
        )
    )

    return lista_de_dados


def gerando_visual(
        dados,
        fps: int = 30
):
    """
    Descrição:
        Função responsável por ler os dados e criar uma janela apresentando
        a simulação gráfica.
        Devemos nos preocupar em:
            * Possibilitar replay -> Chamar a função de apresentação recursivamente
            * Controle de velocidade da simulação -> Controlar velocidade do loop
            * Controle de Escala -> Tentar cartear tamanho dos objetos.

        ERRO_DE_IDEIA = Podemos tentar apresentar os gráficos e sua evolução no tempo
        Fica muito pau


    Parâmetros:
        dados -> matriz de 3 colunas sendo respectivamente t, x, h
    """

    # Criando janela
    pyg.init()
    comp, alt = 600, 400
    ESCALADOR = 5
    janela = pyg.display.set_mode((comp, alt))
    pyg.display.set_caption("Apresentando Simulação")
    relogio = pyg.time.Clock()
    pyg.font.init()
    fonte = pyg.font.SysFont("Arial", 15, True)

    textos_a_serem_inseridos = []

    dicas_de_quadros(textos_a_serem_inseridos, fonte, fps)

    dica_de_replay = fonte.render(
        "R - Replay",
        True,
        (255, 255, 255)
    )
    pos = dica_de_replay.get_rect(
        topleft=(
            0, 60
        )
    )
    textos_a_serem_inseridos.append(
        [
            dica_de_replay,
            pos
        ]
    )

    imagem_estrada = pyg.transform.scale(
        pyg.image.load(
            "estrada.png"
        ),
        (comp + 50, 80)
    )
    estradas = [
        imagem_estrada.get_rect(
            topleft=(0, alt - 80)
        ),
        imagem_estrada.get_rect(
            topleft=(comp, alt - 80)
        )
    ]
    imagem_prop = pyg.transform.scale(pyg.image.load(
        "propulsao.png"
    ),
        (40, 40)
    )

    index = 0
    while True:

        try:
            for evento in pyg.event.get():
                if evento.type == pyg.QUIT:
                    pyg.quit()

                elif evento.type == pyg.KEYDOWN:

                    if evento.key == pyg.K_q:
                        print("Diminuindo taxa de quadros")
                        fps = fps - 1

                        textos_a_serem_inseridos[0][0] = fonte.render(
                            f"FPS: {fps}",
                            True,
                            (255, 255, 255)
                        )

                    elif evento.key == pyg.K_e:
                        print("Aumentando taxa de quadros")
                        fps = fps + 1

                        textos_a_serem_inseridos[0][0] = fonte.render(
                            f"FPS: {fps}",
                            True,
                            (255, 255, 255)
                        )

                    elif evento.key == pyg.K_r:
                        pyg.quit()

                        gerando_visual(dados, fps)

            janela.fill(
                (0, 0, 0)
            )

            dados_sistema = apresentando_dados(
                fonte,
                dados,
                index,
                comp
            )

            for texto_dado, texto_pos in dados_sistema:
                janela.blit(
                    texto_dado,
                    texto_pos
                )

            for ret_est in estradas:
                janela.blit(
                    imagem_estrada,
                    ret_est
                )

            for texto, retangulo_do_texto in textos_a_serem_inseridos:
                janela.blit(
                    texto,
                    retangulo_do_texto
                )

            desenhando_nosso_cenario(
                janela,
                comp,
                alt,
                ESCALADOR,
                dados,
                index,
                imagem_estrada,
                estradas,
                imagem_prop
            )

            pyg.display.flip()
            relogio.tick(fps)

            index += 100

        except IndexError:
            pass


if __name__ == '__main__':
    # Vamos abrir o arquivo apenas uma vez
    informacoes = [[], [], []]
    with open("dados.txt", "r") as base:
        for linha in base:
            linha = linha.replace("\n", '')

            tripla_dados = linha.split(",")

            for indice in range(0, 3):
                informacoes[indice].append(float(tripla_dados[indice]))

    gerando_visual(informacoes)
