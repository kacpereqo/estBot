import discord
import logging
import os
import json
import traceback
from discord.ext import commands

# Definitions
log = logging.getLogger(__name__)
config = json.loads(open('settings/config.json').read())
extensions = [x.replace('.py', '') for x in os.listdir('cogs') if x.endswith('.py')]
path = config['cogs_path']
bot = commands.Bot(command_prefix=config['prefix'])
bot.remove_command('help')

print('Extensiones disponibles: ')
print(extensions)
print()


@bot.command()
async def load(ctx, extension):
    """Load an extension."""
    try:
        bot.load_extension(path + '.' + extension)
        print('Loaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be loaded. [{}]'.format(extension, error))


@bot.command()
async def unload(ctx, extension):
    """Unload an extension."""
    try:
        bot.unload_extension(path + '.' + extension)
        print('Unloaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be unloaded. [{}]'.format(extension, error))


# When BOT is ready
@bot.event
async def on_ready():
    try:
        await load_cogs()
        activity = discord.Game(name="EST BOT | " + config['version'])
        await bot.change_presence(status=discord.Status.online, activity=activity)
        print(f'Bot logged in as {bot.user.name} with ID: {bot.user.id}')
        print('------')
        print('Bot is logged in successfully. Running on servers: ' + str(len(bot.guilds)))
        for s in bot.guilds:
            print(" - %s (%s) \n" % (s.name, s.id))
        print("Bot Ready!")
    except Exception as e:
        print(e)


async def load_cogs():
    """Load automatically all cogs found on folder"""
    for extension in extensions:
        try:
            print('Loading {}...'.format(extension))
            bot.load_extension(path + '.' + extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))
            traceback.print_exc()


def main():
    logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    main()
    print("Starting bot...")

    bot.run(config['token'])
