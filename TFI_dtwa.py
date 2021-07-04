import numpy as np
import setup
import spin_dynamics as sd
import util

if __name__ == '__main__':
    np.set_printoptions(threshold=np.inf)
    structure, system_size, fill, interaction_shape, interaction_param_name, interaction_range_list, instance = setup.configure()
    
    method = 'TFI'
    spin_system = sd.SpinOperators_DTWA(structure, system_size, fill)
    psi_0 = spin_system.get_init_state('x')
    for interaction_range in interaction_range_list:
        Jz = 1
        h_list = - np.array([0, 0.5, 1, 1.5, 2, 10])
        for h in h_list:
            H = spin_system.get_TFI_Hamiltonian(Jz, h, interaction_range)
            spin_evolution = sd.SpinEvolution(H, psi_0)
            t_max = 4.
            t = np.linspace(t_max/500, t_max, 500)
            tdist, t = spin_evolution.evolve([1.], t, store_states=True)
            meanConfig_evol = np.mean(tdist,axis=1)
            
            min_variance_SN_t, min_variance_norm_t, opt_angle_t = spin_system.get_squeezing(tdist, meanConfig_evol)
            results_t = spin_system.get_observed(tdist, meanConfig_evol)
            results_t['min_variance_SN'] = min_variance_SN_t
            results_t['min_variance_norm'] = min_variance_norm_t
            results_t['opt_angle'] = opt_angle_t
            results_t['t'] = t

            util.store_observed_t(results_t, 'observables_vs_t_{}_N_{}_{}_{}_{}_h_{}'.format(method, spin_system.N, interaction_shape, interaction_param_name, interaction_range, h))