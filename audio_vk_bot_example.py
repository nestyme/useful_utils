import os
import random
import numpy as np
import re
import requests
import vk_api
import urllib.request
from vk_api.longpoll import VkLongPoll, VkEventType, VkLongpollMode
from vk_api.upload import VkUpload as vkImport
import soundfile as sf
import librosa
import json
import copy as copy
import scipy.io.wavfile
import soundfile as sf
from random import randint


keyboard = json.dumps({'one_time': True, 'buttons': [[{'color': 'primary', 'action': {'type': 'text',
                                'payload': '123', 
                                'label': 'recognize'}}]]})

token_='***'
group_id = '****'

def handle_attach (event, vk,keyboard):
    global event_temp
    
    try:
        if (event.attachments['attach1_type'] == 'doc'):
            try:
                if (event.attachments['attach1_kind'] == 'audiomsg'):

                    vk.messages.send(random_id = randint(10,20000),
                                     user_id = event.user_id, 
                    keyboard = keyboard, 
                    message = 'Recognize')
                    audio_url = event.message_data['attachments'][0]['audio_message']['link_ogg']
                    audio = urllib.request.urlretrieve(filename="tmp.ogg", url=audio_url)
                    return audio_url
            except KeyError:
                return 1
    except KeyError:
        vk.messages.send(
            # send sticker by its id
            random_id = randint(10,20000),
            user_id = event.user_id,
            sticker_id = 1  
            )
                
                
    try:    
        
        if (event.attachments['attach1_type'] == 'photo'):
            t = random.randint(1,2000)
            vk.messages.send(
                random_id = randint(10,20000),
                user_id = event.user_id,
                message ='photo recieved'
                sticker_id = t              
                )
            return 1
        if (event.attachments['attach1_type'] == 'video'):
            vk.messages.send(
                random_id = randint(10,20000),
                user_id = event.user_id,
                message ='video recieved'             
                )
            return 1
        if not(event.attachments['attach1_type'] == 'audiomsg'):
            print('@No_Audio&Photo@')
            vk.messages.send(
                random_id = randint(10,20000),
                user_id = event.user_id,
                message ='recieved something else'
                )
            return 1
    except KeyError:
        vk.messages.send(
            random_id = randint(10,200),
            user_id = event.user_id,
            sticker_id = 10             
            )
        return 1

    
def handle_text_msg(text_from_usr_, length, vk, name):
    flag=0
    for i in range(len(text_from_usr_)):
        text_from_usr = text_from_usr_[i]
        print(text_from_usr)
        if text_from_usr :
            print('==welocome==')
            flag += 1
            return 'some text'
    else:
            return 'some text'

        
        
def Agregate(audiofile):
    '''
        do here sometring with your audio
    '''
    return audiofile

def main():
    global audio_url, files, filename, vk_doc, vk, curr_id
    
    session = requests.Session()
    vk_session = vk_api.VkApi(token = token_)
    
    print('Initialized vk_session')
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session,preload_messages=True)
    r = 0
    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            
            usr_info = vk_session.method('users.get', {'user_ids': event.user_id, 
                                                       'fields': 'city, verified'})
            name = usr_info[0]['first_name']

            text_usr = re.sub('[!?@#$]', '', event.text)    
            text_from_usr_=text_usr.lower().split()
            if r > 0:
                string = Agregate(filename,event.text)
                vk.messages.send(
                    user_id = event.user_id,
                    random_id = randint(10,20000),
                    message = string
                    )
                r -= 1
                continue
            for i in range(len(text_from_usr_)):
                text_from_usr = text_from_usr_[i]
                

            if event.text:
                
                msg = handle_text_msg(text_from_usr_ = text_from_usr_,
                                    length = len(text_from_usr_),
                                    vk = vk_session.get_api(),
                                    name=name
                                   )
                vk.messages.send(
                                random_id = randint(10,20000),
                                user_id = event.user_id,
                                message = msg
                            )
                
                
            else:
                try:
                    if len(event.text)==0:
                        print('recieved attach')
                        audio = handle_attach(event,vk = vk,keyboard=keyboard)
                        print(audio)
                        if not(audio == 1):
                            print('recieved audio')
                            upload = vk_api.VkUpload(vk_session)
                            audio_url = vk_session.method('docs.getMessagesUploadServer',
                                                            {'type': 'audio_message',
                                                            'peer_id':event.user_id,
                                                            'group_id':group_id})
                            filename = "tmp.ogg"
                            
                            curr_id = filename
                            r += 1
                except FileNotFoundError:
                    vk.messages.send(
                        user_id = event.user_id,
                        message ='something went wrong. Try again!'
                        )
            # print('====================================','Querry',i,'completed','====================================')
            
            tmp = event.text
            tmp_id = event.user_id
                    
            
if __name__ == '__main__':
    main()
