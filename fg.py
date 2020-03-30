#This file sets methods and attributes for the factor_graph and node clases
import numpy as np
import math

#ideally i should have a different class for variable node and check node
# but I stupidly made the decision not to fairly late
class node:
    def __init__(self):
        self.talks_to = []
        self.value = -1
        self.v2c_values = {}
        self.c2v_values = {}

    def add_connection(self,x):
        self.talks_to.append(x)


class factor_graph:
    def connect(self,x,y):
        self.v_nodes[x].add_connection(y)
        self.c_nodes[y].add_connection(x)

    def batch_connect(self,list_of_tuples):
        for t in list_of_tuples:
            self.connect(t[0],t[1])

    def __init__(self,n_v_nodes, n_c_nodes,connections):
        self.v_nodes = [node() for i in range(n_v_nodes)]
        self.c_nodes = [node() for i in range(n_c_nodes)]
        self.n = n_v_nodes
        self.k = n_v_nodes - n_c_nodes
        self.batch_connect(connections)
        self.avg_v_degree = np.count_nonzero(self.parity_check_matrix())/len(self.v_nodes)
        self.avg_c_degree = np.count_nonzero(self.parity_check_matrix()) / len(self.c_nodes)
    def view_attributes (self):

        print("Number of variable nodes :",self.n)
        print("Number of check nodes: ",self.n - self.k)
        print("Rate: ",(self.k/self.n))
        print("Average variable node degree: ",self.avg_v_degree)
        print("Average check node degree: ",self.avg_c_degree)

    def view_variable_connections(self):
        for idx,n in enumerate(self.v_nodes):
            print("Variable",idx,"-->", n.talks_to)

    def view_check_connections(self):
        for idx,n in enumerate(self.c_nodes):
            print("Check node",idx,"-->", n.talks_to)

    def parity_check_matrix(self):
        H = np.zeros((self.n-self.k,self.n))
        for i in range(self.n):
            for j in self.v_nodes[i].talks_to:
                H[j][i]=1
        return H

    def generator_matrix(self):
        H = self.parity_check_matrix()
        assert (H[self.k-self.n:,self.k-self.n:] == np.eye(self.n-self.k)).all()
        P= H[0:self.n - self.k,0:self.k].T

        return np.block([np.eye(self.k),P])


    def lst_codewords(self):
        G = self.generator_matrix()
        for i in range(2 ** self.k):
            b_x = "{0:b}".format(i)[::-1]
            codeword = np.zeros((1, self.n))
            for l in range(len(b_x)):
                codeword += int(b_x[l]) * G[l]
            yield (codeword % 2)

    def decode_educational_bec(self, y):

        # enter values into variable nodes

        for i, n in enumerate(y):
            self.v_nodes[i].value = n

        # start iterations for message passing

        iteration = 0

        while iteration < 100:
            total = 0
            unknowns = 0
            v_idx = 0

            #  iterate through each check node

            for index in self.c_nodes[iteration % (self.n - self.k)].talks_to:

                v = self.v_nodes[index].value
                if v == -1:
                    unknowns += 1
                    v_idx = index
                    # if the value is -1 in the variable node, we will rememeber this one so we can update it if we can
                else:
                    total += v

            if unknowns == 1: #message passing only works if there is one unknown in the parity check equation
                self.v_nodes[v_idx].value = total % 2 #this is one of the rules for the check to variable node
                print("Variable", v_idx, "takes value ",total%2)


            else:
                pass
            iteration += 1

        output = [self.v_nodes[i].value for i in range(len(y))]
        return output

    def decode_bec(self, y):

        # enter values into variable nodes

        for i, n in enumerate(y):
            self.v_nodes[i].value = n

        # start iterations for message passing

        iteration = 0

        while iteration < 100:
            total = 0
            unknowns = 0
            v_idx = 0

            #  iterate through each check node

            for index in self.c_nodes[iteration % (self.n - self.k)].talks_to:

                v = self.v_nodes[index].value
                if v == -1:
                    unknowns += 1
                    v_idx = index
                    # if the value is -1 in the variable node, we will rememeber this one so we can update it if we can
                else:
                    total += v

            if unknowns == 1: #message passing only works if there is one unknown in the parity check equation
                self.v_nodes[v_idx].value = total % 2 #this is one of the rules for the check to variable node



            else:
                pass
            iteration += 1

        output = [self.v_nodes[i].value for i in range(len(y))]
        return output

    def min_distance(self):
        distances = [np.sum(cw) for cw in self.lst_codewords()]
        distances.pop(0) #this will remove the zero vector as this is always a codeword in LBC
        return min(distances)

    def get_inverse_codebook(self):
        i_codebook={}
        for idx, cw in enumerate(self.lst_codewords()):
            msg =[]
            for i in range(self.k):
                msg.append(idx % 2)
                idx = math.floor(idx/2)
            i_codebook[np.array2string(cw)] =  msg
        return i_codebook


    def log_probability_bsc(self,x,p):
        msg = np.log(p / (1 - p))
        if x == 0:
            msg *= -1
        return msg

    def v2c_msg(self):
        for j,v_node in enumerate(self.v_nodes):
            for i in v_node.talks_to:
                msg = v_node.v2c_values[i]
                for i_prime in v_node.talks_to:
                    if i==i_prime:
                        continue
                    else:
                        msg += self.c_nodes[i_prime].c2v_values[j]
                self.v_nodes[j].v2c_values[i] = msg



    def c2v_msg(self):
        for i,c_node in enumerate(self.c_nodes):
            for j in c_node.talks_to:
                msg = 1
                for j_prime in c_node.talks_to:
                    if j==j_prime:
                        continue
                    else:

                        x = np.tanh(0.5 * self.v_nodes[j_prime].v2c_values[i])
                        msg *= x
                msg = 2 * np.arctanh(msg)

                self.c_nodes[i].c2v_values[j] = msg



    def decode_bsc(self,y,p,N = 10,educational_incoming= False,educational_outgoing = False,q=1):

        output = []
        #add values from y into the tree
        for i, n in enumerate(y):
            self.v_nodes[i].value = n

        #send first message
        for j, v_node in enumerate(self.v_nodes):
            for i in v_node.talks_to:
                msg = self.log_probability_bsc(v_node.value,p)
                self.v_nodes[j].v2c_values[i] = msg
        if educational_outgoing:
            print("WARNING - PLEASE NOT THAT CHECK NODE {0} IS USING ZERO BASED NUMBERING \n \n")
            print("Initially, Node {0} sends the following messages to its check nodes".format(q))
            print(self.v_nodes[q].v2c_values)
            print()

        #message passing for a few iterations
        for i in range(N):
            self.c2v_msg()

            if educational_outgoing:
                response = {}
                for c in self.v_nodes[q].talks_to:
                    response[c] = self.c_nodes[c].c2v_values[q]
                print("On iteration{0}, node {1} receives the following messages from its check nodes".format(i+1,q))
                print(response)
                print()

            self.v2c_msg()
            if educational_outgoing:
                print("On iteration {0}, check node {1} sends out the following messages".format(i+1,q))
                print(self.v_nodes[q].v2c_values)
                print()

        for j,v_node in enumerate(self.v_nodes):
            prediction = self.log_probability_bsc(v_node.value,p)
            for i in v_node.talks_to:
                prediction += self.c_nodes[i].c2v_values[j]

            if prediction > 0:
                output.append(0)
            else:
                output.append(1)

        return np.array(output)





























