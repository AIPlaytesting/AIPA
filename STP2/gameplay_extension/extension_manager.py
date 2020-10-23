from .extension_context import ExtensionContext
from .buff_base import BuffBase
class ExtensionManager:
    def __init__(self,extension_context:ExtensionContext):
        self.extension_context = extension_context

    def create_buff_instance(self,buffname:str)->BuffBase:
        pass