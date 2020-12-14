# Socket server at cs server
import socket

class ExperimentExecutor:

    # Simple way to define singleton in a process
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ExperimentExecutor.__instance == None:
            ExperimentExecutor()
        return ExperimentExecutor.__instance

    def __init__(self):

        # Check singleton
        if ExperimentExecutor.__instance != None:
            raise RuntimeError("Trying To Construct Extra New_Trial in Setup Phase")
        else:
            ExperimentExecutor.__instance = self

        self.server = None
        self.glomma_server = ("glomma.cs.wpi.edu", 12345)
        self.remote_servers = {
            "MLCA":("mlcneta.cs.wpi.edu",22345),
            "MLCB":("mlcnetb.cs.wpi.edu",22345),
            "MLCC":("mlcnetc.cs.wpi.edu",22345),
            "MLCD":("mlcnetd.cs.wpi.edu",22345)
        }

    def __send_socket(self, msg, server_and_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            # soc.connect((server_and_port[0], server_and_port[1]))
            soc.connect(("", 12345))
            soc.sendall(bytes(msg, encoding="utf-8"))
            data = soc.recv(1024)

        return data

    def __check_connection(self):
        print(self.__send_socket(msg="CHECK", server_and_port=self.glomma_server))

    def start(self):
        self.__check_connection()

e = ExperimentExecutor()
e.start()


