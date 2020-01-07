from bamboo_jumpstart.util import bamboo_dependencies_dict, camelcase_to_snakecase

class StepsDeclaration:
    def __init__(self, etl):
        self.code = ""
        self.etl = etl
        self.normal_steps = self.get_normal_steps()

    def add_code(self, code):
        self.code += code

    def get_normal_steps(self):
        use_loop = (False, 0)
        normal_steps = []

        for index, step in enumerate(self.etl["etl"]["steps"]):
            if step["class"] == "LoopHelper*":
                use_loop = (True, index)
            else:
                normal_steps.append(step)

        if use_loop[0]:
            iter_step = self.etl["etl"]["steps"][use_loop[1]]["iter_step"][0]
            normal_steps.append(iter_step)
            for step in self.etl["etl"]["steps"][use_loop[1]]["sub_steps"]:
                normal_steps.append(step)

        special_steps = [step + '*' for step in bamboo_dependencies_dict["steps"]]

        return [step["class"] for step in normal_steps if step["class"] not in special_steps]

    def run(self):
        for step in self.normal_steps:
            code = 'class {}(PipelineStep):\n\tdef run_step(self, prev, params):\n\t\tlogger.info("{}...")\n\t\tresult = prev\n\n\t\treturn result\n\n\n'.format(step, step)
            self.add_code(code)

        return self.code


class StepsUse:
    def __init__(self, etl):
        self.code = ""
        self.etl = etl
        self.use_loop = self.get_use_loop()
        self.steps = self.get_steps()
        self.source_vars = {}
        self.db_vars = {}


    def add_code(self, code):
        self.code += code


    def get_use_loop(self):
        use_loop = (False, 0)
        for index, step in enumerate(self.etl["etl"]["steps"]):
            if step["class"] == "LoopHelper*":
                use_loop = (True, index)

        return use_loop


    def get_steps(self):
        steps = []

        for step in self.etl["etl"]["steps"]:
            if step["class"] != "LoopHelper*":
                steps.append(step)

        if self.use_loop[0]:
            iter_step = self.etl["etl"]["steps"][self.use_loop[1]]["iter_step"][0]
            steps.append(iter_step)
            for step in self.etl["etl"]["steps"][self.use_loop[1]]["sub_steps"]:
                steps.append(step)

        return steps


    def get_connectors(self):
        conn_code = ""
        a = 0
        if "sources" in self.etl["etl"].keys():
            for source in self.etl["etl"]["sources"]:
                a += 1
                var_name = source["var_name"] if "var_name" in source.keys() else "source_connector_{}".format(a)
                self.source_vars[source["name"]] = var_name
                if "parent_dir*" not in self.etl["etl"]["special"]:
                    code = '\t\t{} = grab_connector(__file__, "{}")\n'.format(var_name, source["name"])
                    conn_code += code

        b = 0
        if "databases" in self.etl["etl"].keys():
            for db in self.etl["etl"]["databases"]:
                b += 1
                var_name = db["var_name"] if "var_name" in db.keys() else "db_connector_{}".format(b)
                self.db_vars[db["name"]] = var_name
                if "parent_dir*" not in self.etl["etl"]["special"]:
                    code = '\t\t{} = grab_connector(__file__, "{}")\n'.format(var_name, db["name"])
                    if "output-db*" in self.etl["etl"]["special"]:
                        code = '\t\t{} = grab_connector(__file__, params.get("output-db"))\n'.format(var_name)
                    conn_code += code

        return conn_code + "\n"
                

    def process_step(self, step):
        if step["class"] == "DownloadStep*":
            var_name = step["var_name"] if "var_name" in step.keys() else "dl_step"
            source_conn = step["source"] if "source" in step.keys() else '""'
            source_var = self.source_vars[source_conn] if source_conn != '""' else '""'
            code = '\t\t{} = DownloadStep(connector={})\n'.format(var_name, source_var)
            if "special" in self.etl["etl"].keys() and "parent_dir*" in self.etl["etl"]["special"]:
                source_conn = step["source"] if "source" in step.keys() else '""'
                code = '\t\t{} = DownloadStep(connector={}, connector_path=parent_dir)\n'.format(var_name, source_conn)
            return code

        if step["class"] == "WildcardDownloadStep*":
            var_name = step["var_name"] if "var_name" in step.keys() else "wdl_step"
            source_conn = step["source"] if "source" in step.keys() else '""'
            code = '\t\t{} = WildcardDownloadStep(connector={})\n'.format(var_name, self.source_vars[source_conn])
            if "special" in self.etl["etl"].keys() and "parent_dir*" in self.etl["etl"]["special"]:
                source_conn = step["source"] if "source" in step.keys() else '""'
                code = '\t\t{} = WildcardDownloadStep(connector="{}", connector_path=parent_dir)\n'.format(var_name, source_conn)
            return code

        if step["class"] == "LoadStep*":
            var_name = step["var_name"] if "var_name" in step.keys() else "load_step"
            db_conn = step["db"] if "db" in step.keys() else '""'
            db_var = self.db_vars[db_conn] if db_conn != '""' else '""'
            code = '\t\t{} = LoadStep(\n'.format(var_name)
            code += '\t\t\ttable_name="",\n'
            code += '\t\t\tconnector={},\n'.format(db_var)
            code += '\t\t\tif_exists="",\n\t\t\tpk=[]\n\t\t\tdtype= ,\n\t\t\tnullable_list=[]\n\t\t)\n'
            if "special" in self.etl["etl"].keys() and "parent_dir*" in self.etl["etl"]["special"]:
                code = '\t\t{} = LoadStep(\n'.format(var_name)
                code += '\t\t\ttable_name="",\n'
                db_conn_2 = db_conn if "output-db*" not in self.etl["etl"]["special"] else 'params.get("output-db")'
                code += '\t\t\tconnector={},\n'.format(db_conn_2)
                code += '\t\t\tconnector_path=parent_dir,\n'
                code += '\t\t\tif_exists="",\n\t\t\tpk=[]\n\t\t\tdtype= ,\n\t\t\tnullable_list=[]\n\t\t)\n'
            return code
        
        else:
            var_name = step["var_name"] if "var_name" in step.keys() else camelcase_to_snakecase(step["class"].replace("*",""))
            code = '\t\t{} = {}()\n'.format(var_name, step["class"])
            return code


    def get_var_name(self, step):
        if "var_name" in step.keys():
            return step["var_name"]
        else:
            special_var_names = {
                "DownloadStep*": "dl_step", 
                "WildcardDownloadStep*": "wdl_step", 
                "LoadStep*": "load_step"
            }
            if step["class"] in special_var_names.keys():
                return special_var_names[step["class"]]
            else:
                return camelcase_to_snakecase(step["class"].replace("*", ""))


    def get_sub_steps(self):
        loop_helper = self.etl["etl"]["steps"][self.use_loop[1]]
        step_0 = loop_helper["sub_steps"][0]
        code = '\t\tsub_steps = [{}'.format(self.get_var_name(step_0))
        for step in loop_helper["sub_steps"][1:]:
            code += ', {}'.format(self.get_var_name(step))
        code += ']'
        
        if "ingest*" in self.etl["etl"]["special"]:
            code += ' if params.get("ingest") else [{}'.format(self.get_var_name(step_0))
            for step in [s for s in loop_helper["sub_steps"][1:] if s["class"]!="LoadStep*"]:
                code += ', {}'.format(self.get_var_name(step))
            code += ']\n'
        else:
            code += '\n'

        return '\n' + code


    def get_steps_return(self):
        if self.use_loop[0] and self.use_loop[1] == 0:
            loop_helper = self.etl["etl"]["steps"][self.use_loop[1]]
            code = '\n\t\treturn [LoopHelper(iter_step={}, sub_steps=sub_steps)'.format(self.get_var_name(loop_helper["iter_step"][0]))
            for step in self.etl["etl"]["steps"][1:]:
                code += ', {}'
            code += ']\n'

            return code

        elif self.use_loop[0] and self.use_loop[1] > 0:
            loop_helper = self.etl["etl"]["steps"][self.use_loop[1]]
            code = '\n\t\treturn [{}'.format(self.get_var_name(self.etl["etl"]["steps"][0]))
            for step in self.etl["etl"]["steps"][1:self.use_loop[1]]:
                code += ', {}'.format(self.get_var_name(step))
            code += ', '
            code += 'LoopHelper(iter_step={}, sub_steps=sub_steps)'.format(self.get_var_name(loop_helper["iter_step"][0]))
            for step in self.etl["etl"]["steps"][self.use_loop[1]+1:]:
                code += ', {}'
            code += ']\n'

            return code

        else:
            code = "\n\t\treturn [{}".format(self.get_var_name(self.steps[0]))
            for step in self.steps[1:]:
                code += ', {}'.format(self.get_var_name(step))
            code += "]\n"

            return code


    def run(self):
        code = "\n\t@staticmethod\n\tdef steps(params):\n"
        self.add_code(code)

        if "special" in self.etl["etl"].keys() and "parent_dir*" in self.etl["etl"]["special"]:
            code = "\t\tparent_dir = os.path.join(grab_parent_dir(__file__))\n"
            self.add_code(code)

        code = self.get_connectors()
        self.add_code(code)

        for step in self.steps:
            code = self.process_step(step)
            self.add_code(code)

        if self.use_loop[0]:
            code = self.get_sub_steps()
            self.add_code(code)

        code = self.get_steps_return()
        self.add_code(code)

        return self.code + "\n"
        
