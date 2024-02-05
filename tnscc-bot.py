import discord
from discord.ext import commands
from bot_token import TOKEN
import git
import traceback
from bs4 import BeautifulSoup

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

            # Read HTML content
            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Use BeautifulSoup to modify the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Update meta tag
            meta_tag = soup.find('meta', {'http-equiv': 'refresh'})
            if meta_tag:
                meta_tag['content'] = f'0; url={event_link}'

            # Update anchor tag
            anchor_tag = soup.find('a', {'class': 'blink'})
            if anchor_tag:
                anchor_tag['href'] = event_link

            # Write the updated content back to the HTML file
            with open(html_file_path, 'w', encoding='utf-8') as file:
                file.write(str(soup))

            # Git pull to ensure the repository is up to date
            repo.remotes.origin.pull()

            # Git operations (add, commit, push)
            repo.git.add(A=True)
            repo.git.commit(m=f'Updated event link: {event_link}')
            repo.git.push()

            await ctx.send('Event link updated and changes pushed to the repository.')
        except Exception as e:
            print(f'Error updating HTML file: {e}')
            traceback.print_exc()
            await ctx.send('Error updating HTML file.')
    else:
        await ctx.send("You don't have permission to use this command.")

@bot.command(name='help')
async def help(ctx):
    # Display help message
    help_message = "Command(s):\n\n" \
                   "/updateevent (event link) - Update the event link in the HTML file.\n"
    await ctx.send(help_message)

# Run the bot
bot.run(TOKEN)