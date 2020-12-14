import argparse, re, os
import CommandWrapper

# TODO: Should read from config file
machine_ip = {
    "mlcneta.cs.wpi.edu":"130.215.28.202",
    "mlcnetb.cs.wpi.edu":"130.215.28.203",
    "mlcnetc.cs.wpi.edu":"130.215.28.206",
    "mlcnetd.cs.wpi.edu":"130.215.28.207"

}

# Hardcoded solution for checking feasibility
class GlommaExecutor:

    def __init__(self):
        self.cmd = CommandWrapper.CommandWrapper()
        self.REMOTE_DEVICE = "ens2"
        self.LOCAL_DEVICE = "eno2"
        self.remote_iperf_port = 5201
        self.remote_udp_port = 5202

    def executeCommand(self, args):
        if args.command == None:
            return
        elif args.command == "MAKEDIR":
            dir = args.path
            if not os.path.exists(dir):
                os.makedirs(dir)
        elif args.command == "CLEANUP":
            procs_local = ['tcpdump', 'iperf3', 'ssh-agent']
            kill_cmd_local = 'pkill ' + '; pkill '.join(procs_local) + '; pkill -2 cUDPingLnx ;'
            self.cmd.execute(kill_cmd_local)
        elif args.command == "S_TCPDUMP":
            self.cmd.execute(f"screen -dm tcpdump -Z $USER -i {self.LOCAL_DEVICE} -s 96 port {self.remote_iperf_port} -w {args.path}")
        elif args.command == "S_UDPING":
            self.cmd.execute(f"cat > {args.path}")
            self.cmd.execute(f"screen -dm cUDPingLnx -h {args.remote} -p {self.remote_udp_port} -n 4 > {args.path}")
        elif args.command == "S_IPERF":
            self.cmd.execute(f"screen -dm iperf3 -c {args.remote} --reverse {args.amount} -p 5201")
        elif args.command == "S_SCP_PCAP":
            self.cmd.execute(f"scp {args.remote}:pcap.pcap {args.path}")
        elif args.command == "S_PROXY":
            self.cmd.execute(f"$HOME/setup_routes.sh {args.amount}")
        elif args.command == "CHECK":
            print(self.cmd.execute("python3 ConfigCheckerGlomma.py")[0])
            return
        elif args.command == "CHECK_ROUTE":
            route_checking_command = "ip route show"
            out = self.cmd.execute(route_checking_command)[0]

            ip_prefix = re.compile("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) via .*? dev eno2")
            links = ip_prefix.findall(out)

            if (machine_ip[args.remote] not in links):
                self.cmd.execute("~/setup_routes.sh")
        else:
            pass

        print("OK")

parser = argparse.ArgumentParser(description='Glomma Experiment Executor For TCP Experiments Via Satellite')

parser.add_argument('--command', '-C', type=str, action="store", dest="command", help="issue a command to execute")
parser.add_argument('--patharg', '-P', type=str, action="store", dest="path", help="optional path argument")
parser.add_argument('--remote', '-R', type=str, action="store", dest="remote", help="optional remote argument")
parser.add_argument('--amount', '-A', type=str, action="store", dest="amount", help="optional amount argument")

args = parser.parse_args()

GlommaExecutor().executeCommand(args)