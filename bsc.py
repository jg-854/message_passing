from fg import *
from scipy.stats import bernoulli
def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result
def frombits(bits):
    chars = []

    for b in range(int(len(bits) / 8)):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)




#based on example paper  3

my_graph = factor_graph (8,4,[(0,0),(0,1),(1,1),(1,2),(2,1),(2,3),(3,2),(3,3),(4,0),(4,2),(5,0),(5,2),(6,0),(6,3),(7,1),(7,3)])

y = np.array([1,1,0,0,0,0,1,0])

output = my_graph.decode_bsc(y,0.1,6,educational_outgoing = True,q= 3)


print(output)