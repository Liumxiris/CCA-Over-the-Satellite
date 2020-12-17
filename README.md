# CCA-Over-the-Satellite

# About 
This is the main repository for CCA-Over-the-Satellite ISP B term. 

## Directory 
```bash
.
├── notes: all research notes
├── src: project code
│   ├── DataAnalysis: Analysis Scripts
│   ├── DataCollection: Collection Scripts.
│   │   ├── Old_Trial : Trial System used for week 3 - week 7 data collection.
│   │   └── New_Trial : Trial System proposed at week 6, finished at week 7
└──
```

## Findings / Learnings
- Week1:
    - Background presentations on four congestion control algorithms.
        - Cubic: Cubic growth rather than linear growth, and window growth depends only on time between two consecutive congestion events => window growth becomes independent of RTT.
        - Hybla: Window size depends on constant RTT0  => Fast window growth at start, but have overshoot and loss possibility
        - BBR: Estimates RTT and bottleneck capacity, intended to avoid network queuing.
        - PCC: Send several small tests before transmission to estimate optimized throughput at real time.
- Week2:
    - Studied basic commands: route, tcpdump, iperf, etc.
    - Learned how to execute one test manually
        - Used screen to launch tcpdump in background and output as pcap.
        - Used iperf to send certain amount of testing traffic
- Week3:
    - Learned the idea of test automation
    - Learned how to turn proxy on and off manually
    - Inherited and explored scripts for repeated experiment runs and pipelined data analysis.
    - Tried to graph one test
    - Prepared for 24 hours data collection.
- Week4 [Report PPT](./notes/TCP_Nov_18th.pdf):
    - Tested scripts for turning proxy on/off (Old Trial System).
    - Wrote logfile analyzer to estimate throughput with time spent for each test rather than actually using pcaps and csv.
    - Presented data collected over 35 hours run (55 rounds) => Try to make it 24 hours
    - There are busy and non-busy hours => 9-11 in the morning, and 15-19 in the afternoon
    - ProxyOn generally performs better than ProxyOff, especially in non-busy hours.
    - When ProxyOn, all four protocols performed equally
    - When ProxyOff, Hybla, Cubic > BBR > PCC
- Week5 (Thanksgiving Break):
    - Added UDP Ping
    - Finishing Goals on "Next Step" (Page 7) in [Week4 Report PPT](./notes/TCP_Nov_18th.pdf)
- Week6 [Report PPT](./notes/TCP_Dec_2nd.pdf):
    - Developed new script to analyze single trial and best/worst case for each proxy in the entire 24 hours experiment.
    - Found out that there are some issues with timestamp, and logfile is empty for TestDay4 => Possibly due to overwrite (executed another test with same name after ran official one)
    - Used every transaction to draw => should use per second average
    - Scheduled Goals on "Next Step" (Page 7) in [Week6 Report PPT](./notes/TCP_Dec_2nd.pdf)
- Week7 [Report PPT](./notes/TCP_Dec_9.pdf):
    - Failed tests due to multiple errors (ip change, route reset, etc.). Only got one day of successful data
    - Presented data collected over 24 hours run (on workday, Dec.7) and generated more significant data (mean and standard deviation)
    - Best cases occur during non-busy hours, worst cases in busy hour
    - For ProxyOff, Hybla has the highest RTT, Cubic has the highest loss rate
    - For ProxyOn, all perform the same, but BBR has slightly higher loss rate during non-busy hours
    - Hybla has worst performance when ProxyOn, with avg diff of -1
    - PCC has the greatest difference but also greatest std, which may indicate unstable performance
    - Flat line for throughput around non-busy hours since Page 15 => Guess there might be a cap at Satellite link
    - For just Steady State, the results are the same
    - Put in "Download time vs. Download object size" at Page 28 in [Week 7 Report PPT](./notes/TCP_Dec_9.pdf) for Startup State
        - When ProxyOn, there are not much difference among four protocols
        - When ProxyOff, PCC has greatest std (correspond to previous finding), and performs worst. Cubic second worst, and BBR nearly equals to Hybla
- Overall
    - Proxy benefited the most for Startup Phase, especially for Cubic and Hybla (Quick Start)
    - For Startup Phase, Cubic and PCC performs worst - slower start. PCC => High std
    - For Steady State, all four protocols performed similarly. Cubic slightly benefited with ProxyOn, and Hybla got worst withProxyOn.

## System Configurations
- Flow
    ```bash
    ---------                       ---------
    |       |                       |       |
    |   G   |   => Satellite =>     |   M   |
    |       |                       |       |
    ---------                       ---------
    ```
    - For experiments, we used tcpdump to capture packets, iperf3 for simulating traffic.
    - Test Flow: 
        1) Setup Protocols at Glomma and All Machines (CC, MEM)
        2) For x in supposed_rounds:  
            - Switch Proxy
            - Do One Trial
        3) Tests Ends
    - One Trial:
        - Start TCPDUMP and UDP PING at both Glomma and Testing Machine  
        - Start IPERF3, treating Glomma as client and Testing Machine as Server
        - When IPERF3 ends, stop TCPDUMP and UDP PING
        - Store pcap from Glomma and from Testing Machine under specific folder
            - Folder Name: {machine}{protocol}{proxyMode}{dataSize}{roundIndex}

- System Versions
    - GLOMMA
        ```bash
          Static hostname: glomma
                Icon name: computer-server
                  Chassis: server
         Operating System: Ubuntu 18.04.5 LTS
                   Kernel: Linux 4.15.0-123-generic
             Architecture: x86-64
        TCP MEM/WMEM/RMEM: 60000000
                   TCP CC: Cubic
        ```
    - MLCNETA
        ```bash
          Static hostname: mlcneta
                Icon name: computer-vm
                  Chassis: vm
           Virtualization: kvm
         Operating System: Ubuntu 18.04.5 LTS
                   Kernel: Linux 4.15.0-122-generic
             Architecture: x86-64
        TCP MEM/WMEM/RMEM: 60000000
                   TCP CC: Cubic
        ```
    - MLCNETB
        ```bash
          Static hostname: mlcnetb
                Icon name: computer-vm
                  Chassis: vm
           Virtualization: kvm
         Operating System: Ubuntu 18.04.5 LTS
                   Kernel: Linux 4.15.0-128-generic
             Architecture: x86-64
        TCP MEM/WMEM/RMEM: 60000000
                   TCP CC: BBR
        ```
    - MLCNETC
        ```bash
          Static hostname: mlcnetc
                Icon name: computer-vm
                  Chassis: vm
           Virtualization: kvm
         Operating System: Ubuntu 18.04.5 LTS
                   Kernel: Linux 4.15.0-122-generic 
             Architecture: x86-64
        TCP MEM/WMEM/RMEM: 60000000
                   TCP CC: Hybla
        ```
    - MLCNETD
        ```bash
          Static hostname: mlcnetd
                Icon name: computer-vm
                  Chassis: vm
           Virtualization: kvm
         Operating System: Ubuntu 18.04.5 LTS
                   Kernel: Linux 4.15.0-96-generic
             Architecture: x86-64
        TCP MEM/WMEM/RMEM: 60000000
                   TCP CC: PCC
        ```

## Other Information
[Our Data Collection Module](./src/DataCollection/Readme.md)  
[Zack's Final Remarks](./notes/ZackFinalRemarks.txt)   
[Trace Locations/Usage Record](TraceLocations.md)
