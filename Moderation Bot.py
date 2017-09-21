import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import random
import os
import sys
import time


Client = discord.Client()
bot_prefix= "¬"
client = commands.Bot(command_prefix=bot_prefix)

@client.event
async def on_ready():
    print("Bot Online")
    print("name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))

@client.command(pass_context=True)
async def rule1(ctx):
        """displays rule 1"""
        await client.say("Do not have a name of all special charaters!")

@client.command(pass_context = True)
async def dm(ctx, member : discord.Member = None, *, message):
    await client.send_message(member, message)
    await client.say("I have sent a messege to"(member))



@client.command()
async def leave(server_id):
    server = client.get_server(server_id)
    await client.leave_server(server)

@client.command(pass_context = True, no_pm = True)
async def serverid(ctx, *, member = discord.Member):
    embed = (ctx.message.author.mention + ", ID of this server is:** " + ctx.message.channel.server.id + "**")
    await client.say(embed)


@client.command(pass_context=True)
async def flip(ctx):
    choice = random.randint(1,2)
    if choice == 1:
        await client.say("Tails")
    if choice == 2:
        await client.say("Heads")

@client.command(pass_context = True)
async def night(ctx):
    await client.say("Night "+ctx.message.author.mention)

@client.command(pass_context=True)
async def rule2(ctx):
        await client.say("Treat Everyone with Respect")

@client.command(pass_context=True)
async def creator(ctx):
        """displays the owner of the bot"""
        await client.say("@13bathz has created me!")

@client.command(pass_context = True)
async def serverinfo(ctx):
    """displays all the servers infomation"""
    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50: #Just in case there are too many roles...
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = ', '.join(roles);
    channelz = len(server.channels);
    time = str(server.created_at); time = time.split(' '); time= time[0];

    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', colour = discord.Color.dark_purple());
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = '__Owner__', value = str(server.owner) + '\n' + server.owner.id);
    join.add_field(name = '__ID__', value = str(server.id))
    join.add_field(name = '__Member Count__', value = str(server.member_count));
    join.add_field(name = '__Text/Voice Channels__', value = str(channelz));
    join.add_field(name = '__Roles (%s)__'%str(role_length), value = roles);
    join.set_footer(text ='Created: %s'%time);

    return await client.say(embed = join);



@client.command(pass_context=True)
async def exit(ctx):
    close()

@client.command(pass_context=True)
async def cr(ctx):
        """displayers the copy right info"""
        await client.say("This bot has only been made to the service Elysium-Networks if you are found using this bot actions will be implemented!")

@client.command(pass_context=True)
async def rule3(ctx):
        """Displays rule 3 """
        await client.say("Do not spam any of the text channel if you do you may be muted")


@client.command(pass_context = True)
async def banlist(ctx):
    """Gets all the bans on the discord"""
    x = await client.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "Banned Members", description = x, color = 0xFF0000)
    return await client.say(embed = embed)

@client.command(pass_context = True)
async def clear(ctx, number : int):
    if not ctx.message.author.server_permissions.kick_members:
        return await client.say(ctx.message.author.mention + "You have insufficient permissions to use this command!")
    else:
        mgs = []
        async for x in client.logs_from(ctx.message.channel, limit = number + 1):
            mgs.append(x)
        await client.delete_messages(mgs)
        number = str(number)
        await client.say("Deleted " + number + " messages!")

@client.command(pass_context=True, no_pm=True)
async def kick(ctx, *, member : discord.Member = None):###############
    """Kicks a player"""
    if not ctx.message.author.server_permissions.kick_members:
        return
 
    if not member:
        return await client.say(ctx.message.author.mention + "Specify a user to kick!")
    try:
        await client.kick(member)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            return await client.say(":x: Privilege too low!")
    return await client.say("**%s** has been kicked !"%member.name)
    return await client.say("By: %s"%ctx.message.author.mention)



@client.command(pass_context=True, no_pm=True)
async def ban(ctx, *, member : discord.Member = None):###############
    """bans a player also do ¬banlist to make sure the player was banned"""
    if not ctx.message.author.server_permissions.ban_members:
        return
 
    if not member:
        return await client.say(ctx.message.author.mention + "Specify a user to kick!")
    try:
        await client.ban(member)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            return await client.say(":x: Privilege too low!")
    return await client.say("**%s** has been banned !"%member.name)
    return await client.say("By: %s"%ctx.message.author.mention)


word_blacklist = ["string1", "string2", "string3"]

@client.event
async def on_message(message):
    for bleep in word_blacklist:
        if bleep in str(message):
            await client.say("Please do not swear!")
            await client.delete_message(message)
    await client.process_commands(message)


@client.command()
async def ping():
    """Ping to the server or servers"""
    pingtime = time.time()
    pingms = await client.say("Pinging...")
    ping = time.time() - pingtime
    await client.edit_message(pingms, "Pong! The ping time is `%.01f seconds`" % ping)

@client.command(pass_context = True)
async def mute(ctx, *, member : discord.Member):
    """Mutes a player"""
    if not ctx.message.author.server_permissions.manage_messages:
        return
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    await client.edit_channel_permissions(ctx.message.channel, member, overwrite)
    await client.say("**%s** has been muted!"%member.mention)

@client.command(pass_context = True)
async def unmute(ctx, *, member : discord.Member):
    """unmutes a player"""
    if not ctx.message.author.server_permissions.manage_messages:
        return
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = True
    await client.edit_channel_permissions(ctx.message.channel, member, overwrite)
    await client.say("**%s** has been unmuted!"%member.mention)


@client.command(pass_context=True, no_pm=True)
async def unban(ctx, *, user : discord.User = None):###############
    """unbans a player"""
    if not ctx.message.author.server_permissions.ban_members:
        return
 
    if not user:
        return await client.say(ctx.message.author.mention + "Specify a user to kick!")
    try:
        await client.unban(user)
    except Exception as e:
        if 'Privilege is too low' in str(e):
            return await client.say(":x: Privilege too low!")
    return await client.say("**%s** has been unbanned !"%user.name)
    return await client.say("By: %s"%ctx.message.author.mention)



client.run("MzU2Mzk5Mzk0NjA3NTk1NTIy.DJayUA.LhhkyVSShqHFZt1hQfDxuiKwiaM")

try:
    #client.loop.create_task(background_task())
    client.run(token)
except:
    print('Error detected. Restarting in 15 seconds.')
    time.sleep(15)

    os.execl(sys.executable, sys.executable, *sys.argv)

pause
