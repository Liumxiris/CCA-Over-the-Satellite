#replace function parse_csv in analyze.py at line 152
#return entire pcap/csv throughput over time (per second) in to a seperate diff.csv
def parse_csv(filename, reparse=False):
    """
    return pandas version of the csv
    """
    sender_path, receiver_path = parsed_filenames(filename)

    if (path.isfile(receiver_path) and path.isfile(sender_path) and not reparse):
        receiver_flow = feather.read_dataframe(receiver_path)
        sender_flow = feather.read_dataframe(sender_path)
        return (sender_flow, receiver_flow)

    df = load_dataframe(filename)
    #print(f"filename is {filename}")
    if "mlcnetA.cs.wpi.edu" in filename:
        #print("cubic")
        protocol = "cubic"
    if "mlcnetB.cs.wpi.edu" in filename:
        protocol = "bbr"
    if "mlcnetC.cs.wpi.edu" in filename:
        protocol = "hybla"
    if "mlcnetD.cs.wpi.edu" in filename:
        protocol = "pcc"
    # df.columns[df[.columns != 'tcp.analysis.ack_rtt']
    required_columns = ['frame.time', 'frame.number', 'frame.time_epoch', 'eth.src', 'eth.dst',
                        'ip.src', 'ip.dst', 'tcp.srcport', 'tcp.dstport', 'tcp.seq', 'ip.proto', 'time']
    df.dropna(subset=required_columns, inplace=True)
    df = df.set_index('frame.time').sort_index()
    
    # print(df.reset_index()[['time', 'tcp.seq']]) #Dec  4, 2020 13:40:36.023884000 CST
                                                   #2020-12-04 13:40:36.023884+08:00
                                                   #'tcp.srcport' = 5201
    # df = df.loc[df['tcp.srcport'] == 5201]
    # df = df.loc[(df['tcp.srcport'] == 5201) & (df['tcp.dstport'] == 48198)]
    most = df.mode()['tcp.dstport'][0]
    print(most)
    df = df.loc[(df['tcp.srcport'] == 5201) & (df['tcp.dstport'] == most)]
    
#    grouped_df = df.groupby(pd.Grouper(key = 'time', freq='1S')).agg({'tcp.seq':'min', 'tcp.seq':'min'})[['tcp.seq','tcp.seq']].reset_index()
    
    grouped_df = df.groupby(pd.Grouper(key = 'time', freq='1S')).agg({'tcp.seq': [np.min, np.max]})
    print(grouped_df)
    
    difference = grouped_df.diff(axis=0).div(125000).fillna(0).abs()
    print("\n\nDifference between rows(Period=1):")
    # print(difference.keys());
    difference.columns = ['mindiff', 'maxdiff']
    difference['protocol'] = protocol
    print(difference);
    if not difference.empty:
    # store the last non-empty one corrsponding to mlcnet*.csv
        difference.to_csv(f"{DATA_DIR}/diff.csv")
    #difference.plot()
    
#    for key, item in grouped_df:
#        print(grouped_df.get_group(key), "\n\n")
       
#    gb = grouped_df.groups
#    key_list_from_gb = ['time', 'tcp.seq']
#    for key, values in gb.items():
#        if key in key_list_from_gb:
#            print(df.ix[values], "\n")

    group_tuple = ["ip.src", "ip.dst", "tcp.srcport", "tcp.dstport"]

    remote_prefix = "130."
    sender_selection = df['ip.src'].str.contains(remote_prefix)
    receiver_selection = ~sender_selection

    sender_traffic = df[sender_selection].groupby(group_tuple)
    sender_flow = select_data_flow(sender_traffic)
    feather.write_dataframe(sender_flow, sender_path)

    receiver = df[receiver_selection].groupby(group_tuple)
    receiver_flow = select_data_flow(receiver)
    feather.write_dataframe(receiver_flow, receiver_path)

    return (sender_flow, receiver_flow)
