# This is the script to check glomma system configurations
# TODO: Add more checking / testings to this file

from CommandWrapper import CommandWrapper
import re, configparser, inspect

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

class GlommaConfigurationChecker:

    def __init__(self):
        # Read in conf file
        self.config = configparser.ConfigParser()
        self.config.read("./glomma.machine_config")

    @TEST
    def checkIPRoute(self):
        """
        Test For Check and Fix Routes
        !!! Up and low case senstive for ip route show
        """
        try:
            IPS = dict(self.config.items("IPS"))

            route_checking_command = "ssh glomma.cs.wpi.edu 'ip route show'"
            out = cmd.executeOneSSHCommand("yliu31@cs.wpi.edu", route_checking_command, getOut=True)[0]

            ip_prefix = re.compile("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) via .*? dev eno2")
            links = ip_prefix.findall(out)

            for mlcip in IPS:
                if IPS[mlcip] not in links:
                    cmd.execute("./setup_routes.sh", verbose=True)
                    break
        except:
            check_command = "checkIPRoute"
            raise TestFailException(f"{check_command} failed")


    @TEST
    def checkSSHAgents(self):
        """
        Test For Checking if automatically added ssh-agent and can build ssh without password
        """

        # Check Satellite
        try:
            out = self.cmd.executeOneSSHCommand(host="root@192.168.1.1",
                                                command=f"echo 'TEST'",
                                                getOut=True, raiseOnError=True)[0]

            assert ("TEST" in out)
        except:
            raise TestFailException(f"SSH Satellite failed")



        # Check MLC
        IPS = dict(self.config.items("IPS"))

        for mlcip in IPS: # Will read in "mlcnetx.cs.wpi.edu"
            try:
                out = self.cmd.executeOneSSHCommand(host=mlcip,
                                                    command=f"echo 'TEST'",
                                                    getOut=True, raiseOnError=True)[0]

                assert ("TEST" in out)
            except:
                raise TestFailException(f"SSH {mlcip} failed")

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
print(executeAllTestMethods(GlommaConfigurationChecker()))





