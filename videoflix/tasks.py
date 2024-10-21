import subprocess

def convert_video(source, resolution):
    resolutions = {
        '360p': '640x360',
        '720p': 'hd720',
        # '1080p': 'hd1080',
    }

    file_name = source.split('.')
    new_file_name = f"{file_name[0]}_{resolution}.mp4"
    
    cmd = [
        'sudo',
        'ffmpeg',
        '-i', source,
        '-s', resolutions[resolution],
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        new_file_name
    ]

    subprocess.run(cmd, capture_output=True)