# Molecule Hopping Simulation

This project simulates the behavior of molecules hopping on a planetary object's surface. The simulation models individual molecules' movements, their potential loss, and the probability of capture. The model is based on the work of Butler (1993), Butler (1997) and Watson et al. (1961). Full titles are in the Sources section below.

This project uses the following libraries:
- numpy
- matplotlib
- scipy

For easy installation, you can run the following command to install numpy and matplotlib. Scipy is also used for statistical analysis, but it's a part of the scientific Python ecosystem, which usually includes numpy and matplotlib.

```bash
pip install numpy matplotlib scipy
```

## Project Structure

The project consists of the following Python files:

- **molecule.py:** This file defines the `Molecule` class, which represents an individual molecule in the simulation. It contains methods for handling hopping, calculating coordinates, updating values, and checking loss and capture probabilities.

- **model.py:** The `Model` class in this file represents the overall simulation model. It handles generating all the molecules and running the simulation on each until they are all trapped or captured.

- **results.ipynb** This Jupyter Notebook contains code cells that run the simulation and visualize the results in different ways. It uses the Model class from the `model.py` file to do so.

## How to Run the Simulation

**Simulation Configuration**

The simulation will be executed with the default settings, including:

- 1000 molecules
- Moon-like conditions (radius, mass, and gravity)
- A predefined capture percentage based on latitude.

**Customization**

You have the flexibility to modify the simulation parameters within the `model.py` file. By changing the values in the `Model` class constructor, you can tailor the simulation to your specific needs. The parameters you can customize include:

- Number of molecules
- Radius
- Mass
- Gravity

It's also possible to customize the photodestruction time scale and capture percentages in the `molecule.py` file. It's currently set to default values derived from the papers but there are other examples given of models that could be run.

**Example Usage**

To run the simulation multiple times and analyze the results, you can use the following code in a Jupyter Notebook or Python script:

```python
from model import Model

model = Model(1000, RADIUS_MOON, MASS, GRAVITY)
model.run_simulation() 
```
This code will run the simulation once but there is more code in the report.ipynb which demostrates how to use this code further including running the simulation multiple times, collecting the captured percentages, and displaying a histogram of the results with a normal distribution curve.

Enjoy exploring the behavior of molecules on the planetary surface through this simulation!

## Limitations

The primary limitation of this model is complexity. I chose to focus on creating well-documented code for this project and that in turn meant that I needed to write code that was well explored and commented. With the time constraints of the project, I prioritized creating the simpler model from the 93 paper and adding one feature from the 97 paper which is where the capture regions for each latitude comes in. One example of a feature that would have been good to implement was the temperature distribution based on latitude. Additionally I feel there was a lot of way to handle the coordinates and the way I chose may not be the exact method the paper used. 

I wanted to share a second method I was using to determine the coordinates by converting to cartesian for the calculations and the converting back to spherical coordinates.

```python
    # these first two functions are implementing common methods for converting between the two coordinates
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
        # These first few lines are used to calculate variables which will be needed as inputs into
        # later functions.
        velocity = self.calculate_velocity()
        hop_time = self.calculate_hop_time(velocity)

        # This runs the check on whether or not a molecule is lost. If it is it's no longer a part
        # of the simulation and the function returns prior to doing any calculations on future
        # coordinates.
        self.check_for_loss(hop_time)
        if self.state == "Lost":
            return

        # Convert current spherical coordinates to Cartesian coordinates
        x, y, z = self.spherical_to_cartesian()

        # Update the Cartesian coordinates based on the distance
        hop_distance = velocity * hop_time / 2
        x1 = x + hop_distance * np.sin(self.inclination) * np.cos(self.azimuth)
        y1 = y + hop_distance * np.sin(self.inclination) * np.sin(self.azimuth)
        z1 = z + hop_distance * np.cos(self.inclination)

        # Convert the updated Cartesian coordinates back to spherical coordinates
        new_azimuth, new_inclination, new_radius = self.cartesian_to_spherical(x1, y1, z1)
        print(new_azimuth, self.azimuth)
        # Update the molecule's attributes
        self.azimuth = new_azimuth
        self.inclination = new_inclination

        # After coordinates are updates, the check on capture is run using the new coordinates.
        self.check_for_capture()
```
This code was originally included in the Molecule class to handle updating position but something I ran into was that the radius would constantly change and I wasn't able to identify a method of updating the spherical coordinates without simply moving along the radial line. 

There are certainly other limitations as well such as choosing the keep velocity and hop_time constant instead of implementing the more complicated distributions of the 97 paper but given more time, those are the two things I would go back and include for sure. 

A non-modeling related limitation to my code is that the photodestruction time scale and capture percentages need to be changed within the source file rather than as a variable fed into the simulation. That's definitely something I'd like to go back and fix to make the code a bit easier to run.

## Sources
- "Mercury: Full- Disk Radar Images and the Detection and Stability of Ice at the North Pole" by Butler, Muhleman and Slade, 1993
- "The migration of volatiles on the surfaces of Mercury and the Moon." by Butler 1997
- "The Behavior of Volatiles on the Lunar Surface" by Watson et al. 1961