from moviepy.editor import *
"""
为视频添加一个背景音乐
多轨音频合成
"""
#需添加背景音乐的视频
video_clip = VideoFileClip(r'同福ktv之属于港台的八十年代【解说武林外传】.mp4')
#提取视频对应的音频，并调节音量
video_audio_clip = video_clip.audio.volumex(0.8)

#背景音乐
audio_clip = AudioFileClip(r'北京北京.mp3').volumex(0.5)
#设置背景音乐循环，时间与视频时间一致
audio = afx.audio_loop( audio_clip, duration=video_clip.duration)
#视频声音和背景音乐，音频叠加
audio_clip_add = CompositeAudioClip([video_audio_clip,audio])

#视频写入背景音
final_video = video_clip.set_audio(audio_clip_add)

#将处理完成的视频保存
final_video.write_videofile("video_bgm.mp4")