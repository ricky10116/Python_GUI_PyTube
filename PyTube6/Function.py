import json, os
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import time

def mp4tomp3(path):
    video = VideoFileClip(path)
    directory,file=os.path.split(path)
    filewithoutextend,extend=os.path.splitext(file)
    video.audio.write_audiofile(os.path.join(directory, filewithoutextend+".mp3"))
    video.close()
    os.remove(path)

def makefolder():

    try:
        os.mkdir(os.path.join(os.getcwd(),"Downloadfile"))
    except:
        pass

def ReadData():
    ConfigureDataPath=os.path.join(os.getcwd(),"Configure\\")
    with open(ConfigureDataPath+'Configure.json', 'r', encoding='utf-8') as fp:
        datas = json.load(fp)
    return datas
def WriteData(name,data):
    with open(os.path.join(os.getcwd(),"Configure\\") + 'Configure.json', 'r', encoding='utf-8') as fp:
        datas = json.load(fp)
    datas[name]=data
    with open(os.path.join(os.getcwd(),"Configure\\")+ 'Configure.json','w',encoding='utf-8') as fp:
        json.dump(datas,fp,ensure_ascii=False)


if __name__ == "__main__":
    pass

