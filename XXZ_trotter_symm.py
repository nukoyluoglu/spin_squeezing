import numpy as np
import setup
from spin_dynamics import *
import util

if __name__ == '__main__':
    np.set_printoptions(threshold=np.inf)
    structure, system_size, fill, interaction_shape, interaction_param_name, interaction_range_list, instance = setup.configure()

    # only uniform all-to-all interactions in symmetry
    if interaction_shape == 'power_law':
        interaction_range_list = [0]
    else:
        interaction_range_list = [max(interaction_range_list)]

    method = 'XXZ'
    for interaction_range in interaction_range_list:
        spin_system = SpinOperators_Symmetry(system_size)
        observables = spin_system.get_observables()
        psi_0 = spin_system.get_init_state('x')
        B_x = spin_system.get_Hamiltonian(['S_x'], [1.])
        B_y = spin_system.get_Hamiltonian(['S_y'], [1.])

        J_eff_list = [-0.1] ### FILL IN
        for J_eff in J_eff_list:
            Jz = (J_eff + 1.) / 2
            Jperp = 2 * (1 - Jz)
            ham_terms_z = ['Sz_sq']
            ham_terms_perp = ['Sz_sq']
            strengths_z = [Jz]
            strengths_perp = [Jperp/2.]
            H_z = spin_system.get_Hamiltonian(ham_terms_z, strengths_z)
            H_perp = spin_system.get_Hamiltonian(ham_terms_perp, strengths_perp)
            spin_evolution = SpinEvolution((H_z, H_perp), psi_0, B=(B_x, B_y))
            total_T = 3.44
            t_it = np.linspace(1., 1., 1)
            step_list = [1, 5, 10, 100, 1000, 5000, 10000]
            for steps in step_list:
                params = np.ones(3 * steps) * (total_T / steps)
                observed_t = spin_evolution.trotter_evolve_twice(params, t_it, observables=observables, store_states=False, discretize_time=True)
                util.store_observed_t(observed_t, 'observables_vs_t_trotter_{}_N_{}_{}_{}_{}_J_eff_{}_steps_{}'.format(method, spin_system.N, interaction_shape, interaction_param_name, interaction_range, J_eff, steps))