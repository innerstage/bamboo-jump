import yaml
import re

from bamboo_jumpstart.libraries import ExternalLibs, BambooLibs
from bamboo_jumpstart.steps import StepsDeclaration
from bamboo_jumpstart.parameters import ParameterDeclaration


# Open YAML file and store contents in variable "etl"
with open("etl.yaml", "r") as file:
    etl = yaml.load(file, Loader=yaml.FullLoader)

print(ExternalLibs(etl).run())
print(BambooLibs(etl).run())
print(StepsDeclaration(etl).run())
print(ParameterDeclaration(etl).run())
