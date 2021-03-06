## Scripts & Traces used for generating plots (TCP_Dec_9.pptx)
- All scripts are located under (src/DataAnalysis)
- Plots prior to the Slide 11 are based on the test trail
- Plots starting from the Slide 11 are based on 24 hours traces
  - path on the Glomma: /home/yliu31/clayTrials/WEEKEND_TEST_2

#### slides 9-10
- Run **singletrailtimeplot.py** to generate plot for throughput vs. time. 
#### slides 11-14
- **LogFileAnayzer.py** will print out the round number of best case and worst case 
- Run **singletailtimeplot.py** on the corresponding round folder to generate throughput graph
- Best Cases with Proxy on (corresponding trace folders):
  - mlcnetA.cs.wpi.edu_cubic_Proxy2_1G_31 
  - mlcnetB.cs.wpi.edu_bbr_Proxy2_1G_28
  - mlcnetC.cs.wpi.edu_hybla_Proxy2_1G_34
  - mlcnetD.cs.wpi.edu_bbr_Proxy2_1G_28
- Best Cases with Proxy off
  - mlcnetA.cs.wpi.edu_cubic_Proxy3_1G_27 
  - mlcnetB.cs.wpi.edu_bbr_Proxy3_1G_35
  - mlcnetC.cs.wpi.edu_hybla_Proxy3_1G_29
  - mlcnetD.cs.wpi.edu_bbr_Proxy3_1G_36
- Worst Cases with Proxy on
  - mlcnetA.cs.wpi.edu_cubic_Proxy2_1G_13 
  - mlcnetB.cs.wpi.edu_bbr_Proxy2_1G_14
  - mlcnetC.cs.wpi.edu_hybla_Proxy2_1G_7
  - mlcnetD.cs.wpi.edu_bbr_Proxy2_1G_14
- Worst Cases with Proxy off
  - mlcnetA.cs.wpi.edu_cubic_Proxy3_1G_16 
  - mlcnetB.cs.wpi.edu_bbr_Proxy3_1G_7
  - mlcnetC.cs.wpi.edu_hybla_Proxy3_1G_14
  - mlcnetD.cs.wpi.edu_bbr_Proxy3_1G_14
#### slides 15-22
- All plots can be generated by **summarywithmoretimeplot.py**
#### slides 23-27
- All plots can be generted by **summarywithmoretimeplot.py**
- The std and average difference can be calculated by **meanstddev.py**
#### slide 28
- Run **download_time.py** to generate the plot
