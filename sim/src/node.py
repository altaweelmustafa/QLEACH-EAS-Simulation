import numpy as np


class Node:
    def __init__(self, node_id, x, y, initial_energy=1.0):
        self.id = node_id
        self.x = x
        self.y = y
        self.energy = initial_energy
        self.initial_energy = initial_energy
        self.alive = True
        self.is_cluster_head = False
        self.cluster_head_id = None
        self.packets_sent = 0
        self.packets_dropped = 0
        self.topic = "sensors/energy" # example topic. Main category:sensors, sub-category:energy. 

    # Manhattan distance
    def distance_to(self, other):
        return np.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    # still have energy or not
    def is_alive(self):
        return self.alive and self.energy > 0

    # power consume by amount
    def deplete(self, amount):
        self.energy -= amount
        if self.energy <= 0:
            self.energy = 0
            self.alive = False
