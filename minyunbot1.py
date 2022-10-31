from discord.ext import commands
import discord
import os
import random
import datetime
import youtube_dl
import asyncio
mainPath = "C:\\Users\\Joseph C\\Desktop\\bot\\"
intents = discord.Intents().all()
client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix = 'd!', intents = intents)
'''my id:254753871543402497'''
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
dict = {"michael": { 
                    "romantic": "\\IMG_6391.PNG"}, 
        "zoe":     {
                    ""
                   },
        "sagiri":  {
                    'sleepy': "\\sleepSagiri.jpg" 
                   }
        
        
        }
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@bot.command(name='join', help ='Plays bug in the voice channel')
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play_song', help='To play song')
async def play(ctx,url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="C:\\ffmpeg\\bin\\ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format())
    except:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    #for i in message.author.activities:
        #if i.name == "League of Legends":
            #await message.delete()
        #print("pog")
    if message.content.lower().startswith('how about a '):
        for key in dict:
            if key in message.content.lower():
                for key2 in dict[key]:
                    if key2 in message.content.lower():
                        if 'random' in message.content.lower():
                            randomImagePath = "\\" + random.choice(os.listdir(mainPath + key))
                            print (randomImagePath)
                            await message.channel.send(file=discord.File(mainPath + key + (randomImagePath)))   
                        else:
                            await message.channel.send(file=discord.File(mainPath + key + dict[key][key2]))
                    else:
                        randomImagePath = "\\" + random.choice(os.listdir(mainPath + key))
                        await message.channel.send(file=discord.File(mainPath + key + (randomImagePath)))
    if len(message.content) == 1:
        if message.content.startswith('W') or message.content.startswith('L') or message.content.startswith('?'):
            await message.add_reaction("<:weird1:953681874927120454>")
    if message.content.lower().startswith("is nahida out yet"):
        stop = datetime.datetime(2022, 11, 2, 5, 0, 0)
        now = datetime.datetime.now()
        difference = stop - now
        count_hours, rem = divmod(difference.seconds, 3600)
        count_minutes, count_seconds = divmod(rem, 60)
        await message.channel.send('Nahida comes out in '
              + str(difference.days) + " day(s) "
              + str(count_hours) + " hour(s) "
              + str(count_minutes) + " minute(s) "
              + str(count_seconds) + " second(s) "
              )
            
    await bot.process_commands(message)
    #if message.author.id == 335224420509417472 and counter % 10 == 0:
        #await message.channel.send("Happy Birthday Tracy!")
        #counter += 1
    
    #if message.author.id == 186203727307341824:
        #await message.add_reaction("😐")
    #await bot.process_commands(message)


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)
    print("poggggggggggg")
             

bot.run("")
