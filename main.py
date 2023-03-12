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
pygame.display.set_caption("Hardest Game in the World! (level 1)")

map_surface = pygame.image.load('./game/resources/images/maps/level_1.png').convert_alpha()
map_rect = map_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# NEAT
GEN = 0
atw = 0


# DRAW WINDOW
def draw_window(win, balls, players, area):
    win.fill(GROUND)
    win.blit(map_surface, map_rect)

    for b in balls:
        b.draw(win)

    for p in players:
        if p in players:
            p.draw(win)
            p.target_information(win, area, True)

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

    GEN += 1
    WIN_ON = True
    time_max = 10
    won = 0

    # Objects
    map = MapLevel01()

    area = Win(738, 84, 1, 42)

    ball1 = Ball(235, 154, 1)
    ball2 = Ball(665, 202, 2)
    ball3 = Ball(235, 250, 3)
    ball4 = Ball(665, 298, 4)

    # Lists
    balls = [ball1, ball2, ball3, ball4]

    players = []
    nets = []
    ge = []

    # Load model
    with open('pickle_rl_model.pkl', 'rb') as file:
        clf = pickle.load(file)

    for genomes_id, gnome in genomes:
        # net = neat.nn.FeedForwardNetwork.create(clf, config)
        net = neat.nn.FeedForwardNetwork.create(gnome, config)

        nets.append(net)
        players.append(Player())

        gnome.fitness = 0
        ge.append(gnome)

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    run = True

    # Main loop
    while run and len(players) > 0:
        if WIN_ON: clock.tick(FPS)

        # Tempo
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

            # Inputs NN
            outputs = nets[players.index(player)].activate(
                (
                    player.x, player.y,

                    ball1.x, ball1.y,
                    ball2.x, ball2.y,
                    ball3.x, ball3.y,
                    ball4.x, ball4.y,
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

            # Won:
            if player.win:
                # count = 0
                # for p in players:
                #     if p.win:
                #         count += 1
                # if count > (len(players) * (3 / 4)):
                print("Player Win: {} atw: {} won: {}".format(player.win, atw, won))
                if atw >= (len(players) * (3 / 4)):
                    remove_player(nets, ge, x, players, player, 99999999)
                else:
                    remove_player(nets, ge, x, players, player, 5000)
                    won += 1
                    atw += 1

            # Eliminates players who are in spawn after 3.5 seconds
            if time >= 3.5:
                if player.x <= 162 and player.y <= 371:
                    remove_player(nets, ge, x, players, player, -5)  # -5 fitness

        if WIN_ON:
            draw_window(win, balls, players, area)  # Draw everything


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
