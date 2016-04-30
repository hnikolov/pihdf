""" setuptools distribution and installation script. """

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup( name                 = "pihdf",
       version              = "0.1.3",
       description          = 'Hardware Design Framework based on python and MyHDL',
       long_description     = readme(),
       classifiers          = [
           'Development Status :: 3 - Alpha',
           'License :: OSI Approved :: MIT License',
           'Programming Language :: Python :: 2.7',
           'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
       ],
       keywords             = 'myhdl pihdf fpga',
       url                  = 'https://github.com/hnikolov/pihdf.git',
       author               = 'Hristo Nikolov, Nikolay Kavaldjiev',
       author_email         = 'h.n.nikolov@gmail.com, nikolay.kavaldjiev@gmail.com',
       license              = 'MIT',
       packages             = [
           'pihdf',
           'pihdf.interfaces',
           'pihdf.printers',
           'pihdf.bin'
       ],
       install_requires     = [
           'myhdl',
           'myhdl_lib',
           'simplejson',
           'coverage',
           'nose'
       ],
       test_suite           = 'nose.collector',
       tests_require        = ['nose', 'nose-cover3'],
       entry_points         = {
           'console_scripts': ['module=pihdf.bin.command_line:main']
       },
       include_package_data = True,
       zip_safe             = False
    )
