import os, subprocess

image_files = [f[:-5] for f in os.listdir() if f[-5:] == ".html"]
for i in image_files:
	subprocess.call("wkhtmltoimage " + i + ".html " + i + ".png", shell=True)
	

