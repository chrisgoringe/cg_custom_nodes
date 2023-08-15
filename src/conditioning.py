from src.base import Base
from nodes import ConditioningSetMask

class MergeConditionings(Base):
    CATEGORY = "CG/conditioning"
    REQUIRED = {"conditioning1": ("CONDITIONING", ), "conditioning2": ("CONDITIONING", ),"mask": ("MASK", ), }
    RETURN_TYPES = ("CONDITIONING", )
    RETURN_NAMES = ("conditioning", )
    apply_mask = ConditioningSetMask().append

    def func(self, conditioning1, conditioning2, mask):
        c1 = self.apply_mask(conditioning1, mask, "default", 1.0)[0]
        c2 = self.apply_mask(conditioning2, 1.0-mask, "default", 1.0)[0]
        return (c1+c2, )
    
