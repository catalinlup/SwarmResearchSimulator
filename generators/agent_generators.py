import numpy as np
from entities.Agent import Agent

"""
Contains agent generator functions
"""


from entities.MapStructure import MapStructure


def basic_agent_generator(swarm_distance: float, map_structure: MapStructure, agent_size: float, agent_acc_limit: float, agent_perception_distance: float, num_agents: int):
  agents = []

  min_pos_y = 0
  max_pos_y = map_structure.get_map_height()
  min_pos_x = map_structure.get_danger_area_width()
  max_pos_x = map_structure.get_danger_area_width() + map_structure.get_safe_area_width()

  for i in range(num_agents):
    x_pos = np.random.uniform(min_pos_x, max_pos_x)
    y_pos = np.random.uniform(min_pos_y, max_pos_y)

    agents.append(Agent(np.array([x_pos, y_pos]), np.zeros(2), agent_size, agent_acc_limit, f'agent_{i + 1}', agent_perception_distance))

  return agents


def retrieve_agent_generator(generator_name: str):
  """
  Retrieves the right generator based on the provided generator name
  """

  if generator_name == 'basic':
    return basic_agent_generator

  return lambda x, y: []
