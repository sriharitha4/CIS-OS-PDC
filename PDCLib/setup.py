from setuptools import setup, find_packages

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

def read_file(file):
   with open(file) as f:
        return f.read()
    
requirements = read_requirements("requirements.txt")

setup(
    name = 'pdclib',
    url = 'https://github.com/sriharitha4/CIS-OS-PDC',
    packages = find_packages(exclude=["test"]),
    install_requires = requirements,
    py_modules=[ "Locality", "Concurrency", "Asynchronousity", "Performance" ]
)