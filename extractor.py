#!/usr/bin/env python3
# Copyright 2023 Jiro Hayashi <hayashi.jiro@tuta.io>
#
# Licensed under the terms of the GNU GPL v3, or any later version.
import sys
import re
import os

# Help info
if len(sys.argv) <= 1 or sys.argv[1] == "help" or sys.argv[1] == "--help":
    print(
        """
    Higurashi Japanese text extractor
    python extractor.py <chapter or game location> <optional: output directory>
    * To see this message use:
        extractor.py --help

    * To extract a chapter without audio support use:
        extractor.py <name of chapter>
        Ex: extractor.py onikakushi

    * To extract a chapter with audio use:
        extractor.py </path/to/HigurashiEpXX_Data/>
        Ex: extractor.py ~/.local/share/Steam/steamapps/common/Higurashi\\ When\\ They\\ Cry/HigurashiEp01_Data/
          """
    )
    exit(0)

CHAPTERS = {
    "onikakushi": [
        ("onik_op", "Opening 1"),
        ("onik_000", "Opening 2"),
        ("onik_001", "Day 1"),
        ("onik_002", "Day 2"),
        ("onik_003", "Day 3"),
        ("onik_004", "Day 4"),
        ("onik_005", "Day 5"),
        ("onik_009", "Day 9.1"),
        ("onik_009_02", "Day 9.2"),
        ("onik_010", "Day 10"),
        ("onik_011", "Day 11"),
        ("onik_012", "Day 12"),
        ("onik_013", "Day 13"),
        ("onik_014", "Day 14.1"),
        ("onik_014_02", "Day 14.2"),
        ("onik_015", "Day 15.1"),
        ("onik_015_02", "Day 15.2"),
        ("onik_015_03", "Day 15.3"),
        ("onik_tips_01", "Tip 1"),
        ("onik_tips_02", "Tip 2"),
        ("onik_tips_03", "Tip 3"),
        ("onik_tips_04", "Tip 4"),
        ("onik_tips_05", "Tip 5"),
        ("onik_tips_06", "Tip 6"),
        ("onik_tips_07", "Tip 7"),
        ("onik_tips_08", "Tip 8"),
        ("onik_tips_09", "Tip 9"),
        ("onik_tips_10", "Tip 10"),
        ("onik_tips_11", "Tip 11"),
        ("onik_tips_12", "Tip 12"),
        ("onik_tips_13", "Tip 13"),
        ("onik_tips_14", "Tip 14"),
        ("onik_tips_15", "Tip 15"),
        ("onik_tips_16", "Tip 16"),
        ("onik_tips_17", "Tip 17"),
        ("onik_tips_18", "Tip 18"),
        ("onik_tips_19", "Tip 19"),
        ("onik_tips_20", "Tip 20"),
        ("omake_01", "All-Cast Review"),
    ],
    "watanagashi": [
        ("wata_ep_01", "Opening 1"),
        ("wata_ep_02", "Opening 2"),
        ("wata_001", "Day 1"),
        ("wata_002", "Day 2"),
        ("wata_003", "Day 3"),
        ("wata_004", "Day 4"),
        ("wata_005", "Day 5"),
        ("wata_006", "Day 6"),
        ("wata_007", "Day 7"),
        ("wata_008", "Day 8"),
        ("wata_009", "Day 9.1"),
        ("wata_009_02", "Day 9.2"),
        ("wata_010", "Day 10.1"),
        ("wata_010_02", "Day 10.2"),
        ("wata_010_03", "Day 10.3"),
        ("wata_010_04", "Day 10.4"),
        ("wata_011", "Day 11.1"),
        ("wata_011_02", "Day 11.2"),
        ("wata_012", "Day 12.1"),
        ("wata_012_02", "Day 12.2"),
        ("wata_012_03", "Dat 12.3"),
        ("wata_tips_01", "Tip 1"),
        ("wata_tips_02", "Tip 2"),
        ("wata_tips_03", "Tip 3"),
        ("wata_tips_04", "Tip 4"),
        ("wata_tips_05", "Tip 5"),
        ("wata_tips_06", "Tip 6"),
        ("wata_tips_07", "Tip 7"),
        ("wata_tips_08", "Tip 8"),
        ("wata_tips_09", "Tip 9"),
        ("wata_tips_10", "Tip 10"),
        ("wata_tips_11", "Tip 11"),
        ("wata_tips_12", "Tip 12"),
        ("wata_tips_13", "Tip 13"),
        ("wata_tips_14", "Tip 14"),
        ("wata_tips_15", "Tip 15"),
        ("wata_tips_16", "Tip 16"),
        ("wata_tips_17", "Tip 17"),
        ("wata_tips_18", "Tip 18"),
        ("wata_tips_19", "Tip 19"),
        ("wata_tips_20", "Tip 20"),
        ("wata_tips_21", "Tip 21"),
        ("wata_tips_22", "Tip 22"),
        ("wata_tips_23", "Tip 24"),
        ("wata_tips_24", "Tip 23"),
        ("omake_02", "All-Cast Review"),
    ],
    "tatarigoroshi": [
        ("tata_ep01", "Opening 1"),
        ("tata_ep02", "Opening 2"),
        ("tata_001", "Day 1"),
        ("tata_002", "Day 2"),
        ("tata_003", "Day 3"),
        ("tata_004", "Day 4"),
        ("tata_005", "Day 5"),
        ("tata_008", "Day 8.1"),
        ("tata_008_02", "Day 8.2"),
        ("tata_009", "Day 9.1"),
        ("tata_009_02", "Day 9.2"),
        ("tata_010", "Day 10.1"),
        ("tata_010_02", "Day 10.2"),
        ("tata_010_03", "Day 10.3"),
        ("tata_010_04", "Day 10.4"),
        ("tata_011", "Day 11.1"),
        ("tata_011_02", "Day 11.2"),
        ("tata_011_03", "Day 11.3"),
        ("tata_012", "Day 12"),
        ("tata_013", "Day 13.1"),
        ("tata_013_02", "Day 13.2"),
        ("tata_014", "Day 14"),
        ("tata_tips_01", "Tip 1"),
        ("tata_tips_02", "Tip 2"),
        ("tata_tips_03", "Tip 3"),
        ("tata_tips_04", "Tip 4"),
        ("tata_tips_05", "Tip 5"),
        ("tata_tips_06", "Tip 6"),
        ("tata_tips_07", "Tip 7"),
        ("tata_tips_08", "Tip 8"),
        ("tata_tips_09", "Tip 9"),
        ("tata_tips_10", "Tip 10"),
        ("tata_tips_11", "Tip 11"),
        ("tata_tips_12", "Tip 12"),
        ("tata_tips_13", "Tip 13"),
        ("tata_tips_14", "Tip 14"),
        ("tata_tips_15", "Tip 15"),
        ("tata_tips_16", "Tip 16"),
        ("tata_tips_17", "Tip 17"),
        ("tata_tips_18", "Tip 18"),
        ("tata_tips_19", "Tip 19"),
        ("omake_03", "All-Cast Review"),
    ],
    "himatsubushi": [
        ("hima_001", "Day 1"),
        ("hima_002", "Day 2.1"),
        ("hima_002_02", "Day 2.2"),
        ("hima_002_03", "Day 2.3"),
        ("hima_003", "Day 3.1"),
        ("hima_003_02", "Day 3.2"),
        ("hima_003_03", "Day 3.3"),
        ("hima_003_03a", "Day 3.3a"),
        ("hima_003_04", "Day 3.4"),
        ("hima_003_05", "Day 3.5"),
        ("hima_004", "Day 4"),
        ("hima_badend", "Bad Ending"),
        ("hima_tips_01", "Tip 1"),
        ("hima_tips_02", "Tip 2"),
        ("hima_tips_03", "Tip 3"),
        ("hima_tips_04", "Tip 4"),
        ("hima_tips_05", "Tip 5"),
        ("hima_tips_06", "Tip 6"),
        ("hima_tips_07", "Tip 7"),
        ("hima_tips_08", "Tip 8"),
        ("hima_tips_09", "Tip 9"),
        ("hima_tips_10", "Tip 10"),
        ("hima_tips_11", "Tip 11"),
        ("hima_tips_12", "Tip 12"),
        ("hima_tips_13", "Tip 13"),
        ("hima_tips_14", "Tip 14"),
        ("omake_04", "All-Cast Review"),
    ],
    "meakashi": [
        ("_meak_ep_01", "Opening 1"),
        ("_meak_ep_02", "Opening 2"),
        ("_meak_ep_03", "Opening 3"),
        ("_meak_001", "Day 1"),
        ("_meak_002", "Da2 2"),
        ("_meak_003", "Day 3"),
        ("_meak_004", "Day 4"),
        ("_meak_005", "Day 5"),
        ("_meak_006", "Day 6"),
        ("_meak_007", "Day 7"),
        ("_meak_008", "Day 8"),
        ("_meak_009", "Day 9"),
        ("_meak_010", "Day 10"),
        ("_meak_011", "Day 11"),
        ("_meak_012", "Day 12"),
        ("_meak_013", "Day 13"),
        ("_meak_014_1", "Day 14.1"),
        ("_meak_014_2", "Day 14.2"),
        ("_meak_015_1", "Day 15.1"),
        ("_meak_015_2", "Day 15.2"),
        ("_meak_016_1", "Day 16.1"),
        ("_meak_016_2", "Day 16.2"),
        ("_meak_017", "Day 17"),
        ("_meak_018", "Day 18"),
        ("_meak_019_1", "Day 19.1"),
        ("_meak_019_2", "Day 19.2"),
        ("_meak_020", "Day 20"),
        ("_meak_021_1", "Day 21.1"),
        ("_meak_021_2", "Day 21.2"),
        ("_meak_022_1", "Day 22.1"),
        ("_meak_022_2", "Day 22.2"),
        ("_meak_023", "Day 23"),
        ("_meak_024", "Day 24"),
        ("_meak_024a", "Day 24a"),
        ("_meak_024b", "Day 24b"),
        ("_meak_badend", "Bad Ending"),
        ("_meak_tips_01", "Tip 1"),
        ("_meak_tips_02", "Tip 2"),
        ("_meak_tips_03", "Tip 3"),
        ("_meak_tips_04", "Tip 4"),
        ("_meak_tips_05", "Tip 5"),
        ("_meak_tips_06", "Tip 6"),
        ("_meak_tips_07", "Tip 7"),
        ("_meak_tips_08", "Tip 8"),
        ("_meak_tips_09", "Tip 9"),
        ("_meak_tips_10", "Tip 10"),
        ("_meak_tips_11", "Tip 11"),
        ("_meak_tips_12", "Tip 12"),
        ("_meak_tips_13", "Tip 13"),
        ("_meak_tips_14", "Tip 14"),
        ("_meak_tips_15", "Tip 15"),
        ("_meak_tips_16", "Tip 16"),
        ("_meak_tips_17", "Tip 17"),
        ("_meak_tips_18", "Tip 18"),
        ("_meak_tips_19", "Tip 19"),
        ("_meak_tips_20", "Tip 20"),
        ("_meak_tips_21", "Tip 21"),
        ("_meak_tips_22", "Tip 22"),
        ("_meak_tips_23", "Tip 23"),
        ("staffroom", "Staffroom"),
    ],
}

ACTOR_COLOR_RE = re.compile("<.*?</color>")
COLOR_RE = re.compile("=(.*?)>")
ACTOR_RE = re.compile(">(.*?)<")

out_dir = "./out/"
chapter = ""
script_path = ""
voice_path = ""
extra_flag = False
html_body = '<body style="background-color:black;color:white;">'
html_table = '<div style="display:flex;flex-direction:column;" >'

# Parse arguments
if sys.argv[1] in CHAPTERS.keys():  # 07th-res installation
    chapter = sys.argv[1]
    script_path = "./07th_res/{}/Update/".format(chapter)
    voice_path = "./07th_res/{}/voice/".format(chapter)
    if os.path.exists(script_path) and os.path.exists(voice_path):
        print(
            "'{}' detected as chapter.\nExtracting WITHOUT audio support.".format(
                chapter
            )
        )
    else:
        print("Cannot find the 07th-res submodules.")
        exit(1)
else:  # Manual game installation
    game_location = sys.argv[1].rstrip("/")
    script_path = "{}/StreamingAssets/Update/".format(game_location)
    voice_path = "{}/StreamingAssets/voice/".format(game_location)
    if os.path.exists(script_path) and os.path.exists(voice_path):
        chapter_num = int(re.findall("Ep0(\d)", game_location)[0])
        chapter = list(CHAPTERS.keys())[chapter_num - 1]
        extra_flag = True
        print(
            "'{}' detected as chapter.\nExtracting WITH audio support.".format(chapter)
        )
    else:
        print("The provided path does not seem to be valid!")
        exit(1)

# Parse optional out directory arg
if len(sys.argv) >= 3:
    out_dir = sys.argv[2].rstrip("/")


def color_to_html(input):
    color = COLOR_RE.findall(input)[0]
    character = ACTOR_RE.findall(input)[0]
    return '<div style="color: {}; font-weight: bold;">{}</div>'.format(
        color, character
    )


# Parse Japanese "OutputLine" into an HTML paragraph
def line_to_html_paragraph(split_line):
    return "<p>{}</p>".format(split_line[1])


# Parse modded voice line "ModPlayVoice:S" into an HTML audio
def voice_to_html_audio(split_line):
    audio_name = split_line[2].strip().replace('"', "")
    src = voice_path + audio_name + ".ogg"
    return """<audio controls preload="none">
            <source src="{}" type="audio/ogg">
            </audio>""".format(
        src
    )


def actor_to_html_color(line):
    return


print(out_dir)
os.makedirs(os.path.dirname(out_dir + "/"), exist_ok=True)
for script_name in CHAPTERS[chapter]:
    out_file = open("{}/higurashi_{}.html".format(out_dir, script_name[0]), "w")
    script_file = open(script_path + "{}.txt".format(script_name[0]), "r")
    lines = script_file.readlines()

    html_table += '<a href="./higurashi_{}.html">{}</a>'.format(
        script_name[0], script_name[1]
    )
    out_file.write(html_body)
    out_file.write('<a href="./main.html" >All chapters</a>')

    for line in lines:
        stripped_line = line.strip().replace("\u3000", "")
        split_line = stripped_line.split(",")

        if stripped_line.startswith("OutputLine(NULL,"):  # Text line
            out_file.write(line_to_html_paragraph(split_line))

        result = ACTOR_COLOR_RE.search(line)
        if result is not None:
            out_file.write(color_to_html(result.group(0)))

        if extra_flag and stripped_line.startswith("ModPlayVoiceLS"):
            out_file.write(voice_to_html_audio(split_line))

    out_file.write('<a href="./main.html" >All chapters</a>')
    out_file.write("</body>")
    out_file.close()
    script_file.close()

main_file = open("{}/main.html".format(out_dir), "w")
main_file.write(html_body)
main_file.write(chapter)
main_file.write(html_table + "</div>" + "</body>")
main_file.close()
