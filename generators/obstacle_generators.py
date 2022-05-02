"""
Contains obstacle generator functions
"""
import numpy as np
from entities.MapStructure import MapStructure
from entities.Obstacle import Obstacle


def basic_obstacle_generator(map_structure: MapStructure, obstacle_min_size: float, obstacle_max_size: float, num_obstacles: int):
  """
  Generates obstacles obstacles in the danger area.
  """

  min_pos_y = 0
  max_pos_y = map_structure.get_map_height()

  min_pos_x = map_structure.get_danger_area_width() / 4
  max_pos_x = map_structure.get_danger_area_width()

  obstacles = []

  for _ in range(num_obstacles):
    pos_y = np.random.uniform(min_pos_y, max_pos_y)
    pos_x = np.random.uniform(min_pos_x, max_pos_x)
    size = np.random.uniform(obstacle_min_size, obstacle_max_size)

    obstacles.append(Obstacle(np.array([pos_x, pos_y]), size))


  return obstacles



def retrieve_obstacle_generator(generator_name: str):
  """
  Retrieves the right generator based on the provided generator name
  """

  if generator_name == 'basic':
    return basic_obstacle_generator

  return lambda x: []
