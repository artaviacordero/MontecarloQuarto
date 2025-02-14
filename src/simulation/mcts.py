import random
import time

from game.quarto import Quarto
from simulation.node import Node

class MCTS:
    def __init__(self, root:Quarto) -> None:
        self.child_number = 0
        self.visited = {}
        self.root = Node(root)
    
    def search(self, time_limit:float, exploitation:float):
        end = time.time() + time_limit
        # Iterait while there's time remaining
        while time.time() < end:
            self.iteration(exploitation)
        # Return the best action for the AI
        return self.best_action()

    def best_action(self):
        self.root.best_child().action

    def iteration(self, exploitation:float) -> None:
        current_node = self.root
        # List of visited nodes to get to a final state
        path = [current_node]

        while not current_node.final:
            # Explore if the random number is greater than the exploitation factor
            explore = random.random() > exploitation
            
            # If the node has been visited and the random number is less than the exploitation factor
            if len(current_node.children) > 0 and not explore:
                # Exploit
                current_node = current_node.best_child()
            # If the node has not been visited or the explore factor is bigger than the exploitation factor
            else:
                # Explore
                # Get an action from the available actions
                available_actions = current_node.get_available_actions()
                action = random.choice(available_actions)
                # A state is defined by the board state and the picked piece
                key = (hash(current_node), action)
                new_state = current_node.state.do_action(action)
                new_node = Node(new_state, action, current_node)
                # Add the node to the tree if it has not been visited before
                # Otherwise, continue from the previously visited node
                if key in self.visited:
                    current_node = self.visited[key]
                else:
                    self.visited[key] = new_node
                    current_node.children.append(new_node)
                    current_node = new_node
            # Add the node to the path
            path.append(current_node)

        score = current_node.state.get_winner()
        for node in path:
            # Always increase the visit count
            node.visits += 1
            # Increase the score if it is the AI's turn and the AI wins
            if node.state.turn_ai() and score == 1:
                node.score += 1
            # Increase the score if it is the human's turn and the human wins
            elif node.state.turn_player() and score == 0:
                node.score += 1
            

def mcts(root:Quarto, time_limit:float=1.5, exploitation:float=0.5):
    tree = MCTS(root)
    action = tree.search(time_limit, exploitation)
    return action
