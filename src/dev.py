from src.factories import inspect_factory, passthrough_factory

Things = ["Clip", "Conditioning", "Float", "Image", "Int", "Latent", "Mask", "Model", "String", "Vae", ]
for Thing in Things:
    globals()[f"Inspect{Thing}"] = inspect_factory(f"Inspect{Thing}", Thing.upper(), Thing)

CLAZZES = [f"Inspect{Thing}" for Thing in Things]

from nodes import CheckpointLoaderSimple, KSampler, KSamplerAdvanced, LoraLoader

CheckpointLoaderPass = passthrough_factory('CheckpointLoaderPass',CheckpointLoaderSimple,
                                           ("ckpt_name",), 
                                           ("name",),
                                           category="CG/loaders")
CLAZZES.append('CheckpointLoaderPass')

KSamplerPass = passthrough_factory('KSamplerPass', KSampler, 
                                   ('model', 'positive', 'negative', 'seed',), 
                                   category="CG/sampling")
CLAZZES.append('KSamplerPass')

KSamplerAdvancedPass = passthrough_factory('KSamplerAdvancedPass', KSamplerAdvanced, 
                                           ('model', 'positive', 'negative', 'noise_seed', 'steps', 'end_at_step' ), 
                                           category="CG/sampling")
CLAZZES.append('KSamplerAdvancedPass')

LoraLoaderPass = passthrough_factory('LoraLoaderPass', LoraLoader,
                                     ("lora_name",),
                                     ("name",),
                                     category="CG/loaders")
CLAZZES.append('LoraLoaderPass')