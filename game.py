import random
import copy

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        """게임을 초기 상태로 리셋합니다."""
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.moves = 0
        self.game_over = False
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        """보드의 빈 공간에 새로운 타일(2 또는 4)을 추가합니다."""
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def get_state(self):
        """신경망의 입력으로 사용될 현재 게임 보드 상태를 반환합니다."""
        state = []
        for i in range(4):
            for j in range(4):
                state.append(self.board[i][j])
        return state

    def move(self, direction):
        """주어진 방향으로 보드를 이동합니다. (0:Up, 1:Down, 2:Left, 3:Right)"""
        original_board = [row[:] for row in self.board]
        
        if direction == 0: # UP
            self.board = self.transpose(self.board)
            self.board, _ = self.compress(self.board)
            self.board, score_add = self.merge(self.board)
            self.board, _ = self.compress(self.board)
            self.board = self.transpose(self.board)
        elif direction == 1: # DOWN
            self.board = self.transpose(self.board)
            self.board = self.reverse(self.board)
            self.board, _ = self.compress(self.board)
            self.board, score_add = self.merge(self.board)
            self.board, _ = self.compress(self.board)
            self.board = self.reverse(self.board)
            self.board = self.transpose(self.board)
        elif direction == 2: # LEFT
            self.board, _ = self.compress(self.board)
            self.board, score_add = self.merge(self.board)
            self.board, _ = self.compress(self.board)
        elif direction == 3: # RIGHT
            self.board = self.reverse(self.board)
            self.board, _ = self.compress(self.board)
            self.board, score_add = self.merge(self.board)
            self.board, _ = self.compress(self.board)
            self.board = self.reverse(self.board)
        else:
            return False

        self.score += score_add
        moved = (self.board != original_board)
        if moved:
            self.moves += 1
            self.add_new_tile()
            if self.check_game_over():
                self.game_over = True
        
        return moved
        
    def check_game_over(self):
        """게임 오버 상태인지 확인합니다."""
        for i in range(4):
            # 4가지 방향으로 이동을 시도해보고, 모두 이동이 불가능하면 게임 오버
            temp_board_check = [row[:] for row in self.board]
            if self.move_possible(temp_board_check, i):
                return False
        return True

    def move_possible(self, board, direction):
        """임시 보드에서 이동이 가능한지 확인합니다."""
        original = [row[:] for row in self.board]
        
        if direction == 0: # UP
            board = self.transpose(board)
            board, _ = self.compress(board)
            board, _ = self.merge(board)
            board, _ = self.compress(board)
            board = self.transpose(board)
        elif direction == 1: # DOWN
            board = self.transpose(board)
            board = self.reverse(board)
            board, _ = self.compress(board)
            board, _ = self.merge(board)
            board, _ = self.compress(board)
            board = self.reverse(board)
            board = self.transpose(board)
        elif direction == 2: # LEFT
            board, _ = self.compress(board)
            board, _ = self.merge(board)
            board, _ = self.compress(board)
        elif direction == 3: # RIGHT
            board = self.reverse(board)
            board, _ = self.compress(board)
            board, _ = self.merge(board)
            board, _ = self.compress(board)
            board = self.reverse(board)
        
        return board != original

    # 보드 조작 헬퍼 함수들
    def compress(self, board):
        new_board = [[0]*4 for _ in range(4)]
        score_add = 0
        for i in range(4):
            pos = 0
            for j in range(4):
                if board[i][j] != 0:
                    new_board[i][pos] = board[i][j]
                    pos += 1
        return new_board, score_add

    def merge(self, board):
        score_add = 0
        for i in range(4):
            for j in range(3):
                if board[i][j] == board[i][j+1] and board[i][j] != 0:
                    board[i][j] *= 2
                    board[i][j+1] = 0
                    score_add += board[i][j]
        return board, score_add
        
    def reverse(self, board):
        new_board = []
        for i in range(4):
            new_board.append(board[i][::-1])
        return new_board

    def transpose(self, board):
        new_board = [[0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_board[i][j] = board[j][i]
        return new_board