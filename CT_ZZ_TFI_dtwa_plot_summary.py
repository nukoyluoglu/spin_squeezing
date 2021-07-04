import numpy as np
import setup
import spin_dynamics as sd
import util
from collections import defaultdict
import matplotlib.pyplot as plt

if __name__ == '__main__':
    np.set_printoptions(threshold=np.inf)

    fig = plt.figure()
    plt.title('power law, exp = 0')
    plt.xlabel('t')
    plt.ylabel('N * <S_a^2> / <S_x>^2')

    N_list = [10,20,50,100]
    color_idx = np.linspace(1. / len(N_list), 1., len(N_list))
    for i, N in zip(color_idx, N_list):
        # range_list = [0,0.5,1,1.5,2,2.5,3]
        for interaction_range in [0]:
            J_list = [1.]
            for J in J_list: 
                for method in ['CT', 'ZZ', 'TFI, h = +1', 'TFI, h = -1']:
                    if method == 'CT':
                        dirname = method + '_dtwa'
                        filename = 'observables_vs_t_{}_N_{}_{}_{}_{}_J_{}'.format(method, N, 'power_law', 'exp', interaction_range, J)
                        color = plt.cm.get_cmap('Reds')(i)
                    elif method == 'ZZ':
                        dirname = method + '_dtwa'
                        filename = 'observables_vs_t_{}_N_{}_{}_{}_{}'.format(method, N, 'power_law', 'exp', interaction_range)
                        color = plt.cm.get_cmap('Blues')(i)
                    elif method == 'TFI, h = +1':
                        method_name = 'TFI'
                        dirname = method_name + '_dtwa'
                        h = 1
                        filename = 'observables_vs_t_{}_N_{}_{}_{}_{}_h_{}'.format(method_name, N, 'power_law', 'exp', interaction_range, h)
                        color = plt.cm.get_cmap('Greens')(i)
                    elif method == 'TFI, h = -1':
                        method_name = 'TFI'
                        dirname = method_name + '_dtwa'
                        h = -1.
                        filename = 'observables_vs_t_{}_N_{}_{}_{}_{}_h_{}'.format(method_name, N, 'power_law', 'exp', interaction_range, h)
                        color = plt.cm.get_cmap('Purples')(i)
                    observed_t = util.read_observed_t('{}/{}'.format(dirname, filename))
                    variance_SN_t, variance_norm_t, angle_t, t = observed_t['min_variance_SN'], observed_t['min_variance_norm'], observed_t['opt_angle'], observed_t['t']
                    print('N = {}, t_opt = {}'.format(N, t[np.argmin(variance_SN_t)]))
                    plt.plot(t, variance_SN_t, label=method + ', N = {}'.format(N), color=color)
    plt.ylim(bottom=0., top=1.)
    plt.xlim(left=0., right=1.2)
    plt.legend()
    plt.savefig('CT_ZZ_TFI_dtwa/variance_SN_vs_t_power_law_exp_0_all_N.png')


    N_list = [10,20,50,100]
    for i, N in zip(color_idx, N_list):
        fig = plt.figure()
        plt.title('N = {}, power law, exp = 0'.format(N))
        plt.xlabel('t')
        plt.ylabel('N * <S_a^2> / <S_x>^2')
        # range_list = [0,0.5,1,1.5,2,2.5,3]
        for interaction_range in [0]:
            J_list = [1.]
            for J in J_list: 
                for method in ['CT', 'ZZ', 'TFI, h = +1', 'TFI, h = -1']:
                    if method == 'CT':
                        dirname = method + '_dtwa'
                        filename = 'observables_vs_t_{}_N_{}_{}_{}_{}_J_{}'.format(method, N, 'power_law', 'exp', interaction_range, J)
                    elif method == 'ZZ':
                        dirname = method + '_dtwa'
                        filename = 'observables_vs_t_{}_N_{}_{}_{}_{}'.format(method, N, 'power_law', 'exp', interaction_range)
                    elif method == 'TFI, h = +1':
                        method_name = 'TFI'
                        dirname = method_name + '_dtwa'
                        h = 1
                        filename = 'observables_vs_t_{}_N_{}_{}_{}_{}_h_{}'.format(method_name, N, 'power_law', 'exp', interaction_range, h)
                    elif method == 'TFI, h = -1':
                        method_name = 'TFI'
                        dirname = method_name + '_dtwa'
                        h = -1.
                        filename = 'observables_vs_t_{}_N_{}_{}_{}_{}_h_{}'.format(method_name, N, 'power_law', 'exp', interaction_range, h)
                    observed_t = util.read_observed_t('{}/{}'.format(dirname, filename))
                    variance_SN_t, variance_norm_t, angle_t, t = observed_t['min_variance_SN'], observed_t['min_variance_norm'], observed_t['opt_angle'], observed_t['t']
                    plt.plot(t, variance_SN_t, label=method)
        plt.ylim(bottom=0., top=1.)
        plt.xlim(left=0., right=1.2)
        plt.legend()
        plt.savefig('CT_ZZ_TFI_dtwa/variance_SN_vs_t_N_{}_power_law_exp_0.png'.format(N))



