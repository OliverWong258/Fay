import codecs
import os
from threading import Thread
import time

from core.interact import Interact

FILE_URL = "datas/data-" + time.strftime("%Y%m%d%H%M%S") + ".csv"


def __write_to_file(text):
    tm = time.time()
    if not os.path.exists("datas"):
        os.mkdir("datas")
    file = codecs.open(FILE_URL, 'a', 'utf-8')
    file.write(text + "\n")
    file.close()
    print("write to file: ", time.time()-tm)


def storage_live_interact(interact: Interact):
    tm = time.time()
    interact_type = interact.interact_type
    user = interact.data["user"].replace(',', '，')
    msg = interact.data["msg"].replace(',', '，')
    msg_type = {
        0: '主播',
        1: '发言',
        2: '进入',
        3: '送礼',
        4: '关注'
    }
    timestamp = int(time.time() * 1000)
    Thread(target=__write_to_file, args=["%s,%s,%s,%s\n" % (timestamp, msg_type[interact_type], user, msg)]).start()
    print("storage live intaract: ", time.time()-tm)
