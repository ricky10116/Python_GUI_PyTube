import json, os
import subprocess
from shlex import split
import shlex
import time
from pytube import YouTube


def read():
    # with open('data.json', 'r', encoding='utf-8') as fp:
    with open('C:\\Users\\rshang\\Desktop\\PyTube5\\Configure\\data.json', 'r', encoding='utf-8') as fp:
        datas = json.load(fp)
        print(type(datas)) # <class 'dict'>
        print(datas) # {'path': 'AA', 'test': 'BB'}
        for data in datas:
            print(data)
        print(datas["path"]) # AA

def write():
    data={"path":"AA","test":"BB"}
    with open('data.json','w',encoding='utf-8') as fp:
        json.dump(data,fp,ensure_ascii=False)

def pylist():
    from pytube import Playlist
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    # https://www.youtube.com/watch?v=Ip56kmSzXbI&list=RDIp56kmSzXbI&start_radio=1
    p = Playlist('https://www.youtube.com/watch?v=Ya2vreNDCIc&list=PL6CW-qUsjk81zSTgsAWAtG4uzNOSPo8rj')
    p = Playlist('ccccc')
    p = Playlist('https://www.youtube.com/watch?v=Ip56kmSzXbI&list=RDIp56kmSzXbI&start_radio=1')
    try :
        p.title
    except:
        print("error url")
    else:
        print(f'Downloading: {p.title}')
        for video in p.videos:

            print(video.title)
            video = video.streams.get_highest_resolution()
            video.download(os.path.join(os.getcwd(), "Downloadfile1"))

def pytube():
    from pytube import YouTube

    yt = YouTube('http://youtube.com/watch?v=9bZkp7q19f0')
    yt = YouTube('https://www.youtube.com/watch?v=Ip56kmSzXbI&list=RDIp56kmSzXbI&start_radio=1')
    print(yt.title)

def You_Get():
    info = subprocess.Popen(
        "you-get https://www.youtube.com/watch?v=Ip56kmSzXbI&list=RDIp56kmSzXbI&start_radio=1",
        shell=True, stdout=subprocess.PIPE).stdout.read()
    # shell：如果该参数为 True，将通过操作系统的 shell 执行指定的命令。

    info = info.decode("utf-8", "ignore")
    title = info.partition("\r\n")[2].partition("\r\n")[0].partition(":")[2].replace(" ", "")
    print(title)
# https://www.youtube.com/watch?v=Ip56kmSzXbI&list=RDIp56kmSzXbI&start_radio=1
# https://www.youtube.com/watch?v=Sk1M0lBHcA4

def callcmd():
    os.system("you-get https://www.youtube.com/watch?v=rzR9TM8Td5g")
# https://www.youtube.com/watch?v=g8nkG7xmY0Q

def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, shell=True)
    while True:
        # output = process.stdout.readline() run_command("you-get https://www.youtube.com/watch?v=rzR9TM8Td5g")
        output = process.stdout.readline(50).decode('utf-8','ignore')
        if output == '' and process.poll() is not None:
            break
        if output:
            print (output.strip())

    rc = process.poll()
    return rc

def test1(): # https://www.youtube.com/watch?v=ZjDZrReZ4EI
    # yt = YouTube("https://www.youtube.com/watch?v=Ip56kmSzXbI")
    # video = yt.streams.get_highest_resolution()

    # yt = YouTube('http://youtube.com/watch?v=9bZkp7q19f0')
    # yt = YouTube('https://www.youtube.com/watch?v=ZjDZrReZ4EI')
    yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')
    print(yt.streams)
    print("1")

    # video.streams.get_by_itag(137).download()  # salva na pasta
    # video.download()

if __name__ == "__main__":

    # write()
    read()
    # print(os.getcwd()) # C:\Users\ricky\OneDrive\Desktop\PyTube5
    # pylist()
    # pytube()
    # You_Get() #https://www.youtube.com/watch?v=rzR9TM8Td5g
    # callcmd()
    # run_command("you-get https://www.youtube.com/watch?v=rzR9TM8Td5g")
    # run_command("you-get https://www.youtube.com/watch?v=jNQXAC9IVRw")
    # run_command("you-get https://www.youtube.com/watch?v=Sk1M0lBHcA4")
    # https://www.youtube.com/watch?v=Sk1M0lBHcA4
    # callcmd5()
    # print(system_call("you-get https://www.youtube.com/watch?v=rzR9TM8Td5g")
    # test1()
    # print(b' [36\xe9\xa6\x96] 2001\xe5\xb9\xb4\xe5\x9b\xbd\xe8'.decode('utf-8',"ignore"))
    # test1()