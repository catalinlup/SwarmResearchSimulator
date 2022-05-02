from simulator.Environment import Environment
from simulator.SimulatorConfiguration import SimulatorConfiguration


class Simulator:
  """
  Class encoding the problem simulator.
  """

  def __init__(self, configuration: SimulatorConfiguration) -> None:
    """
    Initializes a simulator using the provided configuration.
    """
    self.configuration = configuration


  

  def run(self):
    """
    Generator function that runs the simulation, yielding a summary of the environment each tick.
    """

    # build the initial environment
    env: Environment = self.configuration.build_environment()

    yield env.to_summary()

    # extract the max ticks
    max_ticks = self.configuration.get_max_ticks()

    # run the simulation for the provided number of ticks
    for tick in range(max_ticks):
      env.process(tick)

      yield env.to_summary()


