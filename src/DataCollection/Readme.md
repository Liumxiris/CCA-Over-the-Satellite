## Data Collection
Data Collection module aims to collect data via controlled experiments automatically, which can be used for data analysis.  

Majorly we automates this by 
1. Set up a trial class(old_trial/trial.py) which will automate one round of trial over one machine.
2. Create a loop to execute the Trial class for about 24 hours.

Then we will collect and store pcap files (from tcpdump) from both tested machine and glomma for further analysis.

### Old and New Trial System
- [Old Trial System](./Old_Trial/Readme.md)
- [New Trial System](./New_Trial/Readme.md)

### Data Locations:
At GLOMMA: /home/yliu31/clayTrials 
All folders:
```bash
2020-11-11  TEST_DAY_1_TRIAL2  TEST_DAY_2  TEST_DAY_4
TEST_DAY_1  TEST_DAY_1_WK2     TEST_DAY_3  WEEKEND_TEST_2
```
 
- 2020-11-11: Trial experiment for exploring
- TEST_DAY_1 to TEST_DAY_4: Tests from week 5 to week 6
    - It is already known that due to MLCA issues, MLCA data in TEST_DAY_3 is bad
- WEEKEND_TEST_2: Test on Dec.7, final test

### Scripts Locations:
OLD_TRIAL: /home/yliu31/scripts/OLD_TRIAL
NEW_TRIAL: /home/yliu31/scripts/NEW_TRIAL, or [New_Trial](./New_Trial)