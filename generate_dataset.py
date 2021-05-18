import os
import traceback
import sys
import subprocess
import timeit
import csv
from compiler import run_compiler
from rfun_parser import parse_rfun
from interpreter import eval_rfun
from cs202_support import eval_x86

# Pass the --run-gcc option to this file to run your compiled files in hardware
# You must compile the runtime first and place it in the parent directory
#https://medium.com/analytics-vidhya/save-and-load-your-scikit-learn-models-in-a-minute-21c91a961e9b
files = sorted(os.listdir('data'))
data = []

for file_name in files:
    if file_name.endswith('.rfun'):
        with open('data/' + file_name) as f:
            print(f'Running file {file_name}...')

            try:
                program = f.read()
                ast = parse_rfun(program)
                interpreter_result = eval_rfun(ast)
                emu = eval_x86.X86Emulator(logging=False)
                
                x86_program, live_data = run_compiler(program, "graph_color", logging=False) #TODO: edit compiler to take in allocation method
                start = timeit.default_timer()
                x86_output = emu.eval_program(x86_program)
                stop = timeit.default_timer()
                gc_runtime = start - stop
                
                x86_program, live_data = run_compiler(program, "linear_scan", logging=False) #TODO: edit compiler to take in allocation method
                start = timeit.default_timer()
                x86_output = emu.eval_program(x86_program)
                stop = timeit.default_timer()
                ls_runtime = start - stop
                
                if gc_runtime > ls_runtime:
                    data.append([0, live_data, len(program)]) #TODO: get other data from compiler
                    print("gc")
                else:
                    print("ls")
                    data.append([1, live_data, len(program)])
                #print('Run Time of', file_name, '', stop - start)


                if len(x86_output) != 1: #or x86_output[0] != interpreter_result:
                    print('Program Failed to compile')
                print()

            except:
                print('Test failed with error! **************************************************')
                traceback.print_exception(*sys.exc_info())
          
header = ['target', 'live_data', 'program length'] #TODO: figure out other data to use
data_csv = open('./data.csv', 'w', newline='')
writer = csv.writer(data_csv)
writer.writerow(header)
for val in data:
    writer.writerow(val)
                