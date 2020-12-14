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
    - Week1
            -Used data directory:
    - Week2
            -Used data directory:
    - Week3
            -Used data directory:
    - Week4
            -Used data directory:
    - Week5
            -Used data directory:
    - Week6
            -Used data directory:
    - Week7
            -Used data directory:

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
