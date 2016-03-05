This test design shows how to use pihdf for developing HW modules in Verilog. 
Also, it illustrates the generation and the usage of test vector files.

Design steps:
- start from an 'empty' directory containing only the provided myvrlg.json file:
    myvrlg
      |--- myvrlg.json

- create new module design: execute command 'module myvrlg new'

- add your verilog RTL (or use the provided example code) in file myvrlg.v between the pargmas :
    /* Custom code begin */
    /* Custom code end */

- use the provided 3 test cases
    - test_001 uses test data generated within the utest_myvrlg.py file and 'fdump' to trigger generating test-vector files during the execution of the test
    - test_002 uses test data generated within the utest_myvrlg.py file
    - test_003 uses the generated test-vector files in test_001 for stimuli and reference data


