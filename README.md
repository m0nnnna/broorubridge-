# broorubridge
Szuru Brooru Grabber Bridge

Let's say you have a Szuru Brooru instace and use the program Grabber Brooru.

Let's also say that you use Grabber to download images from the vast number of Broorus out there.

Did you know it's possible to configure Grabber to generate a .txt file when downloading an image containing all tehe tags? Due to NTFS limits this is needed.

This script is made to be ran, or with some editing turning it into a watcher, after downloading a bunch of files through Grabber. 

Fill in the needed 3 lines in the script then run. What will happen is a new .txt file will show in your picture directory. This is here so it can keep track of all the file names, this prevents doubles from being uploaded as Szuru does try to track it but not really. 

All files that are uploaded without issue are deleted, all files that are doubles are also deleted, all files that do not upload will not be deleted so you can review. 

All .txt files containing tags will also be deleted.

There is some small amount of config in Grabber needed I will need to update this with how to do it. 

This can also work with other things as well, the only things it needs is an image file, and a .txt file containing the tags 1 tag per line. It will upload and all the tags.
