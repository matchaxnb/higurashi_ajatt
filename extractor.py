#!/usr/bin/env python3
# Copyright 2023 Jiro Hayashi <hayashi.jiro@tuta.io>
#
# Licensed under the terms of the GNU GPL v3, or any later version.
import sys
import re
import os

# Help info
if len(sys.argv) <= 1 or sys.argv[1] == "help" or sys.argv[1] == "--help":
    print("""
    Higurashi Japanese text extractor
    python extractor.py <chapter or game location> <optional: output directory>
    * To see this message use:
        extractor.py --help

    * To extract a chapter without audio + icon support use:
        extractor.py <name of chapter>
        Ex: extractor.py onikakushi

    * To extract a chapter with audio + icon use:
        extractor.py </path/to/HigurashiEpXX_Data/>
        Ex: extractor.py ~/.local/share/Steam/steamapps/common/Higurashi\\ When\\ They\\ Cry/HigurashiEp01_Data/
          """)
    exit(0)

CHAPTERS = {
    "onikakushi": [("onik_op", "Opening 1"), ("onik_000", "Opening 2"), ("onik_001", "Day 1"), ("onik_002", "Day 2"), ("onik_003", "Day 3"), ("onik_004", "Day 4"), ("onik_005", "Day 5"), ("onik_009", "Day 9.1"), ("onik_009_02", "Day 9.2"), ("onik_010", "Day 10"), ("onik_011", "Day 11"), ("onik_012", "Day 12"), ("onik_013", "Day 13"), ("onik_014", "Day 14.1"), ("onik_014_02", "Day 14.2"), ("onik_015", "Day 15.1"), ("onik_015_02", "Day 15.2"), ("onik_015_03", "Day 15.3"), ("onik_tips_01", "Tip 1"), ("onik_tips_02", "Tip 2"), ("onik_tips_03", "Tip 3"), ("onik_tips_04", "Tip 4"), ("onik_tips_05", "Tip 5"), ("onik_tips_06", "Tip 6"), ("onik_tips_07", "Tip 7"), ("onik_tips_08", "Tip 8"), ("onik_tips_09", "Tip 9"), ("onik_tips_10", "Tip 10"), ("onik_tips_11", "Tip 11"), ("onik_tips_12", "Tip 12"), ("onik_tips_13", "Tip 13"), ("onik_tips_14", "Tip 14"), ("onik_tips_15", "Tip 15"), ("onik_tips_16", "Tip 16"), ("onik_tips_17", "Tip 17"), ("onik_tips_18", "Tip 18"), ("onik_tips_19", "Tip 19"), ("onik_tips_20", "Tip 20"), ]}

ACTOR_COLOR_RE = re.compile("<.*?</color>")
COLOR_RE = re.compile("=(.*?)>")
ACTOR_RE = re.compile(">(.*?)<")

out_dir = "./out/"
chapter = ""
script_path = ""
voice_path = ""
extra_flag = False
html_body = "<body style=\"background-color:black;color:white;\">"
html_table = "<div style=\"display:flex;flex-direction:column;\" >"

# Parse arguments
if sys.argv[1] in CHAPTERS.keys():  # 07th-res installation
    chapter = sys.argv[1]
    script_path = "./07th_res/{}/Update/".format(chapter)
    voice_path = "./07th_res/{}/voice/".format(chapter)
    if os.path.exists(script_path) and os.path.exists(voice_path):
        print("'{}' detected as chapter.\nExtracting WITHOUT audio and icon support.".format(chapter))
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
        print("'{}' detected as chapter.\nExtracting WITH audio and icon support.".format(
            chapter))
    else:
        print("The provided path does not seem to be valid!")
        exit(1)

# Parse optional out directory arg
if len(sys.argv) >= 3:
    out_dir = sys.argv[2].rstrip("/")


def color_to_html(input):
    color = COLOR_RE.findall(input)[0]
    character = ACTOR_RE.findall(input)[0]
    return "<div style=\"color: {}; font-weight: bold;\">{}</div>".format(color, character)


# Parse Japanese "OutputLine" into an HTML paragraph
def line_to_html_paragraph(split_line):
    return "<p>{}</p>".format(split_line[1])


# Parse modded voice line "ModPlayVoice:S" into an HTML audio
def voice_to_html_audio(split_line):
    audio_name = split_line[2].strip().replace("\"", "")
    src = voice_path + audio_name + ".ogg"
    return """<audio controls preload="none">
            <source src="{}" type="audio/ogg">
            </audio>""".format(src)


def actor_to_html_color(line):
    return


os.makedirs(os.path.dirname(out_dir), exist_ok=True)
for script_name in CHAPTERS[chapter]:
    out_file = open(
        "{}/higurashi_{}.html".format(out_dir, script_name[0]), "w")
    script_file = open(script_path + "{}.txt".format(script_name[0]), "r")
    lines = script_file.readlines()

    html_table += "<a href=\"./higurashi_{}.html\">{}</a>".format(
        script_name[0], script_name[1])
    out_file.write(html_body)
    out_file.write("<a href=\"./main.html\" >All chapters</a>")

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

    out_file.write("<a href=\"./main.html\" >All chapters</a>")
    out_file.write("</body>")
    out_file.close()
    script_file.close()

main_file = open("{}/main.html".format(out_dir), "w")
main_file.write(html_body)
main_file.write(chapter)
main_file.write(html_table + "</div>" + "</body>")
main_file.close()
