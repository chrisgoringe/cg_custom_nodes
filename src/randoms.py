import random 
from src.base import Base

class RandomFloats(Base):
    CATEGORY = "CG/random"
    REQUIRED = { 
                "minimum": ("FLOAT", {"default": 0.0}), 
                "maximum": ("FLOAT", {"default": 1.0}), 
                "seed": ("INT",{"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
    RETURN_TYPES = ("FLOAT","FLOAT","FLOAT")
    RETURN_NAMES = ("f1","f2","f3")

    def func(self, minimum, maximum, seed):
        state = random.getstate()
        random.seed(seed)
        rands = [random.uniform(minimum, maximum) for _ in range(3)]
        random.setstate(state=state)
        return rands
