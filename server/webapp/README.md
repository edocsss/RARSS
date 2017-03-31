# Running Tornado Server
1. Open PyCharm
2. Run `tornado_app.py`
3. If the port is being used, you can change it in `server/webapp/web_config.py`

# Running ngrok
By default, the Tornado server cannot be accessible by public internet. The tunnelling service `ngrok` gives us an easy way to access it from anywhere.

Setting up `ngrok`:

1. Download executable: [ngrok](https://ngrok.com/download)
2. Open terminal / command prompt
3. Change directory to where `ngrok` executable file is (the file you will get when you download and possibly unzip it)
4. Run ngrok: `ngrok http <port_number>` (the default port number of the tornado server is `5000`)
5. Take note of the unique ID in the URL shown in the terminal / command prompt
6. Update the ID in the textbox found in the smartphone and smartwatch application
7. **TO KILL** `ngrok`: CTRL + C (for both Windows and Mac/Linux)

Please note that every time ngrok is killed and restarted, a new unique ID will be generated and you have to change the one in the smartphone and smartwatch!
