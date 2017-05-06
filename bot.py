import discord
import asyncio
import random
import bikdip
import starfoxquotes
import ggl

client = discord.Client()
messageLog = list()
last_author = None

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
@asyncio.coroutine
def on_message(message):
    global last_author
    if message.author != client.user:
        notified = False
        for r in message.author.roles:
            if r.permissions.administrator or r.name == 'Moderator':
                print("New message: " + message.content + " (posted by " + message.author.display_name + "#" + message.author.id + ")")
                notified = True
                if message.content.startswith('!kick'):
                    msgparts = message.content.split(" ",1)
                    for m in client.get_all_members():
                        if m.name == msgparts[1]:
                            member = m
                            yield from client.kick(member)
                            break
                    yield from client.send_message(message.channel, "Could not find member " + msgparts[1] + ".")
                    break
                elif message.content.startswith('!mute'):
                    msgparts = message.content.split(" ",1)
                    timeout_role = None
                    muted = False
                    for r in client.get_server(message.author.server.id).roles:
                        if str(r) == 'Timeout':
                            timeout_role = r
                            break
                    for m in client.get_all_members():
                        if m.name == msgparts[1]:
                            if timeout_role not in m.roles:
                                yield from client.add_roles(m, timeout_role)
                            print("Muted " + msgparts[1])
                            muted = True
                            break
                        else:
                            continue
                    if not muted:
                        yield from client.send_message(message.channel, "Could not find member " + msgparts[1] + ".")
                    break
                elif message.content.startswith('!unmute'):
                    msgparts = message.content.split(" ",1)
                    timeout_role = None
                    unmuted = False
                    for r in client.get_server(message.author.server.id).roles:
                        if str(r) == 'Timeout':
                            timeout_role = r
                            break
                    for m in client.get_all_members():
                        if m.name == msgparts[1]:
                            if timeout_role in m.roles:
                                yield from client.remove_roles(m, timeout_role)
                            print("Unmuted " + msgparts[1])
                            unmuted = True
                            break
                        else:
                            continue
                    if not unmuted:
                        yield from client.send_message(message.channel, "Could not find member " + msgparts[1] + ".")
                    break
        if message.channel.name == "slippy-land" or message.channel.name == "bot-training-grounds":
            if not notified:
                print("New message: " + message.content + " (posted by " + message.author.display_name + "#" + message.author.id + ")")
            if message.content.startswith('!ping'):
                print("Sending message... 'Pong!'")
                yield from client.send_message(message.channel, "Pong!")
            elif message.content.startswith('!help'):
                yield from client.send_message(message.channel, "\
Admin Commands: \n\
**!mute** <member name> - Puts the 'timeout' role on the member, so that they cannot speak.\n\
**!unmute** <member name> - Removes the 'timeout' role from the member, if they have it.\n\
**!kick** <member name> - Kicks the member from the server.\n\
Commands: \n\
**!ping** - Pong! \n\
**!starfox64** - Posts a random quote from Star Fox 64. \n\
**!randnum** <min> <max> - Generates a random between <min> and <max> \n\
**!dice** - Rolls a six-sided die. \n\
**!d12** - Rolls a twelve-sided die. \n\
**!d20** - Rolls a twenty-sided die. \n\
**!whoops** - Deletes the last message sent by me\n\
**!video** <search-query>... - Grabs a video off of youtube using the query.\n\
**!news** <search-query>... - Grabs a news article off of Google using the query.\n\
**!whatwoulditbelikeif** - House.\n")
            elif message.content.startswith('!randnum'):
                msgparts = message.content.split(" ")
                if len(msgparts) >= 3:
                    min = float(msgparts[1])
                    max = float(msgparts[2])
                    if min >= max:
                        lastmsg = yield from client.send_message(message.channel, "Usage: !randnum <min> <max>")
                    else:
                        num = random.randrange(min,max+1,1)
                        lastmsg = yield from client.send_message(message.channel, str(num))
                else:
                    lastmsg = yield from client.send_message(message.channel, "Usage: !randnum <min> <max>")
                if len(messageLog) > 8:
                    messageLog.clear()
                messageLog.append(lastmsg)
            elif message.content.startswith('!dice'):
                username = message.author.display_name
                num = random.randrange(1, 7)
                article = 'a'
                if num == 8:
                    article = 'an'
                lastmsg = yield from client.send_message(
                    message.channel, "{user} rolled {a} {n}.".format(user=username,a=article,n=num))
                if len(messageLog) > 8:
                    messageLog.clear()
                messageLog.append(lastmsg)
            elif message.content.startswith('!d12'):
                username = message.author.display_name
                num = random.randrange(1, 13)
                article = 'a'
                if num == 8 or num == 11:
                    article = 'an'
                lastmsg = yield from client.send_message(
                    message.channel, "{user} rolled {a} {n}.".format(user=username,a=article,n=num))
                if len(messageLog) > 8:
                    messageLog.clear()
                messageLog.append(lastmsg)
            elif message.content.startswith('!d20'):
                username = message.author.display_name
                num = random.randrange(1, 21)
                article = 'a'
                if num == 8:
                    article = 'an'
                lastmsg = yield from client.send_message(
                    message.channel, "{user} rolled {a} {n}.".format(user=username,a=article,n=num))
                if len(messageLog) > 8:
                    messageLog.clear()
                messageLog.append(lastmsg)
            elif message.content.startswith('!video'):
                #lastmsg = yield from client.send_message(message.channel, "Unimplemented.")
                msgparts = message.content.split(" ",1)
                if len(msgparts) >= 2:
                    q = msgparts[1]
                    url = ggl.fetch_video(q)
                    lastmsg = yield from client.send_message(message.channel, url)
                else:
                    lastmsg = yield from client.send_message(message.channel, "Usage: !video <query>")
                if len(messageLog) > 8:
                    messageLog.clear()
                messageLog.append(lastmsg)
            elif message.content.startswith('!news'):
                #lastmsg = yield from client.send_message(message.channel, "Unimplemented.")
                msgparts = message.content.split(" ",1)
                if len(msgparts) >= 2:
                    q = msgparts[1]
                    url = ggl.fetch_news(q)
                    lastmsg = yield from client.send_message(message.channel, url)
                else:
                    lastmsg = yield from client.send_message(message.channel, "Usage: !news <query>")
                if len(messageLog) > 8:
                    messageLog.clear()
                messageLog.append(lastmsg)
            elif message.content.startswith('!whoops'):
                if last_author is not None and message.author == last_author:
                    yield from client.delete_message(messageLog[-1])
            elif message.content.startswith('!cl'):
                if message.author.id == "133070028391186432":
                    for m in messageLog:
                        yield from client.delete_message(m)
                    messageLog.clear()
            elif message.content.startswith('!whatwoulditbelikeif'):
                lastmsg = yield from client.send_message(message.channel, "http://www.whatwoulditbelikeif.house")
                if len(messageLog) > 8:
                    messageLog.clear()
                messageLog.append(lastmsg)
            elif message.content.startswith('!starfox64'):
                num = random.randrange(0, len(starfoxquotes.quotes) - 1, 1)
                lastmsg = yield from client.send_message(message.channel, starfoxquotes.quotes[num])
                if len(messageLog) > 8:
                    messageLog.clear()
                messageLog.append(lastmsg)
            last_author = message.author
        elif message.channel.name == "kekistan":
            if message.content.startswith('!video'):
                #lastmsg = yield from client.send_message(message.channel, "Unimplemented.")
                msgparts = message.content.split(" ",1)
                if len(msgparts) >= 2:
                    q = msgparts[1]
                    url = ggl.fetch_video(q)
                    lastmsg = yield from client.send_message(message.channel, url)
                else:
                    lastmsg = yield from client.send_message(message.channel, "Usage: !video <query>")
                if len(messageLog) > 8:
                    messageLog.clear()
                messageLog.append(lastmsg)
            elif message.content.startswith('!news'):
                #lastmsg = yield from client.send_message(message.channel, "Unimplemented.")
                msgparts = message.content.split(" ",1)
                if len(msgparts) >= 2:
                    q = msgparts[1]
                    url = ggl.fetch_news(q)
                    lastmsg = yield from client.send_message(message.channel, url)
                else:
                    lastmsg = yield from client.send_message(message.channel, "Usage: !news <query>")
                if len(messageLog) > 8:
                    messageLog.clear()
                messageLog.append(lastmsg)
            elif message.content.startswith('!ping'):
                print("Sending message... 'Pong!'")
                yield from client.send_message(message.channel, "Pong!")
            elif message.content.startswith('!help'):
                yield from client.send_message(message.channel, "\
Admin Commands: \n\
**!mute** <member name> - Puts the 'timeout' role on the member, so that they cannot speak.\n\
**!unmute** <member name> - Removes the 'timeout' role from the member, if they have it.\n\
**!kick** <member name> - Kicks the member from the server.\n\
Commands: \n\
**!ping** - Pong! \n\
**!video** <search-query>... - Grabs a video off of youtube using the query.\n\
**!news** <search-query>... - Grabs a news article off of Google using the query.\n\
")
    else:
        pass

client.run('YOUR_KEY_HERE')