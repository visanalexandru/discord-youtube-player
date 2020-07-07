from pytube import YouTube
from io import BytesIO

def getStream(link):#returns youtube mp4 file without video
    yt=YouTube(link)
    stream=yt.streams.filter(only_audio=True)[0]
    return stream

def getBufferFromStream(stream):
    to_return=BytesIO()
    stream.stream_to_buffer(to_return)
    to_return.seek(0) #reset the file cursor because the previous function moved it by writting to the byteio obj
    return to_return

