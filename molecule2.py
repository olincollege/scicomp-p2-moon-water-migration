import numpy as np

TAU = 2 * 10 ** 4
BOLTZMANN = 1.38e-23
TEMP_0 = 151.0
TEMP_1 = 161.7
N = 0.59
MASS = 2.988e-26
GRAVITY = 1.623
R_MOON = 1738e3

class Molecule:
    def __init__(self):
        self.radius = R_MOON
        self.inclination = np.random.uniform(
            0, np.pi)  # Inclination angle from 0 to pi
        # Azimuth angle from 0 to 2*pi
        self.azimuth = np.random.uniform(0, 2 * np.pi)
        self.temp = 0
        self.v = 0
        self.state = "Hopping"  # Default state is "Hopping"

    def spherical_to_cartesian(self):
        x = self.radius * np.sin(self.inclination) * np.cos(self.azimuth)
        y = self.radius * np.sin(self.inclination) * np.sin(self.azimuth)
        z = self.radius * np.cos(self.inclination)
        return x, y, z

    def cartesian_to_spherical(self, x, y, z):
        radius = np.sqrt(x**2 + y**2 + z**2)
        inclination = np.arccos(z / radius)
        azimuth = np.arctan2(y, x)
        return azimuth, inclination, radius

    def hop(self):
        velocity = self.get_velocity()
        hop_time = self.get_hop_time(velocity)
        self.determine_loss(hop_time)
        if self.state == "Lost":
            return

        # Convert current spherical coordinates to Cartesian coordinates
        x, y, z = self.spherical_to_cartesian()
        print("original", x, y, z)

        # Update the Cartesian coordinates based on the distance
        hop_distance = velocity * hop_time / 2
        x1 = x + hop_distance * np.sin(self.inclination) * np.cos(self.azimuth)
        y1 = y + hop_distance * np.sin(self.inclination) * np.sin(self.azimuth)
        z1 = z + hop_distance * np.cos(self.inclination)
        print("calculated", x1, y1, z1)

        # Convert the updated Cartesian coordinates back to spherical coordinates
        new_azimuth, new_inclination, new_radius = self.cartesian_to_spherical(x1, y1, z1)
        print(new_azimuth, self.azimuth)
        # Update the molecule's attributes
        self.azimuth = new_azimuth
        self.inclination = new_inclination
        
        print("azimuth:", new_azimuth)
        print("inclination", new_inclination)

        self.check_capture()

    def determine_loss(self, hop_time):
        p_loss = 1 - np.exp(-hop_time / TAU)
        epsilon = np.random.rand()
        if epsilon < p_loss:
            self.state = "Lost"  # Loss happened

    def get_velocity(self):
        return np.sqrt(3 * BOLTZMANN * 500 / MASS)

    def get_hop_time(self, velocity):
        return (2 ** 0.5) * velocity / GRAVITY

    def check_capture(self):
        # Define a dictionary that maps latitude to capture percentages
        f_stable = {
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
        # Calculate latitude in degrees
        lat_in_degrees = 90 - np.degrees(self.inclination)
        # Convert to string to match dictionary keys
        latitude_bin = str(int(lat_in_degrees))
        # Get the capture percentage for the latitude
        capture_percentage = f_stable.get(latitude_bin, 0)
        # if np.random.rand() * 100 < capture_percentage:
        if lat_in_degrees > 80:
            self.state = "Trapped"  # Set state to "Trapped" if molecule is captured
