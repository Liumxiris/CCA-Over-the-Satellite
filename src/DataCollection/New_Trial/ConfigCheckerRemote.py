# This is the script to check glomma system configurations
# TODO: Add more checking / testings to this file

from CommandWrapper import CommandWrapper
import re, configparser, inspect, glob

# Initialize cmd instance
cmd = CommandWrapper()

# To mark test functions
def TEST(function):
    function.__is_test__ = True
    return function

class TestFailException(Exception):
    """
    Exception raised for failing customized tests
    """

    def __init__(self, reason=""):
        self.message = reason
        super().__init__(self.message)

    def __str__(self):
        return f'Test Failed for: {self.message}'

# To execute all test methods in a class
def executeAllTestMethods(instance):
    methods = (getattr(instance, name) for name in dir(instance))
    tests_failed = []
    for method in methods:
        if getattr(method, "__is_test__", False): # Third argument: default value to return if 2nd argument does not exists
            try:
                method()

            except TestFailException:
                tests_failed.append(method.__name__)

            except Exception:
                # TODO: ADD MORE STUFF HERE?
                return False

    if len(tests_failed):
        print("These tests failed", tests_failed)
        return False

    return True

class RemoteConfigurationChecker:

    def __init__(self):
        # Read in conf file
        self.config = configparser.ConfigParser()
        configFile = glob.glob('*.machine_config')[0]
        self.config.read(configFile)

    @TEST
    def checkAndSetTCP(self):

        TCPS = dict(self.config.items("TCP"))
        mem = TCPS["net.ipv4.tcp_mem"]
        wmem = TCPS["net.ipv4.tcp_mem"]
        rmem = TCPS["net.ipv4.tcp_mem"]
        cc = TCPS["net.ipv4.tcp_congestion_control"]

        TCP_SET_COMMAND = ' && '.join([
            f"sudo sysctl -w net.ipv4.tcp_mem='{mem} {mem} {mem}'",
            f"sudo sysctl -w net.ipv4.tcp_wmem='{wmem} {wmem} {wmem}'",
            f"sudo sysctl -w net.ipv4.tcp_rmem='{rmem} {rmem} {rmem}'",
            f"sudo sysctl -w net.ipv4.tcp_congestion_control='{cc}'"])

        try:
            cmd.execute("TCP_SET_COMMAND", verbose=True)
        except:
            raise TestFailException(f"Set TCP Failed")

    @TEST
    def demo_check(self):
        check_command = "1" in "1"
        CHECKING = check_command
        if not CHECKING:
            raise TestFailException(f"{check_command} failed") # If here, test not passed

        # If Here, test passed

    # IF NO @TEST MARK, WILL NOT EXECUTE
    def demo_check0(self):
        raise ValueError("Hey!")
        pass


# RUN TEST AUTOMATICALLY
print(executeAllTestMethods(RemoteConfigurationChecker()))





