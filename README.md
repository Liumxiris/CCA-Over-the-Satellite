# CCA-Over-the-Satellite

# About 
This is the main repository for CCA-Over-the-Satellite ISP B term. 

## Directory 
```bash
.
├── notes: all research notes
├── figures: contains figures we had
│   ├── ?? Category
│   │   └── bar_chunks_fraction: contains the scripts and the data 
│   └── ?? Category
│       └── checkpoint_overhead
├── src: project code
│   ├── DataAnalysis: Analysis Scripts
│   ├── DataCollection: Collection Scripts.
│   │   ├── Old_Trial : Trial System used for week 3 - week 7 data collection.
│   │   └── New_Trial : Trial System proposed at week 6, finished at week 7
└──
```

## Findings

- Progress
    - Week1:
        - Background presentations on four congestion control algorithms.
    - Week2:
        - Studied basic commands: route, tcpdump, iperf, etc.
    - Week3:
        - Developed scripts for repeated experiment runs and pipelined data analysis.
    - Week4:
        - Tested scripts for turning proxy on/off.
        - Prepared for 24 hours data collection.
        - Wrote logfile analyzer to estimate throughputs without actually using pcaps and csv.
    - Week5:
        - Presented data collected over 35 hours run
    - Week6:
        - Developed new script to analyze single trial and best/worst case for each proxy in the entire 24 hours experiment.
    - Week7:
        - Presented data collected over 24 hours run (on workday) and generated more significant data (mean and standard deviation)

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
