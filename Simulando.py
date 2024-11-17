from math import sqrt
from matplotlib import pyplot as pp

DELTA_TEMPO = 0.0001
GRAVIDADE = 9.81

# Constante do Sistema, mas não do foguete
Y = 0.1
u = 0.02

# Valores Característicos
A = GRAVIDADE * (2 * Y) / (1 - (Y * Y))


class Foguete:
    """Vamos criar nosso foguete e seus atributos"""

    def __init__(
            self,
            altura_inicial: float,
            b: float,
    ):
        self.altura = altura_inicial
        self.b = b

        if u != 0:
            # Devemos ter as condicionais
            if altura_inicial < (b / ((A / (u * GRAVIDADE)) - 1)):
                print("Altura Mínima do Reservatório não foi satisfeita.")
                exit(0)

            if Y < (sqrt(1 + (1 / (u * u))) - (1 / u)):
                print("Valor de Y inferior ao mínimo necessário para movimento.")
                exit(0)

        self.acel = 0
        self.vel = 0
        self.pos = 0

    def movimentando(self):
        self.vel = self.vel + self.acel * DELTA_TEMPO
        self.pos = self.pos + self.vel * DELTA_TEMPO + 0.5 * self.acel * DELTA_TEMPO * DELTA_TEMPO

    def derramando_liquido(self):
        if self.altura <= 0:
            self.altura = 0
        else:
            self.altura = self.altura - sqrt(A * Y * self.altura) * DELTA_TEMPO


def simular(
        corpo: Foguete
):
    """Vai simular e plotar talvez"""

    valores_tempo = []
    valores_altura = []
    valores_pos = []
    valores_vel = []
    valores_acel = []

    instante = 0
    while True:

        corpo.acel = A * (corpo.altura / (corpo.altura + corpo.b)) - GRAVIDADE * u

        corpo.derramando_liquido()

        corpo.movimentando()

        valores_tempo.append(
            instante
        )
        valores_pos.append(
            corpo.pos
        )
        valores_vel.append(
            corpo.vel
        )
        valores_acel.append(
            corpo.acel
        )
        valores_altura.append(
            corpo.altura
        )

        instante += DELTA_TEMPO

        if u == 0 and corpo.altura <= 0:
            # Então já que não há atrito, ele nunca chegaria a zero.
            # Devemos encerrar quando não houver mais líquido.
            break

        if corpo.vel <= 0:
            # Como há atrito, devemos encerrar quando não há mais nada
            # Afinal, desejamos saber o instante em que ele para.
            return instante

    # Vamos plotar agora
    pp.subplot(1, 3, 1)
    pp.plot(
        valores_tempo,
        valores_pos
    )
    pp.xlabel("Tempo(s)")
    pp.ylabel("Posição(m)")
    pp.grid(True)

    pp.subplot(1, 3, 2)
    pp.plot(
        valores_tempo,
        valores_vel
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



