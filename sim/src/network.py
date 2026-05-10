"""
Here I build the network topology and track per-round statistics.
Includes the BaseStation class and the Network class which manages
node creation, energy tracking, and simulation metrics.
All node behavior is handled by Node class from node.py.
"""

import numpy as np
from node import Node

# Network configuration
N_NODES        = 50
FIELD_SIZE     = 100    # metres (square field)
INITIAL_ENERGY = 0.25    # joules per node
ROUNDS         = 1000
BS_X           = 50     # base station x position
BS_Y           = 50     # base station y position
SEED           = 42


class BaseStation:
    def __init__(self, x=BS_X, y=BS_Y):
        self.x = x
        self.y = y
        self.subscriptions = {}   # topic -> [subscribers]
        self.message_log   = []   # all received messages

    def subscribe(self, topic, subscriber):
        if topic not in self.subscriptions:
            self.subscriptions[topic] = []
        self.subscriptions[topic].append(subscriber)

    def publish(self, topic, data, sender_id):
        # broker receives and routes
        msg = {"topic": topic,
               "data": data,
               "sender": sender_id}
        self.message_log.append(msg)
        # deliver to all subscribers of this topic
        for sub in self.subscriptions.get(topic, []):
            sub.receive(msg)

    # Manhattan distance (again haha)
    def distance_to(self, node):
        return np.sqrt((self.x - node.x) ** 2 + (self.y - node.y) ** 2)

    # edge processing, level 5 IoT arch respect
    def process(self):
        # analyse received messages this round
        readings = [m['data'] for m in self.message_log]
        if readings:
            avg_energy = sum(readings) / len(readings)
            # base station makes decisions based on data
            # e.g. flag low energy nodes for rerouting
            return avg_energy
        return 0.0

class Network:
    def __init__(self, seed=SEED):
        np.random.seed(seed)
        self.bs    = BaseStation()
        self.nodes = self._create_nodes()
        self.rounds = ROUNDS
        self.field_size = FIELD_SIZE

        self.alive_history  = []
        self.energy_history = []
        self.dead_history   = []

    def _create_nodes(self):
        return [
            Node(i,
                 np.random.uniform(0, FIELD_SIZE),
                 np.random.uniform(0, FIELD_SIZE),
                 INITIAL_ENERGY)
            for i in range(N_NODES)
        ]

    def reset(self):
        # restore network to initial state for a clean re-run
        np.random.seed(SEED)
        self.nodes          = self._create_nodes()
        self.alive_history  = []
        self.energy_history = []
        self.dead_history   = []

    def alive_nodes(self):
        return [n for n in self.nodes if n.is_alive()]

    def total_energy(self):
        return sum(n.energy for n in self.nodes)

    def record_round(self):
        # call at the end of each simulation round
        alive = len(self.alive_nodes())
        self.alive_history.append(alive)
        self.energy_history.append(self.total_energy())
        self.dead_history.append(N_NODES - alive)

    def first_node_death(self):
        # round when the first node died
        for i, a in enumerate(self.alive_history):
            if a < N_NODES:
                return i
        return len(self.alive_history)

    def half_nodes_dead(self):
        # round when 50% of nodes are dead
        for i, d in enumerate(self.dead_history):
            if d >= N_NODES // 2:
                return i
        return len(self.dead_history)

    def network_lifetime(self):
        # round when the last node died
        for i, a in enumerate(self.alive_history):
            if a == 0:
                return i
        return len(self.alive_history)

    def packet_delivery_ratio(self):
        sent    = sum(n.packets_sent    for n in self.nodes)
        dropped = sum(n.packets_dropped for n in self.nodes)
        return sent / max(sent + dropped, 1)

    def print_summary(self, label="Network"):
        print(f"\n── {label} ───────────────────────────────")
        print(f"  First node death  : round {self.first_node_death()}")
        print(f"  50% nodes dead    : round {self.half_nodes_dead()}")
        print(f"  Network lifetime  : round {self.network_lifetime()}")
        print(f"  Final energy      : {self.energy_history[-1]:.4f} J")
        print("─────────────────────────────────────────────")
