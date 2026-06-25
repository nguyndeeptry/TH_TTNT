import numpy as np

def differential_evolution(objective_func, bounds, pop_size=50,
                           max_generations=100, F=0.5, CR=0.7, seed=None):
    np.random.seed(seed)
    n_params = len(bounds)
    population = np.random.uniform(bounds[:, 0], bounds[:, 1],
                                   size=(pop_size, n_params))
    best_solution = None
    best_fitness = np.inf

    for generation in range(max_generations):
        for i in range(pop_size):
            target_vector = population[i]
            indices = [idx for idx in range(pop_size) if idx != i]
            a, b, c = population[np.random.choice(indices, 3, replace=False)]
            mutant_vector = np.clip(a + F * (b - c), bounds[:, 0], bounds[:, 1])
            crossover_mask = np.random.rand(n_params) < CR
            trial_vector = np.where(crossover_mask, mutant_vector, target_vector)

            trial_fitness = objective_func(trial_vector)
            if trial_fitness < best_fitness:
                best_fitness = trial_fitness
                best_solution = trial_vector
            if trial_fitness <= objective_func(target_vector):
                population[i] = trial_vector

    return best_solution, best_fitness


def sphere_function(x):
    return np.sum(x**2)


bounds = np.array([[-5.12, 5.12]] * 10)

best_solution, best_fitness = differential_evolution(sphere_function, bounds)

print("Best solution:", best_solution)
print("Best fitness:", best_fitness)
