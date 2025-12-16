from player import Player
import random
import os
import numpy as np
import json
import time 
from constants import MUTATION_RATE

class Population:
    # 생성
    def __init__(self, size):
        self.size = size
        self.players = []
        self.fitness_sum = 0
        self.generation = 1
        self.best_fitness = 0
        self.current_individual = 0

        # 세대별 임시 저장
        self.population_dir = "population_brains"
        self.stats_file = os.path.join(self.population_dir, "population_stats.json")

        # 신기록 모델 저장
        self.saved_models_dir = "saved_models"
        if not os.path.exists(self.saved_models_dir):
            os.makedirs(self.saved_models_dir)

        self.mutation_rate = MUTATION_RATE

        self.load_population()
    
    # 이전 세대 데이터 불러오기
    def load_population(self):
        os.makedirs(self.population_dir, exist_ok=True)
        
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, "r") as f:
                    stats = json.load(f)
                    self.generation = stats.get("generation", 1)
                    # 전 세대를 통틀어 가장 높은 적합도
                    self.best_fitness = stats.get("best_fitness", 0)
                print(f"--- 통계 로드 성공, (세대: {self.generation}, 최고 적합도: {self.best_fitness}) ---")
            except Exception as e:
                print(f"통계 로드 실패: {e}")
        # 아니면 처음부터 시작
        else:
            print("--- 통계 파일 없음. 1세대부터 시작. ---")

        self.players = []
        loaded_count = 0

        # 가중치 복사 하여 넣어주기
        for i in range(self.size):
            player = Player()
            brain_path = os.path.join(self.population_dir, f"indv_{i}.npy")
            if os.path.exists(brain_path):
                try:
                    player.brain.weights = np.load(brain_path, allow_pickle=True)
                    loaded_count += 1
                except Exception as e:
                    print(f"{brain_path} 로드 실패: {e}")
            self.players.append(player)

        if loaded_count > 0:
            print(f"--- {loaded_count}개의 뇌 로드 완료. ---")
        else:
            print("--- 저장된 뇌 없음, 무작위 뇌로 시작. ---")

    # 가중치 저장 
    def save_population(self):
        # dir 있으면 그냥 넘어가기
        os.makedirs(self.population_dir, exist_ok=True)
        saved_count = 0
        for i, player in enumerate(self.players):
            brain_path = os.path.join(self.population_dir, f"indv_{i}.npy")
            try:
                # 가중치 저장 ( 다른 크기의 행렬 구조가 4개여서 복잡한 객체 저장을 위해 allow_pickl 사용)
                np.save(brain_path, np.array(player.brain.weights, dtype=object), allow_pickle=True)
                saved_count += 1
            except Exception as e:
                print(f"indv_{i} 뇌 저장 실패: {e}")
        print(f"--- {saved_count}/{self.size}개 인구 뇌 저장 완료. ---")

    # population.json에 세대와 최고 적합도 저장
    def save_stats(self):
        stats = {
            "generation": int(self.generation),
            "best_fitness": int(self.best_fitness)
        }
        try:
            with open(self.stats_file, "w") as f:
                json.dump(stats, f, indent=4)
            print(f"--- 통계 저장 완료 (세대: {self.generation}) ---")
        except Exception as e:
            print(f"통계 파일 저장 실패: {e}")

    # 모델 저장
    def save_designated_model(self, player):
        try:
            fitness = int(player.fitness if player.fitness > 0 else player.game.score)
            timestamp = int(time.time())
            filename = os.path.join(
                self.saved_models_dir,
                f"gen_{self.generation}_score_{fitness}_{timestamp}.npy"
            )
            np.save(filename, np.array(player.brain.weights, dtype=object), allow_pickle=True)
            print(f"\n--- 모델 지정 저장 완료: {filename} ---")
        except Exception as e:
            print(f"모델 지정 저장 실패: {e}")

    # 현재 순번 움직이도록
    def update(self):
        if self.current_individual < self.size:
            self.players[self.current_individual].move()

    # 전체 끝났는지 확인
    def done(self):
        if self.current_individual < self.size:
            return self.players[self.current_individual].game.game_over
        return True

    # 적합도 계산
    def calculate_fitness(self):
        for player in self.players:
            player.calculate_fitness()

    # 자연선택 
    def natural_selection(self):
        print(f"\n--- {self.generation}세대 종료. 자연선택 시작... ---")
        self.calculate_fitness()
        # AI 중 가장 높은 적합도 구하기
        current_gen_best = max(self.players, key=lambda p: p.fitness)

        # 적합도가 더 높으면 모델을 자동 기록
        if current_gen_best.fitness > self.best_fitness:
            self.best_fitness = current_gen_best.fitness
            print(f"--- 새로운 역대 최고 적합도: {self.best_fitness} ---")
            print(f" 새로운 최고 기록 달성, 모델 saved_models/ 폴더에 저장됨")
            self.save_designated_model(current_gen_best)

        # 적합도 다 더해주기
        self.fitness_sum = sum(p.fitness for p in self.players)
        new_players = []

        # 1등은 예외로 복제해서 가지고 있기
        best_player_clone = max(self.players, key=lambda p: p.fitness).clone()
        new_players.append(best_player_clone)

        # 1등 제외하고 돌리기
        for _ in range(1, self.size):
            # 부모 1, 2 룰렛으로 뽑기기
            parent1 = self.select_parent()
            parent2 = self.select_parent()

            # 부모1과 2를 교배
            child = parent1.crossover(parent2)
            # 자식에 변이를 확률적으로 줌
            child.mutate(self.mutation_rate)
            new_players.append(child)

        # 다음세대를 위해
        self.players = new_players
        self.generation += 1
        self.current_individual = 0

        self.save_population()
        self.save_stats()

        print(f"--- {self.generation}세대 시작 ---")


    # 룰렛 : 다 더한 적합도에서 랜덤으로 하나를 뽑고 그에 해당하는 점수에 가면 그게 뽑힌거임.
    # 그래서 적합도가 높을수록 뽑힐 확률이 높아짐
    def select_parent(self):
        if self.fitness_sum == 0:
            return random.choice(self.players)

        rand = random.uniform(0, self.fitness_sum)
        running_sum = 0
        for player in self.players:
            running_sum += player.fitness
            if running_sum > rand:
                return player
        return self.players[0]