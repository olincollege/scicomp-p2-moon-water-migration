import numpy as np

TAU = 2 * 10 ** 4
BOLTZMANN = 1.38e-23
MASS = 2.988e-26
GRAVITY = 1.623
RADIUS_MOON = 1738e3

CAPTURE_PERCENTAGES = {
    "0": 0,
    "10": 0,
    "20": 0,
    "30": 0,
    "40": 0,
    "50": 0,
    "60": 1.0,
    "70": 2.2,
    "80": 8.5,
    "90": 27.5
}

class Molecule:
    def __init__(self):
        self.radius = RADIUS_MOON
        self.inclination = np.random.uniform(
            0, np.pi)  # Inclination angle from 0 to pi
        # Azimuth angle from 0 to 2*pi
        self.azimuth = np.random.uniform(0, 2 * np.pi)
        self.start_lat = 90 - np.degrees(self.inclination)
        self.state = "Hopping"  # Default state is "Hopping"

    def hop(self):
        velocity = self.calculate_velocity()
        hop_time = self.calculate_hop_time(velocity)
        hop_distance = velocity * hop_time / 2
        self.check_for_loss(hop_time)
        if self.state == "Lost":  # Set state to "Lost"
            return
        self.update_coordinates(hop_distance)
        self.check_for_capture()

    def check_for_loss(self, hop_time):
        p_loss = 1 - np.exp(-hop_time / TAU)
        epsilon = np.random.rand()
        if epsilon < p_loss:
            self.state = "Lost"  # Loss happened

    def update_coordinates(self, distance):

        scale = distance/RADIUS_MOON
        
        # Generate a random azimuth change in the range [0, 2*pi]
        azimuth_change = np.random.uniform(0, scale)
        
        # Generate a random inclination change in the range [-pi/2, pi/2]
        inclination_change = np.random.uniform(0, scale/2)
        
        new_azimuth = self.azimuth + azimuth_change
        new_inclination = self.inclination + inclination_change
        # Update azimuth and inclination based on the changes
        self.azimuth = new_azimuth % (2 * np.pi)
        self.inclination = new_inclination % (np.pi/2)
        
    def calculate_velocity(self):
        return np.sqrt(3 * BOLTZMANN * 500 / MASS)

    def calculate_hop_time(self, velocity):
        return (2 ** 0.5) * velocity / GRAVITY

    def check_for_capture(self):
        lat_in_degrees = 90 - np.degrees(self.inclination)
        latitude_bin = str(int(lat_in_degrees))
        capture_percentage = CAPTURE_PERCENTAGES.get(latitude_bin, 0)
        if np.random.rand() * 100 < capture_percentage:
            self.state = "Trapped"
