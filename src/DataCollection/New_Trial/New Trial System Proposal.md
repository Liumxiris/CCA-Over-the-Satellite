## New Trial System Proposal

### Issues
1. 
	Previously, we are using Trial class in trial.py as Trial module for experiments. We simply created iterations with Trial class. 
	However, there is a hidden issue in this way of running experiments. Trial class is built for one round of trial only. 
	Thus, it wraps in "set up calls", like the command to set CC protocol and the command to set initial window sizes, into each run of trial.
	Further, since Trial class wraps in "name" or "title" as to identify and store experiment data, previously new Trial instances will be created for each run of experiment (machine+protocol, (round index), (proxy), etc..
	Then many unnecessary set up calls through SSH is built and thus wasting testing time (reducing number of tests we can do)
	Using SSH to execute commands at remote is pretty costly. Each time it has to reconnect to the remote using UDP to execute some command.
	So we need to automate the test in a way that it will not use ssh to send "set up calls" in each run.

2. 
    Extensibility. There are references between modules. Each time we add new functionalities in we need to create a new module to wrap things up, while there are several modules that are commonly used.
    Thus, if we could build a flow and pre-define a way to add changes, that will help the code to be more extensible. 

3.
    Autonomous error reporting. We have encountered many minor but impactful errors on the way. For example, resets of routes (IP addresses), and weird bugs due to full storage of server. 

Briefly, if we can build a simple automation system that is
    1) extensible, 2) easy to add new functionalities, 3) have simple error checking system, 4) save SSH overheads
that will be pretty helpful for long time runs

### New Trial Flow
1. Setup Phase: 
	At Local: 
	- Make the directory for experiment if it does not exist. If --configpath is set, then use that Setup Configuration File as the setup configuration file for this experiment.
	- Reads in the Setup Configuration File, and store those configurations in memory. Default values will be used if no files are provided.
	- Setup Configuration File contains: 
		1. General Parameters for Each Run of Trial:
		- [Machine Protocol Set]
		- [Proxy Modes Set]
		- [Name of The Experiment]
		- [Experiment Related Parameters, like BDP, Window Size, etc]
		2. Trial Parameters for Each Run of Trial:
		- [UDPING]
		- [Verbose]
		- [Data Size + Expected Rounds / Expected Time with Portion for Each Data Size]
		(More detail see Set Up Configuration File Section of this readme)
	- Generate System Configuration File for each machine, including the glomma one, and the ones in [Machine Protocol Set] in Setup Configuration File.
	[TODO: Now for the sake of implementation, ssh-passphrase at Glomma is hard set to null, because if not ssh-add cannot be run (does not get stdin)]
	[More see this: https://unix.stackexchange.com/questions/90853/how-can-i-run-ssh-add-automatically-without-a-password-prompt]
	[Can solve this by modify dev/tty, or using libs like pexpect]
	- Check glomma system configurations with configuration file with local Configuration File Worker (ConfigCheckerGlomma.py). 
		Namely, iptables, routes, etc. Also check command permissions, both at local and local2remote.
	- Then configure machines with configurations appropriately. 
		First, it will scp over the Machine Configuration File and the Configuration File Worker (ConfigCheckerRemote.py) . 
		Second, it will set up config at remote, and check validity of configs. More see At Remote Section of Setup Phase.
	- Check if all remote and local reports set up finished and validated.
	- If all validated, then go to next phase, Experiment Phase.
	
	At Remote:
	- Receieve Machine Configuration File and Configuration File Worker.
	- Set Machine Configuration according to the Machine Configuration File.
	- Check Configurations. First check configurations at machine by comparing with Machine Configuration File, then return config values back to LOCAL asking local to recheck if the value matches those ones in memory.
	
	Additonally, at Setup Phase, local will record all machine configurations, logs, etc. (after finished validations like local memory = remote) to ./logs/SetupReport.txt

2. Experiment Phase:
	- If Verbose, prints out experiment structure (for loop order, etc.)
	
	At Local:
	- Read Trial Parameters from memory
	- Based on hardcoded iterations (should be enough for our experiments) execute trials at remotes.
	- Trials will be pretty similar to the previous implementation. However, only ONE SSH will be sent to remote for set up execution. 
		[Further improvement: use sockets and designate ports / ip addresses so the socket will go through ground line but not satellite]
	-	Based on flags in Trial Parameters, local execute corresponding instructions locally and will send remote instruction sets to remote with only **ONE SSH Communication**. 
		This will help to reduce overheads caused by setting up SSH communications too many times.
		Also, local will record down overall execution time [starting time (before SSH is sent) -> ending time (after scp finished)]
		and experiment execution time [starting time (iperf3 executed) -> ending time (iperf3 ends)]
		UDPING will be recorded if flag is set.	
	- After all are finished, save log files, scp remote pcap to local, and go to next run
	- Will report errors during experiment if (pcap is empty, connection timed out, no permission or transmission)
	
	At Remote:
	- Wait for local to execute 
	
### Setup Configuration File
Should contain key-value pairs in following format:
```
*** FILE START ***
[GENERAL PARAMETERS]
EXPERIMENT_NAME = TRIAL
MACHINE_PROTOCOLS = MLCA_CUBIC, MLCB_BBR, MLCC_HYBLA
PROXIES = 2, 3
BDP = 15000000
WMEM = %(BDP)s * 4

[TRIAL PARAMETERS]
UDPING = False
VERBOSE = True
SETUP_REPORT = True
DATA_SIZE_AND_ROUNDS = 1G_50, 2G_0

*** FILE ENDS ***
```

### To the sudoers file
- give no password to /home/yliu31/setup_routes.sh
    - TBH... I messed up half way, and cannot enter corrupted sudoers file anymore. 
    - However, this saved my life: https://askubuntu.com/questions/799669/etc-sudoers-file-corrupted-and-i-cant-run-pkexec-visudo-over-ssh

+ after glomma reset 
    - check glomma new ip
    - add to machine firewall
    - add root permission at glomma
