from dataclasses import dataclass
from random import randint, choice

@dataclass
class Jogador:
    numero: int

    def __repr__(self):
        return f"Jogador {self.numero}"


@dataclass
class Partida:
    jogador1: Jogador
    jogador2: Jogador

    vencedor: Jogador = None

    def __repr__(self):
        if self.vencedor:
            return f"{self.jogador1} x {self.jogador2} -> {self.vencedor}"
        else:
            return f"{self.jogador1} x {self.jogador2}"


def sorteio(sacola_de_sorteio):

    partidas = []

    while True:
        i = choice(range(len(sacola_de_sorteio)))
        j1 = sacola_de_sorteio.pop(i)

        i = choice(range(len(sacola_de_sorteio)))
        j2 = sacola_de_sorteio.pop(i)

        partidas.append(Partida(j1, j2))

        if not sacola_de_sorteio:
            break

    return partidas

def sorteando_as_partidas_da_primeira_rodada(times):

    n_div, resto = divmod(len(times), 2)
    sacola_de_sorteio = times.copy()

    n_times_ativos = 2 * n_div

    if resto:
        i = randint(0, n_times_ativos - 1)
        time_de_fora = sacola_de_sorteio.pop(i) # não é eficiente

    partidas = sorteio(sacola_de_sorteio)

    # o time que sobra fica com ele mesmo, logo ele ganha a partida
    if resto:
        partidas.append(Partida(time_de_fora, time_de_fora))

    return partidas

def proxima_rodada(partidas):

    n_div, resto = divmod(len(partidas), 2)
    sacola_de_sorteio = [p.vencedor for p in partidas]
    n_times_ativos = 2 * n_div

    if resto:
        i = randint(0, n_times_ativos - 1)
        time_de_fora = sacola_de_sorteio.pop(i) # não é eficiente

    partidas_novas = sorteio(sacola_de_sorteio)

    # o time que sobra fica com ele mesmo, logo ele ganha a partida
    if resto:
        partidas_novas.append(Partida(time_de_fora, time_de_fora))

    return partidas_novas

def informando_os_vencedores_da_rodada(partidas: list[Partida]) -> None:
    for p in partidas:
        i = randint(1, 2)
        p.vencedor = getattr(p, f"jogador{i}")


N_COMPETIDORES = 3

if __name__ == "__main__":

    times = [Jogador(i) for i in range(1, N_COMPETIDORES + 1)]

    historico = []

    # rodada 1
    partidas = sorteando_as_partidas_da_primeira_rodada(times)

    print("*"*40)
    print(f"Primeira rodada: {partidas}")
    print("*"*40)

    while True:

        # Informando os resultados
        informando_os_vencedores_da_rodada(partidas)

        print()
        print("*"*40)
        print(f"Vencedores: {partidas}")
        print("*"*40)

        if len(partidas) == 1:
            historico.append(partidas)
            vencedor = partidas[0].vencedor
            break

        # nova rodada
        novas_partidas = proxima_rodada(partidas)
        historico.append(partidas)
        partidas = novas_partidas

        print()
        print("*"*40)
        print(f"Nova rodada: {partidas}")
        print("*"*40)

    print()
    print("*"*40)
    print(f"O time foi {vencedor} Vencedor!!!")
    print("*"*40)

    print("Histório de partidas")
    for rodada, h in enumerate(historico, start=1):
        print("*"*40)
        print(f"{rodada=} {h}")
        print("*"*40)
