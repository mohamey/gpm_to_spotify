# GPM To Spotify Migration Tool

This tool migrates your Google Play Music Library to Spotify. This lets you start using Spotify with your existing 
library so you don't need to manually seed the Spotify Recommender System. At the moment, this tool only migrates your
library, functionality for Playlists is coming.

This tool doesn't guarantee a one-to-one match for each track, as each track from your GPM Library is matched using
Spotify's search functionality using fuzzy-matching. 

## Requirements
* Python 3.7+
* Pip3
* VirtualEnv is recommended

## Usage
Clone this repo and navigate to the root directory.

```sh
# Install the requirements
pip install -r requirements.txt

# Run the CLI
python command_line_interface.py <username_here>
```
