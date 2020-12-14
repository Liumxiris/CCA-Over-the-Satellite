import argparse, re, os
import CommandWrapper

# Hardcoded solution for checking feasibility
class RemoteExecutor:

    def __init__(self):
        self.cmd = CommandWrapper.CommandWrapper()
        self.REMOTE_DEVICE = "ens2"
        self.LOCAL_DEVICE = "eno2"
        self.remote_iperf_port = 5201
        self.remote_udp_port = 5202

    def executeCommand(self, args):
        if args.command == None:
            return
        elif args.command == "CLEANUP":
            procs_remote = ['tcpdump', 'iperf3', 'sUDPingLnx']
            kill_cmd_remote = 'pkill ' + '; pkill '.join(procs_remote) + ';'
            self.cmd.execute(kill_cmd_remote)
        elif args.command == "S_TCPDUMP":
            self.cmd.execute(f"screen -dm tcpdump -Z $USER -i {self.REMOTE_DEVICE} -s 96 port {self.remote_iperf_port} -w $HOME/pcap.pcap")
        elif args.command == "S_UDPING":
            self.cmd.execute(f"screen -dm sUDPingLnx {self.remote_udp_port}")
        elif args.command == "S_IPERF":
            self.cmd.execute(f"screen -dm iperf3 --server")
        elif args.command == "CHECK":
            print(self.cmd.execute("python3 ConfigCheckerRemote.py")[0])
            return
        else:
            pass

        print("OK")

parser = argparse.ArgumentParser(description='Glomma Experiment Executor For TCP Experiments Via Satellite')

parser.add_argument('--command', '-C', type=str, action="store", dest="command", help="issue a command to execute")
args = parser.parse_args()

RemoteExecutor().executeCommand(args)