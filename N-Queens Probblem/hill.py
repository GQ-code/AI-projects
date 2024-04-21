# Gabriel Quezada
# CECS 451
# Assignment 2
# Due: 2/16/24

from board import Board
import random
import time


# Hill climbing algorithm
def hill(n):
    # create a random initial state and its fitness
    current_board = Board(n)
    current_fitness = current_board.get_fitness()
    local_min = False
    global_min = False

    # Loop until global minimum is found
    while not global_min:
        # Loop through each column
        for i in range(n):
            if current_fitness == 0:
                global_min = True
                break

            # Reset board and fitness if local minimum is found
            if local_min:
                current_board = Board(n)
                current_fitness = current_board.get_fitness()

            # Create temp board to check for better fitness
            temp_board = Board(n)
            temp_board.map[i] = [0] * n
            local_min = True

            # Shuffle the column for random order
            column_indices = list(range(n))
            random.shuffle(column_indices)

            # Check fitness of different positions
            for j in column_indices:
                temp_board.flip(i, j)
                temp_fitness = temp_board.get_fitness()

                # If temp fitness is better, update the current board
                if temp_fitness < current_fitness:
                    current_board = temp_board
                    current_fitness = temp_fitness
                    local_min = False
                    break
                # Revert the flip
                temp_board.flip(i, j)


    return current_board.get_map()


def main():
    start = time.time()
    queens = 5
    final_board = hill(queens)
    end = time.time()
    print(f"Running time: {(end - start) * 1000:.2f}ms")
    for row in final_board:
        print(" ".join(['1' if cell == 1 else '_' for cell in row]))

if __name__ == "__main__":
    main()
