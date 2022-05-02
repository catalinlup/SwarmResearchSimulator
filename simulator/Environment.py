from copy import deepcopy
from typing import List

import numpy as np
from entities.Agent import Agent, AgentPerception
from entities.MapStructure import MapStructure
from entities.Obstacle import Obstacle
from entities.Projectile import Projectile
from entities.TargetArea import TargetArea


class Environment:
  """
  Stores the environment at a particular moment in time
  """

  def __init__(self, swarm_agents: List[Agent], projectile_generator, obtsacles: List[Obstacle], target_area: TargetArea, map_structure: MapStructure, delta_time: float, max_ticks: int = -1) -> None:
    """
    Initializes an environment, containing the provided swarm agents, projectiles, obstacles and target area.
    """
    self.swarm_agents = swarm_agents

    # functions used to generate projectiles based on tick
    self.projectile_generator = projectile_generator
    self.projectiles = projectile_generator(-1)
    self.obstacles = obtsacles
    self.target_area = target_area
    self.delta_time = delta_time

    self.map_structure = map_structure

    # stores the number of agents that have reached the target area
    self.num_agents_that_reached_target_area = 0

    # stores the tick at which the first agent achieved the timestamp
    self.first_agent_reaches_objective_timestamp = -1

    # stores the tick at which the last agent achieved the timestamp
    self.last_agent_reaches_objective_timestamp = -1

    # the last tick that was processed
    self.last_tick = -1

    # stores the number of ticks the simulation should go for
    self.max_ticks = max_ticks

    # stores whether or not the simulation has finished
    self.simulation_finished = False


  def _process_swarm_movement(self, current_tick: int):
    """
    Process the movement of the swarm agents.
    """

    perceived_agents = deepcopy(self.swarm_agents)

    # lambda functions used to filter the projectiles that are seen by the agent.
    def filter_projectiles_within_distance(pos, dist): return list(filter(
        lambda p: np.linalg.norm(pos - p.get_position()) <= dist, self.projectiles))

    for swarm_agent in self.swarm_agents:


      perceived_projectiles = filter_projectiles_within_distance(swarm_agent.get_position(), swarm_agent.get_perception_distance())

      agent_perception = AgentPerception(
          self.obstacles, perceived_agents, self.target_area, perceived_projectiles)

      swarm_agent.process(current_tick, self.delta_time, agent_perception)

  
  def _process_projectile_movement(self, current_tick: int):
    """
    Process the movement of the projectiles
    """

    perceived_agents = deepcopy(self.swarm_agents)

    for projectile in self.projectiles:
      projectile.process(current_tick, self.delta_time, perceived_agents)

    
    # remove the projectiles that are no longer active
    filtered_projectiles = list(filter(lambda p: p.is_active()), self.projectiles)
    self.projectiles = filtered_projectiles
  

  def _process_movement(self, current_tick: int):
    """
    Process the movement of all objects (swarm agents and projectiles) in the environment.
    """
    self._process_swarm_movement(current_tick)
    self._process_projectile_movement(self, current_tick)


  def _has_collided_with_obstacles(self, agent: Agent) -> bool:
    """
    Returns true if the provided agent has collided with some obstacle, false otherwise.
    """

    for obstacle in self.obstacles:
      if obstacle.is_in_collision_with(agent):
        return True
    
    return False

  
  def _has_collided_with_projectiles(self, agent: Agent) -> bool:
    """
    Returns true if the provided agent has collided with some obstacles, false otherwise
    """

    for projectile in self.projectiles:
      if projectile.is_in_collision_with(agent):
        return True
    
    return False

  def _process_collision(self):
    """
    Removes the agents that have collided with some obstacles
    """

    alive_agents = []

    for swarm_agent in self.swarm_agents:
      if not self._has_collided_with_obstacles(swarm_agent) and not self._has_collided_with_projectiles(swarm_agent):
        alive_agents.append(swarm_agent)
    
    self.swarm_agents = alive_agents
  

  def _process_target_area(self, current_tick: int) -> None:
    """
    Processes the events corresponding to the agents reaching the target area.
    """

    agents_still_not_reached = []

    for swarm_agent in self.swarm_agents:
      if self.target_area.contains_agent(swarm_agent):
        
        # increment the number of agents that have reached the target area
        self.num_agents_that_reached_target_area += 1
        # update the timestamps
        if self.first_agent_reaches_objective_timestamp < 0:
          self.first_agent_reaches_objective_timestamp = current_tick
        
        self.last_agent_reaches_objective_timestamp = current_tick
      
      # if the agent has not yet reached the target area, keep the agent
      else:
        agents_still_not_reached.append(swarm_agent)
    
    self.swarm_agents = agents_still_not_reached
  

  def _process_simulation_status(self) -> None:
    """
    Processes the status of the simulation.
    """

    if self.last_tick + 1 >= self.max_ticks or len(self.swarm_agents) == 0:
      self.simulation_finished = True
        

  def process(self, current_tick: int) -> None:
    """
    Processes the eveolution of the environment.
    """

    self.last_tick = current_tick

    # generate new projectiles
    self.projectiles += self.projectile_generator(self.last_tick)

    self._process_movement(current_tick)
    self._process_collision()
    self._process_target_area(current_tick)
    self._process_simulation_status()

  
  def to_summary(self) -> dict:
    """
    Returns a dictionary representation of the environment, 
    summerizing all relevant data about the current state of the environment.
    """

    return {
      'header': {
          'simulation_finished': self.simulation_finished,
          'last_tick': self.last_tick,
          'max_ticks': self.max_ticks,
          'delta_time': self.delta_time,
      },

      'structure': {
        'map_structure': self.map_structure.to_summary(),
        'target_area': self.target_area.to_summary(),
        'obstacles': [obst.to_summary() for obst in self.obstacles],
        'projectiles': [proj.to_summary() for proj in self.projectiles],
        'swarm_agents': [ag.to_summary() for ag in self.swarm_agents],
      }
    }


    


    


