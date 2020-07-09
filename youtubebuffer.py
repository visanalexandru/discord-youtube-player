from pytube import YouTube
from io import BytesIO


max_buffer_size_megabytes=200
max_buffer_size=max_buffer_size_megabytes*10**6

class StreamTooBigError(Exception):
    def __init__(self,message):
        self.message=message

def getStream(link):#returns youtube mp4 file without video
    yt=YouTube(link)
    stream=yt.streams.filter(only_audio=True)[0]
    if(stream.filesize>max_buffer_size):
        raise StreamTooBigError("The youtube video exceeds "+str(max_buffer_size_megabytes)+" megabytes")
    return stream

def getBufferFromStream(stream):
    to_return=BytesIO()
    stream.stream_to_buffer(to_return)
    to_return.seek(0) #reset the file cursor because the previous function moved it by writting to the byteio obj
    return to_return

