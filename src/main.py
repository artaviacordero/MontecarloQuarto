"""
Integrantes del equipo:
Daniel Artavia
Paula Monge
Samantha Romero

Observaciones:
Con 0.25 segundos y 0.75 se le puede ganar a la IA.
Con 1.5 segundos no le logramos ganar en 10 intentos.
El factor de explotación no se modificó y se mantuvo en 0.5
"""

from simulation.mcts import mcts
from game.window import mainWindow

def main():
    x = mainWindow(aiAction=mcts)
