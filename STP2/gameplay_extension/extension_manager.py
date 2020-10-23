from .buff_extension import BuffExtension


class ExtensionManager:
    def __init__(self):
        self.buff_extension_dict = self.__load_buff_extensions()
    
    def get_buff_extension(self,buffname:str)->BuffExtension:
        if buffname in self.buff_extension_dict:
            return self.buff_extension_dict[buffname]
        else:
            print("[Extension Manager]-ERROR- fail to load buff extension: "+buffname)
            return None

    # TODO dynamic load from directory
    def __load_buff_extensions(self)->dict:
        from .weaken import Weaken
        from .strength import Strength
        from .vulnerable import Vulnerable
        extension_dict = {}
        extension_dict['Weakened'] = Weaken()
        extension_dict['Strength'] = Strength()
        extension_dict['Vulnerable'] = Vulnerable()
        return extension_dict