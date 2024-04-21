# Gabriel Quezada
# CECS 451
# Assignment 2
# Due: 2/16/24

from board import Board 
import random
import time

# Function to generate the initial population
def populate(n):
    population = []
    fitness = []
    states = 0
    
    # Generate 8 random states
    while states < 8:
        test = Board(n)
        fitness.append(test.get_fitness())
        # Convert the state to a string
        state = ''.join(str(test.map[row].index(1)) for row in range(n))
        population.append(state)
        states += 1
    
    return population, fitness


def genetic_algorithm(n):
    population, fitness = populate(n)
    current_board = None
    found = False

    # Loop until final board is found
    while not found:
        current_board, found, fitness = genetic(current_board, fitness, population)
        
    return current_board


def genetic(current_board, fitness, population):
    # Calculate the weight of each fitness
    weight = [fit / sum(fitness) for fit in fitness]
    weight.sort(reverse=True)
    selection = []

    # Select the parents based on the weight
    for i in range(len(population)):
        r = random.random()
        accum_weight = 0
        for i, w in enumerate(weight):
            accum_weight += w
            if r < accum_weight:
                # Add the selected parent to the selection list
                selection.append(population[i])
                break
    
    children = []
    # Create the children by combining the parents
    for f, b in zip(population, selection):
        ran = random.randint(1, random.randint(1, len(population) - 1))
        children.append(f[:ran] + b[ran:])

    mutate_children = []
    # Mutate the children
    for location in children:
        child = location
        ran = random.randint(0, 4)
        loc_ran = random.randint(0, len(child) - 1)
        temp = list(child)
        temp[loc_ran] = ran
        mutate_children.append(''.join(map(str, temp)))

    new_fitness = []
    # Calculate the fitness of the mutated children
    for value in mutate_children:
        matrix = Board(5)
        for dex in range(len(matrix.map)):
            for c in range(len(matrix.map[dex])):
                if matrix.map[dex][c] == 1:
                    matrix.map[dex][c] = 0
            matrix.map[dex][int(value[dex])] = 1
            # If the fitness is 0, then the solution is found
        if matrix.get_fitness() == 0:
            current_board = matrix
            return current_board, True, new_fitness
        new_fitness.append(matrix.get_fitness())

    return None, False, new_fitness


def main():
    n = 5
    start = time.time()
    final_board = genetic_algorithm(n)
    while final_board is None:
        final_board = genetic_algorithm(n)
    end = time.time()
    
    print(f"Running time: {(end - start) * 1000:.2f}ms")
    
    for row in final_board.map:
        print(" ".join(['1' if cell == 1 else '_' for cell in row]))


if __name__ == '__main__':
    main()