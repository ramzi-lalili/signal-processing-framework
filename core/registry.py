GENERATORS = {}
OPERATIONS = {}

def register_generator(name, cls):
    GENERATORS[name] = cls
    return cls

def register_operation(name, cls):
    OPERATIONS[name] = cls
    return cls
