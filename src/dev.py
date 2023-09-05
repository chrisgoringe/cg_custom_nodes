from src.factories import inspect_factory, passthrough_factory
from src.base import Base_custom
import random, json

CLAZZES = []

Things = ["Clip", "Conditioning", "Float", "Image", "Int", "Latent", "Mask", "Model", "String", "Vae", ]
for Thing in Things:
    clazz = inspect_factory(f"Inspect{Thing}", Thing.upper(), Thing)
    globals()[f"Inspect{Thing}"] = clazz
    CLAZZES.append(clazz)

from nodes import CheckpointLoaderSimple, KSampler, KSamplerAdvanced, LoraLoader

class CheckpointLoaderSelective(CheckpointLoaderSimple):
    @classmethod
    def INPUT_TYPES(s):
        input_types = CheckpointLoaderSimple.INPUT_TYPES()
        input_types['optional'] = { "name": ("STRING", {"forceInput":True}) }
        return input_types
    FUNCTION = "func"
    category="CG/loaders"
    def func(self, ckpt_name, name=None, output_vae=True, output_clip=True):
        return super().load_checkpoint(name or ckpt_name, output_vae, output_clip)


CheckpointLoaderPass = passthrough_factory('CheckpointLoaderPass',CheckpointLoaderSelective,
                                           ("ckpt_name",), 
                                           ("name",),
                                           category="CG/loaders")
CLAZZES.append(CheckpointLoaderPass)

KSamplerPass = passthrough_factory('KSamplerPass', KSampler, 
                                   ('model', 'positive', 'negative', 'seed',), 
                                   category="CG/sampling")
CLAZZES.append(KSamplerPass)

KSamplerAdvancedPass = passthrough_factory('KSamplerAdvancedPass', KSamplerAdvanced, 
                                           ('model', 'positive', 'negative', 'noise_seed', 'steps', 'end_at_step' ), 
                                           category="CG/sampling")
CLAZZES.append(KSamplerAdvancedPass)

LoraLoaderPass = passthrough_factory('LoraLoaderPass', LoraLoader,
                                     ("lora_name",),
                                     ("name",),
                                     category="CG/loaders")
CLAZZES.append(LoraLoaderPass)

class MakeCombo(Base_custom):
    CATEGORY = "type_transforms"
    REQUIRED = { "string": ("STRING", {"default":""}) }
    RETURN_TYPES = ("euler",)
    RETURN_NAMES = ("COMBO",)
    def func(self, string):
        return( string, )
    
CLAZZES.append(MakeCombo)
