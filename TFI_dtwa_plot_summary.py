import numpy as np
import setup
import spin_dynamics as sd
import util
from collections import defaultdict
import matplotlib.pyplot as plt

if __name__ == '__main__':
    np.set_printoptions(threshold=np.inf)
    
    dirname = 'TFI_dtwa'

    variance_SN_vs_h_vs_range_vs_N = defaultdict(dict)
    t_vs_h_vs_range_vs_N = defaultdict(dict)
    method = 'TFI'
    t_vs_N_vs_range_h_1 = defaultdict(dict)
    for N in [10,20,50,100,200]:
        variance_SN_vs_h_vs_range = defaultdict(dict)
        t_vs_h_vs_range = defaultdict(dict)
        for interaction_range in [0,0.5,1,1.5,2,2.5,3]:
            variance_SN_vs_h = {}
            t_vs_h = {}
            h_list = [0,0.5,1,1.5,2]
            for h in h_list: 
                filename = 'observables_vs_t_{}_N_{}_{}_{}_{}_h_{}'.format(method, N, 'power_law', 'exp', interaction_range, h)
                observed_t = util.read_observed_t('{}/{}'.format(dirname, filename))

                variance_SN_t, variance_norm_t, angle_t, t = observed_t['min_variance_SN'], observed_t['min_variance_norm'], observed_t['opt_angle'], observed_t['t']

                variance_SN_vs_h[h] = variance_SN_t
                t_vs_h[h] = t

                if h == 1:
                    t_vs_N_vs_range_h_1[interaction_range][N] = t[np.argmin(variance_SN_t)]

            variance_SN_vs_h_vs_range[interaction_range] = variance_SN_vs_h
            t_vs_h_vs_range[interaction_range] = t_vs_h
        variance_SN_vs_h_vs_range_vs_N[N] = variance_SN_vs_h_vs_range
        t_vs_h_vs_range_vs_N[N] = t_vs_h_vs_range

    variance_SN_vs_N_vs_range_h_1 = defaultdict(dict)
    for N, variance_SN_vs_h_vs_range in variance_SN_vs_h_vs_range_vs_N.items():
        fig = plt.figure(figsize=(7.2,4.8))
        title = 'N = {}, power law'.format(N)
        plt.title(title)
        plt.xlabel('h')
        plt.ylabel('N * <S_a^2> / <S_x>^2')
        plt.ylim(bottom=0., top=1.)
        color_idx = np.linspace(1. / len(variance_SN_vs_h_vs_range), 1., len(variance_SN_vs_h_vs_range))
        for i, (interaction_range, variance_SN_vs_h) in zip(color_idx, variance_SN_vs_h_vs_range.items()):
            h_list = []
            min_variance_SN_list = []
            for h, variance_SN_t in variance_SN_vs_h.items():
                h_list.append(h)
                min_variance_SN_list.append(min(variance_SN_t))
            plt.plot(h_list, min_variance_SN_list, marker='o', label='exp = {}'.format(interaction_range), color=plt.cm.get_cmap('Reds')(i))
            variance_SN_vs_N_vs_range_h_1[interaction_range][N] = min(variance_SN_vs_h[1])
        plt.legend()
        plt.savefig('TFI_dtwa/plots/min_variance_SN_vs_h_N_{}_all_ranges.png'.format(N))

    fig = plt.figure(figsize=(7.2,4.8))
    title = 'h = 1, power law'.format(N)
    plt.title(title)
    plt.xlabel('N')
    plt.ylabel('N * <S_a^2> / <S_x>^2')
    plt.ylim(bottom=0., top=1.)
    color_idx = np.linspace(1. / len(variance_SN_vs_N_vs_range_h_1), 1., len(variance_SN_vs_N_vs_range_h_1))
    for i, (interaction_range, variance_SN_vs_N) in zip(color_idx, variance_SN_vs_N_vs_range_h_1.items()):
        N_list = []
        min_variance_SN_list = []
        for N, min_variance_SN in variance_SN_vs_N.items():
            N_list.append(N)
            min_variance_SN_list.append(min_variance_SN)
        plt.plot(N_list, min_variance_SN_list, marker='o', label='exp = {}'.format(interaction_range), color=plt.cm.get_cmap('Reds')(i))
    plt.legend()
    plt.savefig('TFI_dtwa/plots/min_variance_SN_vs_N_h_1_all_ranges.png'.format(N))

    fig = plt.figure(figsize=(7.2,4.8))
    title = 'h = 1, power law'.format(N)
    plt.title(title)
    plt.xlabel('N')
    plt.ylabel('N * <S_a^2> / <S_x>^2')
    plt.ylim(bottom=0., top=1.)
    color_idx = np.linspace(1. / len(t_vs_N_vs_range_h_1), 1., len(t_vs_N_vs_range_h_1))
    for i, (interaction_range, t_opt_vs_N) in zip(color_idx, t_vs_N_vs_range_h_1.items()):
        N_list = []
        t_opt_list = []
        for N, t_opt in variance_SN_vs_N.items():
            N_list.append(N)
            t_opt_list.append(t_opt)
        plt.plot(N_list, t_opt_list, marker='o', label='exp = {}'.format(interaction_range), color=plt.cm.get_cmap('Reds')(i))
    plt.legend()
    plt.savefig('TFI_dtwa/plots/t_opt_vs_N_h_1_all_ranges.png'.format(N))

