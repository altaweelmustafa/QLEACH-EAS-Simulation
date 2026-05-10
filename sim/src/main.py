"""
Here I run the full simulation comparing three scenarios over 20 runs.
Each run uses a different random seed to ensure statistical validity.
Results are reported as mean ± standard deviation across all runs.
"""

import os
import numpy as np
from network  import Network
from leach    import run_leach
from qleach_eas import run_qleach_eas
from plot     import plot_alive_nodes, plot_energy, plot_security_overhead
from security import security_overhead_ratio, PACKET_SIZE

os.makedirs('results', exist_ok=True)

N_RUNS = 20

# ── Storage ─────────────────────────────────────────────
results = {
    'leach':     {'first': [], 'half': [], 'lifetime': [], 'pdr': []},
    'leach_aes': {'first': [], 'half': [], 'lifetime': [], 'pdr': []},
    'qleach':    {'first': [], 'half': [], 'lifetime': [], 'pdr': []},
}

# keep last run histories for plotting
last = {'leach': None, 'leach_aes': None, 'qleach': None}

# ── 20 Runs ──────────────────────────────────────────────
for run in range(N_RUNS):
    print(f"Run {run + 1}/{N_RUNS}...", end='\r')

    # Scenario A: LEACH no security
    net_a = Network(seed=run)
    run_leach(net_a, secure=False)
    results['leach']['first'].append(net_a.first_node_death())
    results['leach']['half'].append(net_a.half_nodes_dead())
    results['leach']['lifetime'].append(net_a.network_lifetime())
    results['leach']['pdr'].append(net_a.packet_delivery_ratio())
    last['leach'] = net_a

    # Scenario B: LEACH with AES-128-GCM
    net_b = Network(seed=run)
    run_leach(net_b, secure=True)
    results['leach_aes']['first'].append(net_b.first_node_death())
    results['leach_aes']['half'].append(net_b.half_nodes_dead())
    results['leach_aes']['lifetime'].append(net_b.network_lifetime())
    results['leach_aes']['pdr'].append(net_b.packet_delivery_ratio())
    last['leach_aes'] = net_b

    # Scenario C: QLEACH-EAS
    net_c = Network(seed=run)
    run_qleach_eas(net_c)
    results['qleach']['first'].append(net_c.first_node_death())
    results['qleach']['half'].append(net_c.half_nodes_dead())
    results['qleach']['lifetime'].append(net_c.network_lifetime())
    results['qleach']['pdr'].append(net_c.packet_delivery_ratio())
    last['qleach'] = net_c

print(f"Done. {N_RUNS} runs completed.     ")

# ── Print Results ────────────────────────────────────────
def summary(label, r):
    print(f"\n── {label} ───────────────────────────────")
    print(f"  First node death  : "
          f"{np.mean(r['first']):.1f} ± {np.std(r['first']):.1f}")
    print(f"  50% nodes dead    : "
          f"{np.mean(r['half']):.1f} ± {np.std(r['half']):.1f}")
    print(f"  Network lifetime  : "
          f"{np.mean(r['lifetime']):.1f} ± {np.std(r['lifetime']):.1f}")
    print(f"  Packet delivery   : "
          f"{np.mean(r['pdr'])*100:.1f}% ± {np.std(r['pdr'])*100:.1f}%")
    print("─────────────────────────────────────────────")

summary("LEACH — no security",    results['leach'])
summary("LEACH — with AES-128",   results['leach_aes'])
summary("QLEACH-EAS",             results['qleach'])

ratio = security_overhead_ratio(PACKET_SIZE)
print(f"\n  AES-128-GCM overhead  : {ratio*100:.2f}%")

# ── Plots (last run) ─────────────────────────────────────
plot_alive_nodes(last['leach'], last['leach_aes'], last['qleach'])
plot_energy(last['leach'], last['leach_aes'], last['qleach'])
plot_security_overhead()
