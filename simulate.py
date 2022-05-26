import argparse
import json
import os
import sys
from datetime import datetime

import numpy as np

from NpEncoder import NpEncoder
from simulation_runner import (run_simulation, save_experiment_results,
                               save_results, save_simulation_envs)

SAVED_SIMULATION_PATH = 'output/saved_simulations/'
SIMULATION_RESULT_PATH = 'output/simulation_results/'
PLOT_PATH = 'output/plots/'

## sort out the arguments.
current_timestamp = datetime.now().strftime("%m_%d_%Y-%H_%M_%S")


parser = argparse.ArgumentParser(description='Run simulation')
parser.add_argument('config_file', metavar='c', type=str, help='The name of the configuration file.')
parser.add_argument('--sim_name', metavar='n', default=current_timestamp, type=str, help='The name of the simulation instance.')
parser.add_argument('--save', default=False, action=argparse.BooleanOptionalAction)

parsed_args = parser.parse_args(sys.argv[1:])


# config = SimulatorConfiguration.build_configuration_from_file(
#     parsed_args.config_file)

# simulator = Simulator(config)

# simulation_output = {
#   'name': parsed_args.sim_name,
#   'timestamp': current_timestamp,
#   'associated_config_file': parsed_args.config_file,
#   'result': {}
# }

# saved_environments = {
#   'name': parsed_args.sim_name,
#   'timestamp': current_timestamp,
#   'associated_config_file': parsed_args.config_file,
#   'environments': []
# }

# for env in simulator.run():
#   saved_environments['environments'].append(env)
  

# # save the simulation result
# simulation_output['result'] = simulator.get_last_result()

simulation_output, saved_environments = run_simulation(
    parsed_args.sim_name, parsed_args.config_file)

## CUSTOM ENCODER



# save the simulation, if it is the case
if parsed_args.save:
  save_simulation_envs(parsed_args.sim_name, saved_environments)
  # with open(os.path.join(SAVED_SIMULATION_PATH, f'{parsed_args.sim_name}.json'), 'w') as f:
  #   json.dump(saved_environments, f, cls=NpEncoder, indent=4)

# save the results
# with open(os.path.join(SIMULATION_RESULT_PATH, f'{parsed_args.sim_name}.json'), 'w') as f:
#     json.dump(simulation_output, f, cls=NpEncoder, indent=4)

save_results(parsed_args.sim_name, simulation_output)
    





