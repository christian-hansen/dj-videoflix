import subprocess


def convert_360p(source):
    file_name = source.split('.')
    new_file_name = file_name[0] + '_360p.mp4'
    cmd = 'ffmpeg -i "{}" -s 640x360 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(
        source, new_file_name)
    subprocess.run(cmd, capture_output=True)
