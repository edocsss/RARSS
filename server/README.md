# Quick Setup
1. The raw folder is **NOT** stored in this GitHub. Please asked me or Dr. Wang Di for the full raw data. Then, put the raw data into `<path_to_server_dir>/data/raw`.
2. If you are the next FYP student, the zipped folders containing the self-contained source codes should already have the raw data and database folder inside. Otherwise, you will need to put the raw data in `server/data/raw` and the database folder in `server/data/db` manually.
3. Use PyCharm!! This handles a lot of PYTHONPATH issues much easier.
4. In order to use the classifiers, you will have to perform data preprocessing again **for each subject** and **for each activity**.

# Knowledge Requirements
This project actually made use of many different frameworks and technologies. 
The README and Wiki pages cannot be expected to explain every single step how to use these frameworks and technologies.
However, these are common frameworks so you will be able to find many resources in the internet easily.

**For most technologies**, you will not need to actually go and read the details unless you are trying to do something totally different.
In most cases, I believe you can see how I implemented it, find the patterns, and do a similar thing.

Here is the list of technologies used:

1. Tornado Web Server
2. MongoDB
3. Android OS
4. Tizen OS (with WebSocket)
5. AngularJS (with WebSocket)
6. ngrok (tunnelling)
7. bower
8. npm

# Important Note
This quick setup note is **NOT** complete! Please read my FYP report and the Wiki pages in this repository. The FYP report focuses on the ideas from the high level perspective while the Wiki pages give more technical details.
