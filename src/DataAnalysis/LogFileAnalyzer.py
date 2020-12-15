import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# If you want to disable pop up of plt, use this
# plt.ion()

class LogFileAnalyzer():

    def __init__(self, filename):

        # Two tables, one includes duration, one includes time of day.
        # Must have 2 separate tables because dataframe needs 2D array
        self.duration_table = pd.DataFrame() # Duration table
        self.datetime_table = pd.DataFrame() # Date time table
        self._setUpTables(file=filename) # Set up tables from log file
        self.colordict = {"MLCA_P2":"#9996a7", "MLCA_P3":"#c273bd",
                          "MLCB_P2":"#b4deca", "MLCB_P3":"#7e564a",
                          "MLCC_P2":"#55efd3", "MLCC_P3":"#d7cf13",
                          "MLCD_P2":"#883f9b", "MLCD_P3":"#e08261"}


    # Convert log file to pd.df table
    def _setUpTables(self, file):
        with open(file) as f:
            self.testInfo = f.readline()
            self.testRounds = f.readline()
            numOfRounds = int(re.findall(r"^Rounds:\s+(\d+)$", self.testRounds)[0]) + 1

            # duration_matrix[Col: 0]: Round Index, duration_matrix[Col: 1-8]: machine_proxy
            duration_matrix = [ [0 for machine_proxy in range(9)] for round in range (numOfRounds)] # Machine_Proxy arrays
            duration_matrix = np.array(duration_matrix)

            datetime_matrix = [ [" " for machine_proxy in range(9)] for round in range (numOfRounds)] # Machine_Proxy arrays
            datetime_matrix = np.array(datetime_matrix, dtype='<U30')

            # Process the log file line by line
            for line in f:

                if ("TEST Ended At" in line): # break the loop if processed all data
                    break

                if (re.match(r"^(\W+)Round\s(\d+)\sStarted", line)): # Update round number
                    round = int(line.split(" ")[2])
                    duration_matrix[round][0] = round + 1
                    datetime_matrix[round][0] = round + 1

                if (re.match(r"^(\W+)-\sRound\s(\d+)\smlcnet", line)): # Update machine
                    date_time = line.split(" ")[8]
                    machine = list(line.split(" ")[3])[6]
                    if (machine == 'A'):
                        machine = 1
                    elif (machine == 'B'):
                        machine = 3
                    elif (machine == 'C'):
                        machine = 5
                    else:
                        machine = 7

                if (re.match(r"^Switching Proxy Mode to \d", line)): # Update proxy mode
                    mode = int(line.split(" ")[4])
                    machine_proxyMode = machine if mode == 2 else (machine + 1)

                if ("Duration:" in line): # Fill in data
                    minute =  float(line.split(", ")[0].split("(")[1])
                    sec = float(line.split(", ")[1].replace(')', ''))
                    time = minute * 60 + sec

                    duration_matrix[round][machine_proxyMode] = time
                    datetime_matrix[round][machine_proxyMode] = date_time

            # End of for loop

        # End of file processing

        columnArray = ["Round", "MLCA_P2", "MLCA_P3", "MLCB_P2", "MLCB_P3", "MLCC_P2", "MLCC_P3", "MLCD_P2", "MLCD_P3"]
        self.duration_table = pd.DataFrame(duration_matrix, columns=columnArray, dtype=np.float) # Update self.duration_table
        self.datetime_table = pd.DataFrame(datetime_matrix, columns=columnArray, dtype=np.str) # Update self.duration_table

        print(self.duration_table)
        
        #find the best cases and worst cases 
        worstcases = []
        bestcases = []
        for col_idx in range(8):
            col_array = columnArray[col_idx+1]
            max_round = self.duration_table.set_index("Round")[col_array].idxmin()
            min_round = self.duration_table.set_index("Round")[col_array].idxmax()

            bestcases.append(int(max_round)-1)
            worstcases.append(int(min_round)-1)

        print(bestcases)
        print(worstcases)
    


    def plotWholeDurationTable(self):
        '''
        Will plot the whole table, including 4 machines * 2 proxies
        '''
        self.duration_table.plot.line(x="Round")
        plt.show()

    def plotMachineDurationVsRound(self, machine=["MLCA, MLCB, MLCC, MLCD"], proxy=["P2", "P3"], savepath = ""):
        '''
        Method to plot specific machines with specific proxies (in duration)
        @params: machine = array of machines, like machine = ["MLCA", "MLCB"]
        @params: proxy = array of proxies, like proxy = ["P2", "P3"]
        '''

        if not machine or not proxy:
            print("Empty parameter array detected. Check arguments")
            return

        selected = {f"{mlc}_{p}" for mlc in machine for p in proxy}
        self.duration_table.plot.line(x="Round", y= selected, color=[self.colordict.get(x, '#333333') for x in selected])

        plt.xlabel("Round (index)")
        plt.ylabel("Duration (second)")

        if savepath:
            plt.savefig(savepath)
        else:
            plt.show()

    def plotMachineDurationVsDateTime(self, machine=["MLCA, MLCB, MLCC, MLCD"], proxy=["P2", "P3"], savepath = ""):
        '''
        Method to plot specific machines with specific proxies, duration vs datetime
        @params: machine = array of machines, like machine = ["MLCA", "MLCB"]
        @params: proxy = array of proxies, like proxy = ["P2", "P3"]
        '''

        if not machine or not proxy:
            print("Empty parameter array detected. Check arguments")
            return

        selected = {f"{mlc}_{p}" for mlc in machine for p in proxy}

        if (len(selected) > 1):
            datetimeArrays = np.array([pd.to_datetime([cell for cell in self.datetime_table[machine_proxy].values], format="%Y-%m-%d-%H-%M-%S") for machine_proxy in selected])

            datetimeArrays_int64 = datetimeArrays.astype(np.int64)
            average_time_np = np.mean(datetimeArrays_int64, axis=0)
            datetimeArray = pd.to_datetime(average_time_np)

        else:
            datetimeArray = [cell[0] for cell in self.datetime_table[selected].values]
            datetimeArray = pd.to_datetime(datetimeArray, format="%Y-%m-%d-%H-%M-%S")

        DF = self.duration_table.copy()
        DF = DF.set_index(datetimeArray)

        DF.plot.line(y=selected, color=[self.colordict.get(x, '#333333') for x in selected])

        plt.xlabel("Datetime (M-D-H)")
        plt.ylabel("Duration (seconds)")

        if savepath:
            plt.savefig(savepath)
            return
        else:
            plt.show()

    def plotMachineThroughputVsRound(self, machine=["MLCA, MLCB, MLCC, MLCD"], proxy=["P2", "P3"], savepath = ""):
        '''
        Method to plot specific machines with specific proxies (in duration)
        @params: machine = array of machines, like machine = ["MLCA", "MLCB"]
        @params: proxy = array of proxies, like proxy = ["P2", "P3"]
        '''

        if not machine or not proxy:
            print("Empty parameter array detected. Check arguments")
            return

        selected = {f"{mlc}_{p}" for mlc in machine for p in proxy}

        DF = self.duration_table.copy()
        DF = DF.apply(lambda x: 1024 * 8 / x if x.name in selected else x)

        DF.plot.line(x="Round", y= selected, color=[self.colordict.get(x, '#333333') for x in selected])

        plt.xlabel("Round (index)")
        plt.ylabel("Throughput (Mb/s)")

        if savepath:
            plt.savefig(savepath)
        else:
            plt.show()

    def plotMachineThroughputVsDateTime(self, machine=["MLCA, MLCB, MLCC, MLCD"], proxy=["P2", "P3"], savepath = ""):
        '''
        Method to plot specific machines with specific proxies, duration vs datetime
        @params: machine = array of machines, like machine = ["MLCA", "MLCB"]
        @params: proxy = array of proxies, like proxy = ["P2", "P3"]
        '''

        if not machine or not proxy:
            print("Empty parameter array detected. Check arguments")
            return

        selected = {f"{mlc}_{p}" for mlc in machine for p in proxy}

        if (len(selected) > 1):
            datetimeArrays = np.array([pd.to_datetime([cell for cell in self.datetime_table[machine_proxy].values], format="%Y-%m-%d-%H-%M-%S") for machine_proxy in selected])

            datetimeArrays_int64 = datetimeArrays.astype(np.int64)
            average_time_np = np.mean(datetimeArrays_int64, axis=0)
            datetimeArray = pd.to_datetime(average_time_np)

        else:
            datetimeArray = [cell[0] for cell in self.datetime_table[selected].values]
            datetimeArray = pd.to_datetime(datetimeArray, format="%Y-%m-%d-%H-%M-%S")

        DF = self.duration_table.copy()
        DF = DF.set_index(datetimeArray)
        DF = DF.apply(lambda x: 1024 * 8 / x if x.name in selected else x)

        DF.plot.line(y=selected, color=[self.colordict.get(x, '#333333') for x in selected])

        plt.xlabel("Datetime (M-D-H)")
        plt.ylabel("Throughput (Mb/s)")

        if savepath:
            plt.savefig(savepath)
        else:
            plt.show()


# Example use
A = LogFileAnalyzer("./1G_log.txt")

A.plotMachineDurationVsDateTime(machine=["MLCA", "MLCB"], proxy=["P2", "P3"], savepath="./duration_vs_datetime.png")
A.plotMachineDurationVsRound(machine=["MLCA", "MLCB"], proxy=["P2", "P3"],savepath="./duration_vs_round.png")
A.plotMachineThroughputVsRound(machine=["MLCA", "MLCB"], proxy=["P2", "P3"],savepath="./throughput_vs_round.png")
A.plotMachineThroughputVsDateTime(machine=["MLCA", "MLCB"], proxy=["P2", "P3"],savepath="./duration_vs_round.png")
