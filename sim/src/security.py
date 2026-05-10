"""
Here I model the energy cost of AES-128-GCM security overhead.
This includes the extra bytes added to each packet (IV, tag, DTLS header),
the energy cost of decryption on receive, and the total secure RX cost.
All hardware parameters are imported from energy.py.
"""

from energy import (
    energy_tx,
    energy_rx,
    energy_aes128,
    energy_tx_secure,
    PACKET_SIZE,
    AES_CYCLES,
    CPU_FREQ,
    CPU_POWER,
)

# AES-128-GCM + DTLS 1.3 packet overhead
GCM_IV_SIZE  = 12  # nonce (bytes)
GCM_TAG_SIZE = 16  # authentication tag
DTLS_HEADER  = 13  # DTLS 1.3 record header
OVERHEAD     = GCM_IV_SIZE + GCM_TAG_SIZE + DTLS_HEADER  # 41 bytes in total


def energy_rx_secure(payload_bytes=PACKET_SIZE):
    # receive the full packet (payload + overhead) + decrypt + verify tag
    verify = (AES_CYCLES / CPU_FREQ) * CPU_POWER  # one extra block for GCM tag
    return energy_rx(payload_bytes + OVERHEAD) + energy_aes128(payload_bytes) + verify


def security_overhead_ratio(payload_bytes=PACKET_SIZE):
    # how much extra energy does security add over unsecured tx+rx
    unsecured = energy_tx(payload_bytes) + energy_rx(payload_bytes)
    secured   = energy_tx_secure(payload_bytes) + energy_rx_secure(payload_bytes)
    return (secured - unsecured) / unsecured
