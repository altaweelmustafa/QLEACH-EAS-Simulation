"""
Here I run the full simulation comparing three scenarios:
  A: LEACH without security
  B: LEACH with AES-128-GCM (all packets)
  C: QLEACH-EAS (Q-learning CH + routing, EAS encryption)
Results are printed and saved as graphs.
"""

import os
from network     import Network
from leach       import run_leach
from qleach_eas  import run_qleach_eas
from plot        import plot_alive_nodes, plot_energy, \
                        plot_security_overhead
from security    import security_overhead_ratio, PACKET_SIZE

os.makedirs('results', exist_ok=True)

# ── Scenario A: LEACH no security ───────────────────────
net_a = Network()
run_leach(net_a, secure=False)
net_a.print_summary("LEACH — no security")

# ── Scenario B: LEACH with AES-128-GCM ──────────────────
net_b = Network()
run_leach(net_b, secure=True)
net_b.print_summary("LEACH — with AES-128-GCM")

# ── Scenario C: QLEACH-EAS ──────────────────────────────
net_c = Network()
run_qleach_eas(net_c)
net_c.print_summary("QLEACH-EAS")

# ── Security overhead ────────────────────────────────────
ratio = security_overhead_ratio(PACKET_SIZE)
print(f"\n  AES-128-GCM overhead  : {ratio*100:.2f}%")

# ── Plots ────────────────────────────────────────────────
plot_alive_nodes(net_a, net_b, net_c)
plot_energy(net_a, net_b, net_c)
plot_security_overhead()
