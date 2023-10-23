""" model.py
This file defines the Model class, which represents the overall model in simulation. It handles
generating all the molecules and then running the simulation on each until they are all trapped or
captured.
"""
from molecule import Molecule

class Model:
    """
    Initialize a Model instance.

    Attributes:
        num_molecules: an integer representing the total number of molecules in the simulation
        molecules: a list containing all active Molecules objects in the simulation
        trapped: an integer representing the number of molecules trapped in the simulation
        lost: an integer representing the number of molecules lost in the simulation
        iterations: an integer representing the number of timesteps in the simulation
        captured_start_latitudes: a list representing the starting latitudes of all molecules which
        get trapped
    """
    def __init__(self, num_molecules=1000, radius=1738e3, mass=2.988e-26, gravity=1.623):
        """
        Initialize a Molecule instance.

        Args: 
            num_molecules: an integer representing the total number of molecules in the simulation
            radius: an integer representing the radius of the planetary object in the model
            mass: an integer representing the molecular mass of the chosen molecule in the model
            gravity: an integer representing the gravity of the planetary object in the model

        Returns: N/A
        """
        self.num_molecules = num_molecules

        # Creates a list of Molecule objects corresponding to the num_molecules chosen.
        self.molecules = [Molecule(radius, mass, gravity) for _ in range(num_molecules)]

        # Trapped and lost are incremented as molecules enter either state
        self.trapped = 0
        self.lost = 0

        # Every time the simulation runs the iterations value is incremented
        self.iterations = 0
        self.captured_start_latitudes = []


    def run_simulation(self):
        """
        Run the simulation

        Args: N/A

        Returns: N/A
        """
        # The while loop is set so that the simulation will run until all molecules are either
        # trapped or lost.
        while self.molecules:
            # Increment the iterations
            self.iterations += 1

            # During each timestep, each molecule goes through the hop function
            for molecule in self.molecules:
                molecule.hop()

                # After the molecule hops and the state is updated, it checks whether the state is
                # lost or trapped and incremented the appropriate integer.
                if molecule.state == "Lost":
                    self.lost += 1
                if molecule.state == "Trapped":
                    self.trapped += 1
                    self.captured_start_latitudes.append(molecule.start_lat)

            # self.molecules only keeps the molecules which are still hopping. This ensures that
            # once a molecule reaches a state where it shouldn't move anymore the simulation
            # doesn't continue to use it.
            self.molecules = [
                molecule for molecule in self.molecules
                if molecule.state == "Hopping"]

        # Once all the molecules are trapped or lost, these statements return a few statistics
        # about the number of trapped, lost, and iterations as well as calculating the percent of
        # molecules which were captured.
        print(
            f"Captured: {self.trapped}, Lost: {self.lost}, Total iterations: {self.iterations}")
        print(
            f"Percent captured: {(self.trapped / self.num_molecules) * 100}%")
