"""
Here I plot simulation results for all three scenarios:
LEACH no security, LEACH with AES-128-GCM, and QLEACH-EAS.
"""

import matplotlib.pyplot as plt
import numpy as np
from security import security_overhead_ratio, PACKET_SIZE


def plot_alive_nodes(net_a, net_b, net_c):
    plt.figure(figsize=(10, 5))
    plt.plot(net_a.alive_history, label='LEACH (no security)',
             color='red',    linewidth=2)
    plt.plot(net_b.alive_history, label='LEACH (AES-128-GCM)',
             color='orange', linewidth=2, linestyle='--')
    plt.plot(net_c.alive_history, label='QLEACH-EAS',
             color='blue',   linewidth=2)
    plt.xlabel('Round')
    plt.ylabel('Alive Nodes')
    plt.title('Alive Nodes Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('results/alive_nodes.png', dpi=150)
    plt.show()


def plot_energy(net_a, net_b, net_c):
    plt.figure(figsize=(10, 5))
    plt.plot(net_a.energy_history, label='LEACH (no security)',
             color='red',    linewidth=2)
    plt.plot(net_b.energy_history, label='LEACH (AES-128-GCM)',
             color='orange', linewidth=2, linestyle='--')
    plt.plot(net_c.energy_history, label='QLEACH-EAS',
             color='blue',   linewidth=2)
    plt.xlabel('Round')
    plt.ylabel('Total Energy Remaining (J)')
    plt.title('Energy Consumption Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('results/energy_remaining.png', dpi=150)
    plt.show()


def plot_security_overhead():
    sizes  = np.arange(64, 1025, 64)
    ratios = [security_overhead_ratio(s) * 100 for s in sizes]
    plt.figure(figsize=(10, 5))
    plt.plot(sizes, ratios, color='blue', linewidth=2, marker='o')
    plt.xlabel('Payload Size (bytes)')
    plt.ylabel('Security Overhead (%)')
    plt.title('AES-128-GCM Energy Overhead vs Payload Size')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('results/security_overhead.png', dpi=150)
    plt.show()


def plot_20_runs(results):
    runs    = list(range(1, 21))
    plt.figure(figsize=(10, 5))
    plt.plot(runs, results['leach']['lifetime'],
             label='LEACH', color='red',
             linewidth=2, marker='o', markersize=4)
    plt.plot(runs, results['leach_aes']['lifetime'],
             label='LEACH+AES', color='orange',
             linewidth=2, marker='s', markersize=4,
             linestyle='--')
    plt.plot(runs, results['qleach']['lifetime'],
             label='QLEACH-EAS', color='blue',
             linewidth=2, marker='^', markersize=4)
    plt.xlabel('Run')
    plt.ylabel('Network Lifetime (rounds)')
    plt.title('Network Lifetime Across 20 Independent Runs')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('results/20_runs.png', dpi=150)
    plt.show()
