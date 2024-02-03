import discord
from discord.ext import commands
from bot_token import TOKEN
import json
import asyncio
import os

os.environ['GIT_PYTHON_REFRESH'] = 'quiet'

# Specify the path to the Git executable (either git-bash or git-cmd)
git_executable_path = '/usr/bin/git'  # or git-cmd.exe

# Set the GIT_PYTHON_GIT_EXECUTABLE environment variable
os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = git_executable_path

import git
import re

# Discord Bot Token
# Bot Prefix for Commands
BOT_PREFIX = '/'

# Define Discord Intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

# Initialize the Bot
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

#########################
### Website Function ####
#########################

# Initialize the Discord bot with intents
bot = commands.Bot(command_prefix='/', intents=intents)

# Set up a Git repository
repo = git.Repo('/home/pi/Desktop/tnscc-bot/code-club')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='updateevent')
async def updateevent(ctx, event_link: str):
    # Check if the user has permission to run the command
    if ctx.author.guild_permissions.administrator:
        # Update the HTML file with the new event link
        try:
            html_file_path = '/home/pi/Desktop/tnscc-bot/code-club/events.html'
            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                # Update the link in HTML content
                # Updated regular expression for both href and meta tags
            updated_content = re.sub(
                r'(href=")https://narwhalnation.newschool.edu/event/\d+(")'
                r'|'
                r'(content="0; url=)https://narwhalnation.newschool.edu/event/\d+(")',
                fr'\1https://narwhalnation.newschool.edu/event/{event_link}\2',
                html_content
            )



            
            # Check if the content has actually changed
            if updated_content != html_content:
                with open(html_file_path, 'w', encoding='utf-8') as file:
                    file.write(updated_content)

                # Git pull to ensure the repository is up to date
                repo.remotes.origin.pull()

                # Git operations (add, commit, push)
                repo.git.add(A=True)
                repo.git.commit(m=f'Updated event link: {event_link}')
                repo.git.push()

                await ctx.send('Event link updated and changes pushed to the repository.')
            else:
                await ctx.send('No changes detected in the HTML file.')
        except Exception as e:
            print(f'Error updating HTML file: {e}')
            await ctx.send('Error updating HTML file.')
    else:
        await ctx.send("You don't have permission to use this command.")

# Run the bot
bot.run(TOKEN)
