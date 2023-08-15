from src.base import Base

def func(input, log:bool, label:str):
    if log:
        print(f"{label} {input}")                 
    return (input,) # This is a good place to put a breakpoint...

def inspect_factory(name:str, to_inspect:str, display_name:str=None):
    display_name = display_name or to_inspect
    clazz_contents = {
        "CATEGORY" : "CG/dev",
        "REQUIRED" : { display_name: (to_inspect, {}), "log": (["yes","no"], {}), "label": ("STRING", {"default":""}) },
        "RETURN_TYPES" : (to_inspect,),
        "RETURN_NAMES" : (display_name,),
        "OUTPUT_NODE" : True,
        "func" : lambda *args, **kwargs : func(kwargs[display_name], kwargs['log']=='yes', kwargs['label'] )
    }
    clazz = type(name,(Base,),clazz_contents)
    return clazz

def passthrough_factory(clazz_name:str, base_clazz:type, passed_names, category="CG/dev"):
    clazz = type(clazz_name, (base_clazz,), {"CATEGORY" : category, "FUNCTION" : "func"})
    input_types = clazz.INPUT_TYPES()
    in_types = {name:input_types[typ][name][0] for typ in input_types for name in input_types[typ]}
    passed_types = [(in_types[name] if isinstance(in_types[name],str) else 'STRING') for name in passed_names]

    if 'RETURN_NAMES' not in clazz.__dict__:
        clazz.RETURN_NAMES = clazz.RETURN_TYPES
    clazz.RETURN_NAMES += passed_names
    
    clazz.RETURN_TYPES += tuple(passed_types)
    clazz.__func = base_clazz.__dict__[base_clazz.FUNCTION]
    def func(self, *args, **kwargs):
        orig = self.__func(*args, **kwargs)
        return orig[:-len(passed_names)] + tuple(kwargs[name] for name in passed_names)
    clazz.func = func
    return clazz

Things = ["Clip", "Conditioning", "Float", "Image", "Int", "Latent", "Mask", "Model", "String", "Vae", ]
for Thing in Things:
    globals()[f"Inspect{Thing}"] = inspect_factory(f"Inspect{Thing}", Thing.upper(), Thing)

DEV_CLASSES = [f"Inspect{Thing}" for Thing in Things]

from nodes import CheckpointLoaderSimple, KSampler, KSamplerAdvanced

CheckpointLoaderPass = passthrough_factory('CheckpointLoaderPass',CheckpointLoaderSimple,
                                           ("ckpt_name",), "CG/loaders")
DEV_CLASSES.append('CheckpointLoaderPass')

KSamplerPass = passthrough_factory('KSamplerPass', KSampler, 
                                   ('positive', 'negative', 'latent_image', 'seed',), "CG/sampling")
DEV_CLASSES.append('KSamplerPass')

KSamplerAdvancedPass = passthrough_factory('KSamplerAdvancedPass', KSamplerAdvanced, 
                                           ('positive', 'negative', 'latent_image', 'noise_seed', 'end_at_step' ), "CG/sampling")
DEV_CLASSES.append('KSamplerAdvancedPass')