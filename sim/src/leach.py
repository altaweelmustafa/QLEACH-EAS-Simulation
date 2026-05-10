"""
Here I implement the LEACH clustering algorithm as Routing A (baseline).
Each round, nodes randomly elect cluster heads based on probability p.
Non-CH nodes join the nearest CH and transmit data to it.
CH nodes aggregate and forward data to the base station.
Energy is depleted using functions from energy.py.
"""

import numpy as np

from energy import E_DA, PKT_BITS, energy_rx, energy_tx, energy_tx_secure


def E_DA_cost(ch):
    # data aggregation energy at cluster head
    return E_DA * PKT_BITS


# LEACH configuration
CH_PROB = 0.1  # probability of becoming a cluster head


def elect_cluster_heads(nodes, round_num):
    # random CH election based on LEACH threshold formula
    heads = []
    for node in nodes:
        if not node.is_alive():
            continue
        cycle = round_num % int(1 / CH_PROB)
        threshold = CH_PROB / (1 - CH_PROB * cycle) if cycle != 0 else CH_PROB
        if np.random.random() < threshold:
            node.is_cluster_head = True
            heads.append(node)
        else:
            node.is_cluster_head = False

    # fallback: if no CH elected pick one randomly
    if not heads:
        alive = [n for n in nodes if n.is_alive()]
        if alive:
            ch = np.random.choice(alive)
            ch.is_cluster_head = True
            heads.append(ch)

    return heads


def assign_and_transmit(nodes, heads, secure=False):
    delivered = 0
    dropped = 0
    for node in nodes:
        if not node.is_alive() or node.is_cluster_head:
            continue
        nearest = min(heads, key=lambda h: node.distance_to(h))
        node.cluster_head_id = nearest.id
        dist = node.distance_to(nearest)  # real distance
        cost = energy_tx_secure(distance=dist) if secure else energy_tx(distance=dist)
        node.deplete(cost)
        if node.is_alive():
            nearest.deplete(energy_rx())
            node.packets_sent += 1
            delivered += 1
        else:
            node.packets_dropped += 1
            dropped += 1
    return delivered, dropped


def transmit_to_bs(heads, bs, secure=False):
    for ch in heads:
        if not ch.is_alive():
            continue
        dist = ch.distance_to(bs)
        cost = energy_tx_secure(distance=dist) if secure else energy_tx(distance=dist)
        ch.deplete(cost)
        ch.deplete(E_DA * PKT_BITS)  # aggregation



def run_leach(network, secure=False):
    for r in range(network.rounds):
        alive = network.alive_nodes()
        if not alive:
            break
        heads = elect_cluster_heads(alive, r)
        assign_and_transmit(network.nodes, heads, secure)
        transmit_to_bs(heads, network.bs, secure)
        network.record_round()
