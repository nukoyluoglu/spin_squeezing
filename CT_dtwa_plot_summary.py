import numpy as np
import setup
import spin_dynamics as sd
import util
from collections import defaultdict
import matplotlib.pyplot as plt

if __name__ == '__main__':
    np.set_printoptions(threshold=np.inf)
    
    dirname = 'CT_dtwa'

    variance_SN_vs_range_vs_N = defaultdict(dict)
    t_vs_range_vs_N = defaultdict(dict)
    variance_SN_vs_N_vs_range = defaultdict(dict)
    t_vs_N_vs_range = defaultdict(dict)
    method = 'CT'
    for N in [10,20,50,100,200]:
        for interaction_range in [0,0.5,1,1.5,2,2.5,3]:
            J_list = [1.]
            for J in J_list: 
                filename = 'observables_vs_t_{}_N_{}_{}_{}_{}_J_{}'.format(method, N, 'power_law', 'exp', interaction_range, J)
                observed_t = util.read_observed_t('{}/{}'.format(dirname, filename))

                variance_SN_t, variance_norm_t, angle_t, t = observed_t['min_variance_SN'], observed_t['min_variance_norm'], observed_t['opt_angle'], observed_t['t']

                variance_SN_vs_range_vs_N[N][interaction_range] = variance_SN_t
                t_vs_range_vs_N[N][interaction_range] = t
                variance_SN_vs_N_vs_range[interaction_range][N] = variance_SN_t
                t_vs_N_vs_range[interaction_range][N] = t

    fig = plt.figure()
    title = 'CT, power law'
    plt.title(title)
    plt.xlabel('exp')
    plt.ylabel('N * <S_a^2> / <S_x>^2')
    plt.ylim(bottom=0., top=1.)
    color_idx = np.linspace(1. / len(variance_SN_vs_range_vs_N), 1., len(variance_SN_vs_range_vs_N))
    for i, (N, variance_SN_vs_range) in zip(color_idx, variance_SN_vs_range_vs_N.items()):
        range_list = []
        min_variance_SN_list = []
        for interaction_range, variance_SN_t in variance_SN_vs_range.items():
            range_list.append(interaction_range)
            min_variance_SN_list.append(min(variance_SN_t))
        plt.plot(range_list, min_variance_SN_list, marker='o', label='N = {}'.format(N), color=plt.cm.get_cmap('Reds')(i))
    plt.legend()
    plt.savefig('CT_dtwa/plots/min_variance_SN_vs_range_all_N.png'.format(N))

    fig = plt.figure()
    title = 'CT, power law'
    plt.title(title)
    plt.xlabel('N')
    plt.ylabel('N * <S_a^2> / <S_x>^2')
    plt.ylim(bottom=0., top=1.)
    color_idx = np.linspace(1. / len(variance_SN_vs_N_vs_range), 1., len(variance_SN_vs_N_vs_range))
    for i, (interaction_range, variance_SN_vs_N) in zip(color_idx, variance_SN_vs_N_vs_range.items()):
        N_list = []
        min_variance_SN_list = []
        for N, variance_SN_t in variance_SN_vs_N.items():
            N_list.append(N)
            min_variance_SN_list.append(min(variance_SN_t))
        plt.plot(N_list, min_variance_SN_list, marker='o', label='exp = {}'.format(interaction_range), color=plt.cm.get_cmap('Reds')(i))
    plt.legend()
    plt.savefig('CT_dtwa/plots/min_variance_SN_vs_N_all_ranges.png'.format(N))

    fig = plt.figure()
    title = 'CT, power law'
    plt.title(title)
    plt.xlabel('N')
    plt.ylabel('N * <S_a^2> / <S_x>^2')
    color_idx = np.linspace(1. / len(variance_SN_vs_N_vs_range), 1., len(variance_SN_vs_N_vs_range))
    for i, (interaction_range, variance_SN_vs_N) in zip(color_idx, variance_SN_vs_N_vs_range.items()):
        N_list = []
        min_variance_SN_list = []
        for N, variance_SN_t in variance_SN_vs_N.items():
            N_list.append(N)
            min_variance_SN_list.append(min(variance_SN_t))
        plt.plot(N_list, min_variance_SN_list, marker='o', label='exp = {}'.format(interaction_range), color=plt.cm.get_cmap('Reds')(i))
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig('CT_dtwa/plots/log_min_variance_SN_vs_log_N_all_ranges.png'.format(N))


    fig = plt.figure()
    title = 'CT, power law'
    plt.title(title)
    plt.xlabel('exp')
    plt.ylabel('t_opt')
    color_idx = np.linspace(1. / len(t_vs_range_vs_N), 1., len(t_vs_range_vs_N))
    for i, (N, t_vs_range) in zip(color_idx, t_vs_range_vs_N.items()):
        range_list = []
        t_opt_list = []
        for interaction_range, t in t_vs_range.items():
            range_list.append(interaction_range)
            t_opt_list.append(t[np.argmin(variance_SN_vs_range_vs_N[N][interaction_range])])
        plt.plot(range_list, t_opt_list, marker='o', label='N = {}'.format(N), color=plt.cm.get_cmap('Reds')(i))
    plt.legend()
    plt.savefig('CT_dtwa/plots/t_opt_vs_range_all_N.png'.format(N))

    fig = plt.figure()
    title = 'CT, power law'
    plt.title(title)
    plt.xlabel('N')
    plt.ylabel('t_opt')
    color_idx = np.linspace(1. / len(t_vs_N_vs_range), 1., len(t_vs_N_vs_range))
    for i, (interaction_range, t_vs_N) in zip(color_idx, t_vs_N_vs_range.items()):
        N_list = []
        t_opt_list = []
        for N, t in t_vs_N.items():
            N_list.append(N)
            t_opt_list.append(t[np.argmin(variance_SN_vs_N_vs_range[interaction_range][N])])
        plt.plot(N_list, t_opt_list, marker='o', label='exp = {}'.format(interaction_range), color=plt.cm.get_cmap('Reds')(i))
    plt.plot(N_list, 1 / np.power(N_list, 2/3), label='1 / N^(2/3)', linestyle='dashed')
    plt.legend()
    plt.savefig('CT_dtwa/plots/t_opt_vs_N_all_ranges.png'.format(N))
    plt.yscale('log')
    plt.xscale('log')
    plt.savefig('CT_dtwa/plots/log_t_opt_vs_log_N_all_ranges.png'.format(N))


