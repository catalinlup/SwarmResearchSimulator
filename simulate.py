from simulator.Simulator import Simulator
from simulator.SimulatorConfiguration import SimulatorConfiguration

config = SimulatorConfiguration.build_configuration_from_file('test.json')

simulator = Simulator(config)

for env in simulator.run():
  print(env)
