import pygame
import numpy as np
from population import Population
from constants import *
import os
import sys

# 보드판 그리기 4X4
def draw_board(screen, board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            color = TILE_COLORS.get(value, TILE_COLORS[8192])
            rect_x = BOARD_X + j * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
            rect_y = BOARD_Y + i * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
            pygame.draw.rect(screen, color, (rect_x, rect_y, TILE_SIZE, TILE_SIZE), border_radius=5)

            if value != 0:
                text_color = BLACK if value < 8 else WHITE
                text = TILE_FONT.render(str(value), True, text_color)
                text_rect = text.get_rect(center=(rect_x + TILE_SIZE / 2, rect_y + TILE_SIZE / 2))
                screen.blit(text, text_rect)

# 정보창 그리기
def draw_ui(screen, pop):
    GOLD = (255, 215, 0)
    all_time_text = UI_FONT.render(f"ALL TIME BEST: {int(pop.best_fitness)}", True, GOLD)
    screen.blit(all_time_text, (20, 20))
    gen_text = UI_FONT.render(f"Generation: {pop.generation}", True, WHITE)
    screen.blit(gen_text, (20, 60))
    player_text = UI_FONT.render(f"Player: {pop.current_individual + 1}/{pop.size}", True, WHITE)
    screen.blit(player_text, (20, 100))
    if pop.current_individual < pop.size:
        current_score = pop.players[pop.current_individual].game.score
        score_text = UI_FONT.render(f"Current Score: {current_score}", True, WHITE)
        screen.blit(score_text, (20, 140))

# 뉴럴 네트워크 그리기
def draw_neural_network(screen, brain, vision, decision, actual_move):
    
    x, y, w, h = NN_X, NN_Y, NN_WIDTH, NN_HEIGHT
    layers = [brain.i_nodes] + [brain.h_nodes] * brain.h_layers + [brain.o_nodes]
    max_nodes = max(layers)
    node_size = min(20, h / (max_nodes * 1.5))
    layer_spacing = w / (len(layers) - 1)

    node_positions = []
    all_activations = brain.activations
    max_activations = []
    
    if all_activations:
        for act_layer in all_activations:
            if len(act_layer) > 0:
                max_val = np.max(act_layer)
                max_activations.append(max_val if max_val > 0 else 1.0)
            else:
                max_activations.append(1.0)

    # 노드 위치 계산 및 그리기
    for i, num_nodes in enumerate(layers):
        layer_x = x + i * layer_spacing
        v_spacing = h / (num_nodes + 1)
        layer_nodes = []
        
        current_layer_activations = []
        if all_activations and i < len(all_activations):
            current_layer_activations = all_activations[i]

        for j in range(num_nodes):
            node_y = y + (j + 1) * v_spacing
            layer_nodes.append((layer_x, node_y))
            color = WHITE
            
            if i == 0: # 입력층
                tile_value = vision[j]
                if tile_value > 0:
                    normalized_value = np.log2(tile_value)
                    max_log_val = 11.0 
                    scale_factor = max(0.1, min(normalized_value / max_log_val, 1.0))
                    green_value = int(50 + (205 * scale_factor))
                    color = (0, max(50, min(255, green_value)), 0)
                else:
                    color = WHITE
            
            elif i == len(layers) - 1: # 출력층
                if actual_move is not None and j == actual_move: 
                    color = GREEN
            
            elif i > 0 and i < len(layers) - 1: # 은닉층
                if j < len(current_layer_activations):
                    activation_value = current_layer_activations[j]
                    if activation_value > 0:
                        max_val_in_layer = max_activations[i]
                        scale_factor = max(0.1, min(activation_value / max_val_in_layer, 1.0))
                        green_value = int(50 + (205 * scale_factor))
                        color = (0, max(50, min(255, green_value)), 0) # 값이 있음
                    else:
                        color = WHITE
            
            pygame.draw.circle(screen, color, (layer_x, node_y), node_size)
            pygame.draw.circle(screen, BLACK, (layer_x, node_y), node_size, 1)

        node_positions.append(layer_nodes)

    # 가중치 
    for i in range(len(brain.weights)):
        prev_layer_nodes = node_positions[i]
        curr_layer_nodes = node_positions[i+1]
        weights = brain.weights[i]
        for r in range(weights.shape[0]):
            for c in range(weights.shape[1] - 1):
                weight_val = weights[r, c]
                # 가중치가 양수면 blue 음수면 red
                color = BLUE if weight_val > 0 else RED
                start_pos = prev_layer_nodes[c]
                end_pos = curr_layer_nodes[r]
                line_width = min(5, int(abs(weight_val) * 2))
                if line_width > 0:
                    pygame.draw.line(screen, color, start_pos, end_pos, line_width)

    # (출력층 레이블 로직은 동일)
    output_labels = ["Up", "Down", "Left", "Right"]
    for i, pos in enumerate(node_positions[-1]):
        label_text = NN_FONT.render(output_labels[i], True, WHITE)
        screen.blit(label_text, (pos[0] + node_size * 1.5, pos[1] - node_size/2))

def main():
    show_mode = "show" in sys.argv
    
    screen = None
    
    if show_mode:
        pygame.init()
        pygame.font.init() # 폰트 초기화
        
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2048 AI (Sequential - Show Mode)")
    else:
        print("--- 빠른 학습 모드로 실행 ---")

    clock = pygame.time.Clock()
    FPS = 60 if show_mode else 10000

    pop = Population(POPULATION_SIZE)

    running = True
    while running:
        
        if show_mode:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_s:
                        if pop.current_individual < pop.size:
                            player_to_save = pop.players[pop.current_individual]
                            pop.save_designated_model(player_to_save)

        if pop.current_individual < pop.size:
            if not pop.done():
                pop.update()
            else:
                if not show_mode:
                    current_player = pop.players[pop.current_individual]
                    current_player.calculate_fitness() 
                    score = current_player.game.score
                    fitness = current_player.fitness
                    log_msg = f"  Gen {pop.generation} | Player {pop.current_individual + 1:>3}/{pop.size} | Score: {score:<5} | Fitness: {int(fitness)}"
                    print(log_msg)
                
                pop.current_individual += 1
        
        else:
            pop.natural_selection()
        
        if show_mode:
            screen.fill(BLACK)
            
            if pop.current_individual < pop.size:
                player_to_draw = pop.players[pop.current_individual]
                draw_board(screen, player_to_draw.game.board)
                draw_ui(screen, pop)
                vision = player_to_draw.game.get_state()
                decision = player_to_draw.think()
                actual_move = np.argmax(decision)
                draw_neural_network(screen, player_to_draw.brain, vision, decision, actual_move)
            
            pygame.display.flip()

        clock.tick(FPS)

    if show_mode:
        pygame.quit()
    else:
        print("\n--- 학습 종료 ---")

if __name__ == '__main__':
    main()