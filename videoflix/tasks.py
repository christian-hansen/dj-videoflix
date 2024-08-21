import subprocess


def convert_360p(source):
    # print("source", source)
    file_name = source.split('.')
    # print("file_name", file_name)
    new_file_name = file_name[0] + '_360p.mp4'
    # print("new_file_name", new_file_name)
    cmd = [
        'ffmpeg',
        '-i', source,
        '-s', '640x360',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        new_file_name
    ]

    # print('Executing command:', ' '.join(cmd))
    subprocess.run(cmd, capture_output=True)
