#!pip install fer
#!pip install tensorflow>=1.7 opencv-contrib-python==3.3.0.9

import sys
import math
import os
import cv2
from fer import FER
from shutil import copyfile

WEBEmo = sys.argv[1]
image_list = os.listdir('/home/ubuntu/crop_faces/original_faces/{}'.format(WEBEmo))
image_list.sort()

count = 0

detector = FER()

for path in image_list:
    img = cv2.imread("original_faces/{}/{}".format(WEBEmo, path))
    results = detector.detect_emotions(img)

    if results == []: 
        split = path.split('_')
        if 'jpg' in split[1]:
            name = split[1]
            number = name[7:-4]
        else:
            name = split[1]
            number_1 = name[7:]
            name_2 = split[2]
            number_2 = name_2.split('.')[0]
            name_list = [number_1, number_2]
            number = '_'.join(name_list)
        full_name = 'cropped_{}tonone_{}.jpg'.format(WEBEmo, number)
        copyfile('original_faces/{}/{}'.format(WEBEmo, path), 'rule1/discard/{}'.format(full_name))
        copyfile('original_faces/{}/{}'.format(WEBEmo, path), 'rule2/discard/{}'.format(full_name))
    else: 
        split = path.split('_')
        if 'jpg' in split[1]:
            name = split[1]
            number = name[7:-4]
        else:
            name = split[1]
            number_1 = name[7:]
            name_2 = split[2]
            number_2 = name_2.split('.')[0]
            name_list = [number_1, number_2]
            number = '_'.join(name_list)
        
        max_emotion = detector.top_emotion(img) 
        angry_score = math.floor(results[0]['emotions']['angry']*100)
        disgust_score = math.floor(results[0]['emotions']['disgust']*100)
        fear_score = math.floor(results[0]['emotions']['fear']*100)
        happy_score = math.floor(results[0]['emotions']['happy']*100)
        sad_score = math.floor(results[0]['emotions']['sad']*100)
        surprise_score = math.floor(results[0]['emotions']['surprise']*100)
        neutral_score = math.floor(results[0]['emotions']['neutral']*100)
        full_name = 'cropped_{}to{}_{}_{}_{}_{}_{}_{}_{}_{}.jpg'.format(WEBEmo, max_emotion[0], number, angry_score, disgust_score, fear_score, happy_score, sad_score, surprise_score, neutral_score)

        emotes = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        distribution = list(results[0]['emotions'].values())
        emote_dist = list(zip(distribution, emotes))
        emote_dist.sort(reverse=True)
        first_emote = emote_dist[0][1]
        first_score = emote_dist[0][0]*100
        second_emote = emote_dist[1][1]
        second_score = emote_dist[1][0]*100

        accepted_emotes = ['angry', 'fear', 'happy', 'sad', 'surprise']
        if first_score == second_score:
            copyfile('original_faces/{}/{}'.format(WEBEmo, path),'rule1/same_score/{}'.format(full_name))
            copyfile('original_faces/{}/{}'.format(WEBEmo, path),'rule2/same_score/{}'.format(full_name))
        elif first_emote == 'angry' or first_emote == 'fear' or first_emote == 'happy' or first_emote == 'sad' or first_emote == 'surprise':
            if first_score >= 80:
                copyfile('original_faces/{}/{}'.format(WEBEmo, path),'rule1/high/{}/{}'.format(first_emote, full_name))
                copyfile('original_faces/{}/{}'.format(WEBEmo, path),'rule2/high/{}/{}'.format(first_emote, full_name))
            elif first_score >= 50 and first_score < 80:
                copyfile('original_faces/{}/{}'.format(WEBEmo, path),'rule1/medium/{}/{}'.format(first_emote, full_name))
                copyfile('original_faces/{}/{}'.format(WEBEmo, path),'rule2/medium/{}/{}'.format(first_emote, full_name))
            elif first_score >= 30 and first_score < 50:
                copyfile('original_faces/{}/{}'.format(WEBEmo, path),'rule1/low/{}/{}'.format(first_emote, full_name))
                copyfile('original_faces/{}/{}'.format(WEBEmo, path),'rule2/low/{}/{}'.format(first_emote, full_name))
            elif first_score < 30:
                copyfile('original_faces/{}/{}'.format(WEBEmo, path),'rule1/misc/{}/{}'.format(first_emote, full_name))
                copyfile('original_faces/{}/{}'.format(WEBEmo, path),'rule2/misc/{}/{}'.format(first_emote, full_name))
        else:
            copyfile('original_faces/{}/{}'.format(WEBEmo, path),'rule1/discard/{}'.format(full_name))
            if second_emote == 'angry' or second_emote == 'fear' or second_emote == 'happy' or second_emote == 'sad' or second_emote == 'surprise':
                if second_score >= 80:
                    copyfile('original_faces/{}/{}'.format(WEBEmo, path),'rule2/high/{}/{}'.format(second_emote, full_name))
                elif second_score >= 50 and second_score < 80:
                    copyfile('original_faces/{}/{}'.format(WEBEmo, path),'rule2/medium/{}/{}'.format(second_emote, full_name))
                elif second_score >= 30 and second_score < 50:
                    copyfile('original_faces/{}/{}'.format(WEBEmo, path),'rule2/low/{}/{}'.format(second_emote, full_name))
                elif second_score < 30:
                    copyfile('original_faces/{}/{}'.format(WEBEmo, path),'rule2/misc/{}/{}'.format(second_emote, full_name))
            else:
                copyfile('original_faces/{}/{}'.format(WEBEmo, path),'rule2/discard/{}'.format(full_name))

    count += 1
    if count%100 == 0:
        print('{} images have been detected'.format(count))
