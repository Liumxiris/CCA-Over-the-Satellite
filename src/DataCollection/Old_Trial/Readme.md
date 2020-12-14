## Old Trial
- Source directory: at GLOMMA, /home/yliu31/scripts/OLD_TRIAL
- Used from Week 4 - Week 7 to get experiment data

## Structure and How to Execute
- Majorly inherited from previous codes
- Additions:
    - proxy_test.py: 
        - The main script for executing test. 
        - Can define name of the test, which will determine where data will be stored
        - Can define how many rounds for what data sizes
        - Can define proxy modes
        - Will generate a log file which contains running time of each trial. Can be used for analysis.
    - Some changes in Trial.py
- How to execute:
    - At /home/yliu31/scripts/OLD_TRIAL: screen -dm python3 proxy_tests.py

## UDP Ping
- Where are the udp ping executables?
    - GLOMMA: /home/yliu31/.local/bind/cUDPingLnx
    - MLC: /home/yliu31/.local/bin/sUDPingLnx
    - Usage: 
        - MLC (UDP PING SERVER): 
            - sUDPingLnx _port_, we used "sUDPingLnx 5202"
        - GLOMMA (UDP PING CLIENT): 
            - cUDPingLnx -h _host_ -p _port on host_ -s _size_ -n _packets per second_
            - we used "cUDPingLnx -h {self.remote} -p 5202 -s 12 -n 4 > {self.local_udplog}"
    - Additions in clean up:
        - used kill_cmd_local = 'pkill ' + '; pkill '.join(procs_local) + '; pkill -2 cUDPingLnx ;' at glomma
        - Because for redirection >, it needs SIG as -2 (Interrupt) to write successfully
    