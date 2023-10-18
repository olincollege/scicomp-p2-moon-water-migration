import numpy as np
import random

# Constants
T = 500  # Temperature in Kelvin
m = 2.99e-26  # Mass of a water molecule in kg
g = 9.81  # Surface gravity in m/s^2
r = 2e4  # Photodissociation time scale in seconds
K = 7.5e-3  # Fractional surface area covered by polar regions
initial_molecules = 1000  # Number of initial molecules
polar_radius = 300e3  # Radius of the polar regions in meters

# Helper functions
def calculate_hop_time(T, m, g):
    v_rms = np.sqrt(3 * k * T / m)
    t = (2 ** 0.5 * v_rms) / g
    return t

def calculate_hop_distance(v_rms, t):
    return v_rms * t

def capture_probability(t, r):
    a = 1 - np.exp(-t / r)
    P = K * (1 - a)
    return P

def simulate_poleward_migration(initial_molecules, t, r, polar_radius):
    trapped_molecules = 0
    lost_molecules = 0

    for _ in range(initial_molecules):
        is_trapped = False
        time = 0
        position = [0, 0, 0]

        while not is_trapped:
            hop_time = calculate_hop_time(T, m, g)
            hop_distance = calculate_hop_distance(v_rms, hop_time)
            loss_probability = 1 - np.exp(-hop_time / r)

            if random.random() < loss_probability:
                lost_molecules += 1
                break

            time += hop_time

            # Simulate a random hop in a random direction
            theta = random.uniform(0, 2 * np.pi)
            phi = random.uniform(0, np.pi)
            x = hop_distance * np.sin(phi) * np.cos(theta)
            y = hop_distance * np.sin(phi) * np.sin(theta)
            z = hop_distance * np.cos(phi)
            position = [pos + step for pos, step in zip(position, [x, y, z])]

            if np.linalg.norm(position) < polar_radius:
                is_trapped = True
                trapped_molecules += 1

    return trapped_molecules, lost_molecules

if __name__ == '__main__':
    k = 1.38e-23  # Boltzmann constant in m^2 kg / s^2 K
    v_rms = np.sqrt(3 * k * T / m)

    trapped, lost = simulate_poleward_migration(initial_molecules, r, polar_radius)
    percentage_trapped = (trapped / (trapped + lost)) * 100
    print(f"Percentage of molecules that reach the polar regions: {percentage_trapped:.2f}%")
