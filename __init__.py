from __future__ import (unicode_literals, division, absolute_import, print_function)
from calibre.customize import InterfaceActionBase

class Unplugged(InterfaceActionBase):
    name                    = 'Unplugged'
    description             = 'Enables "unplugged mode", where new devices are not detected'
    supported_platforms     = ['linux','windows','osx']
    author                  = 'Jellby'
    version                 = (1, 0, 0)
    minimum_calibre_version = (2, 37, 1)
    actual_plugin           = 'calibre_plugins.unplugged.ui:InterfacePlugin'
    can_be_disabled         = True

    def is_customizable(self):
        return False
