import random
EXT_CLASSES = []

try:
    from custom_nodes.sdxl_prompt_styler.sdxl_prompt_styler import SDXLPromptStyler
    class RandomSdxlStyle(SDXLPromptStyler):
        @classmethod
        def INPUT_TYPES(cls):
            it = SDXLPromptStyler.INPUT_TYPES()
            it['optional'] = { "seed":("INT", {"default":0,})}
            cls.styles = it['required'].pop('style')[0]
            return it
        CATEGORY = 'CG/prompting'
        FUNCTION = 'func'
        RETURN_TYPES = ('STRING','STRING','STRING',)
        RETURN_NAMES = ('positive_prompt_text_g','negative_prompt_text_g','style_name',)
        def func(self, text_positive, text_negative, log_prompt, seed=None):
            state = random.getstate()
            random.seed(seed)
            style = random.choice(self.styles)            
            random.setstate(state=state)
            return self.prompt_styler(text_positive, text_negative, style, log_prompt)+(style,)
        
    EXT_CLASSES.append("RandomSdxlStyle",)
except:
    print("Random SDXL Prompt requires sdxl_prompt_styler")
