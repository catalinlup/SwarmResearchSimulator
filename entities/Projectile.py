import numpy as np

from entities.Agent import Agent


class Projectile:
  """
  Represents a projectile.
  """

  def __init__(self, size: float, init_pos: np.ndarray, velocity: np.ndarray, init_tick: int, lifetime_ticks: int) -> None:
    """
    Constructs a projectile.

    size - the size of the projectile
    init_pos - the initial position of the projectile
    velocity - the velocity of the projectile (constant velocity)
    init_tick - the tick at which the projectile was spawned
    lifetime_ticks - how many ticks this projectile will survive
    """
    self.size = size
    self.position = init_pos
    self.velocity = velocity
    self.init_tick = init_tick
    self.lifetime_ticks = lifetime_ticks
    self.active = True

  
  def process(self, current_tick: int, delta_time: float):
    """
    Processes the state of the projectile each tick.
    """
    if current_tick - self.init_tick > self.lifetime_ticks:
      self.active = False
      return
    
    self.position += self.velocity * delta_time
  
  def get_position(self) -> np.ndarray:
    """
    Returns the position of the projectile
    """
    return self.position
  
  def get_velocity(self) -> np.ndarray:
    """
    Returns the velocity of the projectile
    """
    return self.velocity

  
  def is_in_collision_with(self, agent: Agent) -> bool:
    """
    Returns true if the projectile is in collision with the provided agent, false otherwise
    """

    center_distance = np.linalg.norm(agent.get_position() - self.position)

    return center_distance < self.size + agent.get_size()

  
  def is_active(self) -> bool:
    """
    Returns true if the projectile is active, false otherwise.
    """
    return self.active


  


    


