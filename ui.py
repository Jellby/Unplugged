from __future__ import (unicode_literals, division, absolute_import, print_function)
from calibre.gui2.actions import InterfaceAction
from calibre.utils.config import JSONConfig

from calibre.gui2.device import DeviceManager

detect_device_original = DeviceManager.detect_device

# Note this is just copied from src/calibre/gui2/device.py
def detect_device_but_do_not_connect(self):
    self.scanner.scan()

    if self.is_device_connected:
        if self.connected_device.MANAGES_DEVICE_PRESENCE:
            cd = self.connected_device.detect_managed_devices(self.scanner.devices)
            if cd is None:
                self.connected_device_removed()
        else:
            connected, detected_device = \
                self.scanner.is_device_connected(self.connected_device,
                        only_presence=True)
            if not connected:
                if DEBUG:
                    # Allow the device subsystem to output debugging info about
                    # why it thinks the device is not connected. Used, for e.g.
                    # in the can_handle() method of the T1 driver
                    self.scanner.is_device_connected(self.connected_device,
                            only_presence=True, debug=True)
                self.connected_device_removed()

class InterfacePlugin(InterfaceAction):

    name = 'Unplugged'
    action_spec = ('Unplugged', None, None, (None))
    prefs = JSONConfig('plugins/unplugged')
    icon_enabled = get_icons('images/unplugged_enabled.png')
    icon_disabled = get_icons('images/unplugged_disabled.png')

    def genesis(self):
        if 'unplugged' in self.prefs:
            self.unplugged = self.prefs['unplugged']
        else:
            self.unplugged = False
            self.prefs['unplugged'] = self.unplugged
        self.change_action()
        self.qaction.triggered.connect(self.toggle_unplugged)

    def toggle_unplugged(self):
        self.unplugged = not self.unplugged
        self.prefs['unplugged'] = self.unplugged
        self.change_action()
 
    def change_action(self):
        if (self.unplugged):
          self.qaction.setIcon(self.icon_enabled)
          DeviceManager.detect_device = detect_device_but_do_not_connect
        else:
          self.qaction.setIcon(self.icon_disabled)
          DeviceManager.detect_device = detect_device_original

