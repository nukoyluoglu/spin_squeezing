import numpy as np
import setup
import spin_dynamics as sd
import util

if __name__ == '__main__':
    np.set_printoptions(threshold=np.inf)
    structure, system_size, fill, interaction_shape, interaction_param_name, interaction_range_list, coupling, instance = setup.configure(specify_coupling=True)
    
    dirname = 'TFI_dtwa'

    variance_SN_vs_range_vs_method_h = {'TFI': {}}
    t_vs_range_vs_method_h = {'TFI': {}}
    method = 'TFI'
    spin_system = sd.SpinOperators_DTWA(structure, system_size, fill)
    N = spin_system.N
    for interaction_range in interaction_range_list:
        h_list = [coupling]
        for h in h_list:
            filename = 'observables_vs_t_{}_N_{}_{}_{}_{}_h_{}'.format(method, N, interaction_shape, interaction_param_name, interaction_range, h)
            observed_t = util.read_observed_t('{}/{}'.format(dirname, filename))

            variance_SN_t, variance_norm_t, angle_t, t = observed_t['min_variance_SN'], observed_t['min_variance_norm'], observed_t['opt_angle'], observed_t['t']

            util.plot_variance_SN_vs_t(variance_SN_t, t, method, N, interaction_shape, interaction_param_name, interaction_range, dirname='{}/plots'.format(dirname), coupling=h, coupling_name='h')
            util.plot_variance_norm_vs_t(variance_norm_t, t, method, N, interaction_shape, interaction_param_name, interaction_range, dirname='{}/plots'.format(dirname), coupling=h, coupling_name='h')
            util.plot_angle_vs_t(angle_t, t, method, N, interaction_shape, interaction_param_name, interaction_range, dirname='{}/plots'.format(dirname), coupling=h, coupling_name='h')
            
            variance_SN_vs_range_vs_method_h['TFI'][interaction_range] = variance_SN_t
            t_vs_range_vs_method_h['TFI'][interaction_range] = t

    util.plot_variance_SN_vs_t_all_ranges(variance_SN_vs_range_vs_method_h, t_vs_range_vs_method_h, N, interaction_shape, interaction_param_name, dirname='{}/plots'.format(dirname), coupling=h, coupling_name='h')
