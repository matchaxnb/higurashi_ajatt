**WORK IN PROGRESS**  
This tool is currently a WIP.  
Basic extraction works as expected but without guarantee for full functionality and text / audio completeness.  
Currently only Onikakushi supported.  
Tested only on Linux thus far.  
Some bugs are to be expected...

# Higurashi When They Cry - Japanese Text Extractor 🇯🇵

This tool allows you to extract all Japanese text and dialogues from the "Higurashi When They Cry" games into an HTML format. The intended usage for this tool is to have the Japanese text of the games in an accessible interface to aid in learning Japanese.

You can use the extracted text to look up words with copy-paste or (more preferably) open the HTML format in your browser with a dictionary tool like [Rikaitain](https://github.com/Ajatt-Tools/rikaitan#rikaitan) to utilize features like automatic [Anki](https://tatsumoto.neocities.org/blog/setting-up-yomichan#anki-settings) card generation.

## Features

-   ✅ ~~Full support for all "When They Cry" games~~
-   🎧 Embedded audio clips to replay voice lines\*
-   📷 Character color codes and ~~icons~~\*
-   🇯🇵 Only Japanese text extraction to [maximize your immersion](https://tatsumoto.neocities.org/blog/should-i-watch-anime-with-english-subtitles)

\* _requires manual installation of the game with 07th-mod_

## How to use / Installation

1. Install [Python](https://www.python.org/downloads/) on your system if you haven't yet
2. Download the `extractor.py` file directly (if you have the game installed) or by cloning this repository (if you wish to use externally provided game data).

> Audio + Icon support:

-   Install your desired game and install the [07th-mod](https://07th-mod.com/wiki/Higurashi/Higurashi-Getting-started/) for it
-   Find the location of the **data folder** of your desired game on your system
    > Example: .../steamapps/common/Higurashi When They Cry/**HigurashiEp01_Data/**
-   Run the downloaded script and provide the **full path to the game's data folder** like so:  
     `python extractor.py <path/to/HigurashiEpXX_Data/>`

> No Audio + Icon support:

-   In the checked out repository, run `git submodule init` and `git submodule update`
-   Run the downloaded script with the name of your desired chapter like so:  
     `python3 extractor.py onikakushi`
-   The script will produce a directory with a `main.html` file and various HTML files for all sections in the game. If you want, you can specify your own output directory like so:  
     `python3 extractor.py <1st argument> /path/to/out`

3. Open the file in your web browser by...

    > - dragging and dropping the main.html file into your browser window
    > - manually typing the local path to the main.html into your URL bar `file:///path/to/main.html`

4. Choose any desired game section from the list and enjoy!

## Troubleshooting
