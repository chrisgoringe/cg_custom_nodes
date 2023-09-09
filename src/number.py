from src.base import Base_custom
from common_custom import read_config

class CommonSizes(Base_custom):
    CATEGORY = "CG/numbers"
    REQUIRED = { "size": (read_config('sizes'), {}) }
    RETURN_TYPES = ("INT","INT")
    RETURN_NAMES = ("width","height")
    def func(self,size:str):
        x, y = [int(v) for v in size.split('x')]
        return (x,y)
    
CLAZZES = [CommonSizes]