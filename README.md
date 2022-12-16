# AutoKim
## About
A bot that utilises selenium to automate changing episodes on Kimcartoon

## Set-up
Requires Google Chrome, was written targeting `Version 108.0.5359.99`

From within the project directory, run: `pip install -r requirements.txt`

## Running
1. Set URL in `history.txt` to episode of show you want to start watching
2. From within the project directory, run: `python autokim.py`

Episodes will fullscreen and play automatically.


## Known issues
- Doesn't support auto-switching seasons.
- Script can't interact with `Hserver` video stream in event of fallback event from `Oserver`
