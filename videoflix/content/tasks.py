import subprocess

def convert720p(source):
    new_file_name = source.replace("mp4", "_720p.mp4") 
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)    
    run = subprocess.run(cmd, capture_output=True)

def convert480p(source):
    new_file_name = source.replace(".mp4", "_480p.mp4")
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)    
    run = subprocess.run(cmd, capture_output=True)
    #subprocess.run(cmd)