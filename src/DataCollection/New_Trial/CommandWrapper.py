from subprocess import Popen, DEVNULL, PIPE, check_call, check_output, CalledProcessError, STDOUT
from time import sleep
import os

class CommandWrapper():

    def checkCommand(self, command_args, _use_check_output=True):
        """
        Method to check if a command can successfully runs
        @params: command_args: must be an array of commands. ["command", "arg1", "arg2", etc]
        Normally will return True if success with test command, else False
        If set returnCode to True, will return exit code instead
        Check_output: will wait for all output is read,
        More see https://stackoverflow.com/questions/36169571/python-subprocess-check-call-vs-check-output#:~:text=1%20Answer&text=check_call()%20returns%20as%20soon,closes%20its%20inherited%20pipe%20ends).
        """

        if type(command_args) != list:
            print("Must use array as input")
            return False

        if "ssh" in command_args:
            print("Dont try ssh. Does not have successful return code")
            return False

        try:
            if _use_check_output:
                check_output(command_args, stderr=STDOUT)
            else:
                check_call(command_args, stderr=PIPE, stdout=PIPE, shell=True)
        except CalledProcessError as cpe:
            print("Error: ", cpe.output.decode('utf-8').strip())
            return False
        except Exception as e:
            print("Error: ", e.args[1])
            return False

        return True

    def execute(self, command, verbose=False):
        """
        Method to execute one command
        """
        process = Popen(command, stdout=PIPE, shell=True)
        out, err = process.communicate(command.encode('utf-8'))
        out = out.decode('utf-8').strip()

        if verbose:
            print(out)

        return out, err

    def executeOneSSHCommand(self, host="cs.wpi.edu", command="", verbose=False, getOut=False, raiseOnError=False):
        """
        SSH command wrapper for execute once
        host is the destination of SSH
        commands is an array of commands to execute
        verbose to print outputs
        getOut to get output in return
        """

        if "SSH_AUTH_SOCK" not in os.environ:
            raise PermissionError("Add SSH Agent First")

        ssh = Popen(["ssh", host],
                    stdin=PIPE, stdout=PIPE, stderr=PIPE,
                    universal_newlines=True, bufsize=0)  # Buffer size = 0 ==> immediately print

        out, err = ssh.communicate(command)

        # Out message processing due to tcsh of cs server at testing
        if "Thus no job control in this shell":
            out = "\n".join(out.split("\n")[3:])

        # Error message processing due to tcsh of cs server at testing
        if "Identity added: " in err:
            err = "\n".join(err.split("\n")[2:])

        if "Pseudo-terminal will not be allocated because stdin is not a terminal." in err:
            err = "\n".join(err.split("\n")[1:])

        if verbose:
            # Print output
            print("*****SSH OUTPUT MSG*****")
            print(out)
            print("*****SSH OUTPUT MSG*****\n")

            print("*****SSH ERROR MSG*****")
            print(err)
            print("*****SSH ERROR MSG*****")

        if raiseOnError and err:
            raise RuntimeError("SSH Execute Once Error: ", err)

        if getOut:
            return out, err

    def executeOneSCPCommand(self, host="cs.wpi.edu", prefix="", localFilepath="", remoteFilepath="", verbose=False, getOut=False, raiseOnError=False):
        """
        SCP command wrapper for executing once
        host is the destination of SCP
        localFilepath = where local file is
        destinationFilepath = where remote file should be
        turn on isDir if it is a dir
        verbose to print outputs
        getOut to get output in return
        """

        if "SSH_AUTH_SOCK" not in os.environ:
            raise PermissionError("Add SSH Agent First")

        # Construct SCP command array
        scp_command_array = ["scp"]
        if prefix: # Prefix
            scp_command_array.append(prefix)

        # Local File argument
        if not os.path.isfile(localFilepath) or os.path.isdir(localFilepath):
            err_msg = "SCP: Cannot find this dir or file: " + localFilepath
            if raiseOnError:
                raise FileNotFoundError(err_msg)
            else:
                return "", err_msg
        scp_command_array.append(localFilepath) # Local file path
        # End of Local File Handling

        # Remote file path argument
        remote_final_path = f"{host}:{remoteFilepath}"
        scp_command_array.append(remote_final_path)

        scp = Popen(scp_command_array,
                    stdin=PIPE, stdout=PIPE, stderr=PIPE,
                    universal_newlines=True, bufsize=0)  # Buffer size = 0 ==> immediately print

        out, err = scp.communicate()
        #
        # # Out message processing due to tcsh of cs server at testing
        # if "Thus no job control in this shell":
        #     out = "\n".join(out.split("\n")[3:])
        #
        # # Error message processing due to tcsh of cs server at testing
        # if "Identity added: " in err:
        #     err = "\n".join(err.split("\n")[2:])

        if verbose:
            # Print output
            print("*****SSH OUTPUT MSG*****")
            print(out)
            print("*****SSH OUTPUT MSG*****\n")

            print("*****SSH ERROR MSG*****")
            print(err)
            print("*****SSH ERROR MSG*****")

        if raiseOnError and err:
            raise RuntimeError("SCP Execute Once Error: ", err)

        if getOut:
            return out, err

    def executeMultipleSSHCommands(self, host="cs.wpi.edu", commands=[], verbose=False, withShell=False, getOut=False):
        """
        SSH command wrapper for multiple commands
        host is the destination of SSH
        commands is an array of commands to execute
        verbose to print outputs
        withShell to execute in shell (so there will be environment parameters) [Not recommend, tested, not good to use]
        """

        if "SSH_AUTH_SOCK" not in os.environ:
            raise PermissionError("Add SSH Agent First")

        if withShell: # If using shell, then you have environment parameters, but Popen has to use string rather than sequence as input
            for command in commands:
                # Send ssh commands to stdin
                # command = command.replace('"', '\\"') # In previous implementation this is included. Dont know why, but left it here.
                print(f"Executing Command {command}")
                ssh = Popen(f"ssh {host} '{command}'", shell=True,
                            stdin=PIPE, stdout=PIPE, stderr=PIPE,
                            universal_newlines=True, bufsize=0)  # Buffer size = 0 ==> immediately print

                out = ssh.stdout.readlines()
                err = ssh.stderr.readlines()

                if verbose:
                    # Print output
                    print("*****SSH OUTPUT MSG*****")
                    for line in out:
                        print(line.strip())
                    print("*****SSH OUTPUT MSG*****\n")

                    print("*****SSH ERROR MSG*****")
                    for line in err:
                        print(line.strip())
                    print("*****SSH ERROR MSG*****")

                ssh.stdin.close()
                ssh.stdout.close()
                ssh.stderr.close()

                if getOut:
                    return

        else:
            ssh = Popen(["ssh", host],
                        stdin=PIPE, stdout=PIPE, stderr=PIPE,
                        universal_newlines=True, bufsize=0) # Buffer size = 0 ==> immediately print

            for command in commands:
                # Send ssh commands to stdin
                print(f"Executing Command {command}")
                ssh.stdin.write(command)
            ssh.stdin.close()

            # communicate is more safe in terms of deadlock, but can only execute one command
            # out, err = ssh.communicate(command)
            # print(out)
            # print("err", err)

            out = ssh.stdout.readlines()
            err = ssh.stderr.readlines()

            if verbose:
                # Print output
                print("*****SSH OUTPUT MSG*****")
                for line in out:
                    print(line.strip())
                print("*****SSH OUTPUT MSG*****\n")

                print("*****SSH ERROR MSG*****")
                for line in err:
                    print(line.strip())
                print("*****SSH ERROR MSG*****")

        if getOut:
            return out, err

    def getOneSSHSession(self, host="cs.wpi.edu", verbose=False):
        """
        Returns an instance of a SSH_Session Class.
        The class will communicate to a certain screen at host.
        However, DO NOT use this for one time long run commands (if you want to run them in background)
        Because this class will terminate that screen session in destructor automatically.
        And the process in local will not wait for background processes at remote
        """
        return SSH_Session(host, verbose)

class SSH_Session():

    def __init__(self, host, verbose):
        # At init, create a ssh session (screen) and binds its session value
        self.host = host
        self.verbose = verbose
        self.session_num = self._create_session()
        print(f"SSH_SESSION {self.session_num} To Host {self.host} Initialized")

    def _create_session(self):
        previous_sessions = self._find_session_nums()
        if previous_sessions != []:
            print(f"Warning: SSH_Session: Already 1+ screen instance in host {self.host} before creation!")

        # Create screen
        # Popen(["ssh", self.host, "screen -dmS session -L -Logfile session.log"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        Popen(["ssh", self.host, "screen -dm"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        sleep(1)
        new_sessions = self._find_session_nums()

        session_num = list(set(new_sessions).difference(previous_sessions))
        if len(session_num) > 1:
            raise InterruptedError("SSH_Session: Get more than 1 session nums", session_num)

        session_num = session_num[0]
        if self.verbose:
            print(f"SSH_Session: Created a screen at host {self.host} with screen num {session_num}")

        return session_num

    def _find_session_nums(self):
        # Create an ssh to find screen num
        ssh = Popen(["ssh", self.host, "screen -ls"], stdout=PIPE, stderr=PIPE)

        # If there is error, report
        errors = ssh.stderr.readlines()
        if errors != []:
            self.session_num = -1
            raise InterruptedError(-1, "Error in SSH_Session _find_session_num", errors)

        # Find session num from output
        session_nums = []
        for line in ssh.stdout.readlines():
            line = line.decode("utf-8")
            if "(Detached)" in line:
                session_num = [int(session) for session in line.split(".") if session.strip("\t").isdigit()][0]
                session_nums.append(session_num)
                if len(session_nums) > 1: # if more than 1 screens at host
                    print(f"Warning: SSH_Session: More than 1 screen instance in host {self.host}!")

        ssh.stderr.close()
        ssh.stdout.close()

        return session_nums

    def getSessionNum(self):
        return self.session_num

    def executeCommand(self, command):
        """
        Method to communicate to the existing screen
        """
        if type(command) != str:
            raise ValueError("SSH_Session: the command has to be a string!")

        ssh = Popen(["ssh", self.host],
                    stdin=PIPE, stdout=PIPE, stderr=PIPE,
                    universal_newlines=True, bufsize=0)  # Buffer size = 0 ==> immediately print

        out, err = ssh.communicate(f"screen -S {self.session_num} -X {command}")
        if self.verbose:
            # Print output
            print("*****SSH OUTPUT MSG*****")
            print(out)
            print("*****SSH OUTPUT MSG*****\n")

            print("*****SSH ERROR MSG*****")
            print(err)
            print("*****SSH ERROR MSG*****")

    def __del__(self):
        # At destruct, destroy the ssh session (screen)
        if self.session_num != -1:
            Popen(["ssh", self.host, f"screen -S {self.session_num} -X quit"], stdout=PIPE, stderr=PIPE)
            print(f"SSH_SESSION {self.session_num} To Host {self.host} Destroyed")


