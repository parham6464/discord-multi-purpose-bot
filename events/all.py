import datetime
from datetime import datetime
from socket import timeout
import discord
from discord.ext import commands 
from discord import File , app_commands
import asyncio
import aiohttp
from logging import getLogger
import sys
from discord.ext.commands import CommandNotFound


intents = discord.Intents.all()
intents.members = True
intents.message_content = True




class MyCog(commands.Cog):
    def __init__(self , client ) :
        self.client = client
        self.log = getLogger('client')

        
    @commands.Cog.listener()
    async def on_connect(self):
        self.log.info(f'succesfully connected')
        if '-sync' in sys.argv:
            synced_command = await self.client.tree.sync()
            self.log.info(f'synced {len(synced_command)} commands')

    @app_commands.command(name="ping")
    async def ping_command(self, interaction: discord.Interaction) -> None:
        """ /ping_command """
        embed = discord.Embed(description=f'my ping is {round(self.client.latency*1000)}ms')
        await interaction.response.send_message(embed=embed)

        
    #@commands.Cog.listener()
   # async def on_message(self,msg):
        
      #  username = msg.author.display_name
       # if msg.author == self.client.user:
       #     return
      #  if msg.content == "!new" and msg.channel.id == 1118867997281493032:  # channel !new
         #   await msg.channel.send ("به ادمین اطلاع داده شد")
           # await self.client.send_message(channel,"hiii")
        
        seasion = aiohttp.ClientSession()
        await seasion.close()
    @commands.command()
    async def black(self , ctx):
        await ctx.send ("white")

   # @commands.command()
    #async def new(self , ctx):
       # channel = self.client.get_channel(1119314021800222860)

    @commands.Cog.listener()
    async def on_command_error(self,ctx, error):
        if isinstance(error, CommandNotFound):
            return
        


    @commands.Cog.listener()
    async def on_member_join(self,member):
        try:
            guild = member.guild
            guildname = guild.name
            if guildname == 'GOLD CLUB':
                channel = self.client.get_channel(1118581819529494559) # channel welcome
                embed = discord.Embed(title=f"Welcome to the {guildname}, {member.name}!" ,description= 'به سرور پابلیک گلد کلاب خوش آمدید امیدوارم اوقات خوبی را در سرور ما داشته باشید. ', timestamp=datetime.now(),color=  0xBAA928 )
                embed.set_image(url=member.avatar.url)
                embed.set_author(name="GOLD CLUB")
                await asyncio.sleep(10)
                await channel.send(embed=embed)      
                seasion = aiohttp.ClientSession()
                await seasion.close()
                return
        except:
            
            guildname = guild.name
            if guildname == 'GOLD CLUB':
                channel = self.client.get_channel(1118581819529494559) # channel welcome
                embed = discord.Embed(title=f"Welcome to the {guildname}, {member.name}!" ,description= 'به سرور پابلیک گلد کلاب خوش آمدید امیدوارم اوقات خوبی را در سرور ما داشته باشید.' , timestamp=datetime.now(),color=  0xBAA928 )
                embed.set_image(url='https://media.discordapp.net/attachments/1118816521016332411/1122837826300542976/photo_2023-06-26_14-05-55.jpg?width=453&height=612')
                embed.set_author(name="GOLD CLUB")
                await asyncio.sleep(10)
                await channel.send(embed=embed)      
                seasion = aiohttp.ClientSession()
                await seasion.close()
                return


async def setup(Bot : commands.Bot):
    await Bot.add_cog(MyCog(Bot))
    seasion = aiohttp.ClientSession()
    await seasion.close()
