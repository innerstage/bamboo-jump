from bamboo_jumpstart.util import camelcase_to_snakecase

class MainDeclaration:
    def __init__(self, etl):
        self.code = ""
        self.etl = etl
        self.pipeline_name = self.get_name()
        self.instance_name = self.get_instance_name()
        self.params = self.get_params()

    def add_code(self, code):
        self.code += code

    def get_name(self):
        if "pipeline_name" in self.etl["etl"]["names"]:
            return self.etl["etl"]["names"]["pipeline_name"]
        else:
            raise ValueError("The pipeline_name value must be specified in the YAML file!\n(etl > names > pipeline_name)")

    def get_instance_name(self):
        if "instance_name" in self.etl["etl"]["names"]:
            return self.etl["etl"]["names"]["instance_name"]
        else:
            return camelcase_to_snakecase(self.pipeline_name)

    def get_params(self):
        params = []
        if "special" in self.etl["etl"].keys() and "output-db*" in self.etl["etl"]["special"]:
            params.append({"name": "output-db", "type": "str"})
        
        if "special" in self.etl["etl"].keys() and "ingest*" in self.etl["etl"]["special"]:
            params.append({"name": "ingest", "type": "bool"})

        if "special" in self.etl["etl"].keys() and "parameters" in self.etl["etl"]:
            for param in self.etl["etl"]["parameters"]:
                params.append(param)

        return params

    def default_val(self, param):
        if param["type"] == "str":
            return '""'
        elif param["type"] == "int":
            return 0
        elif param["type"] == "bool":
            return 'False'

    def run(self):
        code = 'if __name__ == "__main__":\n'
        code += '\t{} = {}()\n'.format(self.instance_name, self.pipeline_name)
        code += '\t{}.run(\n\t\t{{\n'.format(self.instance_name)
        self.add_code(code)

        if len(self.params) != 0:
            name_0 = self.params[0]["name"]
            val_0 = self.params[0]["default"] if "default" in self.params[0] else self.default_val(self.params[0])
            code = '\t\t\t"{}": {}'.format(name_0, val_0)
            self.add_code(code)
            for p in self.params[1:]:
                name = p["name"]
                val = p["default"] if "default" in p else self.default_val(p)
                code = ',\n\t\t\t"{}": {}'.format(name, val)
                self.add_code(code)
        
        code = '\n\t\t}\n'
        self.add_code(code)

        return self.code


