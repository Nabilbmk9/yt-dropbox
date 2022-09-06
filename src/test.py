import time
import progressbar


video_lis = ["je", "suis", "un", "test"]


with progressbar.ProgressBar(max_value=751.68) as bar:
    for i, z  in enumerate(video_lis):
        time.sleep(1)
        bar.update(i+5.6875454564654564544)