import matplotlib.pyplot as plt
import numpy as np
import os
import pandas

FILENAME = 'tarjan_results_final.csv'
PLOT_FILENAME = 'python_res.png'

if __name__=="__main__":

    csv_file_name = FILENAME
    csv_file_path = os.path.join(os.getcwd(), csv_file_name)
    freq = 0.01  # python
    lang= 'python'
    if 'java' in csv_file_name:
        freq = 0.001  # java
        lang = 'java'
    column_names = ['nodes', 'prob', 'edges', 'time']
    result_data = pandas.read_csv(csv_file_path, sep=",", names=column_names, header=None)
    # selected_df = result_data.loc[(result_data['nodes'] == 5000) & np.isclose(result_data['prob'], 0.00006, 1e-20)].copy()
    # print(selected_df['time'] .mean())
    unique_nodes = result_data['nodes'].unique()  # numpy ndarray
    unique_probabilities = result_data['prob'].unique()

    grouped_by_nodes_prob = result_data.groupby(['nodes', 'prob'], as_index=False)
    grouped_by_nodes_prob_mean = grouped_by_nodes_prob['time'].mean()
    g = result_data.groupby(['nodes','prob'])['time'].mean()

    print(grouped_by_nodes_prob_mean) # tutaj wypisuje średnie czasy
    # ax = grouped_by_nodes_prob_mean.plot(x=['nodes', 'prob'], y='time', grid=True)
    ax = g.plot(title=r'Czas(n, $p_0$) dla grafów E-R ({})'.format(lang), grid='True')
    ax.set_xticks(range(len(g)))
    ax.set_xticklabels([(('%.0e' % item[0]), ('%.0e' % item[1])) for item in g.index.tolist()], rotation=90)

    ax.set_ylabel(r'Czas $[s]$')
    ax.set_xlabel('$(n, p_0)$')

    # # hides every nth tick label
    # for label in ax.get_xticklabels()[::2]:
    #     label.set_visible(False)
    n=4
    for index, label in enumerate(ax.xaxis.get_ticklabels()):
        if index % n != 0:
            label.set_visible(False)

    start, end = ax.get_ylim()

    ax.yaxis.set_ticks(np.arange(0.0, end, freq))
    # plt.show()
    plt.savefig(PLOT_FILENAME, bbox_inches='tight')
