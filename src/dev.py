from src.base import Base

def func(log, input):
    if log:
        print(f"{input}")                 
    return (input,) # This is a good place to put a breakpoint...

def inspect_factory(name:str, to_inspect:str, display_name:str=None):
    display_name = display_name or to_inspect
    clazz_contents = {
        "CATEGORY" : "CG/dev",
        "REQUIRED" : { display_name: (to_inspect, {}), "log": (["yes","no"], {}) },
        "RETURN_TYPES" : (to_inspect,),
        "RETURN_NAMES" : (display_name,),
        "OUTPUT_NODE" : True,
        "func" : lambda *args, **kwargs : func(kwargs['log']=='yes', kwargs[display_name])
    }
    clazz = type(name,(Base,),clazz_contents)
    return clazz


Things = ["Clip", "Conditioning", "Float", "Image", "Int", "Latent", "Model", "String", "Vae", ]
for Thing in Things:
    globals()[f"Inspect{Thing}"] = inspect_factory(f"Inspect{Thing}", Thing.upper(), Thing)

DEV_CLASSES = [f"Inspect{Thing}" for Thing in Things]