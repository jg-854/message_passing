# Message Passing and Factor Graphs


This project was done as part of revision and as a tool to help understand how message passing is used in communications across binary channels

* fg.py declares the methods and attributes of the factor graph class as well as the node class. A factor graph has has both variable nodes and check nodes which share the same class


* modelling_bec_channel.py Is a file showing how to construct a factor graph object and what features it has as well as an example of decoding an input with erasures.

* communicating_bec_channel.py goes beyond this to show a practical example. A message (string) is converted into a bit stream, then encoded, pass through a BEC, then decoded on the other side. Have a play with some of the parameters such as the erasure probability as well as the length of the message. 

* The BSC files are exactly the same as the BEC files, however,now they are designed to work with the BSC channel which is a binary output channel with crossover probabilities.

Please email me at jg854@cam.ac.uk for any questions.
