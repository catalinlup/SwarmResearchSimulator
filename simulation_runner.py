"""
Contains a function used to run a simulation based on simulation configs.
"""

import argparse
import json
import os
import sys
from datetime import datetime

import numpy as np

from NpEncoder import NpEncoder
from paths import *
from simulator.Simulator import Simulator
from simulator.SimulatorConfiguration import SimulatorConfiguration


def remove_extension(filename: str) -> str:
  """
  Removes the '.' extension from a file name
  """

  if '.' not in filename:
    return filename
  
  return filename.split('.')[0].strip()


def get_current_timestamp() -> str:
  """
  Return the current timestamp. 
  """
  return datetime.now().strftime("%m_%d_%Y-%H_%M_%S")


def save(name: str, json_data: dict, path: str):
  """
  SAves the provided json_data at the specified path.
  """
  with open(os.path.join(path, f'{name}.json'), 'w') as f:
    json.dump(json_data, f, cls=NpEncoder, indent=4)

def save_simulation_envs(name: str, simulation_envs: dict):
  """
  Saved the provided simulations envs object with the provided name.
  """
  save(name, simulation_envs, SAVED_SIMULATION_PATH)

  # with open(os.path.join(SAVED_SIMULATION_PATH, f'{name}.json'), 'w') as f:
  #   json.dump(simulation_envs, f, cls=NpEncoder, indent=4)



def save_results(name: str, results: dict):
  """
  Saves the results of a simulation
  """
  save(name, results, SIMULATION_RESULT_PATH)
  # with open(os.path.join(SIMULATION_RESULT_PATH, f'{name}.json'), 'w') as f:
  #   json.dump(results, f, cls=NpEncoder, indent=4)


def save_experiment_results(name: str, results):
  """
  Saves the results of an experiment.
  """
  save(name, results, EXPERIMENT_RESULTS_PATH)



def run_experiment(experiment_config: dict):
  """
  Runs an experiment involving averaging multiple simulations
  """

  final_result = {
    'name': experiment_config['experiment_name'],
    'timestamp': get_current_timestamp(),
    'config_files': experiment_config['simulation_config_files'],
    'names': [remove_extension(file) for file in experiment_config['simulation_config_files']],
    'num_repetitions': experiment_config.num_repetitions,
    'avg_agent_success': [],
    'avg_time': [],
    'avg_delta_time': []
  }

  avg_agent_success_histogram = np.zeros(
      len(experiment_config['simulation_config_files']))
  avg_time_histogram = np.zeros(
      len(experiment_config['simulation_config_files']))
  avg_delta_time = np.zeros(
      len(experiment_config['simulation_config_files']))



  for sim_config_index, simulation_config in enumerate(experiment_config['simulation_config_files']):
    name = remove_extension(simulation_config)

    num_repetitions = experiment_config['num_repetitions']

    # add the results from the simulations
    for index in range(1,  num_repetitions + 1):
      simulation_output, simulation_envs = run_simulation(name + '_' + str(index), simulation_config)

      if index in experiment_config['saved_repetitions']:
        save_simulation_envs(name + "_" + str(index), simulation_envs)
      

      # update the histograms
      avg_agent_success_histogram[sim_config_index] += (float(simulation_output['result']['num_agents_reached_target']) / float(simulation_output['result']['num_agents']))
      avg_time_histogram[sim_config_index] += float(simulation_output['result']['total_time'])
      avg_delta_time[sim_config_index] += float(
          simulation_output['result']['delta_time_target'])

    # compute the average results
    avg_agent_success_histogram[sim_config_index] /= num_repetitions
    avg_time_histogram[sim_config_index] /= num_repetitions
    avg_delta_time[sim_config_index] /= num_repetitions
  

  # update the final results with the value of the histograms
  final_result['avg_agent_success'] = list(avg_agent_success_histogram)
  final_result['avg_time_histogram'] = list(avg_time_histogram)
  final_result['avg_delta_time'] = list(avg_delta_time)

  return final_result

    


def run_simulation(sim_name: str, config_file_name_json: str):
  """
  Function used to run one instance of a simulation.

  sim_name - the name of the simulation
  config_file_name - the name of the configuration file (with the .json extension included)
  """

  current_timestamp = get_current_timestamp()

  config = SimulatorConfiguration.build_configuration_from_file(config_file_name_json)

  simulator = Simulator(config)

  simulation_output = {
      'name': sim_name,
      'timestamp': current_timestamp,
      'associated_config_file': config_file_name_json,
      'result': {}
  }

  saved_environments = {
      'name': sim_name,
      'timestamp': current_timestamp,
      'associated_config_file': config_file_name_json,
      'environments': []
  }

  for env in simulator.run():
    saved_environments['environments'].append(env)


  # save the simulation result
  simulation_output['result'] = simulator.get_last_result()

  return simulation_output, saved_environments
