
import numpy as np

from TargetArea import TargetArea


class AgentPerception:
  """
  Contains all of the objects that the agent is able to perceive.
  """

  def __init__(self, obstacles: list, swarm_agents: list, target_area: TargetArea) -> None:
    """
    Initializes an object storing the agents perception.
    """
    self.obstacles: list = obstacles
    self.swarm_agents: list = swarm_agents
    self.target_area: TargetArea = target_area

class Agent:
  """
  Abstract class implementing a generic swarm agent, without any logic associated to it.
  """

  def __init__(self, init_position: np.ndarray, init_velocity: np.ndarray, size: float, acc_limit: float, id: str) -> None:
    """
    Initializes the agent with the initial position, velocity, size, and acc_limit
    """
    self.position: np.ndarray = init_position
    self.velocity: np.ndarray = init_velocity
    self.size: float = size
    self.acc_limit: float = acc_limit
    self.id = id


  def process(self, current_tick: int, delta_time: float, agent_perception: AgentPerception):
    pass


  def _compute_velocity(self, current_tick: int, delta_time: float, agent_perception: AgentPerception):
    """
    Abstract method intended to compute the instant velocity of the swarm agent.
    It needs to be overriden in order to implement a strategy for the agents.
    """

  
  def get_position(self) -> np.ndarray:
    return self.position
  
  def get_velocity(self) -> np.ndarray:
    return self.velocity
  

  def get_size(self) -> np.ndarray:
    return self.size

  def get_id(self) -> np.ndarray:
    return self.id


  def _apply_velocity(self, target_velocity: np.ndarray) -> None:
    """
    Applies a new velocity to the swarm agent as long as the acceleration difference is smaller than the limit.
    """
    diff: float = np.linalg.norm(self.velocity - target_velocity)

    if diff <= self.acc_limit:
      self.velocity = target_velocity
    else:
      raise Exception(f'Cannot apply velocity. Acceleration too high! Limit: {self.acc_limit}, Actual: {diff}')

  
  def __repr__(self) -> str:
      return f'Agent(position: {list(self.position)}, velocity: {list(self.velocity)}, size: {self.size}, acc limit: {self.acc_limit}, id: {self.id})'




    
