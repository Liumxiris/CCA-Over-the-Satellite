import configparser, socket
import CommandWrapper
# To generate system configuration files to set and check system configurations on experiment machines
# Should be executed on a machine that knows about MLC and Glomma ip addresses

class SysConfGenerator:

    # Simple way to define singleton in a process
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if SysConfGenerator.__instance == None:
            SysConfGenerator()
        return SysConfGenerator.__instance

    def __init__(self, GLOBAL_PARAMETERS):

        # Check singleton
        if SysConfGenerator.__instance != None:
            raise RuntimeError("Trying To Construct Extra SysConfGenerator in Setup Phase")
        else:
            SysConfGenerator.__instance = self

        if type(GLOBAL_PARAMETERS) != dict:
            raise ValueError(f"SysConfGenerator: Initialization: Expected Type {dict} But Got Type {type(GLOBAL_PARAMETERS)}")
        self.confParams = GLOBAL_PARAMETERS

    def generateGlommaSysConf(self):
        # configparser instance
        config = configparser.ConfigParser()

        # Experiment Related System Configurations
        config["EXPERIMENT_GENERAL"] = {
            "MACHINE_NAME": "Glomma",
            "EXPERIMENT_NAME": self.confParams["EXPERIMENT_NAME"],
            "EXPERIMENT_DIR_GLOMMA": self.confParams["EXPERIMENT_DIR_GLOMMA"],
            "PROXY_MODES": ', '.join(self.confParams["PROXY_MODES"])
        }

        # For each machine_protocol, create the remote sysconf file
        config["IPS"] = {}
        for machine_protocol in self.confParams["MACHINE_PROTOCOLS"]:
            machine = machine_protocol[0]
            machine_ip = self.__getIP__(machine)
            config["IPS"][f"{machine}"] = machine_ip

        # Trial Related System Configurations
        data_round_strs = []
        for data_round in self.confParams["DATA_SIZE_AND_ROUNDS"]:
            data_round_strs.append(f"{data_round[0]}_{data_round[1]}")

        config["EXPERIMENT_TRIAL"] = {
            'UDPING_FLAG': self.confParams["UDPING_FLAG"],
            'VERBOSE': self.confParams["VERBOSE"],
            'DATA_SIZE_AND_ROUNDS': ', '.join(data_round_strs)
        }

        # TCP Related System Configurations
        config["TCP"] = {
            "net.ipv4.tcp_mem": self.confParams["WMEM"],
            "net.ipv4.tcp_wmem": self.confParams["WMEM"],
            "net.ipv4.tcp_rmem": self.confParams["WMEM"],
            "net.ipv4.tcp_congestion_control": "cubic"
        }

        with open(f'{self.confParams["EXPERIMENT_DIR_LOCAL"]}/glomma.machine_config', 'w') as configfile:
            config.write(configfile)

    def generateMlcSysConf(self):
        try:
            # For each machine_protocol, create the remote sysconf file
            for machine_protocol in self.confParams["MACHINE_PROTOCOLS"]:
                machine = machine_protocol[0]
                protocol = machine_protocol[1]

                # configparser instance
                config = configparser.ConfigParser()

                # Experiment Related System Configurations
                config["EXPERIMENT"] = {
                    "MACHINE_NAME": machine,
                    "EXPERIMENT_NAME": self.confParams["EXPERIMENT_NAME"],
                    "EXPERIMENT_DIR_REMOTE": self.confParams["EXPERIMENT_DIR_REMOTE"],
                    "GLOMMA_IP":""
                }

                # TCP Related System Configurations
                config["TCP"] = {
                    "net.ipv4.tcp_mem":self.confParams["WMEM"],
                    "net.ipv4.tcp_wmem":self.confParams["WMEM"],
                    "net.ipv4.tcp_rmem":self.confParams["WMEM"],
                    "net.ipv4.tcp_congestion_control":protocol
                }

                with open(f'{self.confParams["EXPERIMENT_DIR_LOCAL"]}/{machine}.machine_config', 'w') as configfile:
                    config.write(configfile)

        except KeyError as error:
            errorType = type(error).__name__
            print(f"SysConfGenerator: Generating MLC SysConf: {errorType} Occured")
            print(f"Perhaps GLOBAL_PARAMETERS does not have field {error.args}")

    def __getIP__(self, hostname):
        # IP = socket.gethostbyname(hostname) # Can use socket also
        cmd = CommandWrapper.CommandWrapper()
        IP = cmd.execute(f"dig +short {hostname}")[0]

        return IP