#!/usr/bin/env python3
# Copyright 2023 Jiro Hayashi <hayashi.jiro@tuta.io>
#
# Licensed under the terms of the GNU GPL v3, or any later version.
import sys
import re
import os

chapter = ""
script_path = ""
voice_path = ""
extra_flag = False

chapters = {
    "onikakushi": [("onik_op", "Opening 1"), ("onik_000", "Opening 2"), ("onik_001", "Day 1"), ("onik_002", "Day 2"), ("onik_003", "Day 3"), ("onik_004", "Day 4"), ("onik_005", "Day 5")

                   ]
}

if sys.argv[1] in chapters.keys():
    chapter = sys.argv[1]
    print("'{}' detected as chapter.\nExtracting WITHOUT audio and icon support.".format(
        chapter))
    # TODO: automatic submodule installation
    script_path = "./07th_res/{}/Update/".format(chapter)
    voice_path = "./07th_res/{}/voice/".format(chapter)

else:
    game_location = sys.argv[1].strip("/")
    print(game_location)
    script_path = "/{}/StreamingAssets/Update/".format(game_location)
    voice_path = "/{}/StreamingAssets/voice/".format(game_location)
    if os.path.exists(script_path) and os.path.exists(voice_path):
        chapter_num = re.findall("Ep0(\d)", game_location)
        chapter_num = int(chapter_num[0])
        chapter = list(chapters.keys())[chapter_num - 1]
        extra_flag = True
    else:
        print("Not all good")
        exit()

html_body = "<body style=\"background-color:black;color:white;\">"
html_table = "<div style=\"display:flex;flex-direction:column;\" >"

for file in chapters[chapter]:
    streamAssets = open(script_path + "{}.txt".format(file[0]), "r")
    lines = streamAssets.readlines()

    actorColorRegex = re.compile("<.*?</color>")
    hex_color_regex = re.compile("=(.*?)>")
    character_regex = re.compile(">(.*?)<")

    html_table += "<a href=\"./higurashi_{}.html\">{}</a>".format(
        file[0], file[1])
    out_file = open("./higurashi_{}.html".format(file[0]), "w")
    out_file.write(html_body)
    out_file.write("<a href=\"./main.html\" >All chapters</a>")

    def color_to_html(input):
        color = hex_color_regex.findall(input)[0]
        character = character_regex.findall(input)[0]
        return "<div style=\"color: {}; font-weight: bold;\">{}</div>".format(color, character)

    for line in lines:
        strippedLine = line.strip().replace("\u3000", "")
        splitLine = strippedLine.split(",")

        result = actorColorRegex.search(line)
        if result is not None:
            out_file.write(color_to_html(result.group(0)))

        if extra_flag and strippedLine.startswith("ModPlayVoiceLS"):
            src = strippedLine.split(",")
            src = src[2].strip().replace("\"", "")
            src = voice_path + src + ".ogg"
            out = """<audio controls preload="none">
            <source src="{}" type="audio/ogg">
            </audio>""".format(src)
            out_file.write(out)

        if strippedLine.startswith("OutputLine(NULL,"):
            src = strippedLine.split(",")
            out_file.write("<p>{}</p>".format(src[1]))

    out_file.write("<a href=\"./main.html\" >All chapters</a>")
    out_file.write("</body>")
    out_file.close()
    streamAssets.close()

main_file = open("./main.html", "w")
main_file.write(html_body)
main_file.write(chapter)
main_file.write(html_table + "</div>")
main_file.write("</body>")
main_file.close()
