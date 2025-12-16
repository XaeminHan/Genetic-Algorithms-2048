from game import Game
from neural_net import NeuralNet
import numpy as np

class Player:
    def __init__(self):
        self.game = Game()
        self.fitness = 0
        self.brain = NeuralNet(16, 64, 4, 2)
        # 목숨 3개
        self.lives = 3         
        # 점수 변화 x 시 
        self.starvation_counter = 0
        self.prev_score = 0
        # 잘못된 행동에 대한 누적 패널티 (move()에서 증가)
        self.penalty = 0

    # 움직임 계산
    def think(self):
        state = self.game.get_state()
        normalized_state = [np.log2(x) if x > 0 else 0 for x in state]
        
        decision = self.brain.predict(normalized_state)
        return decision

    # 움직임 기록
    def move(self):
        if not self.game.game_over:
            decision = self.think()
            
            sorted_moves = np.argsort(decision)[::-1]

            best_choice = sorted_moves[0]
            
            if not self.game.move_possible(self.game.board, best_choice):
                # 목숨 차감
                self.lives -= 1
                
                # fitness에 직접 차감하지 x
                self.penalty += 50
                
                # 목숨을 다 썼으면 바로 사망
                if self.lives <= 0:
                    self.game.game_over = True
                    return # 함수 종료

            moved = False
            for move_choice in sorted_moves:
                if self.game.move(move_choice):
                    moved = True
                    break
            
            # 어디로도 못 가면 게임 오버
            if not moved:
                self.game.game_over = True
                return

            # 점수 변동 없으면 카운트
            if self.game.score > self.prev_score:
                self.starvation_counter = 0
            else:
                self.starvation_counter += 1
            
            self.prev_score = self.game.score

            if self.starvation_counter > 50:
                self.game.game_over = True

    # 적합도 계산
    def calculate_fitness(self):
        board = np.array(self.game.board)
        
        # 기본 점수
        fitness = self.game.score - self.penalty
        
        # 큰 타일 보너스
        max_tile = np.max(board)
        max_pos = np.unravel_index(np.argmax(board), board.shape)
        is_corner = (max_pos[0] == 0 or max_pos[0] == 3) and (max_pos[1] == 0 or max_pos[1] == 3)
        
        if is_corner:
            fitness += (max_tile * 2) # 구석에 큰 거 있으면 보너스

        self.fitness = max(1, fitness)
    
    def clone(self):
        clone = Player()
        clone.brain = self.brain.clone()
        return clone

    def crossover(self, parent):
        child = Player()
        child.brain = self.brain.crossover(parent.brain)
        return child

    def mutate(self, mutation_rate):
        self.brain.mutate(mutation_rate)