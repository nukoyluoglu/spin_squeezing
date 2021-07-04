import numpy as np
import setup
import spin_dynamics as sd
import util
from collections import defaultdict
import matplotlib.pyplot as plt
import os

if __name__ == '__main__':
    np.set_printoptions(threshold=np.inf)
    
    dirname = 'XXZ_dtwa'

    variance_SN_vs_J_eff_vs_range_vs_N = defaultdict(dict)
    t_vs_J_eff_vs_range_vs_N = defaultdict(dict)
    variance_SN_vs_J_eff_vs_N_vs_range = defaultdict(dict)
    t_vs_J_eff_vs_N_vs_range = defaultdict(dict)
    method = 'XXZ'
    for N in [10,20,50,100,200]:
        variance_SN_vs_J_eff_vs_range = defaultdict(dict)
        t_vs_J_eff_vs_range = defaultdict(dict)
        for interaction_range in [0.0,0.5,1.0,1.5,2.0,2.5,3.0]:
            variance_SN_vs_J_eff = {}
            t_vs_J_eff = {}
            J_eff_list = sorted(np.concatenate(([1, -1], -1 * np.linspace(0.02, 0.40, 19, endpoint=False), 0.01 * (2 ** (- np.linspace(0, 3, 4))), - 0.01 * (2 ** (- np.linspace(0, 3, 4))))))
            for J_eff in J_eff_list: 
                filename = 'observables_vs_t_{}_N_{}_{}_{}_{}_J_eff_{}'.format(method, N, 'power_law', 'exp', interaction_range, J_eff)
                if os.path.isfile('{}/{}'.format(dirname, filename)):
                    observed_t = util.read_observed_t('{}/{}'.format(dirname, filename))
                    variance_SN_t, variance_norm_t, angle_t, t = observed_t['min_variance_SN'], observed_t['min_variance_norm'], observed_t['opt_angle'], observed_t['t']
                    variance_SN_vs_J_eff[J_eff] = variance_SN_t
                    t_vs_J_eff[J_eff] = t

            variance_SN_vs_J_eff_vs_range_vs_N[N][interaction_range] = variance_SN_vs_J_eff
            t_vs_J_eff_vs_range_vs_N[N][interaction_range] = t_vs_J_eff
            variance_SN_vs_J_eff_vs_N_vs_range[interaction_range][N] = variance_SN_vs_J_eff
            t_vs_J_eff_vs_N_vs_range[interaction_range][N] = t_vs_J_eff

    for N, variance_SN_vs_J_eff_vs_range in variance_SN_vs_J_eff_vs_range_vs_N.items():
        fig = plt.figure(figsize=(7.2,4.8))
        title = 'N = {}, power law'.format(N)
        plt.title(title)
        plt.xlabel('J_eff')
        plt.ylabel('N * <S_a^2> / <S_x>^2')
        plt.ylim(bottom=0., top=1.)
        color_idx = np.linspace(1. / len(variance_SN_vs_J_eff_vs_range), 1., len(variance_SN_vs_J_eff_vs_range))
        for i, (interaction_range, variance_SN_vs_J_eff) in zip(color_idx, variance_SN_vs_J_eff_vs_range.items()):
            J_eff_list = []
            min_variance_SN_list = []
            for J_eff, variance_SN_t in variance_SN_vs_J_eff.items():
                if J_eff not in [1., -1.]:
                    J_eff_list.append(J_eff)
                    min_variance_SN_list.append(min(variance_SN_t))
                else:
                    color = plt.cm.get_cmap("Blues")(i) if J_eff == 1. else plt.cm.get_cmap("Greens")(i)
                    linestyle = 'dashed' if J_eff == 1. else 'solid'
                    plt.hlines(min(variance_SN_t), -0.5, 0.1, color=color, linestyle='dashed', label='{} = {}, J_eff = {}'.format('exp', interaction_range, J_eff))
            plt.plot(J_eff_list, min_variance_SN_list, marker='o', label='exp = {}'.format(interaction_range), color=plt.cm.get_cmap('Reds')(i))
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size': 8})
        plt.tight_layout()
        plt.savefig('XXZ_dtwa/plots/min_variance_SN_vs_J_eff_N_{}_all_ranges.png'.format(N))

    for N, variance_SN_vs_J_eff_vs_range in variance_SN_vs_J_eff_vs_range_vs_N.items():
        fig = plt.figure(figsize=(7.2,4.8))
        title = 'N = {}, power law'.format(N)
        plt.title(title)
        plt.xlabel('- J_eff')
        plt.ylabel('N * <S_a^2> / <S_x>^2')
        # plt.ylim(bottom=0., top=1.)
        color_idx = np.linspace(1. / len(variance_SN_vs_J_eff_vs_range), 1., len(variance_SN_vs_J_eff_vs_range))
        for i, (interaction_range, variance_SN_vs_J_eff) in zip(color_idx, variance_SN_vs_J_eff_vs_range.items()):
            J_eff_list = []
            min_variance_SN_list = []
            for J_eff, variance_SN_t in variance_SN_vs_J_eff.items():
                if J_eff < 0:
                    if J_eff not in [1., -1.]:
                        J_eff_list.append(J_eff)
                        min_variance_SN_list.append(min(variance_SN_t))
                    else:
                        color = plt.cm.get_cmap("Blues")(i) if J_eff == 1. else plt.cm.get_cmap("Greens")(i)
                        linestyle = 'dashed' if J_eff == 1. else 'solid'
                        plt.hlines(min(variance_SN_t), 0, 0.4, color=color, linestyle='dashed', label='{} = {}, J_eff = {}'.format('exp', interaction_range, J_eff))
            plt.plot(- np.array(J_eff_list), min_variance_SN_list, marker='o', label='exp = {}'.format(interaction_range), color=plt.cm.get_cmap('Reds')(i))
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size': 8})
        plt.xscale('log')
        plt.yscale('log')
        plt.tight_layout()
        plt.savefig('XXZ_dtwa/plots/log_min_variance_SN_vs_log_J_eff_N_{}_all_ranges.png'.format(N))

    for interaction_range, variance_SN_vs_J_eff_vs_N in variance_SN_vs_J_eff_vs_N_vs_range.items():
        fig = plt.figure(figsize=(7.2,4.8))
        title = 'exp = {}, power law'.format(interaction_range)
        plt.title(title)
        plt.xlabel('J_eff')
        plt.ylabel('N * <S_a^2> / <S_x>^2')
        plt.ylim(bottom=0., top=1.)
        color_idx = np.linspace(1. / len(variance_SN_vs_J_eff_vs_N), 1., len(variance_SN_vs_J_eff_vs_N))
        for i, (N, variance_SN_vs_J_eff) in zip(color_idx, variance_SN_vs_J_eff_vs_N.items()):
            J_eff_list = []
            min_variance_SN_list = []
            for J_eff, variance_SN_t in variance_SN_vs_J_eff.items():
                if J_eff not in [1., -1.]:
                    J_eff_list.append(J_eff)
                    min_variance_SN_list.append(min(variance_SN_t))
                else:
                    color = plt.cm.get_cmap("Blues")(i) if J_eff == 1. else plt.cm.get_cmap("Greens")(i)
                    linestyle = 'dashed' if J_eff == 1. else 'solid'
                    plt.hlines(min(variance_SN_t), -0.5, 0.1, color=color, linestyle='dashed', label='{} = {}, J_eff = {}'.format('N', N, J_eff))
            plt.plot(J_eff_list, min_variance_SN_list, marker='o', label='N = {}'.format(N), color=plt.cm.get_cmap('Reds')(i))
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size': 8})
        plt.tight_layout()
        plt.savefig('XXZ_dtwa/plots/min_variance_SN_vs_J_eff_range_{}_all_N.png'.format(interaction_range))

    for interaction_range, variance_SN_vs_J_eff_vs_N in variance_SN_vs_J_eff_vs_N_vs_range.items():
        fig = plt.figure(figsize=(7.2,4.8))
        title = 'exp = {}, power law'.format(interaction_range)
        plt.title(title)
        plt.xlabel('J_eff')
        plt.ylabel('N * <S_a^2> / <S_x>^2')
        # plt.ylim(bottom=0., top=1.)
        color_idx = np.linspace(1. / len(variance_SN_vs_J_eff_vs_N), 1., len(variance_SN_vs_J_eff_vs_N))
        for i, (N, variance_SN_vs_J_eff) in zip(color_idx, variance_SN_vs_J_eff_vs_N.items()):
            J_eff_list = []
            min_variance_SN_list = []
            for J_eff, variance_SN_t in variance_SN_vs_J_eff.items():
                if J_eff < 0:
                    if J_eff not in [1., -1.]:
                        J_eff_list.append(J_eff)
                        min_variance_SN_list.append(min(variance_SN_t))
                    else:
                        color = plt.cm.get_cmap("Blues")(i) if J_eff == 1. else plt.cm.get_cmap("Greens")(i)
                        linestyle = 'dashed' if J_eff == 1. else 'solid'
                        plt.hlines(min(variance_SN_t), 0, 0.4, color=color, linestyle='dashed', label='{} = {}, J_eff = {}'.format('N', N, J_eff))
            plt.plot(- np.array(J_eff_list), min_variance_SN_list, marker='o', label='N = {}'.format(N), color=plt.cm.get_cmap('Reds')(i))
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size': 8})
        plt.xscale('log')
        plt.yscale('log')
        plt.tight_layout()
        plt.savefig('XXZ_dtwa/plots/log_min_variance_SN_vs_log_J_eff_range_{}_all_N.png'.format(interaction_range))

    for N, t_vs_J_eff_vs_range in t_vs_J_eff_vs_range_vs_N.items():
        fig = plt.figure(figsize=(7.2,4.8))
        title = 'N = {}, power law'.format(N)
        plt.title(title)
        plt.xlabel('J_eff')
        plt.ylabel('t_opt')
        # plt.ylim(bottom=0., top=1.)
        color_idx = np.linspace(1. / len(t_vs_J_eff_vs_range), 1., len(t_vs_J_eff_vs_range))
        for i, (interaction_range, t_vs_J_eff) in zip(color_idx, t_vs_J_eff_vs_range.items()):
            J_eff_list = []
            opt_t_list = []
            for J_eff, t in t_vs_J_eff.items():
                if J_eff not in [1., -1.]:
                    J_eff_list.append(J_eff)
                    opt_t_list.append(t[np.argmin(variance_SN_vs_J_eff_vs_range_vs_N[N][interaction_range][J_eff])])
                else:
                    color = plt.cm.get_cmap("Blues")(i) if J_eff == 1. else plt.cm.get_cmap("Greens")(i)
                    linestyle = 'dashed' if J_eff == 1. else 'solid'
                    plt.hlines(t[np.argmin(variance_SN_vs_J_eff_vs_range_vs_N[N][interaction_range][J_eff])], -0.5, 0.1, color=color, linestyle='dashed', label='{} = {}, J_eff = {}'.format('exp', interaction_range, J_eff))
            plt.plot(J_eff_list, opt_t_list, marker='o', label='exp = {}'.format(interaction_range), color=plt.cm.get_cmap('Reds')(i))
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size': 8})
        plt.tight_layout()
        plt.savefig('XXZ_dtwa/plots/opt_t_vs_J_eff_N_{}_all_ranges.png'.format(N))

    for N, t_vs_J_eff_vs_range in t_vs_J_eff_vs_range_vs_N.items():
        fig = plt.figure(figsize=(7.2,4.8))
        title = 'N = {}, power law'.format(N)
        plt.title(title)
        plt.xlabel('- J_eff')
        plt.ylabel('t_opt')
        # plt.ylim(bottom=0., top=1.)
        color_idx = np.linspace(1. / len(t_vs_J_eff_vs_range), 1., len(t_vs_J_eff_vs_range))
        for i, (interaction_range, t_vs_J_eff) in zip(color_idx, t_vs_J_eff_vs_range.items()):
            J_eff_list = []
            opt_t_list = []
            for J_eff, t in t_vs_J_eff.items():
                if J_eff < 0:
                    if J_eff not in [1., -1.]:
                        J_eff_list.append(J_eff)
                        opt_t_list.append(t[np.argmin(variance_SN_vs_J_eff_vs_range_vs_N[N][interaction_range][J_eff])])
                    else:
                        color = plt.cm.get_cmap("Blues")(i) if J_eff == 1. else plt.cm.get_cmap("Greens")(i)
                        linestyle = 'dashed' if J_eff == 1. else 'solid'
                        plt.hlines(t[np.argmin(variance_SN_vs_J_eff_vs_range_vs_N[N][interaction_range][J_eff])], 0, 0.5, color=color, linestyle='dashed', label='{} = {}, J_eff = {}'.format('exp', interaction_range, J_eff))
            plt.plot(- np.array(J_eff_list), opt_t_list, marker='o', label='exp = {}'.format(interaction_range), color=plt.cm.get_cmap('Reds')(i))
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size': 8})
        plt.xscale('log')
        plt.yscale('log')
        plt.tight_layout()
        plt.savefig('XXZ_dtwa/plots/log_opt_t_vs_log_J_eff_N_{}_all_ranges.png'.format(N))

    for interaction_range, t_vs_J_eff_vs_N in t_vs_J_eff_vs_N_vs_range.items():
        fig = plt.figure(figsize=(7.2,4.8))
        title = 'exp = {}, power law'.format(interaction_range)
        plt.title(title)
        plt.xlabel('J_eff')
        plt.ylabel('t_opt')
        # plt.ylim(bottom=0., top=1.)
        color_idx = np.linspace(1. / len(t_vs_J_eff_vs_N), 1., len(t_vs_J_eff_vs_N))
        for i, (N, t_vs_J_eff) in zip(color_idx, t_vs_J_eff_vs_N.items()):
            J_eff_list = []
            opt_t_list = []
            for J_eff, t in t_vs_J_eff.items():
                if J_eff not in [1., -1.]:
                    J_eff_list.append(J_eff)
                    opt_t_list.append(t[np.argmin(variance_SN_vs_J_eff_vs_N_vs_range[interaction_range][N][J_eff])])
                else:
                    color = plt.cm.get_cmap("Blues")(i) if J_eff == 1. else plt.cm.get_cmap("Greens")(i)
                    linestyle = 'dashed' if J_eff == 1. else 'solid'
                    plt.hlines(t[np.argmin(variance_SN_vs_J_eff_vs_range_vs_N[N][interaction_range][J_eff])], -0.5, 0.1, color=color, linestyle='dashed', label='{} = {}, J_eff = {}'.format('N', N, J_eff))
            plt.plot(J_eff_list, opt_t_list, marker='o', label='N = {}'.format(N), color=plt.cm.get_cmap('Reds')(i))
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size': 8})
        plt.tight_layout()
        plt.savefig('XXZ_dtwa/plots/opt_t_vs_J_eff_range_{}_all_N.png'.format(interaction_range))

    for interaction_range, t_vs_J_eff_vs_N in t_vs_J_eff_vs_N_vs_range.items():
        fig = plt.figure(figsize=(7.2,4.8))
        title = 'exp = {}, power law'.format(interaction_range)
        plt.title(title)
        plt.xlabel('- J_eff')
        plt.ylabel('t_opt')
        # plt.ylim(bottom=0., top=1.)
        color_idx = np.linspace(1. / len(t_vs_J_eff_vs_N), 1., len(t_vs_J_eff_vs_N))
        for i, (N, t_vs_J_eff) in zip(color_idx, t_vs_J_eff_vs_N.items()):
            J_eff_list = []
            opt_t_list = []
            for J_eff, t in t_vs_J_eff.items():
                if J_eff < 0:
                    if J_eff not in [1., -1.]:
                        J_eff_list.append(J_eff)
                        opt_t_list.append(t[np.argmin(variance_SN_vs_J_eff_vs_N_vs_range[interaction_range][N][J_eff])])
                    else:
                        color = plt.cm.get_cmap("Blues")(i) if J_eff == 1. else plt.cm.get_cmap("Greens")(i)
                        linestyle = 'dashed' if J_eff == 1. else 'solid'
                        plt.hlines(t[np.argmin(variance_SN_vs_J_eff_vs_range_vs_N[N][interaction_range][J_eff])], 0, 0.5, color=color, linestyle='dashed', label='{} = {}, J_eff = {}'.format('N', N, J_eff))
            plt.plot(- np.array(J_eff_list), opt_t_list, marker='o', label='N = {}'.format(N), color=plt.cm.get_cmap('Reds')(i))
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size': 8})
        plt.xscale('log')
        plt.yscale('log')
        plt.tight_layout()
        plt.savefig('XXZ_dtwa/plots/log_opt_t_vs_log_J_eff_range_{}_all_N.png'.format(interaction_range))
