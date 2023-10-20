from omega2auto import omega2auto
import sys
import logging

from pyauto.visualizer import visualizer
from pyauto.models.scenario import Scenario

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")

scenarios = omega2auto.convert(sys.argv[1], hertz=5, start_offset=20, end_offset=20.3, folder="/home/lwesthofen/Dokumente/VVMethoden/SCMs/pyauto/src/pyauto/auto")
scenarios[0].save_abox("/tmp/fka/01/scenario.owl")
visualizer.visualize(scenarios[0])
#loaded = Scenario(folder="/home/lwesthofen/Dokumente/VVMethoden/SCMs/pyauto/src/pyauto/auto", file="/tmp/fka/00/scenario.kbs", hertz=5)
#visualizer.visualize(loaded)

# TODO successor lanes?
# TODO visualization ped. crossing