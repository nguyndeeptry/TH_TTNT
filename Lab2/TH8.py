import numpy as np

def fitness_func(individual):
    return -np.sum(individual ** 2)

def generate_population(size, dim):
    return np.random.rand(size, dim)

def genetic_algorithm(population, fitness_func, n_generations=100, mutation_rate=0.01):
    for _ in range(n_generations):
        population = sorted(population, key=fitness_func, reverse=True)
        next_generation = population[:len(population)//2].copy()
        while len(next_generation) < len(population):
            parents_indices = np.random.choice(len(next_generation), 2, replace=False)
            parent1, parent2 = next_generation[parents_indices[0]], next_generation[parents_indices[1]]
            crossover_point = np.random.randint(1, len(parent1))
            child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
            if np.random.rand() < mutation_rate:
                mutate_point = np.random.randint(len(child))
                child[mutate_point] = np.random.rand()
            next_generation.append(child)
        population = np.array(next_generation)
    return population[0]

if __name__ == "__main__":
    population_size = 10
    dimension = 5
    n_generations = 50
    mutation_rate = 0.05

    population = generate_population(population_size, dimension)
    best_individual = genetic_algorithm(population, fitness_func, n_generations, mutation_rate)
    print("Best individual:", best_individual)
    print("Best fitness:", -fitness_func(best_individual))
