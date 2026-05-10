"""
Here I implement QLEACH-EAS (Q-Learning LEACH with Energy Aware Security).
LEACH handles CH election randomly for fair energy rotation.
Q-learning decides the sleep ratio: what fraction of members skip
transmission this round to save energy.
EAS encrypts only CH-to-BS packets, saving energy on member transmissions.
Reward is total network energy remaining after each round.
"""

import numpy as np
from energy import (
    energy_tx, energy_rx,
    energy_tx_secure,
    E_DA, PKT_BITS
)
from leach import elect_cluster_heads

ALPHA         = 0.1
GAMMA         = 0.9
EPSILON       = 0.3
N_STATES      = 10   # energy level bins (0-9)
N_ACTIONS     = 5    # sleep ratios: 0%, 10%, 20%, 30%, 40%
SLEEP_RATIOS  = [0.0, 0.1, 0.2, 0.3, 0.4]
CH_PROB       = 0.1


def _state(network):
    # state = network energy level (0-9)
    total_e    = network.total_energy()
    total_init = sum(
        n.initial_energy for n in network.nodes
    )
    ratio = total_e / max(total_init, 1e-9)
    return min(int(ratio * 10), 9)


class QLEACHAgent:
    def __init__(self):
        # Q-table: state × action (sleep ratio)
        self.q_table = np.zeros((N_STATES, N_ACTIONS))

    def select_sleep_ratio(self, state, epsilon):
        if np.random.random() < epsilon:
            return np.random.randint(N_ACTIONS)
        return int(np.argmax(self.q_table[state]))

    def update(self, state, action,
               reward, next_state):
        max_q = np.max(self.q_table[next_state])
        self.q_table[state, action] += ALPHA * (
            reward + GAMMA * max_q
            - self.q_table[state, action]
        )


def run_qleach_eas(network):
    agent      = QLEACHAgent()
    total_init = sum(
        n.initial_energy for n in network.nodes
    )

    for r in range(network.rounds):
        alive = network.alive_nodes()
        if not alive:
            break

        # LEACH random CH election (unchanged)
        heads = elect_cluster_heads(alive, r)
        for h in heads:
            h.is_cluster_head = True

        # Q-agent selects sleep ratio this round
        state        = _state(network)
        action       = agent.select_sleep_ratio(
                           state, EPSILON)
        sleep_ratio  = SLEEP_RATIOS[action]

        # member → CH: unencrypted (EAS)
        # some members sleep (skip TX this round)
        members = [n for n in network.nodes
                   if n.is_alive() and
                   not n.is_cluster_head]
        n_sleep  = int(len(members) * sleep_ratio)
        sleeping = set(
            np.random.choice(
                len(members),
                size=n_sleep,
                replace=False
            )
        ) if n_sleep > 0 else set()

        for i, node in enumerate(members):
            if i in sleeping:
                continue   # node sleeps this round
            nearest = min(
                heads, key=lambda h: node.distance_to(h)
            )
            node.cluster_head_id = nearest.id
            node.deplete(energy_tx(
                distance=node.distance_to(nearest)
            ))
            if node.is_alive():
                nearest.deplete(energy_rx())
                node.packets_sent += 1
            else:
                node.packets_dropped += 1

        # CH → BS: encrypted (EAS)
        for ch in heads:
            if not ch.is_alive():
                continue
            ch.deplete(energy_tx_secure(
                distance=ch.distance_to(network.bs)
            ))
            ch.deplete(E_DA * PKT_BITS)

        # reward: normalised network energy
        total_e    = network.total_energy()
        reward     = total_e / total_init

        next_state = _state(network)
        agent.update(state, action, reward, next_state)

        for node in network.nodes:
            node.is_cluster_head = False

        network.record_round()
