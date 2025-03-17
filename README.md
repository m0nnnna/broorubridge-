# broorubridge
Szuru Brooru Grabber Bridge

Let's say you have a Szuru Brooru instace and use the program Grabber Brooru.

Let's also say that you use Grabber to download images from the vast number of Broorus out there.

Did you know it's possible to configure Grabber to generate a .txt file when downloading an image containing all tehe tags? Due to NTFS limits this is needed.

This script is made to be ran, or with some editing turning it into a watcher, after downloading a bunch of files through Grabber. 

In the script you will need to set your szuru url with http/https. Once you log in generate a login token then go to https://www.base64encode.org/ put inside username:token and hit generate. This will be used for auth. Then change directory from "title" to the directory you want it to monitor.

All files that are uploaded without issue are deleted, all files that are doubles are also deleted, all files that do not upload will not be deleted so you can review. 

All .txt files containing tags will also be deleted.

There is some small amount of config in Grabber needed I will need to update this with how to do it. 

This can also work with other things as well, the only things it needs is an image file, and a .txt file containing the tags 1 tag per line. It will upload and all the tags.

# Configure grabber

Go into grabber select Tools > Options expand Save > Separate log files > Add.

Name it tags, change it to suffex, for the suffex put in .txt and for the text file content paste 
```
rating:%rating%
%all:includenamespace,excludenamespace=general,unsafe,spaces,separator=\n%
```
