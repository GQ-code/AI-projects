import sys

# Function to parse the line
def parse_line(line):
    values = line.strip().split(',')
    # Convert values to float if they are not 't' or 'f'
    return [float(val) if val != 't' and val != 'f' else val for val in values]

# Function to perform filtering in Hidden Markov Model
def hmm_filtering(probabilities, evidence):
    # Record probabilities from the probabilities list
    b, c, d, f = probabilities[1:5]
    b_complement = 1 - b
    c_complement = 1 - c
    d_complement = 1 - d
    f_complement = 1 - f

    # Determine emission probabilities
    if evidence[-1] == 't':
        e, e_complement = d, f
    else:
        e, e_complement = d_complement, f_complement

    # Base case
    if len(evidence) == 1:
        a, a_complement = probabilities[0], 1 - probabilities[0]
    # Recursive case
    else:
        a, a_complement = hmm_filtering(probabilities, evidence[:-1])

    # Calculate the probabilities inside the summation for the transition model
    x = a * b + a_complement * c
    x_complement = a * b_complement + a_complement * c_complement
    # Calculate the probabilities outside the summation for the sensor model
    true_prob = e * x 
    false_prob = e_complement * x_complement

    # Normalize and return the result
    total = true_prob + false_prob
    return [true_prob / total, false_prob / total]

def main():
    # Checks if the correct number of arguments are provided
    if len(sys.argv) != 2:
        print("File needs 2 arguments.")
        return

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r') as file:
            for line in file:
                probabilities = parse_line(line) # Parse the line to obtain the probabilities
                evidence = probabilities[5:] # Extract the evidence from the probabilities
                result = hmm_filtering(probabilities, evidence)
                print(line.strip() + "--><{:.4f},{:.4f}>".format(result[0], result[1]))
    except FileNotFoundError:
        print(f"File _complement found: {input_file}")

if __name__ == "__main__":
    main()
