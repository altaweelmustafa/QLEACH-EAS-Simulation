"""
Here I save the power consumption parameters for all components.
Uses the first order radio model (Heinzelman et al. 2000) which is a standard for WSN and LEACH simulations.
AES-128-GCM overhead modelled for ESP32-C3.
"""

# First order radio model
E_ELEC      = 50e-9      # J/bit  (Tx/Rx electronics)
E_AMP       = 100e-12    # J/bit/m² (Tx amplifier)
E_DA        = 5e-9       # J/bit  (data aggregation at CH) 
PACKET_SIZE = 512        # bytes
PKT_BITS    = PACKET_SIZE * 8  # bits

# AES-128-GCM (ESP32-C3)
AES_BLOCK   = 16         # bytes
AES_CYCLES  = 160        # clock cycles per block
CPU_FREQ    = 240e6      # Hz
CPU_POWER   = 0.264      # Watts


def energy_tx(packet_size_bytes=PACKET_SIZE, distance=50):
    k = packet_size_bytes * 8
    return E_ELEC * k + E_AMP * k * distance ** 2


def energy_rx(packet_size_bytes=PACKET_SIZE):
    k = packet_size_bytes * 8
    return E_ELEC * k


def energy_aes128(payload_bytes=PACKET_SIZE):
    blocks = (payload_bytes // AES_BLOCK) + 1
    cycles = blocks * AES_CYCLES
    time   = cycles / CPU_FREQ
    return CPU_POWER * time


def energy_tx_secure(payload_bytes=PACKET_SIZE, distance=50):
    return energy_tx(payload_bytes, distance) + \
           energy_aes128(payload_bytes)


def energy_rx_secure(payload_bytes=PACKET_SIZE):
    return energy_rx(payload_bytes) + \
           energy_aes128(payload_bytes)
