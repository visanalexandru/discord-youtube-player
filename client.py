import youtubebuffer
import asyncio
import discordserver
import pytube
import datetime
from discord import Client
from discord import Embed

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


        if(len(content)==0 or content[0]!='-'):#message is invalid
            return

        if(message.guild==None): #not in a discord server 
            await self.say(text_channel,"You need to be in a server to use this bot")
            return


        content=content[1:] #remove the first character
        tokens=content.split(' ')
        
        operation=tokens[0]
        parameters=tokens[1:]
        server=self.servers[message.guild.id]
        text_channel=message.channel
        voice=message.author.voice


        if (operation=="add"):#adds song to server queue
            if(len(parameters)==0):
                await self.say(text_channel,"Please input a youtube link")
                return
            link=parameters[0]

            try:
                stream=youtubebuffer.getStream(link)
                server.addSongToQueue(stream,link) 

            except youtubebuffer.StreamTooBigError as stream_too_big_error:
                await self.say(text_channel,stream_too_big_error.message)

            except pytube.exceptions.LiveStreamError:
                await self.say(text_channel,"Cannot load a live stream")


            except pytube.exceptions.RegexMatchError:
                await self.say(text_channel,"The youtube link is invalid")


            except pytube.exceptions.VideoUnavailable:
                await self.say(text_channel,"The youtube video is unavailable")

            except Exception as exception:
                print("Exception when loading a youtube link:",exception,link)
                await self.say(text_channel,"Could not process youtube link")


        elif(operation=="play"):

            if(voice==None):
                await self.say(text_channel,"You need to be in a voice channel to start the queue")
                return

            if(not server.hasRemainingSongs()):
                await self.say(text_channel,"The queue is empty")
                return

            if(server.isPlaying()):
                await self.say(text_channel,"The bot is currently playing a song")
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
            if(not server.isPlaying()):
                await self.say(text_channel,"The bot is not playing any songs")
                return
            server.skipSong()



        elif(operation=="pause"):
            if(voice==None):
                await self.say(text_channel,"You need to be in a voice channel to pause a song")
                return

            if(not server.isPlaying()):
                await self.say(text_channel,"The bot is not playing any songs")
                return


            if(server.isPlayingAudioPaused()):
                await self.say(text_channel,"The bot is already paused")
                return
            server.pauseSong()


        elif(operation=="resume"):
            if(voice==None):
                await self.say(text_channel,"You need to be in a voice channel to resume a song")
                return
            if(not server.isPlaying()):
                await self.say(text_channel,"The bot is not playing any songs")
                return
            if(server.isPlayingAudio()):
                await self.say(text_channel,"The bot is already playing audio")
                return
            server.resumeSong()



        elif (operation=="queue"):

            if(not server.hasRemainingSongs()):
                await self.say(text_channel,"The queue is empty")
                return

            embedVar =Embed(title="Song queue", color=0x00ff00)

            index=1
            for song in server.song_queue:
                embedVar.add_field(name=("No. "+str(index)),value=song[1],inline=False)
                index+=1

            await text_channel.send(embed=embedVar)
       


        elif (operation=="clearqueue"):
            if(not server.hasRemainingSongs()):
                await self.say(text_channel,"The queue is already empty")

            server.clearQueue()

        elif (operation=="ping"):
            message_time=message.created_at.timestamp()
            now=datetime.datetime.utcnow().timestamp()
            deltatime=int((now-message_time)*1000)
            message=await self.say(text_channel,"Pong "+str(deltatime)+" ms")


        elif(operation=="help"):
            embedVar=Embed(title="Commands",color=0x00ff00)
            embedVar.add_field(name="```add```",value="Adds a song to the queue",inline=False)
            embedVar.add_field(name="```play```",value="Start playing the queue",inline=False)
            embedVar.add_field(name="```skip```",value="Skip the current song",inline=False)
            embedVar.add_field(name="```pause```",value="Pause the current song",inline=False)
            embedVar.add_field(name="```resume```",value="Resume the current song",inline=False)
            embedVar.add_field(name="```queue```",value="Show all songs in the queue",inline=False)
            embedVar.add_field(name="```clearqueue```",value="Clear the queue",inline=False)
            embedVar.add_field(name="```ping```",value="Displays the latency between discord and the bot",inline=False)
            await text_channel.send(embed=embedVar)
        
        else:
            await self.say(text_channel,"Invalid command, type -help for a list of commands")

