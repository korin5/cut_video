import cv2
import subprocess
import os

# 输入的视频需要是连续的.mp4或.mkv或.h264或.h265文件
input_video_dir = './20240102/直线测试/video（三车道）'
output_video_dir = './20240102_Output'
id_start = 3847  # 第一个视频第一帧的id（左上角显示）
id_cut = [      # 视频切片的id范围列表
    [4042,4750],
    [4971,5500],
    [5870,6450],
]

def cut_video(input_video_dir:str,output_video_dir:str,id_start:int,id_cut:list[list[int]]):
    video_files = [os.path.join(input_video_dir, f) for f in os.listdir(input_video_dir) if f.endswith(('.mp4','.mkv','h264','h265'))]
    if len(video_files) == 0:
        print("没有找到视频文件")
        exit()
    
    video = cv2.VideoCapture(video_files[0])
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    video.release()

    outputs = []
    fourcc = cv2.VideoWriter.fourcc(*'H264')
    for i in range(len(id_cut)):
        outputs.append(cv2.VideoWriter(f"{output_video_dir}/{id_cut[i][0]}-{id_cut[i][1]}.mkv", fourcc, fps, (width, height)))

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
                    print("done: "+f"{id_cut[i][0]}-{id_cut[i][1]}.mkv")
                    outputs[i].release()
                if id_cut[-1][1]+3 == current_id: return

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
        print(result)
        
    do_remove =  input("remove old output? [y|n]\n")
    if do_remove == 'y':
        for file in video_files:
            os.remove(file)

if __name__ == "__main__":
    cut_video(input_video_dir,output_video_dir,id_start,id_cut)
    # to_HEVC(output_video_dir)
