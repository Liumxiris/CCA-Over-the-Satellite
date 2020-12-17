### Traces
We automatically store traces at one location: /home/yliu31/clayTrials/EXPERIMENT_NAME, where EXPERIMENT_NAME varies.

- Trace Locations "/home/yliu31/clayTrials/EXPERIMENT_NAME/":
    - For a certain experiment named as TEST (Old Trial):
        - Base log file: DATASIZE_log.txt (for example, 1G_log.txt)
        - Data folder: data

- Within Data Folder ".../EXPERIMENT_NAME/data/":
Folders named with scheme "YYYY-MM-DD-HH" => When test started

- Within each timestamp folder ".../data/TIMESTAMP":
Trial folders named as _Machine_\__Protocol_\__Proxy_\__Datasize_\__Round_ for each trial on each machine

- For each trial folder ".../TIMESTAMP/mlcnetX_...(TRIAL FOLDER)":
local.pcap => From glomma TCPDUMP
_MACHINENAME_.pcap => From remote
udpLog.txt => UDP PING log (Since TEST_DAY_4. More info about timeline see timeline section below) 

- Since WEEKEND_TEST_2:
One additional layer of directory is added between /TIMESTAMP/ and /TRIAL FOLDER/ => /Proxy2/ and /Proxy3/

### Trace Timeline
-------WITH OLD SYSTEM-------
- 2020-11-11: Few rounds of trial for testing functionality [Not used, saved for record]   
- TEST_DAY_1: 2020-11-13-00: 35 Runs of Proxy2+Proxy3 on 4 machine_protocols, for functionality usage. [Not used, saved for record][Discarded for "for loop sequence" reason]   
- TEST_DAY_1_TRIAL2: 2020-11-14-00: 100 Runs of 50M + 80 Runs of 1G for Proxy2+Proxy3 on 4 machine_protocols. [Not used, saved for record][Discarded for "routing (not used satellite link)" reason]   
- TEST_DAY_2: 2020-11-14-00: 500 Runs of 1G and 250 Runs of 2G for Proxy2+Proxy3 on 4 machine_protocols. [Not used, saved for record][Discarded for "routing (not used satellite link)" reason]   
- TEST_DAY_3: 2020-11-16-00: 55 Runs of 1G for Proxy2+Proxy3 on 4 machine_protocols. [**Used for Week 5 Report**]
- TEST_DAY_4: 2020-11-17-00: 45 Runs of 1G for Proxy2+Proxy3 on 4 machine_protocols. [Not used, saved for record][**Used for Week 6 Report** => Data seemed to be fine, but due to dual folder, there might be some issues happened while processing]
- TEST_DAY_4: 2020-11-23-00: Wrong Launch. Should be ignored => overwrites 1G_log for "2020-11-17-00" test. [Not used, saved for record]
- TEST_DAY_1_WK2: 2020-12-04-00: 5 Runs of 1G for Proxy2+3 on 4 machine_protocols, for testing functionality. [Not used, saved for record]
- WEEKEND_TEST_2: 2020-12-07-00: 47 Runs of 1G for Proxy2+3 on 4 machine_protocols. [**Used for Week 7 Report**]
-------WITH OLD SYSTEM-------

-------WITH NEW SYSTEM-------
-------WITH NEW SYSTEM-------

### Official Usage History
Week 5:
TEST_DAY_3 (55 Rounds => [Week 5 Report](notes/TCP_Nov_18th.pdf))

Week 6:
TEST_DAY_4 and TEST_DAY_1_WK2 (Bad for MLCA due to disk storage issue, and somehow log file is missing)

Week 7:
WEEKEND_TEST_2 (47 Rounds => [Week 7 Report](notes/TCP_Dec_9.pdf))
More info: [Week 7 Trace Usage](notes/Week7_Trace_README.md)
