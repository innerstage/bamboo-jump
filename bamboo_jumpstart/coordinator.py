# A class to create and coordinate all the other classes and generate the final file
 
from classes.external_libs import ExternalLibs
from classes.bamboo_libs import BambooLibs


class Coordinator:
    def __init__(self, etl):
        self.etl = etl
        self.classes = {k: None for k in self.etl["etl"].keys()}

    def init_classes(self):
        self.classes["external_libs"] = ExternalLibs(self.etl) if self.etl["etl"]["external_libs"] else None
        self.classes["bamboo_libs"] = BambooLibs(self.etl) if self.etl["etl"]["bamboo_libs"] else None
    