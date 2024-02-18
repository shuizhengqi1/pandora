import moviepy.editor as mp
import os
import librosa
import numpy as np
from sklearn.svm import SVC

# 视频文件路径
video_path = "IMG_4416.MOV"

# 提取音频
video = mp.VideoFileClip(video_path)
audio = video.audio

# 保存音频文件
audio_path = "video_audio.wav"
audio.write_audiofile(audio_path)

# 加载已标注的音频特征和性别标签
features = np.load("path/to/features.npy")
labels = np.load("path/to/labels.npy")

# 训练SVM分类器
classifier = SVC()
classifier.fit(features, labels)

# 加载待预测的音频文件
audio_path = "path/to/audio.wav"
audio, sr = librosa.load(audio_path)

# 提取MFCC特征
mfcc = librosa.feature.mfcc(audio, sr=sr)

# 对特征进行预测
prediction = classifier.predict(mfcc.T)

# 根据预测结果进行编号和保存
output_folder = "path/to/output"
for i, label in enumerate(prediction):
    output_path = os.path.join(output_folder, f"{label}", f"segment_{i}.wav")
    librosa.output.write_wav(output_path, audio[i*hop_length:(i+1)*hop_length], sr)