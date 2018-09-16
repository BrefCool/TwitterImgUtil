import subprocess
import os
import time

def resize_images(screen_name):
    image_path = 'download_images/' + screen_name
    if not os.path.exists(image_path+'/for_video'):
        os.mkdir(image_path+'/for_video')
    cmd = ['ffmpeg', '-i', image_path+'/image-%05d.jpg', '-vf', 'scale=640:480',
           image_path+'/for_video/image-%05d.png']
    subprocess.call(cmd)

def convert_images_to_video(screen_name):
    resize_images(screen_name)
    image_path = 'download_images/' + screen_name + '/for_video'
    output_path = 'download_images/' + screen_name + '/' + screen_name + '_movie.mp4'
    if os.path.exists(output_path):
        os.remove(output_path)
    cmd = ['ffmpeg', '-r', '1/2', '-i', image_path+'/image-%05d.png', '-c:v',
           'libx264', '-r', '30', '-pix_fmt', 'yuv420p', output_path]
    subprocess.call(cmd)