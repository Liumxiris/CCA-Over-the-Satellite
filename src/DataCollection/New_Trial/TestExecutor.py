import argparse # System imports

from SetupWorker import SetupWorker
from ExperimentExecutor import ExperimentExecutor

# Setup Phase
# Read command line arguments
parser = argparse.ArgumentParser(description='Main Executor For TCP Experiments Via Satellite')

config_group = parser.add_mutually_exclusive_group(required=True)
config_group.add_argument('--configpath', '-C', type=str, action="store", dest = "CONFIG_PATH",
                    help='Specify to use a specific configuration file for experiment. If not specified, then system will use default values')
config_group.add_argument('--name', '-N', type=str, action="store", dest = "TESTNAME", help="Name of The Test")

args = parser.parse_args()

# Pass command arguments to setup worker to build global parameters
setupWorker = SetupWorker()
assert (setupWorker.setup(args) == True)
global_params = setupWorker.getGlobalParameters()

# After setup, do experiment
experimentWorker = ExperimentExecutor(global_params)
# experimentWorker.start()

#  use screen session number to check if session terminates (if successfully runned)