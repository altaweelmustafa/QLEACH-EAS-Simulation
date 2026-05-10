# QLEACH-EAS

**Q-Learning LEACH with Energy-Aware Security** — a clustering protocol for Wireless Sensor Networks (WSNs) that extends network lifetime while maintaining lightweight security.

---

## What It Does

QLEACH-EAS combines three mechanisms:

- **LEACH clustering** — random CH rotation for fair energy distribution
- **Q-learning sleep scheduling** — agent adaptively reduces transmissions as network energy depletes
- **Energy-Aware Security (EAS)** — AES-128-GCM applied only to *CH→BS packets*, not member→CH

---

## Setup

```bash
git clone https://github.com/altaweelmustafa/QLEACH-EAS-Simulation.git
cd qleach/sim
pip install numpy matplotlib
python main.py
```

Output: four graphs saved to `results/` and a summary table printed to terminal.

---

## Simulation Parameters

| Parameter | Value |
|---|---|
| Nodes | 50 |
| Field | 100 × 100 m |
| Initial energy | 0.25 J |
| Rounds | 1000 |
| Runs | 20 (different seeds) |
| CH probability | 0.1 |
| α / γ / ε | 0.1 / 0.9 / 0.2 |
| Packet size | 512 bytes |
| AES hardware | ESP32-C3 |


---

## Energy Model

First-order radio model (Heinzelman et al., 2000):

```
E_tx(k, d) = E_elec × k + E_amp × k × d²
E_rx(k)    = E_elec × k
E_aes(p)   = ⌈p/16⌉ × 160 / 240MHz × 0.264W
```

---

## Results (20 independent runs)

| Metric | LEACH | LEACH+AES | QLEACH-EAS |
|---|---|---|---|
| First node death | 211.6 ± 15.4 | 210.6 ± 14.8 | **226.9 ± 21.4** |
| 50% nodes dead | 347.9 ± 24.2 | 343.9 ± 23.2 | **379.6 ± 23.8** |
| Network lifetime | 543.5 ± 15.4 | 530.0 ± 28.9 | **584.0 ± 33.7** |
| PDR (%) | 98.0 | 98.0 | **98.0** |
| AES-128-GCM overhead | — | 1.97% | 1.97% |

QLEACH-EAS extends network lifetime by **7.45%** over LEACH and **10.19%** over LEACH+AES.

---

## Paper

This simulation accompanies the paper:

> **QLEACH-EAS: A Q-Learning Based Energy-Aware Secure Clustering Protocol for Wireless Sensor Networks**
> Mustafa Altaweel — Birzeit University, 2026 [DOI: 10.13140/RG.2.2.36348.09607](https://www.researchgate.net/publication/404703410_QLEACH-EAS_A_Q-Learning_Based_Energy-Aware_Secure_Clustering_Protocol_for_Wireless_Sensor_Networks)


---
