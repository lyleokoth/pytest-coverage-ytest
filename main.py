import subprocess
from os.path import exists
import os 
import xmltodict
import json

def main():
    code_directory = os.getenv('INPUT_CODEDIRECTORY')
    test_directory = os.getenv('INPUT_TESTDIRECTORY')
    pycov_config_file = os.getenv('INPUT_PYCOVCONFIGFILE')
    pytest_config_file = os.getenv('INPUT_PYTESTCONFIGFILE')

    if code_directory and test_directory:
        print(f'The code directory is {code_directory} and test directory is {test_directory}')
        p = subprocess.run(["python", "-m", "pytest", f"--cov={code_directory}", test_directory], capture_output=True, text=True)
        x = subprocess.run(["python", "-m", "pytest", "--cov-report=xml", f"--cov={code_directory}", test_directory], capture_output=True, text=True)
        if pycov_config_file:
            p = subprocess.run(["python", "-m", "pytest", f"--cov-config={pycov_config_file}", f"--cov={code_directory}", test_directory], capture_output=True, text=True)
            x = subprocess.run(["python", "-m", "pytest", "--cov-report=xml", f"--cov-config={pycov_config_file}", f"--cov={code_directory}", test_directory], capture_output=True, text=True)
        elif pytest_config_file:
            p = subprocess.run(["python", "-m", "pytest", f"--cov-config={pytest_config_file}", f"--cov={code_directory}", test_directory], capture_output=True, text=True)
            x = subprocess.run(["python", "-m", "pytest", "--cov-report=xml", f"--cov-config={pytest_config_file}", f"--cov={code_directory}", test_directory], capture_output=True, text=True)
    else:
        code_directory = '.'
        test_directory = 'tests/'
        print(f'The code directory is {code_directory} and test directory is {test_directory}')
        p = subprocess.run(["python", "-m", "pytest", f"--cov={code_directory}", test_directory], capture_output=True, text=True)
        x = subprocess.run(["python", "-m", "pytest", "--cov-report=xml", f"--cov={code_directory}", test_directory], capture_output=True, text=True)
        
    test_output = p.stdout

    print(test_output)

    if exists('coverage.xml'):
        with open('coverage.xml') as coverage_file:
            data_dict = xmltodict.parse(coverage_file.read())
            test_coverage = json.dumps(data_dict)
            print(f"::set-output name=TESTCOVERAGE::{test_coverage}")


if __name__ == "__main__":
    main()