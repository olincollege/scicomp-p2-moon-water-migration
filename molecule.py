""" molecule.py
This file defines the Molecule class, which represents an individual molecule in the simulation. It
contains methods for handling hopping including calculating coordinates and updates values,
checking loss and capture probabilities.
"""
import numpy as np

# Constants taken from Butler 97
TAU = 2 * 10 ** 4
BOLTZMANN = 1.38e-23

# Capture percentages taken from Watson et al. 61
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
    """
    Initialize a Molecule instance.

    Attributes:
        inclination: an integer representing the inclination angle of the molecule
        azimuth: an integer representing the azimuth angle of the molecule
        start_lat: an integer representing the latitude at which the molecule began
        state: a string representing the current state of the molecule
    """

    def __init__(self, radius, mass, gravity):
        """
        Initialize a Molecule instance (defaults to H20 molecules on the Moon).

        Args: 
            radius: an integer representing the radius of the planetary object in the model
            mass: an integer representing the molecular mass of the chosen molecule in the model
            gravity: an integer representing the gravity of the planetary object in the model

        Returns: N/A
        """
        # A randomly generated inclination angle from 0 to pi
        self.inclination = np.random.uniform(
            0, np.pi)
        # A randomly generated azimuth angle from 0 to 2*pi
        self.azimuth = np.random.uniform(0, 2 * np.pi)

        # These three constants can be modified to change the simulation to different environments
        # (ie. different molecular mass or planetary environmental factors)
        self.radius = radius
        self.mass = mass
        self.gravity = gravity

        # Start latitude calculated based on inclination. This was done to be used as a statistic
        # in later analysis. The absolute value is then taken to handle negative latitudes and
        # rounded to the tens place.
        self.start_lat = round(abs(90 - np.degrees(self.inclination)), -1)

        # self.state is used to track whether or not a molecule is still hopping.
        # It can also be set to "Lost" or "Trapped" depending on how a molecule exited the model.
        self.state = "Hopping"  # Default state is "Hopping"

    def hop(self):
        """
        Simulate one hop for molecule.

        Args: N/A

        Returns: N/A
        """
        # These first few lines are used to calculate variables which will be needed as inputs into
        # later functions.
        velocity = self.calculate_velocity()
        hop_time = self.calculate_hop_time(velocity)
        hop_distance = velocity * hop_time / 2

        # This runs the check on whether or not a molecule is lost. If it is it's no longer a part
        # of the simulation and the function returns prior to doing any calculations on future
        # coordinates.
        self.check_for_loss(hop_time)
        if self.state == "Lost":  # Set state to "Lost"
            return

        # Once a molecule pass the loss check, the function is run to update the coordinates based
        # on the hop distance.
        self.update_coordinates(hop_distance)

        # After coordinates are updates, the check on capture is run using the new coordinates.
        self.check_for_capture()

    def check_for_loss(self, hop_time):
        """
        Calculates probability of loss and checks whether a molecule is lost.

        Args: 
            hop_time: An integer representing the hop time based on velocity and planetary gravity.

        Returns: N/A
        """
        # This equation was provided in both Butler papers to use in calculates of the loss
        # probability. After this calculation is performed, a random number between 0 and 1 is
        # generated and assigned to epsilon.
        p_loss = 1 - np.exp(-hop_time / TAU)
        epsilon = np.random.rand()

        # If epsilon is less than what the loss probability is, the molecule is considered lost and
        # the state is updated accordingly.
        if epsilon < p_loss:
            self.state = "Lost"  # Loss happened

    def update_coordinates(self, distance):
        """
        Calculate new coordinates after hop.

        Args:
            distance: An integer repesenting the hop distance based on velocity and hop time.

        Returns: N/A
        """
        # The way I decided to implement the coordinates updating was using a scale factors.
        # After calculating the distance, which is an input to this function, it's taken and
        # divided by the circumference of the planet (2 * pi * r) to give a scale factor for the
        # angle changes.

        # It's implemented as just the distance divided by radius because it would need to be
        # multiplied by (2 * pi) for the angle range so that it cancelled out.
        scale = distance/self.radius

        # Generate a random azimuth change in the range [0, ((distance/circumference) * 2 * pi)]
        azimuth_change = np.random.uniform(0, scale)

        # Generate a random inclination change in the range [0, ((distance/circumference) * pi)]
        inclination_change = np.random.uniform(0, scale/2)

        # Creating variables of the updated azimuth and inclination after adding the randomly
        # generated changes.
        new_azimuth = self.azimuth + azimuth_change
        new_inclination = self.inclination + inclination_change

        # By using mod, it ensures the angles wrap around and don't grow infinitely larger.
        self.azimuth = new_azimuth % (2 * np.pi)
        self.inclination = new_inclination % (np.pi)

    def calculate_velocity(self):
        """
        Calculate velocity.

        Args: N/A

        Returns: 
            An integer representing the velocity based on temperature and molecular mass.
        """
        # This is the equation given in Butler 93 for calculating velocity. Although it's a
        # constant here, this function could be modified to accomodate a variable temperature which
        # right now is set to be a constant 500 K.
        return np.sqrt(3 * BOLTZMANN * 500 / self.mass)

    def calculate_hop_time(self, velocity):
        """
        Calculate velocity.

        Args: N/A

        Returns: 
            An integer representing the hop time based on velocity and planetary gravity.
        """
        # This is the equation given in Butler 93 for calculating hop time. Although it's a
        # constant here, this function could be modified to accomodate a variable gravity equation
        # similar to what was used in Butler 97.
        return (2 ** 0.5) * velocity / self.gravity

    def check_for_capture(self):
        """
        Calculates probability of capture and checks whether a molecule is captured.

        Args: N/A

        Returns: N/A
        """
        # Converting inclination to latitude using equation provided by Butler 97.
        # The absolute value is then taken to handle negative latitudes and rounded to the tens
        # place to associate with capture percentages.
        lat_in_degrees = round(abs(90 - np.degrees(self.inclination)), -1)

        # Converting integer to string to match dictionary keys
        latitude_bin = str(int(lat_in_degrees))

        # The latitude is then used to retreve the capture percentage for that 10 degree area.
        # This is the percentage of surface area which is cold enough to trap a molecule and we
        # assume that if a molecule enters a capture area it cannot leave. If the latitude isn't
        # found in the dictionary, it defaults to 0.
        capture_percentage = CAPTURE_PERCENTAGES.get(latitude_bin, 0)

        # A number between 0 and 1 is generated and then converted to 0 to 100 to check against the
        # percentages. If the randomly generate number is less than the capture percentage the
        # molecule is considered trapped and the state is updated to reflect that.
        if np.random.rand() * 100 < capture_percentage:
            self.state = "Trapped"
