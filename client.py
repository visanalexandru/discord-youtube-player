import youtubebuffer
import asyncio
import discordserver
import pytube
from discord import Client

class MyClient(Client):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.servers={}

    async def on_ready(self):
        print('Logged on as', self.user)
        print("Connected to servers:")
        for guild in self.guilds:
            self.servers[guild.id]=discordserver.DiscordServer(self.loop)
            print("-"+guild.name+" #"+str(guild.id))

    async def say(self,channel,message):
        await channel.send(message)


    async def on_message(self, message):

        content=message.content


        if(len(content)==0 or content[0]!='~'):#message is invalid
            return

        if(message.guild==None): #not in a discord server 
            await self.say(text_channel,"You need to be in a server to use this bot")
            return


        server=self.servers[message.guild.id]
        content=content[1:] #remove the first character
        tokens=content.split(' ')
        text_channel=message.channel
        voice=message.author.voice


        operation=tokens[0]
        parameters=tokens[1:]


        if (operation=="add"):#adds song to server queue
            if(len(parameters)==0):
                await self.say(text_channel,"Please input a youtube link")
                return

            link=parameters[0]
            try:
                stream=youtubebuffer.getStream(link)
                server.addSongToQueue(stream,link) 
            except pytube.exceptions.RegexMatchError:
                await self.say(text_channel,"The youtube link is invalid")

        elif(operation=="play"):

            if(voice==None):
                await self.say(text_channel,"You need to be in a voice channel to start the queue")
                return

            if(not server.hasRemainingSongs()):
                await self.say(text_channel,"The queue is empty")
                return

            if(server.isPlayingAudio()):
                await self.say(text_channel,"The bot is currently playing audio")
                return

            if(server.isConnectedToVoice() and server.current_voice_client.channel!=voice.channel):
                await server.disconnectFromAudio()

            if(not server.isConnectedToVoice()):
                new_voice_client=await voice.channel.connect()
                server.setCurrentVoiceClient(new_voice_client)
            server.setNewTextChannel(text_channel)
            await server.playTopSong()
        
        elif(operation=="skip"):
            if(voice==None):
                await self.say(text_channel,"You need to be in a voice channel to skip a song")
                return
            if(not server.isPlayingAudio()):
                await self.say(text_channel,"The bot is not playing audio")
                return
            server.skipSong()

