from bamboo_jumpstart.util import bamboo_dependencies_dict

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

        if use_loop:
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
        
