import yaml
import re
import sys

from bamboo_jumpstart.libraries import ExternalLibs, BambooLibs
from bamboo_jumpstart.steps import StepsDeclaration, StepsUse
from bamboo_jumpstart.parameters import ParameterDeclaration
from bamboo_jumpstart.main_block import MainDeclaration


# Open YAML file and store contents in variable "etl"
etl_file = sys.argv[1]

with open(etl_file, "r") as file:
    etl = yaml.load(file, Loader=yaml.FullLoader)

full_code = ""
full_code += ExternalLibs(etl).run()
full_code += BambooLibs(etl).run()
full_code += StepsDeclaration(etl).run()
full_code += ParameterDeclaration(etl).run()
full_code += StepsUse(etl).run()
full_code += MainDeclaration(etl).run()

with open("output_etl.py", "w") as file:
    file.write(full_code)

print("Pipeline generated successfully!")