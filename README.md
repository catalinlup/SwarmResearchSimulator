# Predator-Prey Swarm Silumator

This simulator tool and framework was created to support research into swarm-control algorithms as part of a research project entitled 'Robust distributed swarming of wheeled mobile robots'. The research was conducted as part of a TU Delft course for a duration of 2 months, i.e. May and June 2022. 

The tool's purpose is to allow users to test, visualize and benchmark various swarm control algorithms in the context of a predator-prey game. Information about the problem and the already implemented algorithms can be found in the associated paper: 'http://resolver.tudelft.nl/uuid:06baf67a-5725-4e4a-bebb-a3bf60dcc25b'

## Dependencies

The simulator requires 'python3' and a few pyton libraries in order to run. The list of libraries can be found in the 'requirements.txt' file.

## Installation

No installation is required to run the simulator


## Overview of the problem

![Research Poster](./poster.png)


## Simulator

### Running a simulation


Simulations are generated based on configuration files, which define the parameters of the problem instance to be simulated. This includes, the number of obstacles, the generation method for obstacles, the position and size of the target area, the number of prey agents (swarm agents) and their control algorithm, the number of predator agents (projectiles) and their control algorithm, etc. The configuration files are stored in the 'simulator_configs' folder. If you want to create new types of simulations, feel free to create new configuration files in that folder.

Use the script 'simulate.py' to generate simulations.

Use:

```
  python3 simulate.py <name_of_config_file>.json --sim_name <name_of_the_simulation> --save
```

The simulation results can be found in the folder 'output/simulation_results'.

### Running an experiment

An experiment consists of one or multiple simulation instances that are run a certain number of times for the purpose of benchmarking. An experiment is generated based on a configurarion file, which defines what type of simulations should take part in the experiment, how many times the simulations should be repeated, as well as which simulations should be saved (so they can be visualized). These configuration files are found in the 'experiment_configs' folder. Additional experimental configurations can be added by the user.

Use the script 'simulate.py' to run experiments.

Use:
```
  python3 simulate.py <name_of_experiment_config_file>.json --sim_name <name_of_the_experiment> --experiment --plot
```

The experiment results can be found in json format in 'output/experiment_results' and in image/plot format in 'output/plots'.



### Visualizing a simulation

You can visualize simulations using the associated web-based visualization tool.

Use the following command to start the visualization tool:

```
./start_visualization_server.[sh|bat]
```

You can now navigate to 'localhost:5000', to access the tool.


### Adding a new control algorithms.

New control algorithms can be added by creating the corresponding classes, either in the 'swarm_agents' folder (for prey control algorithms) and in the 'projectiles' folder (for predator control algorithms). The newly created classes should inherit the 'Agent' class. To the new agent move, at least one of the following methods should be overriden '_compute_velocity', which computes the velocity of the agent each tick and '_compute_acceleration', which performs the same operation, but for the acceleration. 

Once a new control algorithm was created, a corresponding generator (function that tell the framework how to initialize the swarm of agents) should be added. Generators for 'prey agents' are added in the 'generators/agent_generators.py' file, while the ones of the predator inside 'generators/projectile_generators.py'. You can follow the model in those file to learn how to add a new generator.


