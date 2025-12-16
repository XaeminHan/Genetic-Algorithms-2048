import pygame
import numpy as np
import sys
import os
from player import Player
from constants import *
from main import draw_board, draw_ui, draw_neural_network

# 지정한 모델 보기
def main_watch(model_path):

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"Watching Model: {os.path.basename(model_path)}")
    clock = pygame.time.Clock()
    
    player = Player()
    
    if not os.path.exists(model_path):
        print(f"오류: {model_path} 파일을 찾을 수 없습니다.")
        return
        
    try:
        weights = np.load(model_path, allow_pickle=True)
        player.brain.weights = weights
        print(f"--- {model_path} 뇌 로드 성공 ---")
    except Exception as e:
        print(f"뇌 로드 실패: {e}")
        return

    class FakePop:
        generation = "WATCH"

        best_fitness = 0
        
        current_individual = 0
        size = 1
        players = [player]

    pop = FakePop()

    running = True
    while running and not player.game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        player.move()

        screen.fill(BLACK)
        
        draw_board(screen, player.game.board)
        draw_ui(screen, pop)

        vision = player.game.get_state()
        decision = player.think()
        actual_move = np.argmax(decision)
        
        draw_neural_network(screen, player.brain, vision, decision, actual_move)
        
        pygame.display.flip()
        clock.tick(10)

    print(f"--- 관전 종료 ---")
    print(f"최종 점수: {player.game.score}")
    
    pygame.time.wait(1000)
    pygame.quit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("사용법: python watch_model.py [모델 파일 경로]")
    else:
        model_file_path = sys.argv[1]
        main_watch(model_file_path)