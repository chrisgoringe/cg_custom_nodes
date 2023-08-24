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

