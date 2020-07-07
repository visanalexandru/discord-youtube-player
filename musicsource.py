from discord import AudioSource
from pydub import AudioSegment
from io import BytesIO


class MusicSource(AudioSource): 

    def read(self):
        chunk=self.sound[self.current_time_milliseconds:self.current_time_milliseconds+self.chunk_size_milliseconds]
        self.current_time_milliseconds+=self.chunk_size_milliseconds
        return  chunk._data



    def is_opus(self):
        return False



    def __init__(self,buffer):

        sound = AudioSegment.from_file(buffer,format="mp4")

        self.sound=sound.set_frame_rate(48000)
        self.chunk_size_milliseconds=20
        self.current_time_milliseconds=0
