import subprocess

def convert1080p(source, destination):
    cmd = ['ffmpeg', '-i', source, '-s', 'hd1080', '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-strict', '-2', destination]
    run = subprocess.run(cmd, capture_output=True)

def convert720p(source, destination):
    cmd = ['ffmpeg', '-i', source, '-s', 'hd720', '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-strict', '-2', destination]
    run = subprocess.run(cmd, capture_output=True)

def convert360p(source, destination):
    cmd = ['ffmpeg', '-i', source, '-s', '640x360', '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-strict', '-2', destination]
    run = subprocess.run(cmd, capture_output=True)

def createThumbnail(source, destination):
    cmd = ['ffmpeg', '-i', source, '-ss', '00:00:00', '-frames:v', '1', destination]
    run = subprocess.run(cmd, capture_output=True) 