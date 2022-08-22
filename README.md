# Intro

This project is capable of extracting the audio files and subtitles from audiobooks on the site `missevan.com`.

# Set up

- You will need python and git installed
- Clone this repository to your PC
- Open a command prompt
- Create a virtual environment with `python -m venv .venv`
- Install dependencies with `.venv/bin/pip install -r requirements.txt`

# Configuration

- Log in to `missevan.com` in a browser, as usual
- Using your browser's dev tools, you now need to find the cookies for this site
    * e.g. For Chrome...
    * Press F12 to bring up the developer console
    * Find the `Application` tab at the top of the console
    * On the left, under `Storage`, there is section for cookies
    * Expand it, and you will see the site `https://www.missevan.com`. Click on it.
- Find the value of the cookie `token` in particular. It will look nonsensical - probably about 91 characters long.
- You also need the numeric ID of one episode in the series to which you are listening. For example, if the URL is `https://www.missevan.com/sound/player?id=5445688` then `5445688` is the value you need.
- Edit the file `main.py` and put both these values in the respective places marked with `TODO`
 
# To run

- At the command line, run `.venv/bin/python main.py`

# Downloading subtitles

No token required this time. You just need one episode ID per drama you wish to download.

In the file `subs.py`, put those numeric values into the array, replacing the placeholder values. Make sure you leave the comma at the end of each line.

At the command line, run `.venv/bin/python subs.py`

You should end up with one subdirectory per drama. In it will be some `.html` files - this is the raw content downloaded from `missevan.com`, in case you need it later. Primarily, the `.txt` files are of interest as these contain the filtered subtitles.