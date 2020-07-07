from discord import VoiceClient
import musicsource
import youtubebuffer
class DiscordServer:

    def __init__(self):
        self.song_queue=[]
        self.current_voice_client=None
        self.current_text_channel=None

    def setCurrentVoiceClient(self,voice_client):
        self.current_voice_client=voice_client

    def setNewTextChannel(self,text_channel):#set main text channel for server for sending messages
        self.current_text_channel=text_channel
        
    async def say(self,message):
        await current_text_channel.send(message)

    def addSongToQueue(self,stream):
        self.song_queue.append(stream)

    def playTopSong(self):
        stream=self.song_queue.pop(0)
        buffer=youtubebuffer.getBufferFromStream(stream)
        source=musicsource.MusicSource(buffer)
        self.current_voice_client.play(source)

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
