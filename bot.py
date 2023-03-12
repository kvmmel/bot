import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
driver = webdriver.Chrome()
intents = discord.Intents.default()
intents.message_content = True
load_dotenv()
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!', intents=intents)
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('huj'):
            with open('counter.txt', 'r') as f:
                    a = f.read(1000)
                    a = int(a)               
                    a+=1
                    a = str(a)
                    with open('counter.txt','w') as d:
                        d.write(a)
            await message.channel.send(f'Yall wrote huj {a} times')
    await client.process_commands(message)

@client.command()
async def kocham(ctx):
    await ctx.send(f'I love {ctx.author.display_name}')

@client.command()
async def ranga(ctx, nick, region):
    nick.replace(" ","%20")
    region = region.lower()
    driver.get(f"https://www.leagueofgraphs.com/pl/summoner/{region}/{nick}")
    driver.find_element(By.CLASS_NAME,"ncmp__btn").click()
    driver.implicitly_wait(60)
    element = driver.find_element(By.CLASS_NAME,"medium-24")
    location = element.location
    size = element.size
    driver.save_screenshot("pageImage.png")
    x = location['x']
    y = location['y']
    width = location['x']+size['width']
    height = location['y']+size['height']
    im = Image.open('pageImage.png')
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save('element.png')
    driver.get('https://www.google.com/')
    await ctx.send(file=discord.File("element.png"))

@client.event
async def on_message(ctx):
    if ctx.content == "!graj":
        user=ctx.author
        voice_channel=user.voice.channel
        conn = await voice_channel.connect(timeout=9999999999999999999999.9, self_deaf = True)
        if voice_channel!= None:
            source = discord.FFmpegPCMAudio(executable="ffmpeg.exe", source="")
            conn.play(source)
    elif ctx.content == "!wyjdz":
        for vc in client.voice_clients:
            if vc.guild == ctx.guild:
                await vc.disconnect()


client.run(os.getenv("DISCORD_TOKEN"))