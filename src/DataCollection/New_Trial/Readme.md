### Changes On Trial [ Data Collection Module ]
We proposed and implemented a new trial system in week 7. 
The [proposal](./New%20Trial%20System%20Proposal.md) lists out motivations for the new system.
The [Flow Diagram](./CS%204999%20NEW%20TRIAL%20SYSTEM%20OVERALL.png) depicts planned system flow.

### How to execute:
At cs server: screen [-dm] python3 TestExecutor.py -C test.config

### Implemented Designs
- Error Checking:
    - SSH based error checking: Currently in the [CommandWrapper](./CommandWrapper.py), for executing commands via "executeOneSSHCommand", we gave out a parameter "raiseOnError".
    When set to True, if there is any error returned by SSH process, the python process will throw the exception. 
        - Run time: can use try/except to handle those exceptions. Currently they are only thrown but not handled.
    - Checker: We implemented two automated checker [GlommaChecker](./ConfigCheckerGlomma.py) and [RemoteChecker](./ConfigCheckerRemote.py).
    There are several test methods within. If tests failed, it will print False, else True. 
    Since we are treating cs server as our experiment executor, the SSH will get this output "True" or "False".
    Currently in setup phase, if check failed, the program will terminate and print failed reasons in console.

- Error Correction:
    - Currently we just have routing in glomma and tcp setting in both glomma and mlcs implemented in Checkers.

- Setup Phase
    - Currently thoroughly implemented in [SetupWorker](./SetupWorker.py)
    - Singleton designed.
    - Expected Input: args from argparser, from the entry program (TestExecutor.py) to method .setup(args).
    - Expected Output: True => Means all set up finished without errors. 
    - Currently Implemented Setups:
        ```
        self.__setupGlobalParameters() => store parsed parameters from test.config in memory, in a python dictionary [Can be retrieved via getGlobalParameters()]
        self.__setupLocalDirectory() => Setup local directory for experiment (logs)
        self.__setupRemoteDirectory() => Setup remote (Glomma + MLC) directories for experiment (data / log / checkers, etc.) 
        self.__generateSysConfFiles() => generate machine configurations based on test.config and dig +short hostname
        self.__checkGlommaSysConf() => scp over checker to glomma experiment directory, and check configurations
        self.__checkRemoteSysConf() => scp over checker to MLC experiment directories, and check configurations
        ```

- Experiment Phase at CS Server:
    - Currently we hardcoded the experiment executor based on proxy_test.py from old_trial in [ExperimentExecutor](./ExperimentExecutor.py)
    - Expected Input: python dictionary containing global parameters from set up phase
    - Expected Output: Experiment Data at Glomma under designated folder
    - Basically, we wrote out [GlommaExecutor](./GlommaExecutor.py) and [RemoteExecutor](./RemoteExecutor.py) and use scp to send those executor over to experiment directories, which were set up in SetupPhase
    - Then the [ExperimentExecutor](./ExperimentExecutor.py) will use ssh to call those two modules at machines.
    - Those modules will return "OK" if no error happened. Else SSH itself will throw errors.
    - Already tested, all pcaps could be found, but udp ping log is missing (blank)
    - errorlog_trial.txt: errors during trial
    - errorlog_executor.txt: errors of the executor

### Extensibility
One goal of our system is to be extensible. We achieved this by modularizing it.
- Error Checking & handling Module:
    - Run time: use try and except to catch errors in experiment executor
    - Checker: add test methods in the [GlommaChecker](./ConfigCheckerGlomma.py) and [RemoteChecker](./ConfigCheckerRemote.py).
- Add to Setup Phase:
    - Add addition method in .setup() in setup worker
- Add to Experiment Phase:
    - Currently can only be added via hardcode in ExperimentExecutor

### Unfinished Designs
- Error checking for pcap < 1KB
- Error checking for multiple people running experiments
- Use Socket to build the system
    - If Using socket, then at setup phase, cs server scp over socket server at both glomma and remote
    - In experiment phase, cs will first use ssh to start socket server, and then execute experiment
    - Not implemented for time reasons and security reasons (open port at cs and servers, etc)

### Known Bugs
- It is already known that udping files will not be stored correctly. Guess its an issue with redirection.
