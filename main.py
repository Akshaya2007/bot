import discord
from discord.ext import commands, tasks
import asyncio
import keep_alive
import os
import datetime
import random
from random import choice
import time
import os
import sqlite3
from discord.ext.commands import CommandOnCooldown, BucketType
import json
from discord import asset
import pandas as pd
import openpyxl
from openpyxl import Workbook

#main code starts here!
intents = discord.Intents.all()
intents.presences = True
intents.members = True
intents.message_content = True


bot = commands.Bot(command_prefix='%', intents=intents)

# Remove the default help command
bot.remove_command('help')

@bot.group(invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(
    title="Help",
    description="Type %help <command> for more info on a command.",
    color=ctx.author.color)
  em.add_field(
    name="Moderation",
    value=
    "kick , ban , unban , clear , addrole , removerole , unlock , lock , massrole , rename"
  )
  em.add_field(name="Fun", value="ping")
  em.add_field(name="Games", value="truth, dare")
  await ctx.reply(embed=em)


@help.command()
async def kick(ctx):

  em = discord.Embed(title="Kick",
                     description="Kicks a member from the guild.",
                     color=ctx.author.color)
  em.add_field(name="**Syntax**", value="%kick <member> [reason]")
  await ctx.reply(embed=em)


@help.command()
async def ban(ctx):

  em = discord.Embed(title="Ban",
                     description="Bans a member from the guild.",
                     color=ctx.author.color)
  em.add_field(name="**Syntax**", value="%ban <member> [reason]")
  await ctx.reply(embed=em)


@help.command()
async def clear(ctx):

  em = discord.Embed(title="Clear",
                     description="Clears messages.",
                     color=ctx.author.color)
  em.add_field(name="**Syntax**", value="%clear <amount>")
  await ctx.reply(embed=em)


@help.command()
async def addrole(ctx):

  em = discord.Embed(title="Addrole",
                     description="Adds a role to a member of the guild. ",
                     color=ctx.author.color)
  em.add_field(name="**Syntax**",
               value="%addrole <membermention> <rolename or mention>")
  await ctx.reply(embed=em)


@help.command()
async def removerole(ctx):

  em = discord.Embed(title="Removerole",
                     description="Removed a role from a member of the giuld. ",
                     color=ctx.author.color)
  em.add_field(name="**Syntax**",
               value="%removerole <membermention> <rolename or mention>")
  await ctx.reply(embed=em)


@help.command()
async def massrole(ctx):

  em = discord.Embed(
    title="Massrole",
    description=
    "Gives a role to many users at same time. Might take some seconds to give role. ",
    color=ctx.author.color)
  em.add_field(name="**Syntax**", value="%massrole <role> <members> ")
  await ctx.reply(embed=em)


@help.command()
async def lock(ctx):

  em = discord.Embed(title="Lock",
                     description="Locks a channel. ",
                     color=ctx.author.color)
  em.add_field(name="**Syntax**", value="%lock")
  await ctx.reply(embed=em)


@help.command()
async def unlock(ctx):

  em = discord.Embed(title="Unlock",
                     description="Unlocks a channel. ",
                     color=ctx.author.color)
  em.add_field(name="**Syntax**", value="%unlock")
  await ctx.reply(embed=em)


@help.command()
async def unban(ctx):

  em = discord.Embed(title="Unban",
                     description="Unbans a member",
                     color=ctx.author.color)
  em.add_field(name="**Syntax**", value="%unban <Username>#<discriminator>")
  await ctx.reply(embed=em)

@help.command()
async def ping(ctx):

  em = discord.Embed(title="Ping",
                     description="Ping....Pong!",
                     color=ctx.author.color)
  em.add_field(name="**Syntax**", value="%ping")
  await ctx.reply(embed=em)


@help.command()
async def rename(ctx):

  em = discord.Embed(title="Rename",
                     description="Renames a member",
                     color=ctx.author.color)
  em.add_field(name="**Syntax**", value="%rename <mention member> <newname> ")
  await ctx.reply(embed=em)


@help.command()
async def truth(ctx):

  em = discord.Embed(title="Truth",
                     description="Sends a truth",
                     color=ctx.author.color)
  em.add_field(name="**Syntax**", value="%truth")
  await ctx.reply(embed=em)


@help.command()
async def dare(ctx):

  em = discord.Embed(title="Dare",
                     description="Sends a dare",
                     color=ctx.author.color)
  em.add_field(name="**Syntax**", value="%dare")
  await ctx.reply(embed=em)


#whatever code you want to add, do it after this line


@bot.event
async def on_ready():

  await bot.change_presence(activity=discord.Game(name="%help"))

  print("Ready")


async def ch_pr():
  await bot.wait_until_ready()

  statuses = ["%help"]

  while not bot.is_closed():
    status = random.choice(statuses)
    await bot.change_presence(activity=discord.Game(name=status))

    await asyncio.sleep(60)
    bot.loop.create_task(ch_pr())


@bot.command()
@commands.has_permissions(kick_members=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def kick(ctx, member: discord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.reply(f"{member.mention} has been kicked!")


@bot.command()
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def ban(ctx, member: discord.Member, *, reason=None):
  await member.ban(reason=reason)
  await ctx.reply(f"{member.mention} has been banned!")


@bot.command()
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.reply(f"Unbanned {user.mention}!")


@bot.command(aliases=['ar'])
@commands.cooldown(1, 15, commands.BucketType.user)
async def addrole(
  ctx,
  user: discord.Member,
  role: discord.Role,
):
  if ctx.author.guild_permissions.manage_roles:
    await user.add_roles(role)
    await ctx.reply(f"Successfully given the role to {user.mention}.")


@bot.command(aliases=['rr'])
@commands.cooldown(1, 15, commands.BucketType.user)
async def removerole(ctx, user: discord.Member, role: discord.Role):
  if ctx.author.guild_permissions.manage_roles:
    await user.remove_roles(role)
    await ctx.reply(f"Successfully removed the role from {user.mention}")


@bot.command(aliases=['madd'])
@commands.cooldown(1, 60, commands.BucketType.user)
async def massrole(ctx, role: discord.Role,
                   members: commands.Greedy[discord.Member]):
  for m in members:
    if ctx.author.guild_permissions.manage_roles:
      await m.add_roles(role)
      await asyncio.sleep(1)  # You don't want to get ratelimited!
  await ctx.reply("Given role to mentioned members!")


@bot.command(aliases=['purge', 'delete', 'clean'])
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=2):
  await ctx.channel.purge(limit=amount)
  await ctx.reply("Cleared the messages!")


@bot.command(aliases=['l'])
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel = None):
  overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
  overwrite.send_messages = False
  await ctx.channel.set_permissions(ctx.guild.default_role,
                                    overwrite=overwrite)
  await ctx.reply('Channel locked.')


@bot.command(aliases=['ul'])
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel = None):
  overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
  overwrite.send_messages = True
  await ctx.channel.set_permissions(ctx.guild.default_role,
                                    overwrite=overwrite)
  await ctx.reply('Channel unlocked.')


def convert(time):
  pos = ["s", "min", "hr", "d"]

  time_dict = {"s": 1, "min": 60, "hr": 3600, "d": 3600 * 24}

  unit = time[-1]

  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2

  return val * time_dict[unit]


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def ping(ctx):
  await ctx.reply(f"Pong! {round(client.latency * 1000)}ms")


@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def rename(ctx, user: discord.Member, *, newName=""):
  if ctx.message.author.guild_permissions.manage_nicknames:
    renameduser = user.nick
    await user.edit(nick=newName)
    await ctx.reply("Renamed the user!")


@bot.event
async def on_command_error(ctx, error):
  await ctx.reply(f"An error occured: {str(error)}")

# Set the role name and message to send
ROLE_NAME = '50K CONFIRMED'
MESSAGE = 'Hi there! Thank you for registering your team in our Battle of Champions S2. Hope you have a great tournament with your team. We have another league going on in our server. Check it out <#1099912872529776682>.'
IMAGE_URL = 'https://media.discordapp.net/attachments/899942122944360468/1102519829723873340/TOURNAMENT_POSTER.png?width=606&height=606'

@bot.event
async def on_member_update(before, after):
    # Check if the user was assigned the specified role
    if ROLE_NAME in [r.name for r in after.roles]:
        # Get the user's DM channel
        dm_channel = await after.create_dm()

         # Create the embed
        embed = discord.Embed(title='REGISTRATION SUCCESSFUL', description=MESSAGE, color=0xFF0000)
        embed.set_image(url=IMAGE_URL)
        embed.set_footer(text="This Server is Owned & Managed By Dastrangers Management©.", icon_url="https://media.discordapp.net/attachments/899942122944360468/1110864825585766420/Logo.png?width=662&height=662")

        # Send the embed
        await dm_channel.send(embed=embed)



@bot.event
async def on_message(message):

    # Define a dictionary mapping channel IDs to role IDs
    channel_roles = {
        1110861056588398663: 1102176716295782492,  # Channel ID : Role ID
    }

    # Check if the message was sent in any of the channels you want to monitor
    if message.channel.id in channel_roles:
        # Get the role object for the specific role you want to mention
        role = message.guild.get_role(channel_roles[message.channel.id])

        # Loop through all the members in the server with the specific role and send them the message
        for member in message.guild.members:
            if role in member.roles:
                try:
                    embed = discord.Embed(title="NOTICE",
                                      description=message.content,
                                          color=0xff0000)
                    embed.set_thumbnail(url="https://media.discordapp.net/attachments/899942122944360468/1110864825585766420/Logo.png?width=662&height=662")
                    embed.set_footer(text="This Server is Owned & Managed By Dastrangers Management©.", icon_url="https://media.discordapp.net/attachments/899942122944360468/1110864825585766420/Logo.png?width=662&height=662")
                    await member.send(embed=embed)
                except discord.errors.Forbidden:
                    print(f"Could not send message to {member.name}")
                  

keep_alive.keep_alive()
token = os.environ.get("TOKEN")
# Run the client on the server
bot.run("TOKEN")
