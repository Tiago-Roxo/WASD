import subprocess
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from tqdm import tqdm

def create_setup(WASD_dir):
    print("...Creating WASD setup...")
    orig_vids_dir = "orig_videos/trainval"
    orig_vids_dir_fullpath = os.path.join(WASD_dir, orig_vids_dir)
    os.makedirs(WASD_dir, exist_ok=True)
    os.makedirs(orig_vids_dir_fullpath, exist_ok=True)


def download_csv(WASD_dir):
    print("...Downloading WASD csv...")
    file_link = "1calMd83IIzYnvETY3bee7juRACMBuuyR"
    fullpath_csv = os.path.join(WASD_dir, "WASD_csv.zip")

    cmd = "gdown --id %s -O %s"%(file_link, fullpath_csv)
    subprocess.call(cmd, shell=True, stdout=None)
    cmd = "unzip %s -d %s"%(fullpath_csv, WASD_dir)
    subprocess.call(cmd, shell=True, stdout=None)
    os.remove(fullpath_csv)


def download_videos(WASD_dir):
    print("...Downloading WASD videos...")
    file_link = "1F6pYUNz1u23Q-PvPHpxzm4RUhgFCfVYL"
    fullpath_csv = os.path.join(WASD_dir, "WASD_videos.zip")

    cmd = "gdown --id %s -O %s"%(file_link, fullpath_csv)
    subprocess.call(cmd, shell=True, stdout=None)
    cmd = "unzip %s -d %s"%(fullpath_csv, WASD_dir)
    subprocess.call(cmd, shell=True, stdout=None)
    os.remove(fullpath_csv)


# ----------------------------------------------------------------

def read_file(filename):
    list_vid = []
    with open(filename, "r") as f:
        list_vid = [line.rstrip() for line in f]
    return list_vid



def get_start_end_time(time_line):
    split_t = time_line.split("-")
    start_time, end_time = split_t[0], split_t[1]
    
    start_time_m, start_time_s = int(start_time.split(":")[0]), int(start_time.split(":")[1])
    end_time_m, end_time_s = int(end_time.split(":")[0]), int(end_time.split(":")[1])

    start_time = start_time_m*60+start_time_s
    end_time = end_time_m*60+end_time_s

    return start_time, end_time



def get_list_video_url(file_name):
    with open(file_name, 'r') as video_file:
        lines = video_file.readlines()
        
    video_url_list = []
    for line in lines:
        video_url_list.append(line.strip("\n"))

    return video_url_list


def get_subvids(vids_dir, output_dir):

    print("...Getting subvideos for WASD...")
    def get_vidnames(vids_dir):
        vids = []
        # Iterate directory
        for file in os.listdir(vids_dir):
            # check only text files
            if file.endswith('.txt'):
                vids.append(file.split(".txt")[0])
        return vids

    vids = get_vidnames(vids_dir)

    for vid_url in tqdm(vids):
        video_name = "{}.mp4".format(vid_url)
        file_txt   = "{}.txt".format(vid_url)

        file_fullpath   = os.path.join(vids_dir, file_txt)
        full_video_name = os.path.join(vids_dir, video_name)

        list_times = read_file(file_fullpath)

        for timer in list_times:

            start_time, end_time = get_start_end_time(timer)

            vid_name = "{}_{}-{}.mp4".format(vid_url, start_time, end_time)
            vid_name_fullpath = os.path.join(output_dir, vid_name)

            ffmpeg_extract_subclip(full_video_name, start_time, end_time, targetname=vid_name_fullpath)

# --------------------------------------------------------------------

if __name__ == '__main__':

    WASD_dir = "WASD"
    vids_dir = "WASD_videos"
    orig_vids = "orig_videos/trainval"
    vids_dir_fullpath = os.path.join(WASD_dir, vids_dir)
    orig_vids_fullpath = os.path.join(WASD_dir, orig_vids)

    create_setup(WASD_dir)
    download_csv(WASD_dir)
    download_videos(WASD_dir)
    get_subvids(vids_dir_fullpath, orig_vids_fullpath)