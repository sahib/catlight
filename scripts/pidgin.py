#!/usr/bin/env python
import dbus, gobject, dbus.mainloop.glib
import re, time, effects


# Actual uIDs are used, not aliases
buddy_reactions = {
        'christoph@jabber.nullcat.de*': [effects.HerrchenFade()],
        'zwille@jabber.i-pobox.net'   : [effects.SimpleFade({'color':(255,0,0)})],
        '431575929'                   : [effects.SimpleFade({'color':(0,255,0)})],
        '395752334'                   : [effects.SimpleFade({'color':(0,0,255)})],
        'default'                     : [effects.SimpleFade()]
}

class Listener:
    def __init__(self):
        self.bus = dbus.SessionBus()
        self.register_signal(self.received_msg,"ReceivedImMsg")
        self.register_signal(self.conversation_updated,"ConversationUpdated")
        self.msgtime = time.time()
        self.effect  = None

    def register_signal(self,func,name):
        self.bus.add_signal_receiver(func, dbus_interface="im.pidgin.purple.PurpleInterface", signal_name=name)

    def get_buddy_reaction(self,sender):
        for key,value in buddy_reactions.items():
            if re.match(key,sender):
                return value
        return buddy_reactions['default']

    def received_msg(self,account, sender, message, conversation, flags):
        print(str(sender) + " said: " + str(message))
        self.effect = effects.Repeater({
            'effects' : self.get_buddy_reaction(sender),
            'times'   : 3
            }).start() # Returns immediately
        self.msgtime = time.time()

    def conversation_updated(self,conv,flag):
        if flag == 4 and 1 < (time.time() - self.msgtime):
            if self.effect != None:
                self.effect.kill()
            self.msgtime = time.time()


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    l = Listener()
    loop = gobject.MainLoop()
    loop.run()
