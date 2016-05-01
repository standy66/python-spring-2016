#! /usr/bin/env python3
import os
import random
import time
from collections import defaultdict


class Display(object):
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.display = [[' '] * size_y for j in range(size_x)]

    def set_pixel(self, x, y, char):
        self.display[x][y] = char

    def get_pixel(self, x, y):
        return self.display[x][y]

    def reset(self):
        for i in range(self.size_x):
            for j in range(self.size_y):
                self.display[i][j] = ' '

    def print_contents(self):
        for i in range(self.size_x):
            for j in range(self.size_y):
                print(self.display[i][j], end="")
            print()


class World(object):
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.timer = 0
        self.entities = []
        self.num = defaultdict(int)

    def add_entity(self, entity):
        self.num[type(entity)] += 1
        self.entities.append(entity)

    def remove_entity(self, entity):
        self.num[type(entity)] -= 1
        self.entities.remove(entity)

    def loc_free(self, x, y):
        return (not (x, y) in map(lambda e: (e.x, e.y), self.entities) and
                0 <= x < self.size_x and
                0 <= y < self.size_y)

    def get_neighbours(self, x, y):
        neighbours = []
        deltas = [-1, 0, 1]
        positions = [(x + dx, y + dy) for dx in deltas for dy in deltas]
        for entity in self.entities:
            pos = (entity.x, entity.y)
            if pos in positions:
                neighbours.append(entity)
        return neighbours

    def run(self):
        self.timer += 1
        for entity in self.entities:
            entity.run()

    def render(self, display):
        for entity in self.entities:
            entity.render(display)


class Entity(object):
    def __init__(self, world, x, y, symbol=None):
        self.world = world
        self.x = x
        self.y = y
        self.symbol = symbol
        world.add_entity(self)

    def run(self):
        pass

    def render(self, display):
        if (self.symbol):
            display.set_pixel(self.x, self.y, self.symbol)


class Obstacle(Entity):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, '*')


class Animal(Entity):
    def __init__(self, world, x, y, symbol, breed_interval):
        super().__init__(world, x, y, symbol)

        self.breed_time = world.timer
        self.breed_interval = breed_interval

    def die(self):
        self.world.remove_entity(self)

    def get_free_neighbours(self):
        neighbours = []
        deltas = [-1, 0, 1]
        for dx in deltas:
            for dy in deltas:
                if self.world.loc_free(self.x + dx, self.y + dy):
                    neighbours.append((self.x + dx, self.y + dy))
        return neighbours

    def spawn(self, x, y):
        raise NotImplementedError("""This method should be implemented
                                     in subclasses""")

    def breed(self):
        neighbours = self.get_free_neighbours()
        if neighbours:
            pos = random.choice(neighbours)
            self.spawn(pos[0], pos[1])
            self.breed_time = self.world.timer

    def move_random(self):
        neighbours = self.get_free_neighbours()
        if neighbours:
            pos = random.choice(neighbours)
            self.x, self.y = pos

    def run(self):
        if self.world.timer - self.breed_time > self.breed_interval:
            self.breed()


class Predator(Animal):
    def __init__(self, world, x, y, breed_interval, starve_interval):
        super().__init__(world, x, y, 'P', breed_interval)
        self.starve_interval = starve_interval
        self.last_meal_time = world.timer

    def spawn(self, x, y):
        return Predator(self.world, x, y, self.breed_interval,
                        self.starve_interval)

    def run(self):
        if self.world.timer - self.last_meal_time > self.starve_interval:
            self.die()
            return
        preys = list(filter(lambda x: isinstance(x, Prey),
                            self.world.get_neighbours(self.x, self.y)))
        if preys:
            prey = random.choice(preys)
            prey.die()
            self.last_meal_time = self.world.timer
        else:
            self.move_random()
        super().run()


class Prey(Animal):
    def __init__(self, world, x, y, breed_interval):
        super().__init__(world, x, y, 'F', breed_interval)

    def run(self):
        super().run()
        self.move_random()

    def spawn(self, x, y):
        return Prey(self.world, x, y, self.breed_interval)


class Engine(object):
    def __init__(self):
        self.world = None
        self.display = None

    def rand_field(self, sz_x, sz_y, prob_block, prob_pray, prob_predator,
                   predator_breed_interval, prey_breed_interval,
                   starve_interval):

        self.world = World(sz_x, sz_y)
        self.display = Display(sz_x, sz_y)
        for i in range(sz_x):
            for j in range(sz_y):
                choice = random.random()
                if choice >= prob_block + prob_pray + prob_predator:
                    pass
                elif choice >= prob_block + prob_pray:
                    Predator(self.world, i, j, predator_breed_interval,
                             starve_interval)
                elif choice >= prob_block:
                    Prey(self.world, i, j, prey_breed_interval)
                else:
                    Obstacle(self.world, i, j)

    def load_world(self, file_name):
        with open(file_name, "r") as f:
            info_line = f.readline().split()
            world_lines = f.readlines()
            sz_x = int(info_line[0])
            sz_y = int(info_line[1])
            prey_breed_interval = int(info_line[2])
            predator_breed_interval = int(info_line[3])
            starve_interval = int(info_line[4])
            self.world = World(sz_x, sz_y)
            self.display = Display(sz_x, sz_y)
            for i in range(sz_x):
                for j in range(sz_y):
                    ch = world_lines[i][j]
                    if ch == '*':
                        Obstacle(self.world, i, j)
                    elif ch == 'P':
                        Predator(self.world, i, j, predator_breed_interval,
                                 starve_interval)
                    elif ch == 'F':
                        Prey(self.world, i, j, prey_breed_interval)
                    elif ch == '.':
                        pass
                    else:
                        raise RuntimeError("invalid symbol %s at (%d, %d)" %
                                           (ch, i, j))

    def simulate(self, steps=1000, debug_file=None, draw=True):
        for step in range(steps):
            self.display.reset()
            self.world.run()
            self.world.render(self.display)
            os.system("clear")
            print("step: " + str(step))
            print("num obstacles:" + str(self.world.num[Obstacle]))
            print("num prey:" + str(self.world.num[Prey]))
            print("num predators:" + str(self.world.num[Predator]))
            if draw:
                self.display.print_contents()
            if debug_file:
                debug_file.write("%d %d %d\n" % (step, self.world.num[Prey],
                                                 self.world.num[Predator]))
                debug_file.flush()
            time.sleep(0.1)


engine = Engine()
# engine.load_world("world.txt")
engine.rand_field(15, 30, 0.1, 0.3, 0.1, 5, 2, 4)
with open("run.txt", "w") as f:
    engine.simulate(1, f, True)
