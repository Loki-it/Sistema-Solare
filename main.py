import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random

abilita_buco_nero = False  # "True" attivi il buco nero "False" lo disattivi
velocita_tempo = 10  # Qui puoi cambiare la velocità della simulazione

pianeti = {
    'Mercurio': {'distance': 0.39, 'period': 88},
    'Venere': {'distance': 0.72, 'period': 225},
    'Terra': {'distance': 1.00, 'period': 365},
    'Marte': {'distance': 1.52, 'period': 687},
    'Giove': {'distance': 5.20, 'period': 4333},
    'Saturno': {'distance': 9.58, 'period': 10759},
    'Urano': {'distance': 19.22, 'period': 30687},
    'Nettuno': {'distance': 30.05, 'period': 60190}
}

colori = {
    'Mercurio': 'grey',
    'Venere': 'yellow',
    'Terra': 'blue',
    'Marte': 'red',
    'Giove': 'orange',
    'Saturno': 'gold',
    'Urano': 'lightblue',
    'Nettuno': 'darkblue'
}

# Funzioni
def calcola_posizione_realistica(dati_pianeta, giorni):
    periodo_orbitale = dati_pianeta['period']
    distanza_dal_sole = dati_pianeta['distance']
    angolo = (giorni / periodo_orbitale) * 2 * np.pi
    x = distanza_dal_sole * np.cos(angolo)
    y = distanza_dal_sole * np.sin(angolo)
    return x, y

def aggiorna_effetto_gravitazionale(posizione_pianeta, posizione_buco_nero, giorni_passati):
    direzione = np.array(posizione_buco_nero) - np.array(posizione_pianeta)
    distanza = np.linalg.norm(direzione)
    forza = 1 / distanza**2
    nuovo_x, nuovo_y = np.array(posizione_pianeta) + direzione / distanza * forza * 0.01
    return nuovo_x, nuovo_y

def aggiorna_dimensione_buco_nero(anni_passati):
    dimensione_base = 100
    aumento_dimensione_per_anno = 100
    nuova_dimensione = dimensione_base + aumento_dimensione_per_anno * (anni_passati // 1)
    return nuova_dimensione

def aggiorna(frame):
    global pianeti
    plt.cla()
    giorni_passati = frame * velocita_tempo
    anni_passati = giorni_passati / 365
    plt.title(f"Anno: {int(anni_passati)}")
    plt.scatter(0, 0, s=200, c='yellow', label='Sole')

    if abilita_buco_nero:
        dimensione_buco_nero = aggiorna_dimensione_buco_nero(anni_passati)
        plt.scatter(*posizione_buco_nero, s=dimensione_buco_nero, c='black', label='Buco Nero')

    for pianeta, dati in list(pianeti.items()):
        x, y = calcola_posizione_realistica(dati, giorni_passati)

        if abilita_buco_nero:
            x, y = aggiorna_effetto_gravitazionale((x, y), posizione_buco_nero, giorni_passati)
            if np.linalg.norm(np.array((x, y)) - np.array(posizione_buco_nero)) < dimensione_buco_nero / 2000:
                del pianeti[pianeta]
                continue

        plt.scatter(x, y, s=50, c=colori[pianeta], label=pianeta)
        plt.text(x, y, pianeta)
    plt.legend()
    plt.xlim(-35, 35)
    plt.ylim(-35, 35)
    plt.xlabel("Coordinate X (UA)")
    plt.ylabel("Coordinate Y (UA)")
    plt.grid(True)

def crea_buco_nero():
    x = random.uniform(-1.5, 1.5)
    y = random.uniform(-1.5, 1.5)
    return x, y

posizione_buco_nero = crea_buco_nero() if abilita_buco_nero else (None, None)

fig, ax = plt.subplots()
ani = FuncAnimation(fig, aggiorna, frames=range(1000), interval=100, repeat=True)

plt.show()
