from discord import VoiceClient
import musicsource
import youtubebuffer
import asyncio
class DiscordServer:

    def __init__(self,client_loop):
        self.song_queue=[]
        self.current_voice_client=None
        self.current_text_channel=None
        self.client_loop=client_loop

    def setCurrentVoiceClient(self,voice_client):
        self.current_voice_client=voice_client

    def setNewTextChannel(self,text_channel):#set main text channel for server for sending messages
        self.current_text_channel=text_channel
        
    async def say(self,message):
        await self.current_text_channel.send(message)

    def addSongToQueue(self,stream,title):
        self.song_queue.append((stream,title))

    async def playTopSong(self):
        if(not self.hasRemainingSongs()):
            await self.say("Finished queue")
            return
        top=self.song_queue.pop(0)
        stream=top[0]
        await self.say("Now playing: "+top[1])
        buffer=youtubebuffer.getBufferFromStream(stream)
        source=musicsource.MusicSource(buffer)
        self.current_voice_client.play(source,after=self.onStoppedPlayer)


    def onStoppedPlayer(self,error):
        coroutine=self.playTopSong()#start the next song in the queue
        future=asyncio.run_coroutine_threadsafe(coroutine,self.client_loop)
        future.result()

    def skipSong(self):
        self.current_voice_client.stop()#this will stop the voice client that will triger another song 


    def hasRemainingSongs(self):
        return len(self.song_queue)!=0

    def hasVoiceClient(self):
        return self.current_voice_client!=None



    async def disconnectFromAudio(self):
       await self.current_voice_client.disconnect()
       self.current_voice_client=None


    def isPlayingAudio(self):
        return self.hasVoiceClient() and self.current_voice_client.is_playing()


    def isConnectedToVoice(self):
        return self.hasVoiceClient() and self.current_voice_client.is_connected()
