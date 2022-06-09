from discord.ext import commands
import discord
import os

import card

intents = discord.Intents(guilds=True, members=True, messages=True)
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


def is_from_command_channel(ctx):
	return ctx.message.channel.name == os.environ['COMMAND_CHANNEL']


def is_from_privileged_member(ctx):
	for role in ctx.author.roles:
		if is_privileged_role(role):
			return True
	return False


def is_privileged_role(role):
	return role and role.name == os.environ['ROLE']


def find_new_role(before_roles, after_roles):
	if len(before_roles) < len(after_roles):
		return next(r for r in after_roles if r not in before_roles)
	return None


async def send_card(member):
	for channel in member.guild.channels:
		if channel.name == os.environ['CARD_CHANNEL']:
			if callable(getattr(channel, 'send', None)):
				card_fp = await card.make(member.name)
				card_file = discord.File(card_fp, 'image.png')
				await channel.send(member.mention, file=card_file)


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
@commands.check(is_from_privileged_member)
async def welcome(ctx):
	await send_card(ctx.author)


@bot.event
async def on_member_update(before, after):
	new_role = find_new_role(before.roles, after.roles)
	if is_privileged_role(new_role):
		await send_card(after)


def run():
	bot.run(os.environ['TOKEN'])


if __name__ == '__main__':
	run()
