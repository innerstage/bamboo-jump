class ParameterDeclaration:
    def __init__(self, etl):
        self.code = ""
        self.etl = etl
        self.pipeline_name = self.get_name()
        self.params = self.get_params()

    def add_code(self, code):
        self.code += code

    def get_name(self):
        if "pipeline_name" in self.etl["etl"].keys() and self.etl["etl"]["names"]["pipeline_name"]:
            return self.etl["etl"]["names"]["pipeline_name"]
        else:
            return "NewPipeline"

    def get_params(self):
        params = []
        if "special" in self.etl["etl"] and "output-db*" in self.etl["etl"]["special"]:
            params.append({"name": "output-db", "type": "str"})
        
        if "special" in self.etl["etl"] and "ingest*" in self.etl["etl"]["special"]:
            params.append({"name": "ingest", "type": "bool"})

        if "parameters" in self.etl["etl"]:
            for param in self.etl["etl"]["parameters"]:
                params.append(param)

        return params

    def run(self):
        code = 'class {}(EasyPipeline):\n\t@staticmethod\n\tdef parameter_list():\n\t\treturn [\n'.format(self.pipeline_name)
        self.add_code(code)
        
        if len(self.params) != 0:
            for param in self.params[:-1]:
                if "default" in param.keys():
                    code = '\t\t\tParameter("{}", dtype={}, default_value="{}"),\n'.format(param["name"], param["type"], param["default"])
                else:
                    code = '\t\t\tParameter("{}", dtype={}),\n'.format(param["name"], param["type"])
                self.add_code(code)

            if "default" in self.params[-1].keys():
                code = '\t\t\tParameter("{}", dtype={}, default_value={})\n'.format(self.params[-1]["name"], self.params[-1]["type"], self.params[-1]["default"])
            else:
                code = '\t\t\tParameter("{}", dtype={})\n'.format(self.params[-1]["name"], self.params[-1]["type"])
            self.add_code(code)
        
        self.add_code("\t\t]\n")

        return self.code
