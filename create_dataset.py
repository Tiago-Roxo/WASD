import os, subprocess, glob, pandas, tqdm, cv2, numpy
from scipy.io import wavfile 
import sys
import argparse

def extract_audio(orig_vid_dir, orig_audio_dir):
    # Take 1 hour to extract the audio from movies
    # for dataType in ['trainval', 'test']:
    for dataType in ['trainval']:
        inpFolder = '%s/%s'%(orig_vid_dir, dataType)
        outFolder = '%s/%s'%(orig_audio_dir, dataType)
        os.makedirs(outFolder, exist_ok = True)
        videos = glob.glob("%s/*"%(inpFolder))
        for videoPath in tqdm.tqdm(videos):
            audioPath = '%s/%s'%(outFolder, videoPath.split('/')[-1].split('.')[0] + '.wav')
            cmd = ("ffmpeg -y -i %s -async 1 -ac 1 -vn -acodec pcm_s16le -ar 16000 -threads 8 %s -loglevel panic" % (videoPath, audioPath))
            subprocess.call(cmd, shell=True, stdout=None)


def extract_audio_clips(dataset_sets, csv_dir, clip_audio_dir, orig_audio_dir):

    dic = {'train':'trainval', 'val':'trainval', 'test':'test'}

    for dataType in dataset_sets:
        df = pandas.read_csv(os.path.join(csv_dir, '%s_orig.csv'%(dataType)), engine='python')
        dfNeg = pandas.concat([df[df['label_id'] == 0], df[df['label_id'] == 2]])
        dfPos = df[df['label_id'] == 1]
        insNeg = dfNeg['instance_id'].unique().tolist()
        insPos = dfPos['instance_id'].unique().tolist()
        df = pandas.concat([dfPos, dfNeg]).reset_index(drop=True)
        df = df.sort_values(['entity_id', 'frame_timestamp']).reset_index(drop=True)
        entityList = df['entity_id'].unique().tolist()
        df = df.groupby('entity_id')
        audioFeatures = {}
        outDir = os.path.join(clip_audio_dir, dataType)
        audioDir = os.path.join(orig_audio_dir, dic[dataType])
        for l in df['video_id'].unique().tolist():
            d = os.path.join(outDir, l[0])
            if not os.path.isdir(d):
                os.makedirs(d)
        for entity in tqdm.tqdm(entityList, total = len(entityList)):
            insData = df.get_group(entity)
            videoKey = insData.iloc[0]['video_id']
            start = insData.iloc[0]['frame_timestamp']
            end = insData.iloc[-1]['frame_timestamp']
            entityID = insData.iloc[0]['entity_id']

            insPath = os.path.join(outDir, videoKey, entityID+'.wav')
            if videoKey not in audioFeatures.keys():                
                audioFile = os.path.join(audioDir, videoKey+'.wav')
                sr, audio = wavfile.read(audioFile)
                audioFeatures[videoKey] = audio
            audioStart = int(float(start)*sr)
            audioEnd = int(float(end)*sr)
            audioData = audioFeatures[videoKey][audioStart:audioEnd]
            wavfile.write(insPath, sr, audioData)


    
def extract_video_clips(dataset_sets, csv_dir, clip_vid_dir, orig_vid_dir, extract_body_data=False):

    dic = {'train':'trainval', 'val':'trainval', 'test':'test'}
    if extract_body_data:
        visual_part  = ['face', 'body']
    else:
        visual_part  = ['face']
    
    for part in visual_part:
        for dataType in dataset_sets:
            print("Extracting {} data of {} set...".format(part, dataType))
            if part == 'face':
                csv_file = "{}_orig.csv".format(dataType)
            else:
                csv_file = "{}_orig_body.csv".format(dataType)
                clip_vid_dir = "{}_body".format(clip_vid_dir)

            df = pandas.read_csv(os.path.join(csv_dir, csv_file))
                    
            dfNeg = df[df['label_id'] == 0]
            dfPos = df[df['label_id'] == 1]

            df = pandas.concat([dfPos, dfNeg]).reset_index(drop=True)
            df = df.sort_values(['entity_id', 'frame_timestamp']).reset_index(drop=True)
            entityList = df['entity_id'].unique().tolist()
            df = df.groupby('entity_id')

            outDir = os.path.join(clip_vid_dir, dataType)
            audioDir = os.path.join(orig_vid_dir, dic[dataType])
            for l in df['video_id'].unique().tolist():
                d = os.path.join(outDir, l[0])
                if not os.path.isdir(d):
                    os.makedirs(d)
            for entity in tqdm.tqdm(entityList, total = len(entityList)):
                insData = df.get_group(entity)
                videoKey = insData.iloc[0]['video_id']
                entityID = insData.iloc[0]['entity_id']
                videoDir = os.path.join(orig_vid_dir, dic[dataType])
                videoFile = glob.glob(os.path.join(videoDir, '{}.*'.format(videoKey)))[0]
                V = cv2.VideoCapture(videoFile)
                insDir = os.path.join(os.path.join(outDir, videoKey, entityID))
                if not os.path.isdir(insDir):
                    os.makedirs(insDir)
                j = 0
                for _, row in insData.iterrows():
                    imageFilename = os.path.join(insDir, str("%.2f"%row['frame_timestamp'])+'.jpg')
                    if os.path.exists(imageFilename):
                        # print('skip', image_filename)
                        continue
                    V.set(cv2.CAP_PROP_POS_MSEC, row['frame_timestamp'] * 1e3)
                    _, frame = V.read()
                    h = numpy.size(frame, 0)
                    w = numpy.size(frame, 1)
                    x1 = int(row['entity_box_x1'] * w)
                    y1 = int(row['entity_box_y1'] * h)
                    x2 = int(row['entity_box_x2'] * w)
                    y2 = int(row['entity_box_y2'] * h)
                    face = frame[y1:y2, x1:x2, :]
                    j = j+1
                    cv2.imwrite(imageFilename, face)


if __name__ == '__main__':

    argParser = argparse.ArgumentParser()
    argParser.add_argument("--body", action='store_true', help='Extract body data')
    args = argParser.parse_args()
    extract_body_data = args.body

    WASD_dir = "WASD"
    orig_vids = "orig_videos"
    orig_audios = "orig_audios"
    cvs_dir     = "csv"
    clip_audios_dir = "clips_audios"
    clip_videos_dir = "clips_videos"
    dataset_sets = ['val'] # ['train', 'val'] # ['val']

    orig_audios_fullpath  = os.path.join(WASD_dir, orig_audios)
    orig_vids_fullpath = os.path.join(WASD_dir, orig_vids)

    print("####### EXTRACTING AUDIO #######")

    extract_audio(orig_vids_fullpath, orig_audios_fullpath)

    csv_dir_fullpath  = os.path.join(WASD_dir, cvs_dir)
    clip_audios_dir_fullpath = os.path.join(WASD_dir, clip_audios_dir)

    print("####### STARTING AUDIO SLICING #######")

    extract_audio_clips(dataset_sets, csv_dir_fullpath, clip_audios_dir_fullpath, orig_audios_fullpath)

    print("####### FINISHED AUDIO SLICING #######")

    clip_videos_dir_fullpath    = os.path.join(WASD_dir, clip_videos_dir)

    if extract_body_data:
        print("####### STARTING FACE AND BODY CROPPING #######")
    else:
        print("####### STARTING FACE CROPPING #######")

    extract_video_clips(dataset_sets, csv_dir_fullpath, clip_videos_dir_fullpath, orig_vids_fullpath, extract_body_data)

    if extract_body_data:
        print("####### FINISHED FACE AND BODY CROPPING #######")
    else:
        print("####### FINISHED FACE CROPPING #######")

    
