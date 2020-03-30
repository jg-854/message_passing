#this program shows a practical use of message passing in the context of communication across a Binary Erasure Channel

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
def bsc_channel(x,p):
    y = []
    for c in x:
        r = bernoulli.rvs(p)
        if r:
            c  = 1 ^ int(c) #bit flip

        y.append(c)
    return y

   ### Feel free the play around with these variables ###
message = "This is the message that we will add some redundancy to and then pass through the channel! Hopefully it should still " \
          "make some sense when we recieve it on the other end!"
crossover_probability = 0.001
my_graph = factor_graph (7,4,[(0,0),(0,1),(0,2),(1,0),(1,2),(1,3),(2,0),(2,1),(2,3),(3,0),(4,1),(5,2),(6,3)])

 ### The following code should not be messed around with ###



G = my_graph.generator_matrix()
ic = my_graph.get_inverse_codebook()
k = my_graph.k
m_bits = tobits(message) #convert string into bitstream
m_split = [m_bits[i:i+k] for i in range(0,len(m_bits)-k,k)] #break up the bitstream into blocks of k for the LBC
c = [np.matmul(z,G) % 2 for z in m_split] #convert each block into the code

y = [bsc_channel(z,crossover_probability) for z in c] #pass each block code through the channel
c_tilde = [np.absolute(np.array(my_graph.decode_bsc(z,crossover_probability))) for z in y] #use the message passing algorithm to try remove the erasures
m_split_tilde=[] #now we will convert the code back into the block of size k, and for messages that still have erausres, we default to [0,0,0]
for z in c_tilde:
    x = np.array2string(np.array([z]).astype(np.float))
    if x in ic:
        m_split_tilde.append(ic[x])
    else:
        m_split_tilde.append([0,0,0]) # #
m_bits_tilde = list(np.array(m_split_tilde).flatten()) #convert blocks back into bit stream
message_tilde = frombits(m_bits_tilde)

print(message_tilde)












