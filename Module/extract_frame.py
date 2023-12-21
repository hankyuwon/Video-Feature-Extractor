import librosa
import librosa.display
import numpy as np
import pandas as pd
import ffmpeg as ff
import os
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import random
import cv2
import pickle
import datetime
import logging
import tqdm

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s]::%(module)s::%(levelname)s::%(message)s')
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
fileHandler = logging.FileHandler('./log/log.log')
fileHandler.setFormatter(formatter)
logger.addHandler(streamHandler)
logger.addHandler(fileHandler)


def get_number_of_frames(file_path: str) -> int:
    probe = ff.probe(file_path)
    video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
    #width = video_streams[0]['coded_width']
    #height = video_streams[0]['coded_height']
    del probe
    return video_streams[0]['nb_frames']

def extract_N_video_frames(file_path: str, number_of_samples: int) -> List[np.ndarray]:
    cap = cv2.VideoCapture(file_path)
    total_frames = int(get_number_of_frames(file_path=file_path))

    video_frames = []
    for i in range(0, total_frames, int(total_frames/(number_of_samples-1))):
        cap.set(1, i)
        ret, frame = cap.read()
        video_frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    cap.release()
    return video_frames


def resize_image(image: np.ndarray, new_size: Tuple[int,int]) -> np.ndarray:
    return cv2.resize(image, new_size, interpolation = cv2.INTER_AREA)

def preprocessing_input(filePath: str, frame_rate: int, height: int, width: int) -> Tuple[np.ndarray]:

    #Video
    sampled = extract_N_video_frames(file_path= filePath, number_of_samples= frame_rate)
    resized_images = [resize_image(image= im, new_size= (height,width)) for im in sampled]
    preprocessed_video = np.stack(resized_images)

    del sampled, resized_images
    return (preprocessed_video)

def extract_frame(filePath = str, frame_rate = int, height = int, width = int):
    logger.debug("=+=+=+=+=+=+=+=+=+=+=+start=+=+=+=+=+=+=+=+=+=+=+")
    data_set = []
    path = filePath
    t1 = datetime.datetime.utcnow()
    for filename in tqdm.tqdm(os.listdir(path)):
        filePath = path +'/'+filename
        logger.debug(filePath)
        data_set.append(preprocessing_input(filePath=filePath,frame_rate=frame_rate,height=height,width=width))
    t2 = datetime.datetime.utcnow()
    logger.debug('Elapsed time: ' + str(t2-t1))
    
    logger.debug('=+=+=+=+=+=+=+=+=+=+=+save dataset=+=+=+=+=+=+=+=+=+=+=+')
    
    savename = "./data/dataset.dat"
    
    with open(savename,"wb") as f:
        pickle.dump(data_set, f)
        
    print("=+=+=+=+=+=+=+=+=+=+=+finish=+=+=+=+=+=+=+=+=+=+=+")