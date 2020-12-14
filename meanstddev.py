#summarize avg difference & stdand dev between two proxy mode: proxy on/off
def DIFF_summary(prefix=""):

    fname = f"{DATA_DIR}/diff.csv"
    df = pd.read_csv(fname, index_col=0).dropna(how='all')
    #print(df)
    #df['start_time'] = df.index.astype(str).str[:-6]
    df['start_time'] = pd.to_datetime(df.index).tz_localize(None)
    df = df.set_index('start_time')
    df['start_time'] = df.index
    
    if 'start_time' in df.keys():
        for protocol, data in df.groupby('protocol'):
        #for protocol, data in df.groupby('protocol'):
        #for proxy, data in df.groupby('proxy'):
            column = 'mindiff'
            column_name = 'mindiff'

            plt.plot(data.index, data[column], label=labelmap[protocol], color=colormap[protocol])
            #plt.plot(data.index, data[column])

    ticks = [df['start_time'].quantile(i) for i in np.arange(0, 1, .1)]
    plt.xticks(fontsize=10, rotation=15)
    plt.legend([protocol])
    #plt.legend(["proxy off", "proxy on"])
    plt.ylabel("Throughput(Mb/s)")
    date_formatter = mpl.dates.DateFormatter("%H:%M:%S")
    ax = plt.gca()
    ax.set_ylim([0,250])
    ax.xaxis.set_major_formatter(date_formatter)
    plt.savefig(f"{DATA_DIR}/{PREFIX}diff_timeplot.png")
    plt.close()
    
def cubic_summary(prefix=""):

    fname = f"{DATA_DIR}/startup_cubic.csv"
    df = pd.read_csv(fname, index_col=0).dropna(how='all')
    df['start_time'] = pd.to_datetime(df['start_time'], errors='coerce').dropna()
    df = df.set_index('start_time').sort_index()
    df['start_time'] = df.index

    plt.close()
    if 'start_time' in df.keys():
        for proxy, data in df.groupby('proxy'):
            column = 'mean'
            column_name = 'mean'
            if m.isnan(data[column][0]):
                column = '0.5'
                column_name = 'median'

            plt.plot(data.index, data[column], label=labelmap[proxy], color=colormap[proxy])

        ticks = [df['start_time'].quantile(i) for i in np.arange(0, 1, .1)]
        plt.xticks(ticks, rotation=15)
        plt.legend()
        plt.ylabel("Cubic")
        date_formatter = mpl.dates.DateFormatter("%m/%d - %H:%M")
        ax = plt.gca()
        ax.xaxis.set_major_formatter(date_formatter)
        ax.set_ylim([0,150])
        plt.savefig(f"{DATA_DIR}/{PREFIX}startup_cubic.png")
        plt.close()
    
    grouped = df.groupby('proxy')
    p2 = grouped.get_group('Proxy2')['mean'].reset_index()
    p3 = grouped.get_group('Proxy3')['mean'].reset_index()
    print("\nmean and std of cubic is")
    print((p2['mean']-p3['mean']).mean())
    print((p2['mean']-p3['mean']).std())
    
def bbr_summary(prefix=""):

    fname = f"{DATA_DIR}/startup_bbr.csv"
    df = pd.read_csv(fname, index_col=0).dropna(how='all')
    df['start_time'] = pd.to_datetime(df['start_time'], errors='coerce').dropna()
    df = df.set_index('start_time').sort_index()
    df['start_time'] = df.index

    plt.close()
    if 'start_time' in df.keys():
        for proxy, data in df.groupby('proxy'):
            column = 'mean'
            column_name = 'mean'
            if m.isnan(data[column][0]):
                column = '0.5'
                column_name = 'median'

            plt.plot(data.index, data[column], label=labelmap[proxy], color=colormap[proxy])

        ticks = [df['start_time'].quantile(i) for i in np.arange(0, 1, .1)]
        plt.xticks(ticks, rotation=15)
        plt.legend()
        plt.ylabel("BBR")
        date_formatter = mpl.dates.DateFormatter("%m/%d - %H:%M")
        ax = plt.gca()
        ax.xaxis.set_major_formatter(date_formatter)
        ax.set_ylim([0,150])
        plt.savefig(f"{DATA_DIR}/{PREFIX}startup_bbr.png")
        plt.close()
        
    grouped = df.groupby('proxy')
    p2 = grouped.get_group('Proxy2')['mean'].reset_index()
    p3 = grouped.get_group('Proxy3')['mean'].reset_index()
    print("\nmean and std of bbr is")
    print((p2['mean']-p3['mean']).mean())
    print((p2['mean']-p3['mean']).std())
    
def hybla_summary(prefix=""):

    fname = f"{DATA_DIR}/startup_hybla.csv"
    df = pd.read_csv(fname, index_col=0).dropna(how='all')
    df['start_time'] = pd.to_datetime(df['start_time'], errors='coerce').dropna()
    df = df.set_index('start_time').sort_index()
    df['start_time'] = df.index

    plt.close()
    if 'start_time' in df.keys():
        for proxy, data in df.groupby('proxy'):
            column = 'mean'
            column_name = 'mean'
            if m.isnan(data[column][0]):
                column = '0.5'
                column_name = 'median'

            plt.plot(data.index, data[column], label=labelmap[proxy], color=colormap[proxy])

        ticks = [df['start_time'].quantile(i) for i in np.arange(0, 1, .1)]
        plt.xticks(ticks, rotation=15)
        plt.legend()
        plt.ylabel("Hybla")
        date_formatter = mpl.dates.DateFormatter("%m/%d - %H:%M")
        ax = plt.gca()
        ax.xaxis.set_major_formatter(date_formatter)
        ax.set_ylim([0,150])
        plt.savefig(f"{DATA_DIR}/{PREFIX}startup_hybla.png")
        plt.close()
        
    grouped = df.groupby('proxy')
    p2 = grouped.get_group('Proxy2')['mean'].reset_index()
    p3 = grouped.get_group('Proxy3')['mean'].reset_index()
    print("\nmean and std of hybla is")
    print((p2['mean']-p3['mean']).mean())
    print((p2['mean']-p3['mean']).std())
    
def pcc_summary(prefix=""):

    fname = f"{DATA_DIR}/startup_pcc.csv"
    df = pd.read_csv(fname, index_col=0).dropna(how='all')
    df['start_time'] = pd.to_datetime(df['start_time'], errors='coerce').dropna()
    df = df.set_index('start_time').sort_index()
    df['start_time'] = df.index

    plt.close()
    if 'start_time' in df.keys():
        for proxy, data in df.groupby('proxy'):
            column = 'mean'
            column_name = 'mean'
            if m.isnan(data[column][0]):
                column = '0.5'
                column_name = 'median'

            plt.plot(data.index, data[column], label=labelmap[proxy], color=colormap[proxy])

        ticks = [df['start_time'].quantile(i) for i in np.arange(0, 1, .1)]
        plt.xticks(ticks, rotation=15)
        plt.legend()
        plt.ylabel("PCC")
        date_formatter = mpl.dates.DateFormatter("%m/%d - %H:%M")
        ax = plt.gca()
        ax.xaxis.set_major_formatter(date_formatter)
        ax.set_ylim([0,150])
        plt.savefig(f"{DATA_DIR}/{PREFIX}startup_pcc.png")
        plt.close()
    
    grouped = df.groupby('proxy')
    p2 = grouped.get_group('Proxy2')['mean'].reset_index()
    p3 = grouped.get_group('Proxy3')['mean'].reset_index()
    print("\nmean and pcc of bbr is")
    print((p2['mean']-p3['mean']).mean())
    print((p2['mean']-p3['mean']).std())


def rtt_summary(prefix=""):
    global PREFIX
    PREFIX = prefix

    fname = f"{DATA_DIR}/proxy2_{PREFIX}rtt_quantiles.csv"
    df = pd.read_csv(fname, index_col=0).dropna(how='all')
    #print(df)
    df['start_time'] = pd.to_datetime(df['start_time'], errors='coerce').dropna()
    #print(df)
    df = df.set_index('start_time').sort_index()
    df['start_time'] = df.index
    
    if 'start_time' in df.keys():
        for protocol, data in df.groupby('protocol'):
            column = 'mean'
            column_name = 'mean'

            plt.plot(data.index, data[column], label=labelmap[protocol], color=colormap[protocol]) # scatter

    ticks = [df['start_time'].quantile(i) for i in np.arange(0, 1, .1)]
    #print(ticks) # Timestamp('2020-12-04 00:36:55.719051008')
    plt.xticks(ticks, rotation=15)
    plt.legend()
    # plt.ylabel(column_name)
    plt.ylabel("RTT(ms)")
    date_formatter = mpl.dates.DateFormatter("%m/%d - %H:%M")
    ax = plt.gca()
    ax.set_ylim([500,4200])
    ax.xaxis.set_major_formatter(date_formatter)
    plt.savefig(f"{DATA_DIR}/{PREFIX}rtt_timeplot.png")
    plt.close()
    
    columns = ['0.1', '0.5', '0.75']

    for column in columns:
        plot_rtt_cdf(df, column)

    plt.close()

    df = df[['0', '0.1', '0.25', '0.5', '0.75',
             '0.9', '1.0', 'host', 'protocol']]

    df.boxplot()
    plt.savefig(f"{DATA_DIR}/{PREFIX}rtt_boxplot.png")
    plt.close()

def loss_summary(prefix=""):
    global PREFIX
    PREFIX = prefix

    fname = f"{DATA_DIR}/proxy2_{PREFIX}losses.csv"
    df = pd.read_csv(fname, index_col=0).dropna(how='all')
    df['start_time'] = pd.to_datetime(df['start_time'], errors='coerce').dropna()
    df = df.set_index('start_time').sort_index()
    df['start_time'] = df.index

    plot_loss_cdf(df)
    plt.close()

    # pdb.set_trace()

    if 'start_time' in df.keys():
        for protocol, data in df.groupby('protocol'):
            column = 'loss'
            column_name = 'loss'

            plt.plot(data.index, data[column] * 100, label=labelmap[protocol], color=colormap[protocol]) # scatter

    ticks = [df['start_time'].quantile(i) for i in np.arange(0, 1, .1)]
    plt.xticks(ticks, rotation=15)
    plt.legend()
    # plt.ylabel(column_name)
    plt.ylabel("Loss rate")
    date_formatter = mpl.dates.DateFormatter("%m/%d - %H:%M")
    ax = plt.gca()
    ax.set_ylim([0,5.5])
    ax.xaxis.set_major_formatter(date_formatter)
    plt.savefig(f"{DATA_DIR}/{PREFIX}loss_timeplot.png")
    plt.close()

def main_summary():
    DIFF_summary()
    cubic_summary()
    bbr_summary()
    hybla_summary()
    pcc_summary()

if __name__ == "__main__":
    main_summary()
