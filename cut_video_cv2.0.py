import cv2
import subprocess
import os

# 输入的视频需要是连续的.mp4或.mkv文件
input_video_dir = './20231216_171535_Video'
output_video_dir = './20231216_171535_Video_Output2'
id_start = 608  # 第一个视频第一帧的id（左上角显示）
id_cut = [      # 视频切片的id范围列表
    [9056,10150],
    [11733,12745],
    [13797,14856],
    [34943,35789],
    [36901,37688]
]

def cut_video(input_video_dir:str,output_video_dir:str,id_start:int,id_cut:list[list[int]]):
    video_files = [os.path.join(input_video_dir, f) for f in os.listdir(input_video_dir) if f.endswith(('.mp4','.mkv'))]
    if len(video_files) == 0:
        print("没有找到视频文件")
        exit()
    
    video = cv2.VideoCapture(video_files[0])
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    video.release()

    outputs = []
    fourcc = cv2.VideoWriter.fourcc(*'MJPG')
    for i in range(len(id_cut)):
        outputs.append(cv2.VideoWriter(f"{output_video_dir}/{id_cut[i][0]}-{id_cut[i][1]}.mp4", fourcc, fps, (width, height)))

    current_id = id_start
    for file in video_files:
        video = cv2.VideoCapture(file)

        while True:
            ret, frame = video.read()
            if not ret: break
            for i in range(len(id_cut)):
                if id_cut[i][0] <= current_id <= id_cut[i][1]:
                    outputs[i].write(frame)
                if current_id == id_cut[i][1]+1:
                    print("done: "+f"{id_cut[i][0]}-{id_cut[i][1]}.mp4")
                    outputs[i].release()
                if id_cut[-1][1]+1 == current_id: return

            current_id += 1

        video.release()
        print("pass: "+file+" | current_id: "+str(current_id))
    return

def to_HEVC(video_dir:str):
    video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith(('.mp4','.mkv'))]
    for file in video_files:
        command = f"ffmpeg -i {file} -map 0 -c:v libx264 -c:a copy -b:v 10M {file}_HEVC.mp4"
        print("run: " + command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        os.remove(file)

if __name__ == "__main__":
    cut_video(input_video_dir,output_video_dir,id_start,id_cut)
    to_HEVC(output_video_dir)
