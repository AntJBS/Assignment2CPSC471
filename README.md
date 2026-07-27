# CPSC 471: Assignment 2

In this lab, you will learn how reliable transport can be built above an unreliable UDP service.
UDP does not guarantee delivery, ordering, or duplicate suppression, so your program will add the
essential mechanisms normally hidden inside a transport protocol. You will develop a sender and
receiver that transfer a file from one host to another using UDP datagrams. Your protocol should
detect corruption, acknowledge correctly received data, retransmit packets after timeout, and
terminate cleanly after the complete file arrives.

## How to Execute the Code

Download the corresponding Python module and open them in a terminal. To launch the program, create 2 separate terminals and complete the following. In terminal 1, in terminal 1, run python rdt_receiver.py 9000 received.txt, and in terminal 2, run python rdt_sender.py 127.0.0.1 9000 input.txt. 

## How to Execute the Test Features

To test the testing features, please look into the rdt_common.py file. At the top of the file, you will see 4 different cases; Normal, Lose, Corruption, and Large File. To test the first 3, please uncomment the necessary case implementation and comment out the rest. Afterwards, run the following commands; in terminal 1, run python rdt_receiver.py 9000 received.txt, in terminal 2, run python rdt_sender.py 127.0.0.1 9000 input.txt. To test the large file test, run the following commands; in terminal 1, run python rdt_receiver.py 9000 large_received.txt, in terminal 2, run python rdt_sender.py 127.0.0.1 9000 large_input.txt. 

## Contributors

Anthony Brooks, AntJBS@csu.fullerton.edu
