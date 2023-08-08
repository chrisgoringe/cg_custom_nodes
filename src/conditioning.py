import torch
from src.base import Base

class ReferenceOnly(Base):
    REQUIRED = { 
        "model": ("MODEL",),
        "reference": ("LATENT",),
        "factor": ("FLOAT", {"default": 1.0, "min": -1.0, "max": 1.0, "step": 0.05})
    }
    RETURN_TYPES = ("MODEL", )
    CATEGORY = "CG/conditioning"

    def func(self, model, reference, factor):
        model_reference = model.clone()
        self.samples = reference["samples"]

        def reference_apply(q, k, v, extra_options):
            k = self.samples.clone() * factor
            return q, k, k

        model_reference.set_model_attn1_patch(reference_apply)

        return (model_reference, )

NODE_CLASS_MAPPINGS = {
    "ReferenceOnly": ReferenceOnly,
}
