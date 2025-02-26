import cv2
import os

def extract_frames(video_path, output_dir, frame_rate):
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    
    # 确保视频文件成功打开
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 帧计数器
    frame_count = 0
    
    # 读取视频的帧
    while True:
        ret, frame = cap.read()
        
        # 确保成功读取帧
        if not ret:
            break
        
        # 每隔指定帧率抽取一帧
        if frame_count % frame_rate == 0:
            # 构建输出文件路径
            output_path = os.path.join(output_dir, f"frame_{frame_count}.png")
            # 保存帧为PNG格式
            cv2.imwrite(output_path, frame)
        
        frame_count += 1
    
    # 释放视频对象
    cap.release()

# 调用抽帧函数
video_path = ".\\self_made.mp4"  # 视频文件路径
output_dir = ".\\images"    # 输出帧的目录
frame_rate = 1                 # 帧率，每隔多少帧抽取一帧

extract_frames(video_path, output_dir, frame_rate)
