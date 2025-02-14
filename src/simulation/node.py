from __future__ import annotations

from game.quarto import Quarto

class Node:
    def __init__(self, state:Quarto, action=None, parent:Node=None) -> None:
        self.state = state
        self.action = action
        self.parent = parent
        self.children = []
        self.available_actions = state.get_available_actions()
        self.final = state.has_finished()
        self.score = 0
        self.visits = 0

    def average(self) -> float:
        if self.visits == 0:
            return -1
        return self.score/self.visits

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def get_available_actions(self) -> list:
        return self.available_actions

    def best_child(self) -> Node:
        # Maximize if the next turn is for the AI.
        if self.children[0].state.turn_ai():
            return sorted(self.children, key=lambda c: c.average(), reverse=True)[0]
        # Minimize if the next turn is for the human
        return sorted(self.children, key=lambda c: c.average())[0]

    def __hash__(self) -> int:
        return hash(self.state.board.tobytes())
