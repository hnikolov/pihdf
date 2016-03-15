`pihdf` and HW Modules in Verilog
=================================

This test design shows how to use pihdf for developing HW modules in Verilog. 
Also, it illustrates the generation and the usage of test vector files.

Design steps:
-------------

- Start from an empty directory, i.e., 'myvrlg', containing only the provided myvrlg.json file: ::

    myvrlg
      |--- myvrlg.json

- Create new module design: execute command: ::

    $ module myvrlg new

  This command creates the HW module directory structure and generates required files.

- Add your Verilog RTL (or use the provided example code) in file `myvrlg.v` between the pragmas: ::

    /* Custom code begin */
    -- Add your Verilog code here
    /* Custom code end */


  If your design consists of several Verilog files, they have to be specified with an absolute path in file: ::

        myvrlg
          |--- src
                |--- compile_list.txt

- Use the provided 3 test cases:

    - `test_001` uses test data generated within the `utest_myvrlg.py` file and uses option `fdump` to trigger generation of test-vector files during the execution of the test. Test vector files are generated in directory: ::

        myvrlg
          |--- test
                |--- vectors

    - `test_002` uses test data generated within the `utest_myvrlg.py` file
    - `test_003` uses the generated test-vector files in `test_001` for stimuli and reference data


