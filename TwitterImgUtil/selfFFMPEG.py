import subprocess
import os

def convert_images_to_video(screen_name):
    image_path = 'download_images/' + screen_name + '/image-%05d.jpg'
    output_path = 'download_images/' + screen_name + '/' + screen_name + '_movie.mp4'
    if os.path.exists(output_path):
        os.remove(output_path)
    cmd = ['ffmpeg', '-i', image_path, '-framerate', '1/5', output_path]
    subprocess.call(cmd)