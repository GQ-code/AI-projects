import sorobn as hh
import pandas as pd
import numpy as np

TRANS_MAP = [[0.9322, 0.0069, 0.0610, 0.0000],
             [0.4932, 0.1620, 0.0000, 0.3449],
             [0.4390, 0.0000, 0.4701, 0.0909],
             [0.0000, 0.1552, 0.4091, 0.4358]]

bn = hh.BayesNet(
    ('C', ['S', 'R']),
    ('S', 'W'),
    ('R', 'W')
)

bn.P['C'] = pd.Series({True: 0.5, False: 0.5})
bn.P['S'] = pd.Series({
    (True, True): 0.1, (True, False): 0.9,
    (False, True): 0.5, (False, False): 0.5
})
bn.P['R'] = pd.Series({
    (True, True): 0.8, (True, False): 0.2,
    (False, True): 0.2, (False, False): 0.8
})
bn.P['W'] = pd.Series({
    (True, True, True): 0.99, (True, True, False): 0.01,
    (True, False, True): 0.9, (True, False, False): 0.1,
    (False, True, True): 0.95, (False, True, False): 0.05,
    (False, False, True): 0.05, (False, False, False): 0.95
})


bn.prepare()

result_a = bn.query('C', event={'S': False, 'W': True})
exact_prob = [result_a[True], result_a[False]]  



def mcmc(trans_list):
    ps = []
    remove = None  
    for i in range(len(trans_list)):
        if trans_list[i] != 0:
            ps.append(i)
        # Assign remove variable if trans_list[i] == 
        else:
            remove = i
    if remove is not None:
        # Remove the element at index remove
        trans_list.pop(remove)  
    trans_list = np.cumsum(trans_list)

    num = np.random.rand()

    if num > trans_list[1]:
        return ps[2] 
    elif num > trans_list[0]:
        return ps[1]
    else:
        return ps[0]


def normalize(a, b):
    alpha = 1 / (a + b)
    return [a * alpha, b * alpha]

def main():
    print("Part A: The sampling Probabilities")
    print("P(C|-s,r) = <0.8780, 0.1220>")
    print("P(C|-s,-r) = <0.3103, 0.6897>")
    print("P(R|c,-s,w) = <0.9863, 0.0137>")
    print("P(R|-c,-s,w) = <0.8182, 0.1818>")
    print()

    print("Part B. The transition probability matrix")
    print("\tS1\t\tS2\t\tS3\t\tS4")
    for i, row in enumerate(TRANS_MAP):
        print("S{}".format(i + 1), end="")
        for val in row:
            print("\t{:.4f} ".format(val), end="")
        print()
    print()

    print("Part C. The probability for the query")
    print("Exact probability: <%.4f, %.4f>" % (exact_prob[0], exact_prob[1]))
    
    n_values = [10**i for i in range(3, 7)]
    for n in n_values:
        # Initialize counters for each state
        states = [0] * len(TRANS_MAP)  
        for _ in range(n):
            # Randomly choose initial state index
            current_state_index = np.random.randint(0, len(TRANS_MAP))
            # Perform 100 iterations of mcmc  
            for _ in range(100):  
                current_state_index = mcmc(TRANS_MAP[current_state_index])
            states[current_state_index] += 1

        prob = normalize((states[0] + states[1]), (states[2] + states[3]))
        error = abs(prob[0] - exact_prob[0]) / exact_prob[0] * 100
        print("n = 10^{}: <{:.4f}, {:.4f}>, error = {:.2f}%".format(int(np.log10(n)), prob[0], prob[1], error))

if __name__ == "__main__":
    main()
