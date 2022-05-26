"""
Command line interface used to run more advanced experiments than a simple simulation.
"""

import argparse
import json
import os
import sys
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from simulator.Simulator import Simulator
from simulator.SimulatorConfiguration import SimulatorConfiguration

SAVED_SIMULATION_PATH = 'output/saved_simulations/'
SIMULATION_RESULT_PATH = 'output/simulation_results/'
PLOT_PATH = 'output/plots/'
EXPERIMENT_CONFIG_PATH = 'experiment_configs/'

current_timestamp = datetime.now().strftime("%m_%d_%Y-%H_%M_%S")


parser = argparse.ArgumentParser(description='Run Experiment')
parser.add_argument('config_file', metavar='c', type=str,
                    help='The name of the configuration file that defines the experiment')

parsed_args = parser.parse_args(sys.argv[1:])

# load the experiment configuration data
experiment_config = json.loads(open(EXPERIMENT_CONFIG_PATH, 'r'))


# run the experiments

# go through each simulation configuration
final_result = {}
histogram = np.zeros(len(experiment_config.simulation_config_files))

for index, simulation_config in enumerate(experiment_config.simulation_config_files):
  name = simulation_config
  config = SimulatorConfiguration.build_configuration_from_file(
      simulation_config + '.json')
  
  results = []

  for i in range(experiment_config.num_repetitions):
    simulator = Simulator(config)    
  
  




