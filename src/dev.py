from src.base import Base

def func(*args, **kwargs):
    input = list(kwargs.values())[0]
    print(f"{input}")                 # This is a good place to put a breakpoint...
    return (input,)

def factory(name:str, to_inspect:str):
    clazz_contents = {
        "CATEGORY" : "CG/dev",
        "REQUIRED" : { to_inspect: (to_inspect, {}) },
        "RETURN_TYPES" : (to_inspect,),
        "func" : func
    }
    clazz = type(name,(Base,),clazz_contents)
    return clazz

InspectConditioning = factory('InspectConditioning', 'CONDITIONING')

