from src.base import Base, SeedContext
import random, math
       
class CommonSizes(Base):
    CATEGORY = "CG/numbers"
    REQUIRED = { "size": (("512x512", "512x768", "512x1024", "768x512", "768x768", "768x1024", "1024x512", "1024x768", "1024x1024",
                           "640x1536", "768x1344", "832x1216", "896x1152"), {}) }
    RETURN_TYPES = ("INT","INT")
    RETURN_NAMES = ("width","height")
    def func(self,size:str):
        x, y = [int(v) for v in size.split('x')]
        return (x,y)
    
class RandomShape(Base):
    CATEGORY = "CG/numbers"
    REQUIRED = { "square_size" : ("INT", {"default":1024, "min":256, "max":2048, "step": 8}),
                 "max_aspect" : ("FLOAT", {"default":2.5, "min": 1.1, "max":10.0, "step":0.1}),
                 "seed": ("INT",{"default": 0, "min": 0, "max": 0xffffffffffffffff}), }
    RETURN_TYPES = ("INT","INT","INT")
    RETURN_NAMES = ("width","height","seed")
    def func(self,square_size:int, max_aspect:float, seed:int):
        with SeedContext():
            aspect = math.sqrt(random.random() * (max_aspect-1.0) + 1.0)
            bigger = (int(square_size * aspect) // 8) * 8
            smaller = (int(square_size / aspect) // 8) * 8
            return (bigger, smaller, seed) if random.random() > 0.5 else (smaller, bigger, seed)

class RandomBase(Base):
    RETURN_NAMES = ("rand",)
    CATEGORY = "CG/numbers"
    def IS_CHANGED(self, minimum, maximum, seed):
        return self.func(minimum, maximum, seed)[0]
    def func(self, minimum, maximum, seed):
        with SeedContext(seed):
            rand = self.gen(minimum, maximum)
        return (rand,)
    gen = lambda a,b:0

class RandomFloat(RandomBase):
    REQUIRED = { 
                "minimum": ("FLOAT", {"default": 0.0}), 
                "maximum": ("FLOAT", {"default": 1.0}), 
                "seed": ("INT",{"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
    RETURN_TYPES = ("FLOAT",)
    gen = random.uniform

class RandomInt(RandomBase):
    REQUIRED = { 
                "minimum": ("INT", {"default": 0}), 
                "maximum": ("INT", {"default": 99999999}), 
                "seed": ("INT",{"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
    RETURN_TYPES = ("INT",)
    gen = random.randint
    
CLAZZES = [CommonSizes, RandomShape, RandomFloat, RandomInt]