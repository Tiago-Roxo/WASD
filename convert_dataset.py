
import os
import shutil

def list_dir(dir):
    list_dir = os.listdir(dir)
    list_dir_fullpath = [os.path.join(dir, f) for f in list_dir]
    
    return list_dir_fullpath

    

def cleanup_empty_dirs(dir):
    list_dir_fullpath = list_dir(dir)

    for vid_dir in list_dir_fullpath:
        if os.path.isdir(vid_dir):
            if len(os.listdir(vid_dir)) == 0:
                os.rmdir(vid_dir)

    return 



def convert_images(directory):
    list_dir_fullpath = list_dir(directory)

    for sub_dir in list_dir_fullpath:
        if os.path.isdir(sub_dir):
            list_sub_dir_fullpath = list_dir(sub_dir)

            for entity_sub_dir in list_sub_dir_fullpath:
                # Only move directories and not images
                if os.path.isdir(entity_sub_dir):
                    prev_dir = "/".join(sub_dir.split("/")[:-1])
                    
                    # Remove fullpath
                    entity_sub_dir_name = entity_sub_dir.split("/")[-1]
                    dest_dir = os.path.join(prev_dir, entity_sub_dir_name)

                    shutil.move(entity_sub_dir, dest_dir)

        # Checking if dir is empty for safety
        # os.rmdir(sub_dir)

    return



def convert_audio(directory):
    list_dir_fullpath = list_dir(directory)

    for sub_dir in list_dir_fullpath:
        if os.path.isdir(sub_dir):
            list_sub_dir_fullpath = list_dir(sub_dir)

            for entity_sub_dir in list_sub_dir_fullpath:
                prev_dir = "/".join(sub_dir.split("/")[:-1])

                # Remove fullpath
                entity_sub_dir_name = entity_sub_dir.split("/")[-1]
                dest_dir = os.path.join(prev_dir, entity_sub_dir_name)

                shutil.move(entity_sub_dir, dest_dir)

    return


if __name__ == '__main__':

    subsets        = ['val'] # ['train', 'val'] # ['val']
    dataset_dir    = "WASD"
    image_dir      = "clips_videos"
    body_image_dir = "clips_videos_body"
    audio_dir      = "clips_audios"

    image_dir = os.path.join(dataset_dir, image_dir) 
    body_image_dir = os.path.join(dataset_dir, body_image_dir) 
    audio_dir = os.path.join(dataset_dir, audio_dir)

    for subset in subsets:

        print("####### Converting {} folder of images #######".format(subset))
        image_dir_subset = os.path.join(image_dir, subset)
        convert_images(image_dir_subset)

        cleanup_empty_dirs(image_dir_subset)
        
        # Check if body folder exists
        if os.path.isdir(body_image_dir):
            print("####### Converting {} folder of body images #######".format(subset))
            body_image_dir_subset = os.path.join(body_image_dir, subset)
            convert_images(body_image_dir_subset)

            cleanup_empty_dirs(body_image_dir_subset)


        print("####### Converting {} folder of audio #######".format(subset))
        audio_dir_subset = os.path.join(audio_dir, subset)
        convert_audio(audio_dir_subset)

        cleanup_empty_dirs(audio_dir_subset)

        print(audio_dir_subset, image_dir_subset)

    # Change audio directory name
    dest_audio_dir = os.path.join(dataset_dir, "clip_audio")
    os.rename(audio_dir, dest_audio_dir)

