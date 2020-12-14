# Setup Worker
import os, myutil, configparser, argparse
from SysConfGenerator import SysConfGenerator
from CommandWrapper import CommandWrapper

class SetupWorker:

    # Simple way to define singleton in a process
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if SetupWorker.__instance == None:
            SetupWorker()
        return SetupWorker.__instance

    def __init__(self):
        """
        Init supported fields
        """

        # Check singleton
        if SetupWorker.__instance != None:
            raise RuntimeError("Trying To Construct Extra SetupWorker in Setup Phase")
        else:
            SetupWorker.__instance = self

        # Supported Protocols
        self.supportedProtocols = {"BBR", "CUBIC", "HYBLA", "PCC"}

        # Supported self.supportedMachines [including acronym dictionary for conversion]
        self.supportedMachines = {
            "MLCA": "mlcneta.cs.wpi.edu",
            "MLCB": "mlcnetb.cs.wpi.edu",
            "MLCC": "mlcnetc.cs.wpi.edu",
            "MLCD": "mlcnetd.cs.wpi.edu",
            "mlcneta.cs.wpi.edu": "mlcneta.cs.wpi.edu",
            "mlcnetb.cs.wpi.edu": "mlcnetb.cs.wpi.edu",
            "mlcnetc.cs.wpi.edu": "mlcnetc.cs.wpi.edu",
            "mlcnetd.cs.wpi.edu": "mlcnetd.cs.wpi.edu"
        }

        # Supported Proxy Modes
        self.supportedProxies = {"1", "2", "3"}

        # Default Global Parameters
        self.GLOBAL_PARAMETERS = {
            "EXPERIMENT_NAME": "EXAMPLE_EXPERIMENT",
            "EXPERIMENT_DIR_LOCAL": "./experiment/EXAMPLE_EXPERIMENT/",
            "EXPERIMENT_DIR_GLOMMA":"./experiment/EXAMPLE_EXPERIMENT/",
            "EXPERIMENT_DIR_REMOTE":"./experiment/EXAMPLE_EXPERIMENT/",
            "MACHINE_PROTOCOLS": [["mlcneta.cs.wpi.edu", "cubic"]],
            "PROXY_MODES": ["2", "3"],
            "BDP": 15000000,
            "WMEM": 60000000,
            "UDPING_FLAG": False,
            "VERBOSE": False,
            "SETUP_REPORT": True,
            "DATA_SIZE_AND_ROUNDS": [["1G", "50"]]
        }

        self.__global_parameter_setted = False
        self.__finished_sysconf_generation = False
        self.local_dir = None
        self.mlc_dir = None
        self.glomma_dir = None
        self.glomma_addr = "glomma.cs.wpi.edu"
        self.args = None
        self.cmd = CommandWrapper()

    def __check_args__(self):
        if not self.args:
            raise RuntimeError("Setup Phase: Called Setup Global Parameters Before Reads In Arguments")

    def __setupGlobalParameters(self):
        '''
        Method to setup global parameters for trial
        '''

        self.__check_args__()

        # Read config file if specified. Else use default values.
        if self.args.CONFIG_PATH:
            if not os.path.isfile(self.args.CONFIG_PATH):
                raise FileNotFoundError("Setup Phase: Setup Global Parameters: Configuration file does not exists")

            config = configparser.ConfigParser()
            config.read(self.args.CONFIG_PATH)

            # Experiment name
            # TODO: Currently set up directory names based on experiment name, guess it should be fine
            # TODO: Else, read optional EXPERIMENT_DIR_* from set up configuration file
            self.GLOBAL_PARAMETERS["EXPERIMENT_NAME"] = config["GENERAL PARAMETERS"]["EXPERIMENT_NAME"]
            self.GLOBAL_PARAMETERS["EXPERIMENT_DIR_LOCAL"] = f"./experiment/{self.GLOBAL_PARAMETERS['EXPERIMENT_NAME']}"
            self.GLOBAL_PARAMETERS["EXPERIMENT_DIR_GLOMMA"] = f"$HOME/experiment/{self.GLOBAL_PARAMETERS['EXPERIMENT_NAME']}"
            self.GLOBAL_PARAMETERS["EXPERIMENT_DIR_REMOTE"] = f"$HOME/experiment/{self.GLOBAL_PARAMETERS['EXPERIMENT_NAME']}"

            # Process Machine Parameter in Configuration File.
            # Expected Format: MACHINE_PROTOCOLS = {MACHINE}_{PROTOCOL}, separated with comma
            MACHINE_PROTOCOLS = [x.strip() for x in config["GENERAL PARAMETERS"]["MACHINE_PROTOCOLS"].split(",")]
            MACHINE_PROTOCOLS = [x.split("_") for x in MACHINE_PROTOCOLS] # Split machine and protocol

            # Value checking for machine & protocols
            for m_p in MACHINE_PROTOCOLS:
                if m_p[0] not in self.supportedMachines:
                    raise ValueError(f"Machine {m_p[0]} is not a supported machine. Check parameters, or check supported list in TestExecutor.py")
                elif m_p[1] not in self.supportedProtocols :
                    raise ValueError(f"Protocol {m_p[1]} is not a supported protocol. Check parameters, or check supported list in TestExecutor.py")
                m_p[0] = self.supportedMachines[m_p[0]] # Convert acronyms to full remote names
            self.GLOBAL_PARAMETERS["MACHINE_PROTOCOLS"] = MACHINE_PROTOCOLS

            # Read proxy modes. Expected format: {PROXYMODE}, separated with comma
            PROXIES = [x.strip() for x in config["GENERAL PARAMETERS"]["PROXIES"].split(",")]

            for proxy in PROXIES:
                if proxy not in self.supportedProxies:
                    raise ValueError(f"Proxy mode {proxy} is not supported. Check parameters, or check supported list in TestExecutor.py")
            self.GLOBAL_PARAMETERS["PROXY_MODES"] = PROXIES

            # Other general parameters
            self.GLOBAL_PARAMETERS["BDP"] = int(config["GENERAL PARAMETERS"]["BDP"])
            self.GLOBAL_PARAMETERS["WMEM"] = int(myutil.NSP.eval(config["GENERAL PARAMETERS"]["WMEM"])) # Give up using python eval for security concerns

            # Trial related parameters
            self.GLOBAL_PARAMETERS["UDPING_FLAG"] = config["TRIAL PARAMETERS"].getboolean("UDPING")
            self.GLOBAL_PARAMETERS["VERBOSE"] = config["TRIAL PARAMETERS"].getboolean("VERBOSE")
            self.GLOBAL_PARAMETERS["SETUP_REPORT"] = config["TRIAL PARAMETERS"].getboolean("SETUP_REPORT")

            # Read proxy modes. Expected format: {DATASIZE_ROUND}, separated with comma
            DATA_SIZE_AND_ROUNDS = [x.strip() for x in config["TRIAL PARAMETERS"]["DATA_SIZE_AND_ROUNDS"].split(",")]
            for data_round in DATA_SIZE_AND_ROUNDS:
                if not myutil.DSRCHECKER.check(data_round):
                    raise ValueError(f"Datasize_round {data_round} is not supported. Check parameters.")
            DATA_SIZE_AND_ROUNDS = [x.split("_") for x in DATA_SIZE_AND_ROUNDS]  # Split datasize and rounds
            self.GLOBAL_PARAMETERS["DATA_SIZE_AND_ROUNDS"] = DATA_SIZE_AND_ROUNDS

        else:
            self.GLOBAL_PARAMETERS["EXPERIMENT_NAME"] = self.args.TESTNAME

        self.__global_parameter_setted = True
        print("Setup Phase: Global Parameters Set Up Completed")

    def getGlobalParameters(self):
        '''
        Return GLOBAL_PARAMETERS
        '''
        self.__check_args__()

        if not self.__global_parameter_setted:
            self.setupGlobalParameters()

        return self.GLOBAL_PARAMETERS

    def __setupLocalDirectory(self):
        '''
        Method to set up directory at local (where the command to start experiments is executed)
        '''
        self.__check_args__()

        if not self.__global_parameter_setted:
            self.setupGlobalParameters()

        if not os.path.exists(self.GLOBAL_PARAMETERS["EXPERIMENT_DIR_LOCAL"]):
            os.makedirs(self.GLOBAL_PARAMETERS["EXPERIMENT_DIR_LOCAL"])
            print(f"Setup Phase: Made A New Experiment Directory At {self.GLOBAL_PARAMETERS['EXPERIMENT_DIR_LOCAL']}")

        self.local_dir = self.GLOBAL_PARAMETERS["EXPERIMENT_DIR_LOCAL"]
        print("Setup Phase: Local Directory Setup Finished")

    def __setupRemoteDirectory(self):
        """
        Method to set up remote directories (in current version, MLCs + Glomma)
        """
        self.__check_args__()

        # Inner method for check and set a specific directory at host
        def __check_and_set_dir(host, dir_path, debug=False):
            # Inner worker method for check and set a specific sub path at host
            def __inner_worker(dir_path_inner):
                dir_checking_command = f"[ -d {dir_path_inner} ] && echo EXISTS || echo DNE"
                out, err = self.cmd.executeOneSSHCommand(host=host,
                                                         command=dir_checking_command,
                                                         getOut=True, raiseOnError=True)

                if "DNE" in out:
                    self.cmd.executeOneSSHCommand(host=host,
                                                  command=f"mkdir {dir_path_inner}",
                                                  raiseOnError=True)

            # Split the dir into subpaths
            dir_hierachy = dir_path.split("/")

            # Iterate over subpaths, and check_and_set them one by one
            current_dir = ""
            while len(dir_hierachy):
                subpath = dir_hierachy.pop(0) # Get current subpath
                if subpath == "$HOME": # Skip if home
                    current_dir += subpath
                    continue
                current_dir += ("/" + subpath) # Add subpath to current dir
                if debug:
                    print("Current Dir: ", current_dir)
                __inner_worker(current_dir) # Check and set the dir
        # End of Inner Method check_and_set_dir

        # Setup MLC dirs
        for m_p in self.GLOBAL_PARAMETERS["MACHINE_PROTOCOLS"]:
            machine = m_p[0]
            __check_and_set_dir(host=self.supportedMachines[machine], dir_path=self.GLOBAL_PARAMETERS['EXPERIMENT_DIR_REMOTE'])

        # Setup Glomma dir
        __check_and_set_dir(host=self.glomma_addr, dir_path=self.GLOBAL_PARAMETERS['EXPERIMENT_DIR_GLOMMA'])



        print("Setup Phase: Remote Directory Setup Finished")

    def __generateSysConfFiles(self):
        self.__check_args__()

        SCG = SysConfGenerator(self.GLOBAL_PARAMETERS)

        SCG.generateMlcSysConf()
        SCG.generateGlommaSysConf()

        self.__finished_sysconf_generation = True
        print("Setup Phase: System Configuration File Setup Finished")

    def __checkGlommaSysConf(self):
        self.__check_args__()

        if not self.__finished_sysconf_generation or not self.__global_parameter_setted:
            raise RuntimeError("Setup Phase: Called Check Glomma SysConf Before Generated It")

        glomma_sysconf_path = f'{self.GLOBAL_PARAMETERS["EXPERIMENT_DIR_LOCAL"]}/glomma.machine_config'

        # Check if can find Glomma configuration file at local
        if not os.path.isfile(glomma_sysconf_path):
            raise FileNotFoundError("Setup Phase: Check Glomma SysConf: Cannot find file. Bugs exists. "
                                    "Check Generate SysConf Command")

        # First scp over glomma system configuration file, config checker, and command wrapper which config checker needs
        self.cmd.executeOneSCPCommand(host=self.glomma_addr,
                                      localFilepath=glomma_sysconf_path,
                                      remoteFilepath=self.GLOBAL_PARAMETERS["EXPERIMENT_DIR_GLOMMA"],
                                      raiseOnError=True)
        self.cmd.executeOneSCPCommand(host=self.glomma_addr,
                                      localFilepath="./ConfigCheckerGlomma.py",
                                      remoteFilepath=self.GLOBAL_PARAMETERS["EXPERIMENT_DIR_GLOMMA"],
                                      raiseOnError=True)
        self.cmd.executeOneSCPCommand(host=self.glomma_addr,
                                      localFilepath="./CommandWrapper.py",
                                      remoteFilepath=self.GLOBAL_PARAMETERS["EXPERIMENT_DIR_GLOMMA"],
                                      raiseOnError=True)

        # Then run check file
        remote_checker_path = self.GLOBAL_PARAMETERS["EXPERIMENT_DIR_GLOMMA"] + "/ConfigCheckerGlomma.py"
        out = self.cmd.executeOneSSHCommand(host=self.glomma_addr,
                                      command=f"""python3 {remote_checker_path}""",
                                      getOut=True, raiseOnError=True)[0]

        # Process out
        if "False" in out:
            out = out.split("\n")[0]
            raise RuntimeError("Setup Phase: ConfigCheckerGlomma Failed for ", out)

        print("Setup Phase: Glomma System Configuration Checked")

    def __checkRemoteSysConf(self):
        self.__check_args__()

        if not self.__finished_sysconf_generation or not self.__global_parameter_setted:
            raise RuntimeError("Setup Phase: Called Check Remote SysConf Before Generated It")

        def __inner_checking_worker(machine):
            machine_sysconf_path = f'{self.GLOBAL_PARAMETERS["EXPERIMENT_DIR_LOCAL"]}/{machine}.machine_config'

            # Check if can find Machine configuration file at local
            if not os.path.isfile(machine_sysconf_path):
                raise FileNotFoundError(f"Setup Phase: Check {machine} SysConf: Cannot find file. Bugs exists. "
                                        "Check Generate SysConf Command")

            # First scp over machine system configuration file, config checker, and command wrapper which config checker needs
            self.cmd.executeOneSCPCommand(host=machine,
                                          localFilepath=machine_sysconf_path,
                                          remoteFilepath=self.GLOBAL_PARAMETERS["EXPERIMENT_DIR_REMOTE"],
                                          raiseOnError=True)
            self.cmd.executeOneSCPCommand(host=machine,
                                          localFilepath="./ConfigCheckerRemote.py",
                                          remoteFilepath=self.GLOBAL_PARAMETERS["EXPERIMENT_DIR_REMOTE"],
                                          raiseOnError=True)
            self.cmd.executeOneSCPCommand(host=machine,
                                          localFilepath="./CommandWrapper.py",
                                          remoteFilepath=self.GLOBAL_PARAMETERS["EXPERIMENT_DIR_REMOTE"],
                                          raiseOnError=True)

            # Then run check file
            remote_checker_path = self.GLOBAL_PARAMETERS["EXPERIMENT_DIR_REMOTE"] + "/ConfigCheckerRemote.py"
            out = self.cmd.executeOneSSHCommand(host=machine,
                                          command=f"""python3 {remote_checker_path}""",
                                          getOut=True, raiseOnError=True)[0]

            # Process out
            if "False" in out:
                out = out.split("\n")[0]
                raise RuntimeError("Setup Phase: ConfigCheckerRemote Failed for ", out)

        for m_p in self.GLOBAL_PARAMETERS["MACHINE_PROTOCOLS"]:
            machine = m_p[0]
            __inner_checking_worker(machine)
            print(f"Setup Phase: {machine} Configuration Checked")

        print("Setup Phase: All Remote System Configuration Checked")

    def setup(self, args):
        '''
        Reads in command line arguments
        '''
        # if not isinstance(args, argparse.Namespace):
        #     raise TypeError("Setup Phase: Read Arguments: Not argparse.Namespace instance.")
        self.args = args

        # Set up phase executions
        self.__setupGlobalParameters()
        self.__setupLocalDirectory()
        self.__setupRemoteDirectory()
        self.__generateSysConfFiles()
        self.__checkGlommaSysConf()
        self.__checkRemoteSysConf()

        # Report finishing
        # TODO: Add logging to setup phase
        return True