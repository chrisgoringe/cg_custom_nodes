from src.base import Base

def func(*args, **kwargs):
    input = list(kwargs.values())[0]
    print(f"{input}")                 # This is a good place to put a breakpoint...
    return (input,)

def inspect_factory(name:str, to_inspect:str, display_name:str=None):
    display_name = display_name or to_inspect
    clazz_contents = {
        "CATEGORY" : "CG/dev",
        "REQUIRED" : { display_name: (to_inspect, {}) },
        "RETURN_TYPES" : (to_inspect,),
        "RETURN_NAMES" : (display_name,),
        "OUTPUT_NODE" : True,
        "func" : func
    }
    clazz = type(name,(Base,),clazz_contents)
    return clazz

InspectConditioning = inspect_factory('InspectConditioning', 'CONDITIONING', 'Conditioning')

