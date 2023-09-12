# WhatsApp-stats
Enter the chat on WhatsApp, press 3 dots -> "More" -> "Export chat" -> "Without media" and send .txt file to yourself somewhere where you can download it from your pc.

In the "Input" folder in the project make a folder for that chat and put the exported file there. Exported files must be named like the name of the folder + 1/2/3... 
For example, if the name of the folder is "person", chat files are "person1", "person2", "person3"...

Why are there more chat files? Well, you can export only 40k messages from WhatsApp. This program can work with more than 40k messages if you have them stored. 
For example, you exported 35k messages a month ago and stored them in that folder. In last month you had 10k new messages. When you export a new file, it will have 40k messages. When you put it in the input folder with the old file and run the program, it will work with 45k messages.
If you have more input files, they must overlap.

Output files are in the "Stats" folder. After running the program, you can zip those files and keep them somewhere if you want, because they will be deleted after a new run.

There is one border case that will not work. For example, if the last 10 messages from the first input file are the same and are sent in the same minute from the same person, and also the first 10 messages from the second input file, you can't know if there should be 11 or 20 messages like that, so don't spam same messages if you don't have to. :) 
