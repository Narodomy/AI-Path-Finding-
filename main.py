import os
import pickle

import neat

from game.entities import *
from game.map import *
from game.map_data import *

# PYGAME
pygame.init()
pygame.display.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Level 1
pygame.display.set_caption("Hardest Game in the World! (level 1)")
map_surface = pygame.image.load('./game/resources/images/maps/level_1.png').convert_alpha()
WIDTH = 900
HEIGHT = 450

# Level 2
# pygame.display.set_caption("Hardest Game in the World! (level 2)")
# map_surface = pygame.image.load('./game/resources/images/maps/level_2.png').convert_alpha()
# WIDTH = 950
# HEIGHT = 375


# GAME
level = 1
final_map = False

# NEAT
GEN = 0
atw = 0


# DRAW WINDOW
def draw_window(win, balls, players, coins, area, level):
    title = 'Hardest Game in the World! (level {})'.format(level)
    source = './game/resources/images/maps/level_{}.png'.format(level)
    # if (next_map):
    pygame.display.set_caption(title)
    map_surface = pygame.image.load(source).convert_alpha()
    map_rect = map_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    win.fill(GROUND)
    win.blit(map_surface, map_rect)

    for b in balls:
        b.draw(win)

    coins.draw(win)

    for p in players:
        if p in players:
            p.draw(win)
            p.target_information(win, area, coins, True)

    # LEFT

    # Generation
    score_label = STAT_FONT.render("Gen: " + str(GEN - 1), 1, BLACK)
    win.blit(score_label, (30, 10))

    # Alive
    alive = ALIVE_FONT.render("alive: " + str(len(players)), 1, BLACK)
    win.blit(alive, (30, 40))

    # RIGHT

    # ATW
    atw_text = ATW_FONT.render("ATW: " + str(atw), 1, RED)
    win.blit(atw_text, ((WIDTH - 260, 40)))

    # Won
    counter_wins = WON_FONT.render("W: " + str(won), 1, BLACK)
    win.blit(counter_wins, (WIDTH - 170, 40))

    # Time
    time_text = TIME_FONT.render("T: " + str(time), 1, BLACK)
    win.blit(time_text, (WIDTH - 110, 40))

    pygame.display.flip()


def main(genomes, config):
    # NEAT
    global GEN
    global WIN_ON
    global time
    global time_max
    global won
    global atw

    # GAME
    global level
    global final_map
    GEN += 1
    WIN_ON = True
    time_max = 16
    won = 0

    # Game Setup
    map = level == 1 and MapLevel01() or MapLevel02()
    # Coins
    coins = map.coin

    # Area
    area = map.area

    # Lists
    balls = map.balls

    players = []
    nets = []
    ge = []

    # Load model
    with open('./models/pickle_square_model_3.pkl', 'rb') as file:
        clf = pickle.load(file)

    # NEAT
    for genomes_id, gnome in genomes:
        # net = neat.nn.FeedForwardNetwork.create(clf, config)
        net = neat.nn.FeedForwardNetwork.create(gnome, config)

        nets.append(net)
        player_on_map = Player()
        player_on_map.x = map.player_x
        player_on_map.y = map.player_y
        players.append(player_on_map)

        gnome.fitness = 0
        ge.append(gnome)

    if level == 2:
        final_map = True
        width = 950
        height = 375
        window = pygame.display.set_mode((width, height))
        draw_window(window, balls, players, coins, area, level)
        for p in players:
            p.x = map.player_x
            p.y = map.player_y

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    run = True
    # Main loop
    while run and len(players) > 0:
        if WIN_ON: clock.tick(FPS)

        # Time
        time = (pygame.time.get_ticks() - start_time) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
                break

        for b in balls:
            b.move()

        # Neural Network
        for x, player in enumerate(players):
            # Collisions
            player.collision_balls(balls)
            player.collision_walls(map)
            player.collision_win(area)
            player.collision_coins(coins)

            # Which balls will be provided to NN
            ball1_ind = 0
            ball2_ind = 1
            if len(players) > 0:
                for i in range(len(balls) - 1):
                    if player.x >= 716:
                        ball1_ind = len(balls) - 1
                        ball2_ind = len(balls) - 1
                    elif balls[i].x <= player.x <= balls[i + 1].x:
                        ball1_ind = i
                        ball2_ind = i + 1
            # Inputs NN
            outputs = nets[players.index(player)].activate(
                (
                    player.x, player.y,  # player position
                    player.target.x, player.target.y,  # Distance from player to target
                    balls[ball1_ind].x, balls[ball1_ind].y,  # ball closer to the left
                    balls[ball2_ind].x, balls[ball2_ind].y  # Distance from player to nearest ball 2
                )
            )

            # Movements based on output (up, down, right)
            if max(outputs) == outputs[0]:
                if outputs[0] > 0.5:
                    player.move_up()

            if max(outputs) == outputs[1]:
                if outputs[1] > 0.5:
                    player.move_down()

            if max(outputs) == outputs[2]:
                if outputs[2] > 0.5:
                    player.move_right()

            # Fitness

            # Maximum time
            if time >= time_max:
                remove_player(nets, ge, x, players, player, 0)

            # Collision with the balls
            if player.collided:
                remove_player(nets, ge, x, players, player, -2.5)

            # Pass the coin without picking it up
            if player.x >= coins.x and not player.coin:
                remove_player(nets, ge, x, players, player, -10)

            # Won:
            if player.win:
                if atw >= (len(players) * (3 / 4)):
                    if final_map :
                        remove_player(nets, ge, x, players, player, 99999999)
                    # else:
                    #     remove_player(nets, ge, x, players, player, 5000)
                    level = 2
                    # time = time_max
                    atw = 0
                    print("PLAYERS:{}".format(len(players)))
                else:
                    remove_player(nets, ge, x, players, player, 5000)
                    won += 1
                    atw += 1

            # Eliminates players who are in spawn after 3.5 seconds
            if time >= 3.5:
                if player.x <= 162 and player.y <= 371:
                    remove_player(nets, ge, x, players, player, -5)  # -5 fitness

        if WIN_ON:
            draw_window(win, balls, players, coins, area, level)  # Draw everything


# NEW GENERATION
def remove_player(nets, ge, x, players, player, value):
    if player in players:
        ge[x].fitness += player.fitness + (2500 / player.distance) + value

        # Remove player from game

        nets.pop(players.index(player))
        ge.pop(players.index(player))
        players.pop(players.index(player))


# NEAT
def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_file)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 9999)

    print('\nBest genome:\n{!s}'.format(winner))

    counter = 0
    pkl_file = "./models/pickle_square_model_{}.pkl"
    while os.path.isfile(pkl_file.format(counter)):
        counter += 1
    model_file = pkl_file.format(counter)
    with open(model_file, 'wb') as file:
        pickle.dump(winner, file)


# Config file path
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
