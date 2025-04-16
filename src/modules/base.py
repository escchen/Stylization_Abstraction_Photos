# COMPONENT DETAILS:
# Input: ...
# Output: ...

# CONFIG DETAILS:
# var1: ...
# var2: ...



class BaseComponent:
    def __init__(self, config=None):
        if config:
            self.config = config
    
    def load_inputs(self, inputs):
        return inputs

    def process(self, inputs):
        raise NotImplementedError("Any subclass of BaseComponent needs to implement 'process()' method")
    
    def save_outputs(self, outputs, path):
        with open(path, 'w') as f:
            f.write(outputs)
