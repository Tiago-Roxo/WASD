# Wilder Active Speaker Detection (WASD) Dataset ([Paper](https://arxiv.org/pdf/2303.05321.pdf))

*To view further details about WASD go to [dataset website](https://tiago-roxo.github.io/WASD/)*

**Wilder Active Speaker Detection (WASD)** dataset has increased difficulty by targeting the two key components of current Active Speaker Detection: audio and face. Grouped into **5 categories**, ranging from optimal conditions to surveillance settings, WASD contains incremental challenges for Active Speaker Detection with tactical impairment of audio and face data. 

![dataset_main_image](images/dataset_main_image.png)
*Considered categories of WASD, with relative audio and face quality represented. Categories range from low (Optimal Conditions) to high (Surveillance Settings) ASD difficulty by varying audio and face quality. Easier categories contain similar characteristics to AVA-ActiveSpeaker (AVA-like), while harder ones are the novelty of WASD.*



## Categories

*   **Optimal Conditions**: People talking in an alternate manner, with minor interruptions, cooperative poses, and face availability;

![dataset_main_image](images/OC_5_images.png)

*   **Speech Impairment**: Frontal pose subjects either talking via video conference call (Delayed Speech) or in a heated discussion, with potential talking overlap (Speech Overlap), but ensuring face availability;

![dataset_main_image](images/SI_5_images.png)

*   **Face Occlusion**: People talking with at least one of the subjects having partial facial occlusion, while keeping good speech quality (no delayed speech and minor communication overlap);

![dataset_main_image](images/FO_5_images.png)

*   **Human Voice Noise**: Communication between speakers where another human voice is playing in the background, with face availability and subject cooperation ensured;

![dataset_main_image](images/HVN_5_images.png)

*   **Surveillance Settings**: Speaker communication in scenarios of video surveillance, with varying audio and image quality, without any guarantee of face access, speech quality, or subject cooperation.

![dataset_main_image](images/SS_5_images.png)



## State-of-the-art Results

### Models Trained on AVA-ActiveSpeaker
Comparison of AVA-ActiveSpeaker trained state-of-the-art models on AVA-ActiveSpeaker and categories of WASD, using the mAP metric. We train and evaluate each model following the authors’ implementation. OC refers to Optimal Conditions, SI to Speech Impairment, FO to Face Occulsion, HVN to Human Voice Noise, and SS to Surveillance Settings. AVA refers to AVA-ActiveSpeaker.

| Model                                                        | AVA       | OC        | SI        | FO        | HVN       | SS        |
|:-------------------------------------------------------------|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| [ASC](https://github.com/fuankarion/active-speakers-context) | 83.6      | 86.4      | 84.8      | 69.9      | 66.4      | 51.1      |
| [MAAS](https://github.com/fuankarion/MAAS)                   | 82.0      | 83.3      | 81.3      | 68.6      | 65.6      | 46.0      |
| [TalkNet](https://github.com/TaoRuijie/TalkNet-ASD)          | 91.8      | 91.6      | 93.0      | 86.4      | 77.2      | 64.6      |
| [ASDNet](https://github.com/okankop/ASDNet)                  | 91.1      | 91.1      | 90.4      | 78.2      | 74.9      | 48.1      |

### Models Trained on WASD
Comparison of state-of-the-art models on the different categories of WASD, using the mAP metric. OC refers to Optimal Conditions, SI to Speech Impairment, FO to Face Occulsion, HVN to Human Voice Noise, and SS to Surveillance Settings.

| Model                                                        | OC        | SI        | FO        | HVN       | SS        | Pretrained  |
|:-------------------------------------------------------------|:---------:|:---------:|:---------:|:---------:|:---------:|------------:|
| [ASC](https://github.com/fuankarion/active-speakers-context) | 91.2      | 92.3      | 87.1      | 66.8      | 72.2      | Download    |
| [MAAS](https://github.com/fuankarion/MAAS)                   | 90.7      | 92.6      | 87.0      | 67.0      | 76.5      | Download    |
| [TalkNet](https://github.com/TaoRuijie/TalkNet-ASD)          | 95.8      | 97.5      | 93.1      | 81.4      | 77.5      | Download    |
| [ASDNet](https://github.com/okankop/ASDNet)                  | 96.5      | 97.4      | 92.1      | 77.4      | 77.8      | Download    |



## Download Dataset

1. Download the content of this GitHub repository;
2. Execute `python3 prepare_setup.py` to create the `WASD` directory and necessary subfolders;
3. Execute `python3 create_dataset.py` to extract audio and face data;
    1. (OPTIONAL) If you want to obtain body data, execute `python3 create_dataset.py --body`;

In the end you should have the following directory structure:
```bash
|-- WASD
|   |-- clips_audios
|   |   |-- ...
|   |-- clips_videos
|   |   |-- ...
|   |-- clips_videos_body
|   |   |-- ...
|   |-- csv
|       |-- train_body_loader.csv
|       |-- train_body_orig.csv
|       |-- train_loader.csv
|       |-- train_orig.csv
|       |-- val_body_loader.csv
|       |-- val_body_orig.csv
|       |-- val_loader.csv
|       |-- val_orig.csv
|   |-- orig_videos
|   |   |-- ...
|   |-- orig_audios
|   |   |-- ...
|   |-- WASD_videos
|   |   |-- ...
|-- convert_dataset.py
|-- create_dataset.py
|-- prepare_setup.py
```
The following folders are not necessary for ASD and can be deleted (if you want) from the `WASD` folder:
* `orig_videos`;
* `orig_audios`;
* `WASD_videos`.

(OPTIONAL) If you wish to use the dataset in a format compatible with ASC, ASDNet, and MAAS, execute `python3 convert_dataset.py`. 

![Warning](images/triangle-exclamation-solid.png) **Note: This will change the WASD folder to this format.** If you want to have both formats available, do a backup of the original `WASD`.



## Evaluate Models on WASD

To evaluate models we use the official implementation to compute active speaker detection on AVA-ActiveSpeaker:

```bash
python3 -O WASD_evaluation.py -g $GT -p $PRED
```
where `$GT` is the groundtruth CSV (*val_orig.csv* of WASD) and `$PRED` is the predictions of your ASD model (usually it is called *val_res.csv*). The execution of `WASD_evaluation.py` requires the presence of `dataset_division.txt` (both files are in `eval` folder), for category division. The output is the mAP for the 5 WASD categories.


## Cite

```bibtex
@article{roxo2023wasd,
    title={WASD: A Wilder Active Speaker Detection Dataset},
    author={Roxo, Tiago and Costa, Joana C and In{\'a}cio, Pedro RM and Proen{\c{c}}a, Hugo},
    journal={arXiv preprint arXiv:2303.05321},
    year={2023}
}
```
