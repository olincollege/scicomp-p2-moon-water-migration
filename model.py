from molecule import Molecule

class Model:
    def __init__(self, num_molecules):
        self.num_molecules = num_molecules
        self.molecules = [Molecule() for _ in range(num_molecules)]
        self.trapped = 0
        self.lost = 0

    def run_simulation(self):
        while self.molecules:
            for molecule in self.molecules:
                molecule.hop()
                if molecule.state == "Lost":
                    self.lost += 1
                if molecule.state == "Trapped":
                    self.trapped += 1

            # Remove molecules that are either lost or trapped
            self.molecules = [molecule for molecule in self.molecules if molecule.state not in ["Lost", "Trapped"]]

        print(f"Captured: {self.trapped}, Lost: {self.lost}, Total: {self.num_molecules}")
        print(f"Percent captured: {(self.trapped / self.num_molecules) * 100}%")
