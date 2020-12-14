import matplotlib as mpl
mpl.use('AGG')
font = { 'size'   : 40 }
from pylab import rcParams
rcParams['figure.figsize'] = 10, 8
import pdb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math as m


mpl.style.use('seaborn-paper')
rcParams['figure.figsize'] = 10,8
# rcParams['savefig.pad_inches'] = 0.5
rcParams['figure.constrained_layout.use'] = True
mpl.rcParams['font.size'] =  15.0

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'x-large',
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)

labelmap = {
    'pcc': 'PCC',
    'bbr': 'BBR',
    'cubic': 'Cubic',
    'hybla' : 'Hybla'#,
    #'Proxy2' : 'proxy on',
    #'Proxy3' : 'proxy off'
}

colormap = {
    'pcc': 'firebrick',
    'bbr': 'olivedrab',
    'cubic': 'teal',
    'hybla' : 'darkorchid'#,
    #'Proxy2': 'teal',
    #'Proxy3' : 'darkorchid'
}

#DATA_DIR = './data/2020-12-04-00/'
#DATA_DIR = './data/first10/'
DATA_DIR = './csv_proxy2'

#test trials group by proxy mode
def test_summary(prefix=""):
    fname = f"{DATA_DIR}/test.csv"
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
        plt.savefig(f"{DATA_DIR}/{PREFIX}testtimeplot.png")
        plt.close()



#update rtt_summary by adding rtt timeplot
def rtt_summary(prefix=""):
    global PREFIX
    PREFIX = prefix

    fname = f"{DATA_DIR}/{PREFIX}rtt_quantiles.csv"
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
    rtt_summary()
    loss_summary()
    test_summary()

    rtt_summary(prefix="steady_")
    loss_summary(prefix="steady_")


if __name__ == "__main__":
    main_summary()
