import irc.bot
import irc.strings
import queue

class MyIRCBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, command_queue = None, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.command_queue = command_queue
        self.channel = channel

    def monitor_Queue(self):
        while True:
            self.reactor.process_once(timeout=0.2)
            try:
                command = self.command_queue.get_nowait()
                self.handle_command(command)
            except queue.Empty:
                continue

    def handle_command(self, command):
        if command['action'] == "attack":
            self.on_attack(command['message'])

        elif command['action'] == "hit":
            self.on_hit()

    def on_nicknameinuse(self, connection, event):
        connection.nick(connection.get_nickname() + "_")

    def on_welcome(self, connection, event):
        connection.join(self.channel)
        self.monitor_Queue()

    def on_privmsg(self, connection, event):
        self.do_command(event)

    def on_pubmsg(self, connection, event):
        self.do_command(event)
        return

    def on_hit(self):
        self.connection.privmsg(self.channel, self.connection.nickname + "Hit")

    def on_attack(self, target):
        self.connection.privmsg(self.channel, "Attacked " + str(target))

    def do_command(self, event):
        nick = event.source.nick
        connection = self.connection
                                            #Add whatever logic you want to have happen based on event messages here

        # print(event.arguments[0])          #Print event messages for testing

def start_bot(botName, server, command_queue):
    bot = MyIRCBot("#DroneCompetition", botName, server, command_queue = command_queue)
    bot.start()