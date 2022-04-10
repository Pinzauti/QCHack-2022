# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 14:47:19 2022

@author: tinar
"""

import numpy as np
import qiskit.quantum_info.operators as qi
from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from pylab import imread
import matplotlib.pyplot as plt
from qiskit.tools.visualization import circuit_drawer
import qiskit.quantum_info as qi
from qiskit import Aer, assemble

#level=0

#sudoku - start for the player
def play():
    print("Which level do you whant to play, 1 or 2 ?")
    level = input()

    if level == '1':
        image2 = imread(r"2x2_image.jpeg")  #// choose image location
        plt.axis('off')
        plt.imshow(image2)
        plt.pause(0.001)  # to print it before gates are chosen
        
        #input player single qubit gates list
        input_player_gates=[]
        
        for i in range(4):
            print("Choice of the", i, "single-qubit gate:", "\n"
                "Options: I, X, Z, H")
            choice = input()

            if choice == 'I' or choice == 'X' or choice == 'H' or choice == 'Z':
                input_player_gates.append(choice)
                #print("You have chosen: option", choice)
        
            else:
                print("Your choice is not valid !!")
                break 
            
        print("Your chosen single-qubit gates", input_player_gates) 
        
    
        # measure -----
        # create initializing gates
        Norm = 1/np.sqrt(2)

        # input 0
        in_zero = qi.Operator([[1,0],
                               [0,1]])
        # input 1 (X on 0)
        in_one = qi.Operator([[0,1],
                              [1,0]])
        # input + (Hadamard on 0)
        in_plus = qi.Operator([[Norm,Norm],
                               [Norm,-Norm]])
        # input - (Hadamard on 1)
        in_minus = qi.Operator([[Norm, Norm],
                                [-Norm, Norm]])
        # empty box for drop down
        empty_box = qi.Operator([[1,0],
                                 [0,1]])  # use in_zero ?
        #measurement box / only for the graphics
        measure = qi.Operator([[1,0],
                               [0,1]]) 
        
        
        # ugly function to append gates as chosen: improvable!
        def user_input_gates(circuit, chosen_gates, q_index):
            ''' input: circuit (level)
                number of drop down menu
                index of qubit for adding the gate
            output: chosen gate appended to circuit'''
            if chosen_gates == 'I':
                circuit.id(q_index)
            elif chosen_gates == 'X':
                circuit.x(q_index)
            elif chosen_gates == 'Y':
                circuit.y(q_index)
            elif chosen_gates == 'Z':
                circuit.z(q_index)
            elif chosen_gates == 'H':
                circuit.h(q_index)
                
        # create circuit
        circ_01 = QuantumCircuit(4)
        circ_01.unitary(in_zero, 0, label="0")
        circ_01.unitary(in_one, 2, label="1")
        circ_01.barrier()
        circ_01.unitary(in_zero, 1, label="0")
        circ_01.unitary(in_plus, 3, label="+")
        
        circ_01.barrier()
        
        circ_01.x(0)
        circ_01.cnot(0,1)
        user_input_gates(circ_01, input_player_gates[0], 1)
        user_input_gates(circ_01, input_player_gates[1], 2)
        user_input_gates(circ_01, input_player_gates[2], 2)
        user_input_gates(circ_01, input_player_gates[3], 3)
        circ_01.x(3)

        circ_01.barrier()

        circ_01.measure_all()
        circ_01.draw('mpl', plot_barriers=False,   style={'displaycolor': {'0': ('#BBBBBB'),  '1': ('#BBBBBB'),  '+': ('#BBBBBB'),  '-': ('#BBBBBB'), ' ':('#FF8300'), ' M ': ('#BBBBBB')}})
        plt.show()
        plt.pause(0.001)  # to print it before gates are chosen
        
        # measure
        # qasm simulation
        qasm_sim = Aer.get_backend('qasm_simulator')
        t_qc = transpile(circ_01, qasm_sim)
        qobj = assemble(t_qc)
        shots=1024
        result = qasm_sim.run(qobj, shots=shots, memory=True).result()
        counts = result.get_counts()
        print(counts)
    
        #check if the result solve the sudoku
        if '1001' in counts:
            if counts['1001'] == shots:
                res = True
            else:
                res = False
        else:
            res = False

        print(res)    
    
        
    elif level == '2':   # work in progress!
        image1 = imread(r"4x4_image.jpeg")  #// choose image location
        plt.axis('off')  
        plt.imshow(image1)
        plt.pause(0.001)  # to print it before gates are chosen
        
        print('Sorry, work in progress! Update coming soon...')
        
    #     input_player_squbit_gates=[]

    #     for i in range(12):
    #         print("Choice of the", i, "single-qubit gate:", "\n"
    #         "Options: I, X, Z, H")
    #         choice = input()

    #         if choice == 'I' or choice == 'X' or choice == 'Y' or choice == 'Z':
    #             input_player_squbit_gates.append(choice)
    #             #print("You have chosen: option", choice)
        
    #         else:
    #             print("Your choice is not valid !!")
    #             break 
        
    #     print("Your chosen single-qubit gates", input_player_squbit_gates)  


    #     #input player two-qubit gates list
    #     input_player_two_qubit_gates=[]

    #     for i in range(3):
    #         print("Choice of the", i, "-th two-qubit gate:", "\n"
    #         "Options: CI (control Identity), CX (control-X), CZ (control-Z)")
    #         choice = input()
        
    #         if choice == 'CI' or  choice == 'CX' or choice == 'CZ':
    #             input_player_two_qubit_gates.append(choice)
    #             #print("You have chosen: option", choice)
        
    #         else:
    #             print("Your choice is not valid !!")
    #             break

    #     print("Your chosen single-qubit gates", input_player_two_qubit_gates)


    #     #input player measurement gates list
    #     input_player_measurement_basis=[]

    #     for i in range(10):
    #         print("Choice of the", i, "single-qubit gate:", "\n"
    #                     "Options: Mz (Z basis), Mx (X basis)")
    #         choice = input()

    #         if choice == 'Mx' or choice == 'Mz':
    #             input_player_measurement_basis.append(choice)
    #             #print("You have chosen: option", choice)
        
    #         else:
    #             print("Your choice is not valid !!")
    #             break

    #     print("Your chosen measurement basis", input_player_measurement_basis)

        
    # else:
    #     print("The level is work in progress, choose another one !!")


