from omega2auto import omega2auto
import sys
import logging

from pyauto.visualizer import visualizer
from pyauto.models.scenario import Scenario

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")

scenarios = omega2auto.convert(sys.argv[1], hertz=5, start_offset=10, end_offset=15, folder="/home/lwesthofen/Dokumente/VVMethoden/SCMs/pyauto/src/pyauto/auto")
scenarios[0].save_abox("/tmp/fka/00/scenario.owl")
visualizer.visualize(scenarios[0])
#loaded = Scenario(folder="/home/lwesthofen/Dokumente/VVMethoden/SCMs/pyauto/src/pyauto/auto", file="/tmp/fka/00/scenario.kbs", hertz=5)
#visualizer.visualize(loaded)

# TODO successor lanes?
# TODO Parking vehicle drivers
# TODO visualization ped. crossing