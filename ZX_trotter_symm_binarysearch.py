import numpy as np
import setup
import spin_dynamics as sd
import util

if __name__ == '__main__':
    np.set_printoptions(threshold=np.inf)
    structure, system_size, fill, interaction_shape, interaction_param_name, interaction_range_list, instance = setup.configure()

    # only uniform all-to-all interactions in symmetry
    if interaction_shape == 'power_law':
        interaction_range_list = [0]
    else:
        interaction_range_list = [max(interaction_range_list)]

    method = 'ZX'
    for interaction_range in interaction_range_list:
        spin_system = sd.SpinOperators_Symmetry(system_size)
        observables = spin_system.get_observables()
        psi_0 = spin_system.get_init_state('x')

        H = spin_system.get_Hamiltonian(['Sz_sq'], [1.])
        B = spin_system.get_Hamiltonian(['S_y'], [1.])
        spin_evolution = sd.SpinEvolution(H, psi_0, B=B)

        if N == 4:
            total_T = 0.343
            min_exact = 0.5115571542345448
            up = 100
            down = 10
        elif N == 8:
            total_T  = 0.228
            min_exact = 0.35406145011383566
            up = 100
            down = 10
        elif N == 16:
            total_T  = 0.153
            min_exact = 0.22972942396940316
            up = 100
            down = 10
        elif N == 32:
            total_T  = 0.101
            min_exact = 0.14298666610554997
            up = 100
            down = 10
        elif N == 64:
            total_T  = 0.066
            min_exact = 0.08707120160776315
            up = 100
            down = 10
        elif N == 128:
            total_T  = 0.043
            min_exact = 0.05258751298349856
            up = 100
            down = 10
        elif N == 256:
            total_T  = 0.028
            min_exact = 0.031775412603442695
            up = 100
            down = 10
        elif N == 512:
            total_T  = 0.018
            min_exact = 0.019279045257913154
            up = 100
            down = 10
        elif N == 1024:
            total_T  = 0.011
            min_exact = 0.011791810668625637
            up = 100
            down = 10
        elif N == 2048:
            total_T  = 0.007
            min_exact = 0.007229169359499022
            up = 100
            down = 10
        elif N == 4096:
            total_T  = 0.005
        
        t_it = np.linspace(1., 1., 1)
        step_list = [int((up + down) / 2)]
        while len(alphas) > 0:
            for steps in step_list:
                params = np.ones(2 * steps) * (total_T / steps)
                observed_t = spin_evolution.trotter_evolve(params, t_it, observables=observables, store_states=False, discretize_time=True)
                util.store_observed_t(observed_t, 'observables_vs_t_trotter_{}_N_{}_{}_{}_{}_steps_{}'.format(method, spin_system.N, interaction_shape, interaction_param_name, interaction_range, steps))
                
                min_variance_SN_t, min_variance_norm_t, opt_angle_t = spin_system.get_squeezing(observed_t)
                
                # if min_variance_SN_t[-1] > 1 and up - down > 1:
                # if min_variance_SN_t[-1] > 2 * min_exact and up - down > 1:
                if min(min_variance_SN_t) > 2 * min_exact and up - down > 1:
                    down = alpha
                    step_list = [int((up + down) / 2)]
                # elif min_variance_SN_t[-1] < 1 and up - down > 1:
                # elif min_variance_SN_t[-1] < 2 * min_exact and up - down > 1:
                elif min(min_variance_SN_t) < 2 * min_exact and up - down > 1:
                    up = alpha
                    step_list = [int((up + down) / 2)]
                else:
                    step_list = []
