from turtle import distance, pos

import numpy as np

from entities.Agent import Agent


class TargetArea:
  """
  Class representing the target area.
  """

  def __init__(self, position: np.ndarray, size: float) -> None:
    """
    Constructs a target area having a certain position and velocity.
    """
    self.position: np.ndarray = position
    self.size: float = size

  
  def get_position(self):
    return self.position

  def get_size(self):
    return self.size

  def contains_agent(self, agent: Agent) -> bool:
    """
    Returns true if the target area contains the provided agent, false otherwise.
    """
    distance_between_centers = np.linalg.norm(self.position - agent.get_position())

    return distance_between_centers <= self.size - agent.get_size()
  
  
