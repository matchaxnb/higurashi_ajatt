# Archived as of October 2024

This tool's development has been archived in favor of a [better webapp rewrite with extended functionality!](https://kitsugo.com/app/higurashi-extractor/)

The webapp version features better styling, a graphical setup and is entirely contained within a web browser, requiring no downloading or execution of Python scripts.
**If you want to use the Higurashi Japanese Text Extractor, use the link to the webapp above!**

# Higurashi - Japanese Text Extractor 🇯🇵

This tool allows you to extract all Japanese text and dialogues from the "Higurashi When They Cry" games into an HTML format. The intended usage for this tool is to have the Japanese text of the games in an accessible interface to aid in learning Japanese.

You can use the extracted text to look up words with copy-paste or open the HTML format in your browser with a dictionary tool like [Rikaitain](https://github.com/Ajatt-Tools/rikaitan#rikaitan) to utilize features like automatic [Anki](https://tatsumoto.neocities.org/blog/setting-up-yomichan#anki-settings) card generation.

**Note:** The chronological order of sections has not been verified, and it has not been tested that 100% of all data is extracted without any minor losses.

## Features

-   ✅ Full support for all "When They Cry" games
-   🎧 Embedded audio clips to replay voice lines\*
-   🎨 Character color codes
-   🇯🇵 Only Japanese text extraction to [maximize your immersion](https://tatsumoto.neocities.org/blog/should-i-watch-anime-with-english-subtitles)
-   🎚️ Extraction of all extra content from the 07th-mod + respecting censorship level

\* _requires manual installation of the game with 07th-mod_

![screenshot of primary features](https://github.com/kitsugo/higurashi_ajatt/assets/32716622/59a9a318-c25a-4952-b489-c0abc1bf4869)

## How to use / Installation

-   Install [Python](https://www.python.org/downloads/) on your system if you haven't yet
-   Download the file `extractor.py` or clone this repository (cloning is only necessary if you do not have the games installed and don't need audio support)

-   Audio support:

    -   Install your desired game and install the [07th-mod](https://07th-mod.com/wiki/Higurashi/Higurashi-Getting-started/) for it
    -   Find the location of the **data folder** of your desired game on your system
        > Example: .../steamapps/common/Higurashi When They Cry/**HigurashiEp01_Data/**
    -   Run the downloaded script and provide the **full path to the game's data folder** like so:  
        `python extractor.py <path/to/HigurashiEpXX_Data/>`

-   No Audio support:

    -   In the checked out repository, run these two commands:  
        `git submodule init`  
        `git submodule update ./07th_res/<chapter>`
    -   Run the downloaded script with the name of your desired chapter like so:  
        `python3 extractor.py onikakushi`

-   The script will produce a directory with a `main.html` file and various HTML files for all sections in the game. If you want, you can specify your own output directory like so:  
    `python3 extractor.py <1st argument> /path/to/out`

-   Open the `main.html` file in your web browser by...

    > -   dragging and dropping the main.html file into your browser window
    > -   manually typing the local path to the main.html into your URL bar `file:///path/to/main.html`

-   Choose any desired game section from the list and enjoy!

## Troubleshooting
