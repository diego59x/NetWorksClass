# Instant messaging app using xmpp 
# UVG
# Diego Alvarez 19498
# Documentation: 
# https://slixmpp.readthedocs.io/en/latest/
# https://oriolrius.cat/wp-content/uploads/2009/10/Oreilly.XMPP.The.Definitive.Guide.May.2009.pdf
import asyncio
import logging
import slixmpp
import xmpp
from slixmpp.xmlstream import ET
from slixmpp.exceptions import IqError, IqTimeout

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class XMPPChat(slixmpp.ClientXMPP):


    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.user = jid
        self.add_event_handler("session_start", self.start)


    def deleteUser(self):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['id'] = 'delete-user-1'
        resp['from'] = self.boundjid
        resp['to'] = 'alumchat.fun'
        query = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        resp.append(query)
        try:
            resp.send()
            print("User Deleted")

        except IqError as err:
            print("Delete Process Failed")
            self.disconnect()

        except IqTimeout:
            print("Session Timeout")
            self.disconnect()

    def getContacts(self, infoContact):
        

        contacts = self.client_roster.groups()

        for contact in contacts:
            print("\n\n------------ Friends --------------")

            for jid in contacts[contact]:
                name = self.client_roster[jid]['name']

                if name == '':
                    name = jid
                # We not show our user
                if name == self.user:
                    continue

                if (infoContact != 'SeeAll' and infoContact == name):
                    self.seeConnections(name, jid)
                elif (infoContact == 'SeeAll'):
                    self.seeConnections(name, jid)     

    def seeConnections(self, name, jid):
        connections = self.client_roster.presence(jid)
        for res, pres in connections.items():
            # 'res' is the id of their device
            show = 'available'
            # Default value available
        
            print('Name: %s (%s)' % (name, show))
            # Users with a different status
            if pres['status']:
                print('%s' % pres['status'])

    def notificationMessage(self, emisor, state):
        message = self.Message()
        message["chat_state"] = state
        message["to"] = emisor

        message.send()

    async def start(self, event):
        self.send_presence()

        print("Welcome! ", self.user)
        await self.get_roster()
        # 2 4 5 6 8 9
        menu = True
        while menu == True:
            print("1. See Users Info \n2. Add Friend \n3. See 1 User Info \n4. Send Private Message \n5. Send Group Message \n6. Set Presence Message\n7. Log Out\n8. Delete Account")#9. Send notifications\n 10. Send files")
            option = input("")

            if option == "1":
                self.getContacts('SeeAll')

            elif (option == "2"):
                print("--- Add a friend ---")
                user = input("Type email to add ")

            elif (option == "3"):
                print("--- See info of a friend ---")
                user = input("Type email to see ")
                self.getContacts(user)

            elif (option == "4"):

                user = input("Type email to send message: ")
                message = input("Message: ")

                self.send_message(mto=user, mbody=message, mtype='chat')

                self.notificationMessage(user, 'paused')

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
                menu = False
                self.deleteUser()
            else: 
                print("Try another option!")
        

if __name__ == '__main__':

    menuUserLogOut = True

    while menuUserLogOut:

        print("Welcome! Choose an option \n1. Login \n2. Create User\n3. Close")
        option = input("")

        if option == "1":
            print("--- Log In ---")
            email = input("Email: ")
            password = input("Password: ")

            # email = "alvarez@alumchat.fun"
            # password = "swais"

            logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
            login = XMPPChat(email, password)
            login.register_plugin('xep_0030') # Service Discovery
            login.register_plugin('xep_0199') # XMPP Ping
            login.register_plugin("xep_0085")
            login.register_plugin("xep_0133")


            # Connect to the XMPP server and start processing XMPP stanzas.
            login.connect(disable_starttls=True)
            login.process(forever=False)
        elif (option == "2"):
            email = input("Email: ")
            password = input("Password: ")

            jid = xmpp.JID(email)
            cli = xmpp.Client(jid.getDomain(), debug=[])
            cli.connect()

            if xmpp.features.register(cli, jid.getDomain(), {'username': jid.getNode(), 'password': password}):
                print("Creation Done \n--> Please login with new credentials <--")
            else:
                print("Something went wrong, try again")
        elif (option == "3"):
            print("See you later! :D")
            menuUserLogOut = False
        else:
            print("Try another option!")
        

