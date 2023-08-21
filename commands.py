import datetime
from datetime import datetime
from io import BytesIO
from socket import timeout
from unicodedata import name
import discord 
from discord import app_commands
from typing import Literal, Optional
from discord.ext import commands , tasks
from discord.ext.commands import Greedy, Context
import os
import asyncio
from dotenv import load_dotenv
import aiohttp
import sys
from logging import getLogger
import requests
import json
import random


PREFIX = "!"

intents = discord.Intents.all()
intents.message_content = True


Bot = commands.AutoShardedBot(command_prefix=PREFIX, intents=intents,  description= "GOLD CLUB" , chunk_guild_at_startup=False)
Bot.remove_command('help')




############################################## help command ########################################################
#class PaginationView(discord.ui.View):
    #current_page : int =1
    #sep : int = 5

    #async def send (self , ctx):
     #   self.message = await ctx.send(view=self)
    #    await self.update_message(self.data[:self.sep])
    
   # def create_embed (self,data):
       # embed = discord.Embed(title ="example")
      #  for item in data :
     #       embed.add_field(name = item , value= item , inline=False)
    #    return embed

   # async def update_message(self, data):
     #   self.update_buttons()
    #    await self.message.edit(embed = self.create_embed(data) , value= self)


   # def update_buttons(self):
      #  if self.current_page ==1 :
     #       self.first_page_button.disabled = True
    #        self.prev_button.disabled = True
   #     else:
  #           self.first_page_button.disabled = False
 #            self.prev_button.disabled = True
#
        #if self.current_page == int(len(self.data) / self.sep) + 1:
         #   self.next_button.disabled = True
        #    self.last_page_button.disabled = True
       # else:
      #      self.next_button.disabled = True
     #       self.last_page_button.disabled = True

    #discord.ui.button(label='!<' , style=discord.ButtonStyle.primary)
   # async def first_page_button (self , interaction : discord.Interaction , button : discord.ui.Button):
        #await interaction.response.defer()
        #self.current_page =1
       # util_item = self.current_page * self.sep
      #  from_item = util_item - self.sep
     #   await self.update_message(self.data[:util_item])

    #discord.ui.button(label='<' , style=discord.ButtonStyle.primary)
    #async def prev_button (self , interaction : discord.Interaction , button : discord.ui.Button):
       # await interaction.response.defer()
        #self.current_page -=1
       # util_item = self.current_page * self.sep
      #  from_item = util_item - self.sep
     #   await self.update_message(self.data[from_item:util_item])

    #discord.ui.button(label='>' , style=discord.ButtonStyle.primary)
   # async def next_button (self , interaction : discord.Interaction , button : discord.ui.Button):
       # await interaction.response.defer()
        #self.current_page +=1
       # util_item = self.current_page * self.sep
      #  from_item = util_item - self.sep
     #   await self.update_message(self.data[from_item:util_item])

    #discord.ui.button(label='>!' , style=discord.ButtonStyle.primary)
   # async def last_page_button (self , interaction : discord.Interaction , button : discord.ui.Button):
     #   await interaction.response.defer()
    #    self.current_page += int(len(self.data) / self.sep) + 1
   #     util_item = self.current_page * self.sep
  #      from_item = util_item - self.sep
 #       await self.update_message(self.data[from_item:])


#@Bot.command()
#async def help1(ctx):
   # data = [1,2,3,4,5,6,7]
  #  pagination_view = PaginationView()
 #   pagination_view.data = data
#    await pagination_view.send(ctx)

############################################# poll bot ################################################################
@Bot.command()
@commands.has_role(1120042928069423195)
async def poll(ctx , minutes : int , title , *options):
    if ctx.channel.id ==1118813108782252032 or ctx.channel.id ==1118814650960715817 or ctx.channel.id ==1118838681512443914 or ctx.channel.id ==1118828167273128036:
        numbers = ["1","2","3","4","5","6","7","8","9", "10"]
        numbers1 = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣", "🔟"]


        if len(options) == 0:
            pollembed = discord.Embed(title = title , description=f"you have **{minutes}** minutes remaining")
            msg = await ctx.send(embed=pollembed)
            await asyncio.sleep(1)
            await msg.add_reaction ("✅")
            await msg.add_reaction ("❌")
        else:
            pollembed = discord.Embed(title = title , description=f"you have **{minutes}** minutes remaining")
            for number , option in enumerate(options):
                pollembed.add_field(name = f"{numbers[number]}" ,value=f"**{option}**" , inline=False)
            await asyncio.sleep(2)
            msg = await ctx.send(embed=pollembed)
            for x in range(len(pollembed.fields)):
                await asyncio.sleep(1)
                await msg.add_reaction(numbers1[x])

        poll_loop.start(ctx , minutes , title , options , msg)

    
@tasks.loop(minutes = 1)
async def poll_loop(ctx , minutes , title , options , msg):
    numbers = ["1","2","3","4","5","6","7","8","9", "10"]
    count = poll_loop.current_loop
    remaining_time = minutes - count
    newEmbed = discord.Embed(title = title , description=f"you have **{remaining_time}** minutes remainig")
    for number , option in enumerate(options):
            newEmbed.add_field(name = f"{numbers[number]}" ,value=f"**{option}**" , inline=False)
    
    await asyncio.sleep(3)
    await msg.edit(embed=newEmbed)

    if remaining_time == 0:
        counts = []
        msg = discord.utils.get(Bot.cached_messages , id=msg.id)
        reactions = msg.reactions

        for reaction in reactions:
            counts.append(reaction.count)
        max_value = max(counts)
        i = 0
        for n in range (len(counts)):
            if counts[i] == max_value:
                i+=1
                if i == len(counts):
                    await asyncio.sleep(3)
                    await ctx.send('نتایج رای گیری مساوی شد')
                    break
        for count in counts:
            if i == len(counts):
                break
            else:
                max_index = counts.index(max_value)

                if len(options) == 0:
                    winneremoji= reactions[max_index]
                    if winneremoji.emoji =="✅":
                        await asyncio.sleep(3)
                        await ctx.send("جواب رای گیری مثبت هست")
                        break
                    if winneremoji.emoji == "❌":  
                        await asyncio.sleep(3)
                        await ctx.send("جواب رای گیری منفی هست")
                        break
                
                else:
                    winner = options[max_index]
                    winneremoji = reactions[max_index]

                    await asyncio.sleep(3)
                    await ctx.send("زمان تمام شد")
                    await ctx.send(f"{winneremoji.emoji} **{winner}** این گزینه برنده شد")
                    break
        poll_loop.stop()
#######################################################################################################################
#class dokme marbot be fasla
class button_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None )
        

    @discord.ui.button(label='پاک کردن همه رول های این بخش' , style=discord.ButtonStyle.red , custom_id='delete')
    async def verify(self , inter:discord.Integration , button:discord.ui.Button):
        role = inter.guild.get_role(1119619868036182167)
        role1 = inter.guild.get_role(1119619909912117338)
        role2 = inter.guild.get_role(1119621097453785200)
        role3 = inter.guild.get_role(1119621132195201165)
        role4 = inter.guild.get_role(1119621168991850517)
        role5 = inter.guild.get_role(1119621198763012198)
        role6 = inter.guild.get_role(1119621232300671108)
        role7 = inter.guild.get_role(1119621258133385246)
        role8 = inter.guild.get_role(1119621282133200929)
        role9 = inter.guild.get_role(1119621304648204328)
        role10 = inter.guild.get_role(1119621330740969613)
        role11 = inter.guild.get_role(1119621356464635955)
        await inter.response.defer()
        await inter.user.remove_roles(role , role1 , role2 , role3 , role4 , role5 , role6 , role7 , role8 , role9 , role10 , role11) 
#liste marbot be fasla
class Dropdown(discord.ui.Select):
    def __init__(self ):
        options = [
            discord.SelectOption(label='فروردین' , value=str(1119619868036182167),emoji='🌸'),
            discord.SelectOption(label='اردیبهشت' , value=str(1119619909912117338), emoji='💐'),
            discord.SelectOption(label='خرداد' , value=str(1119621097453785200), emoji='🌻'),
            discord.SelectOption(label='تیر' , value=str(1119621132195201165), emoji='🌅'),
            discord.SelectOption(label='مرداد' , value=str(1119621168991850517), emoji='☀️'),
            discord.SelectOption(label='شهریور' , value=str(1119621198763012198), emoji='🏖️'),
            discord.SelectOption(label='مهر' , value=str(1119621232300671108), emoji='🍃'),
            discord.SelectOption(label='آبان' , value=str(1119621258133385246), emoji='🍂'),
            discord.SelectOption(label='آذر' , value=str(1119621282133200929), emoji='🍁'),
            discord.SelectOption(label='دی' , value=str(1119621304648204328), emoji='🌧️'),
            discord.SelectOption(label='بهمن' , value=str(1119621330740969613), emoji='❄️'),
            discord.SelectOption(label='اسفند' , value=str(1119621356464635955), emoji='☃️')

        ]
        

        super().__init__(placeholder='menu' , options=options )
    
    async def callback(self , inter:discord.Interaction):

        jj= discord.utils.get(inter.guild.roles ,id=int(self.values[0]))


        if jj not in inter.user.roles:
            await inter.user.add_roles(jj)
            await inter.response.send_message(f"رول انتخابی اضافه شد" , ephemeral=True)
        else: 
            await inter.response.send_message(f"رول انتخابی را از قبل داشتید" , ephemeral=True)

        
        #await inter.user.add_roles(discord.utils.get(inter.guild.roles ,id=int(self.values[0])))
       # await inter.response.defer()
        
class DropDownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())

#command fasl
@Bot.command()
@commands.has_permissions(administrator=True)
async def rolebirth(ctx):

    embed = discord.Embed(

        title="GOLD CLUB BIRTH ROLES",
        description= "لیست رول های ماه تولد :",
        timestamp=datetime.now(),
        color= 0xBAA928
    )
    embed.set_image(url='https://media.discordapp.net/attachments/1026604090567970866/1118867213345099858/IMG_20230615_150633.jpg?width=691&height=612')
    embed.add_field(name='1:' , value='فروردین')
    embed.add_field(name='2:' , value='اردیبهشت')
    embed.add_field(name='3:' , value='خرداد')
    embed.add_field(name='4:' , value='تیر')
    embed.add_field(name='5:' , value='مرداد')
    embed.add_field(name='6:' , value='شهریور')
    embed.add_field(name='7:' , value='مهر')
    embed.add_field(name='8:' , value='آبان')
    embed.add_field(name='9:' , value='آذر')
    embed.add_field(name='10:' , value='دی')
    embed.add_field(name='11:' , value='بهمن')
    embed.add_field(name='12:' , value='اسفند')

    msg = await ctx.send(embed=embed)
    await ctx.send("منوی انتخاب :" , view=DropDownView())
    await ctx.send(view=button_view())

########################################################## GENDER ROLE ############################################################
class button_view1(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='پاک کردن همه رول های این بخش' , style=discord.ButtonStyle.red , custom_id='delete')
    async def verify(self , inter:discord.Integration , button:discord.ui.Button):
        role = inter.guild.get_role(1119618173377986642)
        role1 = inter.guild.get_role(1119618333109661841)
        

        await inter.response.defer()
        await inter.user.remove_roles(role , role1) 

#liste marbot be fasla
class Dropdown1(discord.ui.Select):
    def __init__(self ):
        options = [
            discord.SelectOption(label='مرد' , value=str(1119618173377986642),emoji='♂'),
            discord.SelectOption(label='زن ' , value=str(1119618333109661841), emoji='♀')

        ]
        

        super().__init__(placeholder='menu' , options=options)
    
    async def callback(self , inter:discord.Interaction):
        jj= discord.utils.get(inter.guild.roles ,id=int(self.values[0]))

        if jj not in inter.user.roles:
            await inter.user.add_roles(jj)
            await inter.response.send_message(f"رول انتخابی اضافه شد" , ephemeral=True)
        else: 
            await inter.response.send_message(f"رول انتخابی را از قبل داشتید" , ephemeral=True)

        
        #await inter.user.add_roles(discord.utils.get(inter.guild.roles ,id=int(self.values[0])))
       # await inter.response.defer()
        
class DropDownView1(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown1())

#command fasl
@Bot.command()
@commands.has_permissions(administrator=True)
async def rolegender(ctx):

    embed = discord.Embed(

        title="GOLD CLUB GENDER ROLES",
        description= "لیست رول های جنسیت :",
        timestamp=datetime.now(),
        color= 0xBAA928
    )
    embed.set_image(url='https://media.discordapp.net/attachments/1026604090567970866/1118867213345099858/IMG_20230615_150633.jpg?width=691&height=612')
    embed.add_field(name='رول اول :' , value='مرد')
    embed.add_field(name='رول دوم :' , value='زن')
    msg = await ctx.send(embed=embed)
    await ctx.send("منوی انتخاب :" , view=DropDownView1())
    await ctx.send(view=button_view1())
    

################################################### AGE ROLE #############################################################

class button_view2(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='پاک کردن همه رول های این بخش' , style=discord.ButtonStyle.red , custom_id='delete')
    async def verify(self , inter:discord.Integration , button:discord.ui.Button):
        role = inter.guild.get_role(1119622149125181561)
        role1 = inter.guild.get_role(1119622184562860064)
        role2 = inter.guild.get_role(1119622217517498501)
        role3 = inter.guild.get_role(1119622250757361734)
        role4 = inter.guild.get_role(1119622279198949417)
        role5 = inter.guild.get_role(1119622308798140546)
        role6 = inter.guild.get_role(1119622344281960518)
        role7 = inter.guild.get_role(1119622376322236509)

        await inter.response.defer()
        await inter.user.remove_roles(role , role1 , role2 , role3 , role4 , role5 , role6 , role7) 


#liste marbot be fasla
class Dropdown2(discord.ui.Select):
    def __init__(self ):
        options = [
            discord.SelectOption(label='-18' , value=str(1119622149125181561),emoji='👶'),
            discord.SelectOption(label='18-21' , value=str(1119622184562860064), emoji='🧒'),
            discord.SelectOption(label='21-25' , value=str(1119622217517498501), emoji='👱‍♂️'),
            discord.SelectOption(label='25-30' , value=str(1119622250757361734), emoji='👨'),
            discord.SelectOption(label='30-35' , value=str(1119622279198949417), emoji='👨‍🦲'),
            discord.SelectOption(label='35-40' , value=str(1119622308798140546), emoji='🧔'),
            discord.SelectOption(label='40-45' , value=str(1119622344281960518), emoji='👨‍🦳'),
            discord.SelectOption(label='+45' , value=str(1119622376322236509), emoji='👴')

        ]
        

        super().__init__(placeholder='menu' , options=options)
    
    async def callback(self , inter:discord.Interaction):
        jj= discord.utils.get(inter.guild.roles ,id=int(self.values[0]))

        if jj not in inter.user.roles:
            await inter.user.add_roles(jj)
            await inter.response.send_message(f"رول انتخابی اضافه شد" , ephemeral=True)
        else: 
            await inter.response.send_message(f"رول انتخابی را از قبل داشتید" , ephemeral=True)

        
        #await inter.user.add_roles(discord.utils.get(inter.guild.roles ,id=int(self.values[0])))
       # await inter.response.defer()
        
class DropDownView2(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown2())

#command fasl
@Bot.command()
@commands.has_permissions(administrator=True)
async def roleage(ctx):

    embed = discord.Embed(

        title="GOLD CLUB AGE ROLES",
        description= "لیست رول های سن",
        timestamp=datetime.now(),
        color= 0xBAA928
    )
    embed.set_image(url='https://media.discordapp.net/attachments/1026604090567970866/1118867213345099858/IMG_20230615_150633.jpg?width=691&height=612')
    embed.add_field(name='رول اول :' , value='-18')
    embed.add_field(name='رول دوم :' , value='18-21')
    embed.add_field(name='رول سوم :' , value='21-25')
    embed.add_field(name='رول چهارم :' , value='25-30')
    embed.add_field(name='رول پنجم :' , value='30-35')
    embed.add_field(name='رول ششم :' , value='35-40')
    embed.add_field(name='رول هفتم' , value='+45')
    msg = await ctx.send(embed=embed)
    await ctx.send("منوی انتخاب :" , view=DropDownView2())
    await ctx.send(view=button_view2())

################################################### GAME ROLES ##########################################################

class button_view3(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='پاک کردن همه رول های این بخش' , style=discord.ButtonStyle.red , custom_id='delete')
    async def verify(self , inter:discord.Integration , button:discord.ui.Button):
        role = inter.guild.get_role(1119618012111196161)
        role1 = inter.guild.get_role(1119618055148949614)
        role2 = inter.guild.get_role(1119618080931323976)
        role3 = inter.guild.get_role(1119618108353675318)
        role4 = inter.guild.get_role(1119618145603289118)
        role5 = inter.guild.get_role(1119620625175166986)
        role6 = inter.guild.get_role(1119620676639281226)
        role7 = inter.guild.get_role(1119620728300515328)
        role8 = inter.guild.get_role(1119620777868795914)
        role9 = inter.guild.get_role(1119620835032973424)
        await inter.response.defer()
        await inter.user.remove_roles(role , role1 , role2 , role3 , role4 , role5 , role6 , role7 , role8 , role9 ) 

#liste marbot be fasla
class Dropdown3(discord.ui.Select):
    def __init__(self ):
        options = [
            discord.SelectOption(label='World Of Warcraft' , value=str(1119618012111196161),emoji='⚔️'),
            discord.SelectOption(label='Call of Duty' , value=str(1119618055148949614), emoji='⚔️'),
            discord.SelectOption(label='CS:GO' , value=str(1119618080931323976), emoji='⚔️'),
            discord.SelectOption(label='Dota 2' , value=str(1119618108353675318), emoji='⚔️'),
            discord.SelectOption(label='Plato' , value=str(1119618145603289118), emoji='⚔️'),
            discord.SelectOption(label='codenames' , value=str(1119620625175166986), emoji='⚔️'),
            discord.SelectOption(label='among us' , value=str(1119620676639281226), emoji='⚔️'),
            discord.SelectOption(label='PUBG' , value=str(1119620728300515328), emoji='⚔️'),
            discord.SelectOption(label='Mobile Legends' , value=str(1119620777868795914), emoji='⚔️'),
            discord.SelectOption(label='PUBG Mobile' , value=str(1119620835032973424), emoji='⚔️')
        ]
        

        super().__init__(placeholder='menu' , options=options)
    
    async def callback(self , inter:discord.Interaction):
        jj= discord.utils.get(inter.guild.roles ,id=int(self.values[0]))

        if jj not in inter.user.roles:
            await inter.user.add_roles(jj)
            await inter.response.send_message(f"رول انتخابی اضافه شد" , ephemeral=True)
        else: 
            await inter.response.send_message(f"رول انتخابی را از قبل داشتید" , ephemeral=True)

        
        #await inter.user.add_roles(discord.utils.get(inter.guild.roles ,id=int(self.values[0])))
       # await inter.response.defer()
        
class DropDownView3(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown3())

#command fasl
@Bot.command()
@commands.has_permissions(administrator=True)
async def rolegame(ctx):

    embed = discord.Embed(

        title="GOLD CLUB GAME ROLES",
        description= "لیست رول های گیم",
        timestamp=datetime.now(),
        color= 0xBAA928
    )
    embed.set_image(url='https://media.discordapp.net/attachments/1026604090567970866/1118867213345099858/IMG_20230615_150633.jpg?width=691&height=612')
    embed.add_field(name='1:' , value='World of Warcraft')
    embed.add_field(name='2:' , value='Call of Duty')
    embed.add_field(name='3:' , value='CS:GO')
    embed.add_field(name='4:' , value='Dota 2')
    embed.add_field(name='5:' , value='Plato')
    embed.add_field(name='6:' , value='codenames')
    embed.add_field(name='7:' , value='Among Us')
    embed.add_field(name='8:' , value='PUBG')
    embed.add_field(name='9:' , value='Mobile Legends')
    embed.add_field(name='10:' , value='PUBG Mobile')
    
    
    msg = await ctx.send(embed=embed)
    await ctx.send("منوی انتخاب :" , view=DropDownView3())
    await ctx.send(view=button_view3())


#################################################### COLOR ##########################################################

class button_view4(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='پاک کردن همه رول های این بخش' , style=discord.ButtonStyle.red , custom_id='delete')
    async def verify(self , inter:discord.Integration , button:discord.ui.Button):
        role = inter.guild.get_role(1119614700309729443)
        role1 = inter.guild.get_role(1119614792135614505)
        role2 = inter.guild.get_role(1119614879830118411)
        role3 = inter.guild.get_role(1119614929926897674)
        role4 = inter.guild.get_role(1119614958750150747)
        role5 = inter.guild.get_role(1119615228175470622)
        role6 = inter.guild.get_role(1119615619168485476)
        await inter.response.defer()
        await inter.user.remove_roles(role , role1 , role2 , role3 , role4 , role5 , role6) 


#liste marbot be fasla
class Dropdown4(discord.ui.Select):
    def __init__(self ):
        options = [
            discord.SelectOption(label='زرد' , value=str(1119614700309729443),emoji='🟡'),
            discord.SelectOption(label='بنفش' , value=str(1119614792135614505), emoji='🟣'),
            discord.SelectOption(label='قرمز' , value=str(1119614879830118411), emoji='🔴'),
            discord.SelectOption(label='آبی' , value=str(1119614929926897674), emoji='🔵'),
            discord.SelectOption(label='نارنجی' , value=str(1119614958750150747), emoji='🟠'),
            discord.SelectOption(label='صورتی' , value=str(1119615228175470622), emoji='💄'),
            discord.SelectOption(label='مشکی' , value=str(1119615619168485476), emoji='⚫')

        ]
        

        super().__init__(placeholder='menu' , options=options)
    
    async def callback(self , inter:discord.Interaction):
        jj= discord.utils.get(inter.guild.roles ,id=int(self.values[0]))

        if jj not in inter.user.roles:
            await inter.user.add_roles(jj)
            await inter.response.send_message(f"رول انتخابی اضافه شد" , ephemeral=True)
        else: 
            await inter.response.send_message(f"رول انتخابی را از قبل داشتید" , ephemeral=True)

        
        #await inter.user.add_roles(discord.utils.get(inter.guild.roles ,id=int(self.values[0])))
       # await inter.response.defer()
        
class DropDownView4(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown4())

#command fasl
@Bot.command()
@commands.has_permissions(administrator=True)
async def rolecolor(ctx):

    embed = discord.Embed(

        title="GOLD CLUB COLOR ROLES",
        description= "لیست رول های رنگ :",
        timestamp=datetime.now(),
        color=  0xBAA928 #0x1abc9c
    )
    embed.set_image(url='https://media.discordapp.net/attachments/1026604090567970866/1118867213345099858/IMG_20230615_150633.jpg?width=691&height=612')
    embed.add_field(name='1:' , value='زرد')
    embed.add_field(name='2:' , value='بنفش')
    embed.add_field(name='3:' , value='قرمز')
    embed.add_field(name='4:' , value='آبی')
    embed.add_field(name='5:' , value='نارنجی')
    embed.add_field(name='6:' , value='صورتی')
    embed.add_field(name='7:' , value='مشکی')

    msg = await ctx.send(embed=embed)
    await ctx.send("منوی انتخاب :" , view=DropDownView4())
    await ctx.send(view=button_view4())


################################################# relationship ##########################################################

class button_view5(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='پاک کردن همه رول های این بخش' , style=discord.ButtonStyle.red , custom_id='delete')
    async def verify(self , inter:discord.Integration , button:discord.ui.Button):
        role = inter.guild.get_role(1119670678971494440)
        role1 = inter.guild.get_role(1119670860316426290)
        role2 = inter.guild.get_role(1119670898430062752)
        role3 = inter.guild.get_role(1119670925810479124)
        
        await inter.response.defer()
        await inter.user.remove_roles(role , role1 , role2 , role3) 

            

#liste marbot be fasla
class Dropdown5(discord.ui.Select):
    def __init__(self ):
        options = [
            discord.SelectOption(label='در رابطه' , value=str(1119670678971494440),emoji='💑'),
            discord.SelectOption(label='ازدواج کرده ' , value=str(1119670860316426290), emoji='💍'),
            discord.SelectOption(label='مجرد' , value=str(1119670898430062752), emoji='🦅'),
            discord.SelectOption(label='به دنبال رابطه' , value=str(1119670925810479124), emoji='😇')

        ]
        

        super().__init__(placeholder='menu' , options=options)
    
    async def callback(self , inter:discord.Interaction):
       
        jj= discord.utils.get(inter.guild.roles ,id=int(self.values[0]))

        if jj not in inter.user.roles:
            await inter.user.add_roles(jj)
            await inter.response.send_message(f"رول انتخابی اضافه شد" , ephemeral=True)
        else: 
            await inter.response.send_message(f"رول انتخابی را از قبل داشتید" , ephemeral=True)

        
        #await inter.user.add_roles(discord.utils.get(inter.guild.roles ,id=int(self.values[0])))
       # await inter.response.defer()
        
class DropDownView5(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown5())

#command fasl
@Bot.command()
@commands.has_permissions(administrator=True)
async def rolerel(ctx):

    embed = discord.Embed(

        title="GOLD CLUB RELATIONSHIP STATUS ROLES",
        description= "لیست رول های وضعیت رابطه :",
        timestamp=datetime.now(),
        color= 0xBAA928
    )
    embed.set_image(url='https://media.discordapp.net/attachments/1026604090567970866/1118867213345099858/IMG_20230615_150633.jpg?width=691&height=612')
    embed.add_field(name='1:' , value='در رابطه')
    embed.add_field(name='2:' , value='ازدواج کرده')
    embed.add_field(name='3:' , value='مجرد')
    embed.add_field(name='4:' , value='به دنبال رابطه')
    msg = await ctx.send(embed=embed)
    await ctx.send("منوی انتخاب :" , view=DropDownView5())
    await ctx.send(view=button_view5())
    

################################################### API FALL HAFEZ #############################################################
@Bot.command(pass_context=True)
@commands.has_role(1118845954737586278)
async def fallhafez(ctx):
    if ctx.channel.id ==1123446799395459122:
        try:
            response = requests.get("https://one-api.ir/hafez/?token=617767:649b5576c3049")
            text = response.json()
            title = text['result']['TITLE'] 
            sher = text['result']['RHYME'] 
            mani = text['result']['MEANING']
            embed = discord.Embed(

                title="GOLD CLUB FALL HAFEZ",
                description= f' فال برای {ctx.message.author.mention}\n\nشعر :\n· · · ━┈┈── ·𖥸· ──┈┈━ · · ·\n {sher} \n معنی فال : {mani}',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
            
        except:
            await asyncio.sleep(10)
            response = requests.get("https://one-api.ir/hafez/?token=617767:649b5576c3049")
            text = response.json()
            title = text['result']['TITLE'] 
            sher = text['result']['RHYME'] 
            mani = text['result']['MEANING']
            embed = discord.Embed(

                title="GOLD CLUB FALL HAFEZ",
                description= f'فال برای {ctx.message.author.mention}\n\n شعر :\n· · · ━┈┈── ·𖥸· ──┈┈━ · · ·\n {sher} \n معنی فال : {mani}',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)

#############################################API danestani#################################################################
@Bot.command(pass_context=True)
@commands.has_role(1118845954737586278)
async def danestani(ctx):
    if ctx.channel.id ==1123446756361912432:
        try:
            response = requests.get("https://one-api.ir/danestani/?token=617767:649b5576c3049")
            text = response.json()
            matn = text['result']['Content']
            embed=discord.Embed(
                title="GOLD CLUB DANESTANI !",
                description= f'{ctx.message.author.mention}\n{matn} ',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
            
        except:
            await asyncio.sleep(10)
            response = requests.get("https://one-api.ir/danestani/?token=617767:649b5576c304")
            text = response.json()
            matn = text['result']['Content']
            embed = discord.Embed(

                title="GOLD CLUB DANESTANI !",
                description= f'{ctx.message.author.mention}\n{matn}',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
####################################################translator########################################################
@Bot.command(pass_context=True)
@commands.has_role(1118845954737586278)
async def joke(ctx):
    if ctx.channel.id ==1123446674786885632:
        try:
            response = requests.get("https://api.codebazan.ir/jok/json/")
            text = response.json()
            jok= text['result']['jok']
            embed=discord.Embed(
                title="GOLD CLUB JOKE :D",
                description= f'{ctx.message.author.mention}\n{jok} ',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
            
        except:
            await asyncio.sleep(10)
            response = requests.get("https://api.codebazan.ir/jok/json/")
            text=response.json()
            jok= text['result']['jok']
            embed = discord.Embed(

                title="GOLD CLUB JOKE :D",
                description= f'{ctx.message.author.mention}\n{jok}',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)

##############################################API KHATERE#####################################################################
@Bot.command(pass_context=True)
@commands.has_role(1118845954737586278)
async def eteraf(ctx):
    if ctx.channel.id ==1123446627781324991:
        try:
            response = requests.get("http://api.codebazan.ir/jok/khatere/")
            text = response.text
            embed=discord.Embed(
                title="GOLD CLUB ETERAF =))",
                description= f'{ctx.message.author.mention}\n{text} ',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
            
        except:
            await asyncio.sleep(10)
            response = requests.get("http://api.codebazan.ir/jok/khatere/")
            text = response.text
            embed = discord.Embed(

                title="GOLD CLUB ETERAF =))",
                description= f'{ctx.message.author.mention}\n{text}',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
#####################################################hadis###########################################################
@Bot.command(pass_context=True)
@commands.has_role(1118845954737586278)
async def manavi(ctx):
    if ctx.channel.id ==1123446563084193874:
        try:
            response = requests.get("http://api.codebazan.ir/hadis/")
            text = response.text
            embed=discord.Embed(
                title="GOLD CLUB SOKHAN MANAVI",
                description= f'{ctx.message.author.mention}\n{text} ',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
            
        except:
            await asyncio.sleep(10)
            response = requests.get("http://api.codebazan.ir/hadis/")
            text = response.text
            embed = discord.Embed(

                title="GOLD CLUB SOKHAN MANAVI",
                description= f'{ctx.message.author.mention}\n{text}',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
##################################################post akhir########################################################
@Bot.command(pass_context=True)
@commands.has_role(1118845954737586278)
async def password(ctx):
    if ctx.channel.id ==1123446515189420042:
        try:
            response = requests.get("http://api.codebazan.ir/password/?length=20")
            text = response.text
            embed=discord.Embed(
                title="GOLD CLUB PASSWORD GENERATOR",
                description= f'{ctx.message.author.mention}\n{text} ',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
            
        except:
            await asyncio.sleep(10)
            response = requests.get("http://api.codebazan.ir/password/?length=20")
            text = response.text
            embed = discord.Embed(

                title="GOLD CLUB PASSWORD GENERATOR",
                description= f'{ctx.message.author.mention}\n{text}',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)

###################################################clock##########################################################
@Bot.command(pass_context=True)
@commands.has_role(1118845954737586278)
async def pingweb(ctx,*,amount:str):
    if ctx.channel.id ==1123446466518712350:
        web=amount
        temp='http://api.codebazan.ir/ping/?url='+web
        try:
            response = requests.get(temp)
            text = response.text
            embed=discord.Embed(
                title="GOLD CLUB PINGER",
                description= f'{ctx.message.author.mention}\n{text} ',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
            
        except:
            await asyncio.sleep(10)
            response = requests.get(temp)
            text = response.text
            embed = discord.Embed(

                title="GOLD CLUB PINGER",
                description= f'{ctx.message.author.mention}\n{text}',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
        
##################################################dastan kotah##########################################################
@Bot.command(pass_context=True)
@commands.has_role(1118845954737586278)
async def dastankotah(ctx):
    if ctx.channel.id ==1123446420561735783:
        try:
            response = requests.get('http://api.codebazan.ir/dastan/')
            text = response.text
            embed=discord.Embed(
                title="GOLD CLUB SHORT STORY",
                description= f'{ctx.message.author.mention}\n{text} ',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
            
        except:
            await asyncio.sleep(10)
            response = requests.get('http://api.codebazan.ir/dastan/')
            text = response.text
            embed = discord.Embed(

                title="GOLD CLUB SHORT STORY",
                description= f'{ctx.message.author.mention}\n{text}',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)

#################################################dialog##############################################################
@Bot.command(pass_context=True)
@commands.has_role(1118845954737586278)
async def dialog(ctx):
    if ctx.channel.id ==1123446369240232016:
        try:
            response = requests.get('http://api.codebazan.ir/dialog/')
            text = response.text
            embed=discord.Embed(
                title="GOLD CLUB CINEMA DIALOG",
                description= f'{ctx.message.author.mention}\n{text} ',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
            
        except:
            await asyncio.sleep(10)
            response = requests.get('http://api.codebazan.ir/dialog/')
            text = response.text
            embed = discord.Embed(

                title="GOLD CLUB CINEMA DIALOG",
                description= f'{ctx.message.author.mention}\n{text}',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)

#################################################dollar#############################################################
@Bot.command(pass_context=True)
@commands.has_role(1118845954737586278)
async def usd(ctx):
    if ctx.channel.id ==1123446208380276746:
        try:
            response = requests.get("http://api.codebazan.ir/arz/?type=arz")
            text = response.json()
            name_arz= text['Result'][0]['name']
            price_arz= text['Result'][0]['price']
            embed=discord.Embed(
                title="GOLD CLUB USD PRICE LIVE",
                description= f'{name_arz} \n قیمت : {price_arz} ',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
            
        except:
            await asyncio.sleep(10)
            response = requests.get("http://api.codebazan.ir/arz/?type=arz")
            text=response.json()
            name_arz= text['Result'][0]['name']
            price_arz= text['Result'][0]['price']
            embed = discord.Embed(

                title="GOLD CLUB USD PRICE LIVE",
                description= f'{name_arz} \n قیمت : {price_arz}',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)

###############################################chistan################################################################
@Bot.command(pass_context=True)
@commands.has_role(1118845954737586278)
async def chistan(ctx):
    if ctx.channel.id ==1123446150876364860:
        try:
            response = requests.get("https://api.codebazan.ir/chistan/")
            temp_num = random.randint(1 , 140)
            text = response.json()
            question1= text['Result'][temp_num]['soal']
            answer1= text['Result'][temp_num]['javab']
            embed=discord.Embed(
                title="GOLD CLUB CHISTAN :)",
                description= f'{ctx.message.author.mention}\n{question1} ',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
            await ctx.send('جواب:')
            await ctx.send('||'+answer1+'||')
            
        except:
            await asyncio.sleep(10)
            response = requests.get("https://api.codebazan.ir/chistan/")
            text=response.json()
            question1= text['Result'][temp_num]['soal']
            answer1= text['Result'][temp_num]['javab']
            embed = discord.Embed(

                title="GOLD CLUB CHISTAN :)",
                description= f'{ctx.message.author.mention}\n{question1}',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
            await ctx.send('جواب:')
            await ctx.send('||'+answer1+'||')
####################################################bio##############################################################
@Bot.command(pass_context=True)
@commands.has_role(1118845954737586278)
async def bio(ctx):
    if ctx.channel.id ==1123446104961331200:
        try:
            response = requests.get('https://api.codebazan.ir/bio/')
            text = response.text
            msg = await ctx.send(f'بیو ایجاد شده برای {ctx.message.author.mention} \n {text}')
            
        except:
            await asyncio.sleep(10)
            response = requests.get('https://api.codebazan.ir/bio/')
            text = response.text
            msg = await ctx.send(f'بیو ایجاد شده برای {ctx.message.author.mention} \n {text}')


################################################phishing detector##############################################################
@Bot.command(pass_context=True)
@commands.has_role(1118845954737586278)
async def detector(ctx,*,amount:str):
    if ctx.channel.id ==1123447590697054279:
        web=amount
        temp='https://api.codebazan.ir/fishinfo/index.php?link='+web
        try:
            response = requests.get(temp)
            text = response.json()
            answer1= text['t']
            temp_answer = ""
            if answer1 == "ادرس معتبر است":
                temp_answer = 'درگاه پرداخت یا ارائه دهنده درگاه پرداخت معتبر است'
            else:
                temp_answer = "درگاه یا ارائه دهنده نامعتبر است یا سایت وارد شده سایت نیست سعی کنید دقیق آدرس درگاه پرداخت را وارد کنید"
            embed=discord.Embed(
                title="GOLD CLUB PHISHING DETECTOR",
                description= f'{ctx.message.author.mention}\n{temp_answer} ',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
            
        except:
            await asyncio.sleep(10)
            response = requests.get(temp)
            text = response.text
            answer1= text['t']
            temp_answer = ""
            if answer1 == "ادرس معتبر است":
                temp_answer = 'درگاه پرداخت یا ارائه دهنده درگاه پرداخت معتبر است'
            else:
                temp_answer = "درگاه یا ارائه دهنده نامعتبر است یا سایت وارد شده سایت نیست سعی کنید دقیق آدرس درگاه پرداخت را وارد کنید"

            embed = discord.Embed(

                title="GOLD CLUB PHISHING DETECTOR",
                description= f'{ctx.message.author.mention}\n{temp_answer}',
                timestamp=datetime.now(),
                color= 0xBAA928
            )
            msg = await ctx.send(embed=embed)
        
#################################################zibanevis#######################################################
@Bot.command(pass_context=True)
@commands.has_role(1118845954737586278)
async def fontgenerator(ctx,*,amount:str):
    if ctx.channel.id ==1123446008089673790:
        if len(amount)<25:
            web=amount
            temp='https://api.codebazan.ir/font/?text='+web
            try:
                response = requests.get(temp)
                text = response.json()
                answer1= text['result']['1'] + '\n' +  text['result']['2'] + '\n' + text['result']['3'] + '\n' + text['result']['4'] + '\n' + text['result']['5'] + '\n' + text['result']['6'] + '\n' + text['result']['7'] + '\n' + text['result']['8'] + '\n' +text['result']['9'] + '\n' + text['result']['10'] + '\n' + text['result']['11'] + '\n' + text['result']['12'] + '\n' +text['result']['13'] + '\n' + text['result']['14'] + '\n' + text['result']['15'] + '\n' + text['result']['16'] + '\n' +text['result']['17'] + '\n' + text['result']['18'] +'\n' + text['result']['19'] + '\n' + text['result']['20'] + '\n' + text['result']['21'] +'\n' +text['result']['22'] + '\n' + text['result']['23'] + '\n' + text['result']['24'] + '\n' +text['result']['25'] + '\n' + text['result']['26'] + '\n' + text['result']['27'] + '\n' + text['result']['28'] + '\n' +text['result']['29'] + '\n' + text['result']['30'] + '\n' + text['result']['31'] + '\n' + text['result']['32'] + '\n' + text['result']['33'] + '\n' + text['result']['34'] + '\n' + text['result']['35'] + '\n' + text['result']['36'] + '\n' + text['result']['37'] + '\n' + text['result']['38'] + '\n' + text['result']['39'] + '\n' + text['result']['40'] + '\n' + text['result']['41'] + '\n' + text['result']['42'] + '\n' + text['result']['43'] + '\n' + text['result']['44'] + '\n' + text['result']['45'] + '\n' + text['result']['46'] + '\n' + text['result']['47'] + '\n' + text['result']['48'] + '\n' + text['result']['49'] + '\n' + text['result']['50']                   
                embed=discord.Embed(
                    title="GOLD CLUB FONT GENERATOR",
                    description= f'font for {ctx.message.author.mention}\n {answer1} ',
                    timestamp=datetime.now(),
                    color= 0xBAA928
                )
                msg = await ctx.send(embed=embed)
                
            except:
                await asyncio.sleep(10)
                response = requests.get(temp)
                text = response.text
                embed = discord.Embed(

                    title="GOLD CLUB FONT GENERATOR",
                    description= f'font for {ctx.message.author.mention}\n {answer1}',
                    timestamp=datetime.now(),
                    color= 0xBAA928
                )
                msg = await ctx.send(embed=embed)
        else:
            await ctx.send('تعداد کاراکترت خیلی زیاده')
##############################################NO EVENT###################################################################
@Bot.command(pass_context=True)
async def noevent(ctx , *, user:discord.Member):
    temp_admin = [role.id for role in ctx.author.roles]
    temp_author = ctx.message.author

    admin_announcement = discord.utils.find(lambda r: r.id == 1118846506770898984, ctx.message.guild.roles) #ban roles
    assisstant = discord.utils.find(lambda r: r.id == 1118846285257117736, ctx.message.guild.roles) #ban roles
    manager = discord.utils.find(lambda r: r.id == 1118846225228242974, ctx.message.guild.roles) #ban roles
    supervisor = discord.utils.find(lambda r: r.id == 1120030200672034816, ctx.message.guild.roles) #ban roles
    Admin_global = discord.utils.find(lambda r: r.id == 1120030200672034816, ctx.message.guild.roles) #ban roles
    enterteiment_admin = discord.utils.find(lambda r: r.id == 1123668705386184754, ctx.message.guild.roles) #ban roles
    bot_role = discord.utils.find(lambda r: r.id == 1120701097456177222, ctx.message.guild.roles) #ban roles
    music_bot = discord.utils.find(lambda r: r.id == 1119627388964315187, ctx.message.guild.roles) #ban roles
    admin_event = discord.utils.find(lambda r: r.id == 1118846374407049236, ctx.message.guild.roles) #ban roles
    no_enterteiment = discord.utils.find(lambda r: r.id == 1120030200672034816, ctx.message.guild.roles) #ban roles
    owner_role = discord.utils.find(lambda r: r.id == 1118570697640378549, ctx.message.guild.roles) #ban roles


    give = discord.utils.find(lambda r: r.id == 1123654376377036861, ctx.message.guild.roles) #roli ke mikhay bedi
    if 1118846374407049236 in temp_admin:   #admin event
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if admin_announcement in user.roles or assisstant in user.roles or manager in user.roles or supervisor in user.roles or Admin_global in user.roles or enterteiment_admin in user.roles or bot_role in user.roles or music_bot in user.roles or admin_event in user.roles or owner_role in user.roles:                #ban roles
            await ctx.channel.send(f'you dont have permission !')
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654376377036861)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO EVENT گرفته شد')
                await channel1.send(f'NO EVENT REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654376377036861)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO EVENT داده شد')
                await channel1.send(f'NO EVENT ADD TO {user.mention} by Admin {ctx.message.author.mention}')

    
    elif 1118846285257117736 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if admin_announcement in user.roles or assisstant in user.roles or manager in user.roles or supervisor in user.roles or Admin_global in user.roles or enterteiment_admin in user.roles or bot_role in user.roles or music_bot in user.roles or admin_event in user.roles or owner_role in user.roles:                #ban roles
            await ctx.channel.send(f'you dont have permission !')
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654376377036861)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO EVENT گرفته شد')
                await channel1.send(f'NO EVENT REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654376377036861)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO EVENT داده شد')
                await channel1.send(f'NO EVENT ADD TO {user.mention} by Admin {ctx.message.author.mention}')


    elif 1118846225228242974 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if manager in user.roles or supervisor in user.roles or owner_role in user.roles:
            await ctx.channel.send(f'you dont have permission')
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654376377036861)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO EVENT گرفته شد')
                await channel1.send(f'NO EVENT REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654376377036861)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO EVENT داده شد')
                await channel1.send(f'NO EVENT ADD TO {user.mention} by Admin {ctx.message.author.mention}')


    elif 1120030200672034816 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if supervisor in user.roles or owner_role in user.roles:
            await ctx.channel.send(f'you dont have permission')
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654376377036861)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO EVENT گرفته شد')
                await channel1.send(f'NO EVENT REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654376377036861)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO EVENT داده شد')
                await channel1.send(f'NO EVENT ADD TO {user.mention} by Admin {ctx.message.author.mention}')


    else:
        await ctx.channel.send("you dont have permission !")

##############################################NO DEKLAME #############################################################
@Bot.command(pass_context=True)
async def nodeklame(ctx , *, user:discord.Member):
    temp_admin = [role.id for role in ctx.author.roles]
    temp_author = ctx.message.author

    admin_announcement = discord.utils.find(lambda r: r.id == 1118846506770898984, ctx.message.guild.roles) #ban roles
    assisstant = discord.utils.find(lambda r: r.id == 1118846285257117736, ctx.message.guild.roles) #ban roles
    manager = discord.utils.find(lambda r: r.id == 1118846225228242974, ctx.message.guild.roles) #ban roles
    supervisor = discord.utils.find(lambda r: r.id == 1120030200672034816, ctx.message.guild.roles) #ban roles
    Admin_global = discord.utils.find(lambda r: r.id == 1120030200672034816, ctx.message.guild.roles) #ban roles
    enterteiment_admin = discord.utils.find(lambda r: r.id == 1123668705386184754, ctx.message.guild.roles) #ban roles
    bot_role = discord.utils.find(lambda r: r.id == 1120701097456177222, ctx.message.guild.roles) #ban roles
    music_bot = discord.utils.find(lambda r: r.id == 1119627388964315187, ctx.message.guild.roles) #ban roles
    admin_event = discord.utils.find(lambda r: r.id == 1118846374407049236, ctx.message.guild.roles) #ban roles
    owner_role = discord.utils.find(lambda r: r.id == 1118570697640378549, ctx.message.guild.roles) #ban roles



    give = discord.utils.find(lambda r: r.id == 1123654417267302503, ctx.message.guild.roles) #roli ke mikhay bedi
    if 1118846374407049236 in temp_admin:   #admin event
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if admin_announcement in user.roles or assisstant in user.roles or manager in user.roles or supervisor in user.roles or Admin_global in user.roles or enterteiment_admin in user.roles or bot_role in user.roles or music_bot in user.roles or admin_event in user.roles or owner_role in user.roles:                #ban roles
            await ctx.channel.send("you dont have permission !")
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654417267302503)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO DEKLAME گرفته شد')
                await channel1.send(f'NO DEKLAME REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654417267302503)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO DEKLAME داده شد')
                await channel1.send(f'NO DEKLAME ADD TO {user.mention} by Admin {ctx.message.author.mention}')


    elif 1118846285257117736 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if admin_announcement in user.roles or assisstant in user.roles or manager in user.roles or supervisor in user.roles or Admin_global in user.roles or enterteiment_admin in user.roles or bot_role in user.roles or music_bot in user.roles or admin_event in user.roles or owner_role in user.roles:                #ban roles
            await ctx.channel.send("you dont have permission !")
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654417267302503)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO DEKLAME گرفته شد')
                await channel1.send(f'NO DEKLAME REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654417267302503)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO DEKLAME داده شد')
                await channel1.send(f'NO DEKLAME ADD TO {user.mention} by Admin {ctx.message.author.mention}')


    elif 1118846225228242974 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if manager in user.roles or supervisor in user.roles or owner_role in user.roles:
            await ctx.channel.send(f'you dont have permission')
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654417267302503)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO DEKLAME گرفته شد')
                await channel1.send(f'NO DEKLAME REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654417267302503)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO DEKLAME داده شد')
                await channel1.send(f'NO DEKLAME ADD TO {user.mention} by Admin {ctx.message.author.mention}')


    elif 1120030200672034816 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if supervisor in user.roles or owner_role in user.roles:
            await ctx.channel.send(f'you dont have permission')
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654417267302503)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO DEKLAME گرفته شد')
                await channel1.send(f'NO DEKLAME REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654417267302503)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO DEKLAME داده شد')
                await channel1.send(f'NO DEKLAME ADD TO {user.mention} by Admin {ctx.message.author.mention}')


    else:
        await ctx.channel.send("you dont have permission !")

##############################################NO GLOBAL##############################################################
@Bot.command(pass_context=True)
async def noglobal(ctx , *, user:discord.Member):
    temp_admin = [role.id for role in ctx.author.roles]
    temp_author = ctx.message.author

    admin_announcement = discord.utils.find(lambda r: r.id == 1118846506770898984, ctx.message.guild.roles) #ban roles
    assisstant = discord.utils.find(lambda r: r.id == 1118846285257117736, ctx.message.guild.roles) #ban roles
    manager = discord.utils.find(lambda r: r.id == 1118846225228242974, ctx.message.guild.roles) #ban roles
    supervisor = discord.utils.find(lambda r: r.id == 1120030200672034816, ctx.message.guild.roles) #ban roles
    Admin_event = discord.utils.find(lambda r: r.id == 1118846374407049236, ctx.message.guild.roles) #ban roles
    enterteiment_admin = discord.utils.find(lambda r: r.id == 1123668705386184754, ctx.message.guild.roles) #ban roles
    bot_role = discord.utils.find(lambda r: r.id == 1120701097456177222, ctx.message.guild.roles) #ban roles
    music_bot = discord.utils.find(lambda r: r.id == 1119627388964315187, ctx.message.guild.roles) #ban roles
    admin_global = discord.utils.find(lambda r: r.id == 1120030200672034816, ctx.message.guild.roles) #ban roles
    owner_role = discord.utils.find(lambda r: r.id == 1118570697640378549, ctx.message.guild.roles) #ban roles



    give = discord.utils.find(lambda r: r.id == 1123654064689905725, ctx.message.guild.roles) #roli ke mikhay bedi
    if 1118846440190529647 in temp_admin:   #admin event
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if admin_announcement in user.roles or assisstant in user.roles or manager in user.roles or supervisor in user.roles or Admin_event in user.roles or enterteiment_admin in user.roles or bot_role in user.roles or music_bot in user.roles or admin_global in user.roles or owner_role in user.roles:                #ban roles
            await ctx.channel.send("you dont have permission !")
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654064689905725)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO CLUB PERMISSION گرفته شد')
                await channel1.send(f'NO CLUB PERMISSION REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654064689905725)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO CLUB PERMISSION داده شد')
                await channel1.send(f'NO CLUB PERMISSION ADD TO {user.mention} by Admin {ctx.message.author.mention}')


    elif 1118846285257117736 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if admin_announcement in user.roles or assisstant in user.roles or manager in user.roles or supervisor in user.roles or admin_global in user.roles or enterteiment_admin in user.roles or bot_role in user.roles or music_bot in user.roles or Admin_event in user.roles or owner_role in user.roles:                #ban roles
            await ctx.channel.send("you dont have permission !")
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654064689905725)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO CLUB PERMISSION گرفته شد')
                await channel1.send(f'NO CLUB PERMISSION REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654064689905725)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO CLUB PERMISSION داده شد')
                await channel1.send(f'NO CLUB PERMISSION ADD TO {user.mention} by Admin {ctx.message.author.mention}')


    elif 1118846225228242974 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if manager in user.roles or supervisor in user.roles or owner_role in user.roles:
            await ctx.channel.send(f'you dont have permission')
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654064689905725)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO CLUB PERMISSION گرفته شد')
                await channel1.send(f'NO CLUB PERMISSION REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654064689905725)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO CLUB PERMISSION داده شد')
                await channel1.send(f'NO CLUB PERMISSION ADD TO {user.mention} by Admin {ctx.message.author.mention}')


    elif 1120030200672034816 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if supervisor in user.roles or owner_role in user.roles:
            await ctx.channel.send(f'you dont have permission')
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654064689905725)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO CLUB PERMISSION گرفته شد')
                await channel1.send(f'NO CLUB PERMISSION REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123654064689905725)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO CLUB PERMISSION داده شد')
                await channel1.send(f'NO CLUB PERMISSION ADD TO {user.mention} by Admin {ctx.message.author.mention}')


    else:
        await ctx.channel.send("you dont have permission !")

##############################################NO TEXT ENTERTEIMENT###################################################

@Bot.command(pass_context=True)
async def noenterteiment(ctx , *, user:discord.Member):
    temp_admin = [role.id for role in ctx.author.roles]
    temp_author = ctx.message.author

    admin_announcement = discord.utils.find(lambda r: r.id == 1118846506770898984, ctx.message.guild.roles) #ban roles
    assisstant = discord.utils.find(lambda r: r.id == 1118846285257117736, ctx.message.guild.roles) #ban roles
    manager = discord.utils.find(lambda r: r.id == 1118846225228242974, ctx.message.guild.roles) #ban roles
    supervisor = discord.utils.find(lambda r: r.id == 1120030200672034816, ctx.message.guild.roles) #ban roles
    admin_global = discord.utils.find(lambda r: r.id == 1118846440190529647, ctx.message.guild.roles) #ban roles
    admin_event = discord.utils.find(lambda r: r.id == 1118846374407049236, ctx.message.guild.roles) #ban roles
    bot_role = discord.utils.find(lambda r: r.id == 1120701097456177222, ctx.message.guild.roles) #ban roles
    music_bot = discord.utils.find(lambda r: r.id == 1119627388964315187, ctx.message.guild.roles) #ban roles
    no_enterteiment = discord.utils.find(lambda r: r.id == 1120030200672034816, ctx.message.guild.roles) #ban roles
    owner_role = discord.utils.find(lambda r: r.id == 1118570697640378549, ctx.message.guild.roles) #ban roles
    enterteiment_admin = discord.utils.find(lambda r: r.id == 1123668705386184754, ctx.message.guild.roles) #ban roles


    give = discord.utils.find(lambda r: r.id == 1123669340714184804, ctx.message.guild.roles) #roli ke mikhay bedi
    if 1123668705386184754 in temp_admin:   #admin event
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if admin_announcement in user.roles or assisstant in user.roles or manager in user.roles or supervisor in user.roles or admin_global in user.roles or admin_event in user.roles or bot_role in user.roles or music_bot in user.roles or enterteiment_admin in user.roles or owner_role in user.roles:                #ban roles
            await ctx.channel.send("you dont have permission !")
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123669340714184804)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO TEXT ENTERTEIMENT گرفته شد')
                await channel1.send(f'NO TEXT ENTERTEIMENT REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123669340714184804)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO TEXT ENTERTEIMENT داده شد')
                await channel1.send(f'NO TEXT ENTERTEIMENT ADD TO {user.mention} by Admin {ctx.message.author.mention}')

    elif 1118846285257117736 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if admin_announcement in user.roles or assisstant in user.roles or manager in user.roles or supervisor in user.roles or admin_global in user.roles or enterteiment_admin in user.roles or bot_role in user.roles or music_bot in user.roles or admin_event in user.roles or owner_role in user.roles:                #ban roles
            await ctx.channel.send("you dont have permission !")
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123669340714184804)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO TEXT ENTERTEIMENT گرفته شد')
                await channel1.send(f'NO TEXT ENTERTEIMENT REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123669340714184804)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO TEXT ENTERTEIMENT داده شد')
                await channel1.send(f'NO TEXT ENTERTEIMENT ADD TO {user.mention} by Admin {ctx.message.author.mention}')


    elif 1118846225228242974 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if manager in user.roles or supervisor in user.roles or owner_role in user.roles:
            await ctx.channel.send(f'you dont have permission')
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123669340714184804)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO TEXT ENTERTEIMENT گرفته شد')
                await channel1.send(f'NO TEXT ENTERTEIMENT REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123669340714184804)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO TEXT ENTERTEIMENT داده شد')
                await channel1.send(f'NO TEXT ENTERTEIMENT ADD TO {user.mention} by Admin {ctx.message.author.mention}')


    elif 1120030200672034816 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if supervisor in user.roles or owner_role in user.roles:
            await ctx.channel.send(f'you dont have permission')
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123669340714184804)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO TEXT ENTERTEIMENT گرفته شد')
                await channel1.send(f'NO TEXT ENTERTEIMENT REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123669340714184804)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO TEXT ENTERTEIMENT داده شد')
                await channel1.send(f'NO TEXT ENTERTEIMENT ADD TO {user.mention} by Admin {ctx.message.author.mention}')



    else:
        await ctx.channel.send("you dont have permission !")

###############################################NO BOT TEXT############################################################
@Bot.command(pass_context=True)
async def nobot(ctx , *, user:discord.Member):
    temp_admin = [role.id for role in ctx.author.roles]
    temp_author = ctx.message.author

    admin_announcement = discord.utils.find(lambda r: r.id == 1118846506770898984, ctx.message.guild.roles) #ban roles
    assisstant = discord.utils.find(lambda r: r.id == 1118846285257117736, ctx.message.guild.roles) #ban roles
    manager = discord.utils.find(lambda r: r.id == 1118846225228242974, ctx.message.guild.roles) #ban roles
    supervisor = discord.utils.find(lambda r: r.id == 1120030200672034816, ctx.message.guild.roles) #ban roles
    admin_global = discord.utils.find(lambda r: r.id == 1118846440190529647, ctx.message.guild.roles) #ban roles
    admin_event = discord.utils.find(lambda r: r.id == 1118846374407049236, ctx.message.guild.roles) #ban roles
    bot_role = discord.utils.find(lambda r: r.id == 1120701097456177222, ctx.message.guild.roles) #ban roles
    music_bot = discord.utils.find(lambda r: r.id == 1119627388964315187, ctx.message.guild.roles) #ban roles
    bot_admin = discord.utils.find(lambda r: r.id == 1123671073783816223, ctx.message.guild.roles) #ban roles
    moderator_admin = discord.utils.find(lambda r: r.id == 1123668187104411659, ctx.message.guild.roles) #ban roles
    owner_role = discord.utils.find(lambda r: r.id == 1118570697640378549, ctx.message.guild.roles) #ban roles
    enterteiment_admin = discord.utils.find(lambda r: r.id == 1123668705386184754, ctx.message.guild.roles) #ban roles


    give = discord.utils.find(lambda r: r.id == 1123671295876415528, ctx.message.guild.roles) #roli ke mikhay bedi
    if 1123671073783816223 in temp_admin:   #admin event
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if admin_announcement in user.roles or assisstant in user.roles or manager in user.roles or supervisor in user.roles or admin_global in user.roles or admin_event in user.roles or bot_role in user.roles or music_bot in user.roles or bot_admin in user.roles or moderator_admin in user.roles or owner_role in user.roles or enterteiment_admin in user.roles:                #ban roles
            await ctx.channel.send("you dont have permission !")
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123671295876415528)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO BOT TEXT گرفته شد')
                await channel1.send(f'NO BOT TEXT REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123671295876415528)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO BOT TEXT داده شد')
                await channel1.send(f'NO BOT TEXT ADD TO {user.mention} by Admin {ctx.message.author.mention}')

    elif 1118846285257117736 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if admin_announcement in user.roles or assisstant in user.roles or manager in user.roles or supervisor in user.roles or admin_global in user.roles or admin_event in user.roles or bot_role in user.roles or music_bot in user.roles or bot_admin in user.roles or moderator_admin in user.roles or owner_role in user.roles or enterteiment_admin in user.roles:   
            await ctx.channel.send("you dont have permission !")
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123671295876415528)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO BOT TEXT گرفته شد')
                await channel1.send(f'NO BOT TEXT REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123671295876415528)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO BOT TEXT داده شد')
                await channel1.send(f'NO BOT TEXT ADD TO {user.mention} by Admin {ctx.message.author.mention}')


    elif 1118846225228242974 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if manager in user.roles or supervisor in user.roles or owner_role in user.roles:
            await ctx.channel.send(f'you dont have permission')
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123671295876415528)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO BOT TEXT گرفته شد')
                await channel1.send(f'NO BOT TEXT REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123671295876415528)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO BOT TEXT داده شد')
                await channel1.send(f'NO BOT TEXT ADD TO {user.mention} by Admin {ctx.message.author.mention}')


    elif 1120030200672034816 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if supervisor in user.roles or owner_role in user.roles:
            await ctx.channel.send(f'you dont have permission')
        else:
            if give in user.roles:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123671295876415528)  # role dadni
                await user.remove_roles(rolename)
                await ctx.channel.send(f'رول NO BOT TEXT گرفته شد')
                await channel1.send(f'NO BOT TEXT REMOVED FROM {user.mention} by Admin {ctx.message.author.mention}')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1123671295876415528)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'رول NO BOT TEXT داده شد')
                await channel1.send(f'NO BOT TEXT ADD TO {user.mention} by Admin {ctx.message.author.mention}')



    else:
        await ctx.channel.send("you dont have permission !")

################################################welcomer add role ##################################################
@Bot.command(pass_context=True)
async def addnew(ctx , *, user:discord.Member):
    temp_admin = [role.id for role in ctx.author.roles]
    temp_author = ctx.message.author

    admin_announcement = discord.utils.find(lambda r: r.id == 1118846506770898984, ctx.message.guild.roles) #ban roles
    assisstant = discord.utils.find(lambda r: r.id == 1118846285257117736, ctx.message.guild.roles) #ban roles
    manager = discord.utils.find(lambda r: r.id == 1118846225228242974, ctx.message.guild.roles) #ban roles
    supervisor = discord.utils.find(lambda r: r.id == 1120030200672034816, ctx.message.guild.roles) #ban roles
    admin_global = discord.utils.find(lambda r: r.id == 1118846440190529647, ctx.message.guild.roles) #ban roles
    admin_event = discord.utils.find(lambda r: r.id == 1118846374407049236, ctx.message.guild.roles) #ban roles
    bot_role = discord.utils.find(lambda r: r.id == 1120701097456177222, ctx.message.guild.roles) #ban roles
    music_bot = discord.utils.find(lambda r: r.id == 1119627388964315187, ctx.message.guild.roles) #ban roles
    bot_admin = discord.utils.find(lambda r: r.id == 1123671073783816223, ctx.message.guild.roles) #ban roles
    moderator_admin = discord.utils.find(lambda r: r.id == 1123668187104411659, ctx.message.guild.roles) #ban roles
    owner_role = discord.utils.find(lambda r: r.id == 1118570697640378549, ctx.message.guild.roles) #ban roles


    give = discord.utils.find(lambda r: r.id == 1118845954737586278, ctx.message.guild.roles) #roli ke mikhay bedi
    if 1118846260259069962 in temp_admin:   #admin event
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if music_bot in user.roles or bot_role in user.roles or owner_role in user.roles:                #ban roles
            await ctx.channel.send("you dont have permission !")
        else:
            if give in user.roles:
                await ctx.channel.send(f'این رول را این شخص دارد !')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1118845954737586278)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'ممبر جدید اضافه شد')
                await channel1.send(f'gold family ADD TO {user.mention} by welcomer {ctx.message.author.name}')

    elif 1118846285257117736 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if music_bot in user.roles or bot_role in user.roles or owner_role in user.roles:                #ban roles
            await ctx.channel.send("you dont have permission !")
        else:
            if give in user.roles:
                await ctx.channel.send(f'این رول را این شخص دارد !')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1118845954737586278)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'ممبر جدید اضافه شد')
                await channel1.send(f'gold family ADD TO {user.mention} by welcomer {ctx.message.author.name}')


    elif 1118846225228242974 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if music_bot in user.roles or bot_role in user.roles or owner_role in user.roles:                #ban roles
            await ctx.channel.send(f'you dont have permission')
        else:
            if give in user.roles:
                await ctx.channel.send(f'این رول را این شخص دارد !')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1118845954737586278)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'ممبر جدید اضافه شد')
                await channel1.send(f'gold family ADD TO {user.mention} by welcomer {ctx.message.author.name}')


    elif 1120030200672034816 in temp_admin:
        channel1 = Bot.get_channel(1119183277215989850) # id channel log
        if music_bot in user.roles or bot_role in user.roles or owner_role in user.roles:                #ban roles
            await ctx.channel.send(f'you dont have permission')
        else:
            if give in user.roles:
                await ctx.channel.send(f'این رول را این شخص دارد !')
            else:
                rolename =discord.utils.get(temp_author.guild.roles , id=1118845954737586278)  # role dadni
                await user.add_roles(rolename)
                await ctx.channel.send(f'ممبر جدید اضافه شد')
                await channel1.send(f'gold family ADD TO {user.mention} by welcomer {ctx.message.author.name}')



    else:
        await ctx.channel.send("you dont have permission !")

#############################################remove all roles#########################################################
@Bot.command(pass_context=True)
async def admin_update(ctx ,  user:discord.Member, num):
    temp_admin = [role.id for role in ctx.author.roles]
    temp_author = ctx.message.author

    admin_announcement = discord.utils.find(lambda r: r.id == 1118846506770898984, ctx.message.guild.roles) #ban roles
    assisstant = discord.utils.find(lambda r: r.id == 1118846285257117736, ctx.message.guild.roles) #ban roles
    manager = discord.utils.find(lambda r: r.id == 1118846225228242974, ctx.message.guild.roles) #ban roles
    supervisor = discord.utils.find(lambda r: r.id == 1120030200672034816, ctx.message.guild.roles) #ban roles
    admin_global = discord.utils.find(lambda r: r.id == 1118846440190529647, ctx.message.guild.roles) #ban roles
    admin_event = discord.utils.find(lambda r: r.id == 1118846374407049236, ctx.message.guild.roles) #ban roles
    bot_role = discord.utils.find(lambda r: r.id == 1120701097456177222, ctx.message.guild.roles) #ban roles
    music_bot = discord.utils.find(lambda r: r.id == 1119627388964315187, ctx.message.guild.roles) #ban roles
    bot_admin = discord.utils.find(lambda r: r.id == 1123671073783816223, ctx.message.guild.roles) #ban roles
    moderator_admin = discord.utils.find(lambda r: r.id == 1123668187104411659, ctx.message.guild.roles) #ban roles
    enter_admin = discord.utils.find(lambda r: r.id == 1123668705386184754, ctx.message.guild.roles) #ban roles
    welcomer = discord.utils.find(lambda r: r.id == 1118846260259069962, ctx.message.guild.roles) #ban roles
    vip = discord.utils.find(lambda r: r.id == 1123649631008591953, ctx.message.guild.roles) #ban roles
    owner_role = discord.utils.find(lambda r: r.id == 1118570697640378549, ctx.message.guild.roles) #ban roles


    if owner_role in user.roles or manager in user.roles or supervisor in user.roles:
        await ctx.channel.send(f'you dont have permission')
    else:

        if 1118846225228242974 in temp_admin and 1120030200672034816 not in temp_admin :
            channel1 = Bot.get_channel(1119183277215989850) # id channel log
            if num == 'assistant':
                muteRole = ctx.guild.get_role(1118846285257117736) # role dadni
                if assisstant in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role assistant deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role assistant Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
            if num == 'admin-announcement':
                muteRole = ctx.guild.get_role(1118846506770898984) # role dadni
                if admin_announcement in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role admin announcement deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role admin announcement Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
            if num == 'admin-event':
                muteRole = ctx.guild.get_role(1118846374407049236) # role dadni
                if admin_event in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role Admin Event deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role Admin Event Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
            if num == 'admin-global':
                muteRole = ctx.guild.get_role(1118846440190529647) # role dadni
                if admin_global in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role Admin Global deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role Admin Global Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
            if num == 'media-moderator':
                muteRole = ctx.guild.get_role(1123668187104411659) # role dadni
                if moderator_admin in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role Media Moderator deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role Media Moderator Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
            if num == 'enterteiment-admin':
                muteRole = ctx.guild.get_role(1123668705386184754) # role dadni
                if enter_admin in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role Enterteiment Admin deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role Enterteiment Admin Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
            if num == 'bot-section':
                muteRole = ctx.guild.get_role(1123671073783816223) # role dadni
                if bot_admin in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role BOT ADMIN deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role BOT ADMIN Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
            if num == 'welcomer':
                muteRole = ctx.guild.get_role(1118846260259069962) # role dadni
                if welcomer in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role Welcomer deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role Welcomer Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
            if num == 'vip':
                muteRole = ctx.guild.get_role(1123649631008591953) # role dadni
                if vip in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role VIP deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role VIP Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')

    

        elif 1120030200672034816 in temp_admin:
            channel1 = Bot.get_channel(1119183277215989850) # id channel log
            if num == 'assistant':
                muteRole = ctx.guild.get_role(1118846285257117736) # role dadani
                if assisstant in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role assistant deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role assistant Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
            if num == 'admin-announcement':
                muteRole = ctx.guild.get_role(1118846506770898984) # role dadani
                if admin_announcement in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role admin announcement deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role admin announcement Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
            if num == 'admin-event':
                muteRole = ctx.guild.get_role(1118846374407049236) # role dadani
                if admin_event in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role Admin Event deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role Admin Event Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
            if num == 'admin-global':
                muteRole = ctx.guild.get_role(1118846440190529647) # role dadani
                if admin_global in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role Admin Global deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role Admin Global Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
            if num == 'media-moderator':
                muteRole = ctx.guild.get_role(1123668187104411659) # role dadani
                if moderator_admin in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role Media Moderator deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role Media Moderator Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
            if num == 'enterteiment-admin':
                muteRole = ctx.guild.get_role(1123668705386184754) # role dadani
                if enter_admin in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role Enterteiment Admin deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role Enterteiment Admin Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
            if num == 'bot-section':
                muteRole = ctx.guild.get_role(1123671073783816223) # role dadani
                if bot_admin in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role BOT ADMIN deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role BOT ADMIN Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
            if num == 'welcomer':
                muteRole = ctx.guild.get_role(1118846260259069962) # role dadani
                if welcomer in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role Welcomer deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role Welcomer Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
            if num == 'vip':
                muteRole = ctx.guild.get_role(1123649631008591953) # role dadani
                if vip in user.roles:
                    await user.remove_roles(muteRole)
                    await channel1.send(f'role VIP deleted from {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')
                else:
                    await user.add_roles(muteRole)
                    await channel1.send(f'role VIP Add to {user.mention} by {ctx.message.author.mention}')
                    await ctx.channel.send(f'user updated')


        
        else : 
            await ctx.channel.send(f'you dont have permission')



##############################################image generator##########################################################

######################################################################################################################
# class DropDown10(discord.ui.Select):
#     def __init__(self , message , images , user):
#         self.message=message
#         self.images=images
#         self.user=user

#         options = [
#             discord.SelectOption(label='1'),
#             discord.SelectOption(label='2'),
#             discord.SelectOption(label='3'),
#             discord.SelectOption(label='4'),
#             discord.SelectOption(label='5'),
#             discord.SelectOption(label='6'),
#             discord.SelectOption(label='7'),
#             discord.SelectOption(label='8'),
#             discord.SelectOption(label='9')

#         ]

#         super().__init__(
#             placeholder="choose the image you wants to see",
#             min_values=1,
#             max_values=1,
#             options=options
#         )

#     async def callback(self, interaction:discord.Integration):
#         if not int(user) == int(interaction.user.id):
#             await interaction.respone.send_message('you are not the author' , ephemeral=True)
#         selection = int(self.values[0])-1
#         image = 

# @Bot.command(pass_context=True)
# async def generate(ctx:commands.Context , * , prompt:str):
#     ETA = int (time.time()+60)
#     msg = await ctx.send(f'go grabe a coffe')
#     async with aiohttp.request('POST', "https://backend.craiyon.com/generate" , json={"prompt":prompt} as resp:
#         r = await resp.json
#         images= r['images']
#         image = BytesIO(base64.decodebytes(images[0].encode('utf8')))
#         retunr await msg.edit(content='generated' , file = discord.File(image,"generatediImage.png") , view=DropDown10(msg , images , ctx.author.id))
        
        
#         )
#######################################################################################################################
@Bot.command(pass_context=True)
@commands.has_role(1120042891130196079)
async def embedpost(ctx , *,amount:str):
    embed = discord.Embed(

        title="GOLD CLUB",
        description= amount,
        timestamp=datetime.now(),
        color= 0xBAA928
    )
    await ctx.message.delete()
    msg = await ctx.send(embed=embed)


@Bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx , amount:str):
    if amount == "all":
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=(int(amount)+ 1))


@Bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def post(ctx ,* ,amount:str):
    if amount =="":
        pass
    else:
        await ctx.message.delete()
        await ctx.send(f"{amount}")


@Bot.command (pass_context=True)
async def new(ctx):
    moderator = discord.utils.get(ctx.guild.roles , id=1118846260259069962) #id role welcomer
    channel1 = Bot.get_channel(1119307092558352566) # id channel welcomer
    if ctx.message.author.voice:
        voice_id = ctx.message.author.voice.channel.id
        if ctx.channel.id ==1118867997281493032:  #id channel waiting chat  
            if voice_id == 1118830281567248395 or voice_id ==1118830313372667955:
                await channel1.send(f'{ctx.message.author.mention} در وویس منتظر تایید ممبری هست {moderator.mention}')
                await ctx.channel.send(f'به ادمین اطلاع داده شد')
            else:
                await ctx.channel.send(f'کاربر عزیز در یکی از وویس های ویتینگ روم جوین شوید و بعد از دستور استفاده کنید.' )
    else:
        await ctx.channel.send(f'کاربر عزیز در یکی از وویس های ویتینگ روم جوین شوید و بعد از دستور استفاده کنید.')
        
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

async def load():
    for filename in os.listdir('./events'):
        if filename.endswith('.py'):
            await Bot.load_extension(f'events.{filename[:-3]}')


async def main():
    await load()
    discord.utils.setup_logging()
    await Bot.start(TOKEN , reconnect=True)
    seasion = aiohttp.ClientSession()
    await seasion.close()



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())