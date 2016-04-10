``pihdf`` and HW Modules designed in Verilog
============================================

This example illustrates how to use ``pihdf`` for developing HW modules in **Verilog**. 
In addition, although not the main purpose of this example, it illustrates the generation and the usage of test vector files for testing the design.
For brevity, we use just a ``pass-through`` behavior, i.e., input data is propagatede to the output, respecting the handshake synchronization mechanism of ``pihdf``.

Design steps:
-------------

- Start from an empty directory, i.e., ``myvrlg``, containing only the provided ``myvrlg.json`` file: ::

    myvrlg
      |--- myvrlg.json

- Create new HW module design by running command ``new``: ::

    $ module myvrlg new

  This command creates the HW module directory structure and generates required files. This includes file ``myvrlg_beh.py`, a wrapper file ``myvrlg_wrp.py``, and an empty implementation file ``myvrlg.v``, all located in directory ``src``. The ``_beh.py`` file is used to specify functional behavior in pure python. For the simple pass-through example, it looks like: ::

    if rx_hs.hasPacket():
        data = rx_hs.get()
        tx_hs.append(data)


- Add your Verilog RTL (or use the provided example code) in file ``myvrlg.v`` between the pragmas: ::

    /* Custom code begin */
    -- Add your Verilog code here
    /* Custom code end */


  If your design consists of several Verilog files, they have to be specified with an absolute path in file: ::

        myvrlg
          |--- src
                |--- compile_list.txt

- Note/Use the provided 3 test cases:

    - ``test_001`` tests the behavior model by using test data generated within the ``utest_myvrlg.py`` file. In addition, it uses option ``fdump`` to trigger generation of test-vector files during the execution of the test. Test vector files are generated in directory: ::

        myvrlg
          |--- test
                |--- vectors

    - ``test_002`` tests the Verilog design by using test data generated within the ``utest_myvrlg.py`` file
    - ``test_003`` tests the Verilog defing by using the generated test-vector files (during ``test_001``) for stimuli and reference data

- Run all test by: ::

    $ module myvrlg test
