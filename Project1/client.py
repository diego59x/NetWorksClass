# Instant messaging app using xmpp 
# UVG
# Diego Alvarez 19498
# Documentation: 
# https://slixmpp.readthedocs.io/en/latest/
# https://oriolrius.cat/wp-content/uploads/2009/10/Oreilly.XMPP.The.Definitive.Guide.May.2009.pdf

import asyncio
import logging

from slixmpp import ClientXMPP

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class EchoBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')

    xmpp = EchoBot('somejid@example.com', 'use_getpass')
    xmpp.connect()
    xmpp.process()