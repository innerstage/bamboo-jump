import re
from bamboo_jumpstart.util import bamboo_dependencies_dict

class ExternalLibs:
    def __init__(self, etl):
        self.code = ""
        self.etl = etl
        self.libs_list = etl["etl"]["external_libs"] if etl["etl"]["external_libs"] else []

    def add_code(self, code):
        self.code += code

    def process(self, entry):
        if "as" in entry and "." in entry: # Example: ["math.sqrt as square_root"] -> "from math import sqrt as square_root"
            t1 = re.match(r"(\w+).(\w+) as (\w+)", entry)
            lib, func, name = t1.groups()
            return "from {} import {} as {}\n".format(lib, func, name)
        
        elif "." in entry: # Example: ["time.perf_counter"] -> "from time import perf_counter"
            t2 = re.match(r"(\w+).(\w+)", entry)
            lib, func = t2.groups()
            return "from {} import {}\n".format(lib, func)

        elif "as" in entry: # Example: ["pandas as pd"] -> "import pandas as pd"
            t3 = re.match(r"(\w+) as (\w+)", entry)
            lib, name = t3.groups()
            return "import {} as {}\n".format(lib, name)

        elif "." not in entry and "as" not in entry and " " not in entry: # Example: ["numpy"] -> "import numpy"
            t4 = re.match(r"(\w+)", entry)
            lib = t4.groups()[0]
            return "import {}\n".format(lib)

        elif ">" in entry: # Example: ["> from etl.util import hs6_revision as rev"] -> "from etl.util import hs6_revision as rev"
            return entry.replace("> ",">").replace(">","") + "\n"

    def run(self):
        if "parent_dir*" in self.etl["etl"]["special"]:
            if "os" not in self.libs_list:
                self.libs_list.append("os")

        for entry in self.libs_list:
            self.add_code(self.process(entry))
        
        return self.code


class BambooLibs:
    def __init__(self, etl):
        self.code = ""
        self.etl = etl
        self.dependency = bamboo_dependencies_dict
        self.reverse_dep = {v:k for k in self.dependency for v in self.dependency[k]}
        self.instance = {k:[] for k in self.dependency.keys()}
        self.bamboo_list = etl["etl"]["bamboo_libs"] + ["EasyPipeline", "PipelineStep", "Parameter", "logger"]

    def add_code(self, code):
        self.code += code

    def add_to_instance(self, element):
        key = self.reverse_dep[element]
        self.instance[key].append(element)

    def instance_to_code(self):
        for k in self.instance.keys():
            vals = self.instance[k]
            if len(vals) == 0:
                continue
            elif len(vals) == 1:
                line = "from bamboo_lib.{} import {}\n".format(k, vals[0])
                self.add_code(line)
            elif len(vals) >= 2:
                line = "from bamboo_lib.{} import ".format(k)
                for i in range(len(vals)-1):
                    line += "{}, ".format(vals[i])
                line += "{}\n".format(vals[-1])
                self.add_code(line)
        self.add_code("\n")

    def run(self):
        if "parent_dir*" in self.etl["etl"]["special"]:
            self.add_to_instance("parent_dir")

        for element in self.bamboo_list:
            self.add_to_instance(element)

        self.instance_to_code()

        return self.code
