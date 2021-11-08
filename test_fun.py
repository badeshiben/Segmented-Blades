import openmdao.api as om

class Addition(om.ExplicitComponent):
    def setup(self):
        self.add_input('x', val=0.0)
        self.add_input('y', val=0.0)
        self.add_output('z', val=0.0)

    def compute(self, inputs, outputs):
        x = inputs['x']
        y = inputs['y']

        outputs['z'] = x + y

if __name__ == "__main__":

    model = om.Group()
    model.add_subsystem('add', Addition())
    prob = om.Problem(model)
    prob.setup(derivatives=False)
    prob.set_val('add.x', 1)
    prob.set_val('add.y', 2)
    prob.run_model()
    print(prob.get_val('add.z'))