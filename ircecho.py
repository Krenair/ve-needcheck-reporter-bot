# Quick and ugly script to echo something to a given IRC channel
# Alex Monk, 2014-07-22

from socket import socket, AF_INET, SOCK_STREAM

def ircecho(nick, channel, message, host = "chat.freenode.net", port = 6667):
	s = socket(AF_INET, SOCK_STREAM)
	s.connect((host, port))
	f = s.makefile()

	def readLineWithoutServername(f):
		l = f.readline().strip()
		print(l)
		return l[l.find(" ") + 1:]

	def send(s, text):
		s.send(text + "\r\n")
		print("> " + text)

	while True:
		line = readLineWithoutServername(f)
		if line == "NOTICE * :*** No Ident response" or line == "NOTICE * :*** Got Ident response":
			send(s, "user " + nick + " 0 0 :" + nick)
			send(s, "nick " + nick)
			break

	while True:
		line = readLineWithoutServername(f)
		if line == "376 " + nick + " :End of /MOTD command.":
			send(s, "join " + channel)
			break
		elif line == "433 * " + nick + " :Nickname is already in use.":
			nick += "_"
			send(s, "nick " + nick)

	while True:
		line = readLineWithoutServername(f)
		if line == "366 " + nick + " " + channel + " :End of /NAMES list.":
			for messageLine in message.splitlines():
				send(s, "privmsg " + channel + " :" + messageLine)
			send(s, "quit :Done")
			s.close()
			break
