# WhatsApp-stats v0.5
Enter the chat on WhatsApp, press 3 dots -> "More" -> "Export chat" -> "Without media" and send .txt file to yourself somewhere where you can download it from your PC.

Enter the app. Import the .txt file in the Import tab. In the Run tab, select the chat name you entered in the Import tab and click Run. You can see your stats in the other 4 tabs.

You can export only 40k messages from WhatsApp. This program can work with more than 40k messages if you have them stored in a database. 
For example, you exported 35k messages a month ago and stored them in that folder. Last month you had 10k new messages. When you export a new file, it will have 40k messages. When you put it in the input folder with the old file and run the program, it will work with 45k messages.
If you have more input files, THEY MUST OVERLAP.

There is one border case that will not work. For example, if the last 10 messages from the first input file are the same and are sent in the same minute from the same person, and also the first 10 messages from the second input file, you can't know if there should be 11 or 20 messages like that, so don't spam the same messages if you don't have to. :) 
