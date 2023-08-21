import random, os
from src.base import Base, SeedContext

EXT_CLASSES = []

try:
    from custom_nodes.sdxl_prompt_styler.sdxl_prompt_styler import SDXLPromptStyler, read_json_file, read_sdxl_styles
    class RandomSdxlStyle(SDXLPromptStyler):
        resource_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'resources')
        @classmethod
        def INPUT_TYPES(cls):
            it = SDXLPromptStyler.INPUT_TYPES()
            it['optional'] = { "seed":("INT", {"default":0,"min": 0,"max":0xffffffffffffffff})}
            it['required'].pop('style')
            it['required']['json_file'] = (list((f for f in os.listdir(cls.resource_dir) if f.endswith("styles.json"))),{})

            return it
        CATEGORY = 'CG/prompting'
        FUNCTION = 'func'
        RETURN_TYPES = ('STRING','STRING','STRING',)
        RETURN_NAMES = ('positive','negative','style_name',)
        def func(self, text_positive, text_negative, log_prompt, json_file, seed=None):
            file_path = os.path.join(self.resource_dir, json_file)
            self.json_data = read_json_file(file_path)
  
            with SeedContext(seed):
                style = random.choice(self.json_data)
                stylename = style['name'] if 'name' in style else 'none'

            return self.prompt_styler(text_positive, text_negative, stylename, log_prompt)+(stylename,)
        
    EXT_CLASSES.append("RandomSdxlStyle",)

except:
    print("Random SDXL Prompt requires sdxl_prompt_styler")


