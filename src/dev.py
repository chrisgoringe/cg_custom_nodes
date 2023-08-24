from src.factories import inspect_factory, passthrough_factory
from src.base import Base
import random, json

CLAZZES = []

Things = ["Clip", "Conditioning", "Float", "Image", "Int", "Latent", "Mask", "Model", "String", "Vae", ]
for Thing in Things:
    clazz = inspect_factory(f"Inspect{Thing}", Thing.upper(), Thing)
    globals()[f"Inspect{Thing}"] = clazz
    CLAZZES.append(clazz)

from nodes import CheckpointLoaderSimple, KSampler, KSamplerAdvanced, LoraLoader

CheckpointLoaderPass = passthrough_factory('CheckpointLoaderPass',CheckpointLoaderSimple,
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

class MakeDictionary(Base):
    CATEGORY = "CG/dev"
    REQUIRED = {}
    OPTIONAL = { "append_to": ("DICTIONARY", {}), "label": ("STRING", {}), "object": ("*", {}), "label2": ("STRING", {}), "object2": ("*", {}) }
    RETURN_TYPES = ("DICTIONARY",)
    def func(self, append_to=None, label=None, object=None, label2=None, object2=None):
        dictionary = append_to or {}
        if label and object:
            dictionary[label] = object
        if label2 and object2:
            dictionary[label2] = object2
        return (dictionary,)
CLAZZES.append(MakeDictionary)

class AddExtraPngInfo(Base):
    CATEGORY = "CG/dev"
    REQUIRED = { "image": ("IMAGE", {}), "label": ("STRING", {"default":"cg"}) }
    OPTIONAL = { "dictionary": ("DICTIONARY", {}) }
    HIDDEN = { "extra_pnginfo": "EXTRA_PNGINFO" }
    RETURN_TYPES = ("IMAGE",)
    def func(self, image, label:str, dictionary:dict=None, extra_pnginfo:dict=None):
        if label and dictionary:
            if extra_pnginfo:
                extra_pnginfo[label] = dictionary
            else:
                print("ERROR - AddExtraPngInfo didn't receive extra_pnginfo")
        return (image,)
CLAZZES.append(AddExtraPngInfo)