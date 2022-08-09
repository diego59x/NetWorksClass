# Instant messaging app using xmpp 
# UVG
# Diego Alvarez 19498
# Documentation: 
# https://slixmpp.readthedocs.io/en/latest/
# https://oriolrius.cat/wp-content/uploads/2009/10/Oreilly.XMPP.The.Definitive.Guide.May.2009.pdf
import asyncio
import logging
import slixmpp

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class SendMsgBot(slixmpp.ClientXMPP):


    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.user = jid
        # The message we wish to send, and the JID that
        # will receive it.

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        await self.get_roster()

        print("Welcome! ", self.user)

        menu = True
        while menu == True:
            print("1. See Users Info \n2. Add Friend \n3. See 1 User Info \n4. Send Private Message \n5. Send Group Message \n6. Set Presence Message\n7. Log Out\n8. Delete Account")#9. Send notifications\n 10. Send files")
            option = input("")

            if option == "1":
                print("--- Users info ---")
            elif (option == "2"):
                print("--- Add a friend ---")
                user = input("Type email to add ")

            elif (option == "3"):
                print("--- See info of a friend ---")
                user = input("Type email to add ")
            elif (option == "4"):
                await self.get_roster()
                
                user = input("Type email to send message: ")
                message = input("Message: ")

                self.send_message(mto=user,
                                mbody=message,
                                mtype='chat')
                self.disconnect(wait=False)

            elif (option == "5"):
                message = input("Message: ")
            elif (option == "6"):
                newPresenceMsg = input("Type new presence message: ")
            elif (option == "7"):
                print("Have a nice day! :D")
                menu = False
                self.disconnect()
            elif (option == "8"):
                print("Deleting current account...")
            else: 
                print("Try another option!")
        

if __name__ == '__main__':



    menuUserLogOut = True

    while menuUserLogOut:

        print("1. Login \n2. Create User")
        option = input("")

        if option == "1":
            print("--- Log In ---")
            email = input("Email: ")
            password = input("Password: ")

            # Setup the EchoBot and register plugins. Note that while plugins may
            # have interdependencies, the order in which you register them does
            # not matter.
            logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
            xmpp = SendMsgBot(email, password)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0199') # XMPP Ping

            # Connect to the XMPP server and start processing XMPP stanzas.
            xmpp.connect()
            xmpp.process(forever=False)
        elif (option == "2"):
            pass
        else:
            print("Try another option!")
            

