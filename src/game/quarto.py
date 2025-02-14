# -*- coding: utf-8 -*-

import copy
import enum
import numpy as np
import random

### Piece properties
class Properties(enum.IntFlag):
    DARK = 0x1
    LIGHT = 0x2
    SHORT = 0x4
    TALL = 0x8
    HOLLOW = 0x10
    FLAT = 0x20
    CIRCLE = 0x40
    SQUARE = 0x80

### Game phases
class QuartoPhase(enum.IntEnum):
    CHOOSE_PIECE = 1
    CHOOSE_SPACE = 2
    FINISHED = 3
    
### Game class
class Quarto():
    def __init__(self):
        self.reset()
    
    def copy(self):
        new_state = copy.copy(self)
        new_state.pieces = copy.copy(self.pieces)
        new_state.spaces = copy.copy(self.spaces)
        new_state.board = self.board.copy()
        return new_state
    
    def reset(self):
        self.pieces = []
        self.spaces = [(i,j) for i in range(4) for j in range(4)]
        for i in range(16):
            piece = (Properties.LIGHT if i&0x1 else Properties.DARK) \
                | (Properties.TALL if i&0x2 else Properties.SHORT) \
                | (Properties.FLAT if i&0x4 else Properties.HOLLOW) \
                | (Properties.SQUARE if i&0x8 else Properties.CIRCLE)
            self.pieces.append(piece)
        self.board = np.zeros((4,4),dtype=np.uint8)
        self.phase = QuartoPhase.CHOOSE_PIECE
        self.player = int(random.random()*2)
        self.chosen_piece = None
        self.winner = -1
        
    def turn_player(self):
        return self.player==0
    
    def turn_ai(self):
        return self.player==1
        
    def has_finished(self):
        return self.phase == QuartoPhase.FINISHED
    
    def get_winner(self):
        return self.winner
    
    def get_available_actions(self):
        if self.phase == QuartoPhase.CHOOSE_PIECE:
            return self.pieces
        elif self.phase == QuartoPhase.CHOOSE_SPACE:
            return self.spaces
        return []
    
    def do_action(self, action):
        new_state = self
        if self.phase == QuartoPhase.CHOOSE_PIECE:
            if not action in self.pieces: return self
            new_state = copy.copy(self)
            new_state.pieces = [piece for piece in self.pieces if piece!=action]
            new_state.phase = QuartoPhase.CHOOSE_SPACE
            new_state.player = (new_state.player + 1)%2
            new_state.chosen_piece = action
        elif self.phase == QuartoPhase.CHOOSE_SPACE:
            if not action in self.spaces: return self
            new_state = copy.copy(self)
            new_state.board = self.board.copy()
            new_state.spaces = [space for space in self.spaces if space!=action]
            new_state.phase = QuartoPhase.CHOOSE_PIECE
            new_state.board[action] = new_state.chosen_piece
            new_state.chosen_piece = None
            new_state._check_victory()
        return new_state

    def _check_victory(self):
        fin = np.any(np.bitwise_and.reduce(self.board, axis=0)) or \
                np.any(np.bitwise_and.reduce(self.board, axis=1)) or \
                ((self.board[0,0] & self.board[1,1] & self.board[2,2] & self.board[3,3]) > 0) or \
                ((self.board[3,0] & self.board[2,1] & self.board[1,2] & self.board[0,3]) > 0)
        if fin:
            self.winner = self.player
            self.phase = QuartoPhase.FINISHED
        elif (len(self.pieces)==0 and self.chosen_piece==None):
            self.phase = QuartoPhase.FINISHED
    
    def __hash__(self) -> int:
        return hash(self.board.tobytes())
