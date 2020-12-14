# Simple test experiment executor based on previous proxy_test.py
from datetime import date, datetime
import os
from CommandWrapper import CommandWrapper

machines = [
    "mlcnetA.cs.wpi.edu",
    "mlcnetB.cs.wpi.edu",
    "mlcnetC.cs.wpi.edu",
    "mlcnetD.cs.wpi.edu"
]
protocols = [
     "cubic",
     "bbr",
     "hybla",
     "pcc"
]

class Trial:

    def __init__(self, remote="mlcneta.cs.wpi.edu", localdir="./", glommadir="", remotedir="", rootdir="./rdir", datasize="50M", round="0"):
        self.cmd = CommandWrapper()
        self.remote = remote
        self.trialroot = rootdir
        self.glommadir = glommadir
        self.remotedir = remotedir
        self.localdir = localdir

        self.local_udping_path = f"{self.trialroot}/udpLog.txt"
        self.local_pcap_path = f"{self.trialroot}/local.pcap"
        self.remote_pcap_path = f"{self.trialroot}/{self.remote}.pcap"

        self.amount = datasize
        self.round = round

        # Open Log File
        try:
            ERR_FILE = self.localdir + f"/errorlog_trial.txt"
            self.errorlog = open(ERR_FILE, 'a+')
        except:
            raise ValueError("cannot open error log file for trial")

    # Simple SSH Checkings here
    def command_glomma(self, command):
        glomma_executor_path = self.glommadir + "/GlommaExecutor.py"
        out, err = self.cmd.executeOneSSHCommand(host="glomma.cs.wpi.edu",
                                                 command=f"python3 {glomma_executor_path} {command}",
                                                 getOut=True, raiseOnError=True)

        if "ok" in out:
            return

        if err:
            self.errorlog.write(f"#{self.round} - Glomma: SSH ERROR: {err}") # Simple Report mechanism

    def command_remote(self, command):
        remote_executor_path = self.remotedir + "/RemoteExecutor.py"
        out, err = self.cmd.executeOneSSHCommand(host=self.remote,
                                                 command=f"python3 {remote_executor_path} {command}",
                                                 getOut=True, raiseOnError=True)

        if "ok" in out:
            return

        if err:
            self.errorlog.write(f"#{self.round} - {self.remote}: SSH ERROR: {err}")  # Simple Report mechanism

    def start(self):
        # self.command_glomma(command="-C CHECK_ROUTE") # Check Route
        self.command_glomma(command=f"-C CLEANUP") # CLEANUP G
        self.command_remote(command=f"-C CLEANUP") # CLEANUP M
        self.command_glomma(command=f"-C MAKEDIR -P {self.trialroot}") # Make Trial Root at G
        self.command_remote(command=f"-C S_UDPING") # Start UDPING at M
        self.command_glomma(command=f"-C S_UDPING -R {self.remote} -P {self.local_udping_path}") # Start UDPING at G
        self.command_glomma(command=f"-C S_TCPDUMP -P {self.local_pcap_path}") # Start TCPDUMP at G
        self.command_remote(command=f"-C S_TCPDUMP")  # Start TCPDUMP at M
        self.command_remote(command=f"-C S_IPERF")  # Start IPERF at M
        self.command_glomma(command=f"-C S_IPERF -R {self.remote} -A {self.amount}") # Start IPERF at G
        self.command_glomma(command=f"-C CLEANUP") # CLEANUP G
        self.command_remote(command=f"-C CLEANUP") # CLEANUP M
        self.command_glomma(command=f"-C S_SCP_PCAP -R {self.remote} -P {self.remote_pcap_path}") # Start SCP at G

    def __del__(self):
        # Close The File
        try:
            self.errorlog.close()
        except:
            raise ValueError("cannot close error log for trial")

class ExperimentExecutor:

    # Simple way to define singleton in a process
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ExperimentExecutor.__instance == None:
            ExperimentExecutor()
        return ExperimentExecutor.__instance

    def __init__(self, args):

        # Check singleton
        if ExperimentExecutor.__instance != None:
            raise RuntimeError("Trying To Construct Extra New_Trial in Setup Phase")
        else:
            ExperimentExecutor.__instance = self

        self.args = args
        self.cmd = CommandWrapper()
        # Open Log File
        try:
            ERR_FILE = self.args["EXPERIMENT_DIR_LOCAL"] + f"/errorlog_executor.txt"
            self.errorlog = open(ERR_FILE, 'w+')
        except:
            raise ValueError("cannot open error log file")

        self.cmd.executeOneSCPCommand(host="glomma.cs.wpi.edu",
                                      localFilepath="./GlommaExecutor.py",
                                      remoteFilepath=self.args["EXPERIMENT_DIR_GLOMMA"],
                                      raiseOnError=True)

        for m_p in self.args["MACHINE_PROTOCOLS"]:
            machine = m_p[0]
            self.cmd.executeOneSCPCommand(host=machine,
                                          localFilepath="./RemoteExecutor.py",
                                          remoteFilepath=self.args["EXPERIMENT_DIR_REMOTE"],
                                          raiseOnError=True)

    #Wrapper For Print
    def PRINT(self, logfile, msg):
        print(msg)
        try:
            logfile.write(msg)
        except:
            print("LOG FILE ERROR")

    # Execute test on a specific machine with specific protocol once
    def executeTestOnce(self, machine, protocol, proxyMode, roundIndex, logfile, dataSize="50M"):
        """
        Method to execute test once on a specific machine with specific protocol once
        @params: machine, protocol: being tested machine and protocol
        @params: roundIndex: current round (most outer loop)
        """

        # Trial Constructor:
        #    def __init__(self, name='experiment', dir='.', local='glomma', remote='mlc1.cs.wpi.edu', data=None)

        # Switch Proxy Mode
        msg = "Switching Proxy Mode to %d\n" % (proxyMode)
        self.PRINT(logfile, msg)

        # SIMPLE CHECKING HERE
        out = self.cmd.executeOneSSHCommand(host="glomma.cs.wpi.edu", command=f"python3 GlommaExecutor.py -C S_PROXY -A {proxyMode}", getOut=True)[0]
        if "OK" not in out:
            self.errorlog.write(f"FAIL TO SWITCH PROXY IN ROUND {roundIndex} with {machine}_{protocol}")

        # Print Round Start
        test_start_time = datetime.now()
        test_start_time_str = test_start_time.strftime("%Y-%m-%d-%H-%M-%S")
        msg = "# Round %d %s %s ProxyMode %d Started At : %s\n" % (roundIndex, machine, protocol, proxyMode, test_start_time_str)
        self.PRINT(logfile, msg)

        # Trial
        title = f"{self.args['EXPERIMENT_DIR_GLOMMA']}/data/{machine}_{protocol}_Proxy{proxyMode}_{dataSize}_{roundIndex}"  # Title of the trial.
        trial = Trial(localdir=self.args['EXPERIMENT_DIR_LOCAL'], glommadir=self.args['EXPERIMENT_DIR_GLOMMA'],
                      remotedir=self.args['EXPERIMENT_DIR_REMOTE'],
                      rootdir=title, datasize=dataSize, remote=machine)
        trial.start()

        test_end_time = datetime.now()
        test_end_time_str = test_end_time.strftime("%Y-%m-%d-%H-%M-%S")
        duration = divmod((test_end_time - test_start_time).total_seconds(), 60)
        msg = """# Round %d %s %s ProxyMode %d Ended At : %s
        Duration: %s \n""" % (roundIndex, machine, protocol, proxyMode, test_end_time_str, str(duration))
        self.PRINT(logfile, msg)

    def __start(self, numOfTests=10, dataSize="50M"):

        # Open Log File
        try:
            LOG_FILE = self.args["EXPERIMENT_DIR_LOCAL"] + f"/{dataSize}_log.txt"
            logfile = open(LOG_FILE, 'w+')
        except:
            raise ValueError("cannot open logfile")
        print_msg = ""

        # Record Start time, and then End Time After Test Ends, for Analysis Purposes
        start_time = datetime.now()
        start_time_str = start_time.strftime("%Y-%m-%d-%H-%M-%S")
        print_msg = f"TEST Started At {start_time_str}\n" \
                    f"Rounds: {numOfTests}"
        self.PRINT(logfile, print_msg)

        # Main Loop For Testing
        current_time_str = ""
        for i in range(numOfTests):

            # Record The Time When A Round Starts
            current_time_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            print_msg = "\n**************************************** Round %d Started At [ %s ] ****************************************\n" % (
            i, current_time_str)
            self.PRINT(logfile, print_msg)

            # Loop 2: Traverse (Machine, Protocol) groups
            for [machine, protocol] in self.args["MACHINE_PROTOCOLS"]:
                # Record The Time When A (Machine Protocol) Group Starts
                current_time_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                print_msg = "\n------------------------------ Round %d %s %s Started At [ %s ] ------------------------------\n" % (
                i, machine, protocol, current_time_str)
                self.PRINT(logfile, print_msg)

                # Loop Body 3: Run Test With Proxy 2 Once and Proxy 3 Once (Machine, Protocol)
                self.executeTestOnce(machine, protocol, 2, i, logfile, dataSize)
                self.executeTestOnce(machine, protocol, 3, i, logfile, dataSize)

                # Record The Time When A (Machine Protocol) Group Ends
                current_time_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                print_msg = "\n------------------------------- Round %d %s %s Ended At [ %s ] -------------------------------\n" % (
                i, machine, protocol, current_time_str)
                self.PRINT(logfile, print_msg)

            # Record The Time When A Round Ends
            current_time_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            print_msg = "\n***************************************** Round %d Ended At [ %s ] *****************************************\n" % (
            i, current_time_str)
            self.PRINT(logfile, print_msg)
        # End of Testing Loop

        # Record Test Ending Time and Print Overall Statistics
        end_time = datetime.now()
        end_time_str = end_time.strftime("%Y-%m-%d-%H-%M-%S")
        duration = divmod((end_time - start_time).total_seconds(), 60)
        print_msg = "TEST Ended At " + end_time_str
        self.PRINT(logfile, print_msg)

        print_msg = """ \n\n
        ********** TEST ENDED **********
        Start Time: %s
        End Time: %s
        Duration: %s
        """ % (start_time_str, end_time_str, str(duration))
        self.PRINT(logfile, print_msg)
        # End of Recording

        # Close The File
        try:
            logfile.close()
        except:
            raise ValueError("cannot close logfile")

    def start(self):
        for size_and_round in self.args["DATA_SIZE_AND_ROUNDS"]:
            numoftest = int(size_and_round[1])
            datasize = size_and_round[0]
            self.__start(numOfTests=numoftest, dataSize=datasize)
