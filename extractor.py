#!/usr/bin/env python3
# Copyright 2023 Jiro Hayashi <hayashi.jiro@tuta.io>
#
# Licensed under the terms of the GNU GPL v3, or any later version.
import sys
import re
import os
import typing


TRANSLATE = os.getenv('TRANSLATE', '0') in ('1', 'true', 'yes')
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
        ("onik_tips_01", "Tip 1: うちって学年混在？"),
        ("onik_tips_02", "Tip 2: うちって制服自由？"),
        ("onik_tips_03", "Tip 3: 前原屋敷"),
        ("onik_tips_04", "Tip 4: ダム現場のバラバラ殺人"),
        ("onik_tips_05", "Tip 5: 雛見沢ダム計画"),
        ("onik_tips_06", "Tip 6: 週刊誌の特集記事"),
        ("onik_tips_07", "Tip 7: レナってどういう名前だよ？"),
        ("onik_tips_08", "Tip 8: 回覧板"),
        ("onik_tips_09", "Tip 9: ダム推進派の夫婦の転落事故"),
        ("onik_tips_10", "Tip 10: 古手神社の神主の病死"),
        ("onik_tips_11", "Tip 11: 主婦殺人事件"),
        ("onik_tips_12", "Tip 12: 無線記録"),
        ("onik_tips_13", "Tip 13: 犯人は４人以上？"),
        ("onik_tips_14", "Tip 14: 捜査メモ"),
        ("onik_tips_15", "Tip 15: 本部長通達"),
        ("onik_tips_16", "Tip 16: 自殺を誘発するクスリは？"),
        ("onik_tips_17", "Tip 17: 脅迫"),
        ("onik_tips_18", "Tip 18: 元気ないね。"),
        ("onik_tips_19", "Tip 19: 二重人格？？？"),
        ("onik_tips_20", "Tip 20: セブンスマートにて"),
        ("omake_01", "All-Cast Review"),
    ],
    "watanagashi": [
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
        ("wata_ep_01", "Epilog 1"),
        ("wata_ep_02", "Epilog 2"),
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
        ("tata_ep01", "Epilog 1"),
        ("tata_ep02", "Epilog 2"),
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
        ("_meak_ep_01", "Epilog 1"),
        ("_meak_ep_02", "Epilog 2"),
        ("_meak_ep_03", "Epilog 3"),
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
    "tsumihoroboshi": [
        ("_tsum_op", "Opening"),
        ("_tsum_001", "Day 1"),
        ("_tsum_002_1", "Day 2.1"),
        ("_tsum_002_2", "Day 2.2"),
        ("_tsum_003_1", "Day 3.1"),
        ("_tsum_003_2", "Day 3.2"),
        ("_tsum_003_3", "Day 3.3"),
        ("_tsum_003_4", "Day 3.4"),
        ("_tsum_004", "Day 4"),
        ("_tsum_005", "Day 5"),
        ("_tsum_006", "Day 6"),
        ("_tsum_007", "Day 7"),
        ("_tsum_008", "Day 8"),
        ("_tsum_009", "Day 9"),
        ("_tsum_010", "Day 10"),
        ("_tsum_011", "Day 11"),
        ("_tsum_012_1", "Day 12.1"),
        ("_tsum_012_2", "Day 12.2"),
        ("_tsum_013", "Day 13"),
        ("_tsum_014", "Day 14"),
        ("_tsum_015_1", "Day 15.1"),
        ("_tsum_015_2", "Day 15.2"),
        ("_tsum_016", "Day 16"),
        ("_tsum_017", "Day 17"),
        ("_tsum_018", "Day 18"),
        ("_tsum_019", "Day 19"),
        ("_tsum_020", "Day 20"),
        ("_tsum_021", "Day 21"),
        ("_tsum_022", "Day 22"),
        ("_tsum_023_1", "Day 23.1"),
        ("_tsum_023_2", "Day 23.2"),
        ("_tsum_024_1", "Day 24.1"),
        ("_tsum_024_1a", "Day 24.1a"),
        ("_tsum_024_2", "Day 24.2"),
        ("_tsum_025", "Day 25"),
        ("_tsum_026", "Day 26"),
        ("_tsum_026a", "Day 26a"),
        ("tsum_badend1", "Bad Ending 1"),
        ("tsum_badend2", "Bad Ending 2"),
        ("_tsum_tips_001", "Tip 1"),
        ("_tsum_tips_002", "Tip 2"),
        ("_tsum_tips_003", "Tip 3"),
        ("_tsum_tips_004", "Tip 4"),
        ("_tsum_tips_005", "Tip 5"),
        ("_tsum_tips_006", "Tip 6"),
        ("_tsum_tips_007", "Tip 7"),
        ("_tsum_tips_008", "Tip 8"),
        ("_tsum_tips_009", "Tip 9"),
        ("_tsum_tips_010", "Tip 10"),
        ("_tsum_tips_011", "Tip 11"),
        ("_tsum_tips_012", "Tip 12"),
        ("_tsum_tips_013", "Tip 13"),
        ("_tsum_tips_014", "Tip 14"),
        ("staffroom", "Staffroom"),
    ],
    "minagoroshi": [
        ("_mina_op", "Opening"),
        ("_mina_001", "Day 1"),
        ("_mina_002_1", "Day 2.1"),
        ("_mina_002_1a", "Day 2.1a"),
        ("_mina_002_1b", "Day 2.1b"),
        ("_mina_002_2", "Day 2.2"),
        ("_mina_003_1", "Day 3.1"),
        ("_mina_003_2", "Day 3.2"),
        ("_mina_004", "Day 4"),
        ("_mina_005", "Day 5"),
        ("_mina_006", "Day 6"),
        ("_mina_007", "Day 7"),
        ("_mina_008", "Day 8"),
        ("_mina_009_1", "Day 9.1"),
        ("_mina_009_2", "Day 9.2"),
        ("_mina_010", "Day 10"),
        ("_mina_011_1", "Day 11.1"),
        ("_mina_011_2", "Day 11.2"),
        ("_mina_012", "Day 12"),
        ("_mina_013", "Day 13"),
        ("_mina_014", "Day 14"),
        ("_mina_015_1", "Day 15.1"),
        ("_mina_015_2", "Day 15.2"),
        ("_mina_016", "Day 16"),
        ("_mina_017", "Day 17"),
        ("_mina_018", "Day 18"),
        ("_mina_019", "Day 19"),
        ("_mina_020", "Day 20"),
        ("_mina_021", "Day 21"),
        ("_mina_022", "Day 22"),
        ("_mina_023_1", "Day 23.1"),
        ("_mina_023_2", "Day 23.2"),
        ("_mina_024", "Day 24"),
        ("_mina_025", "Day 25"),
        ("_mina_026", "Day 26"),
        ("_mina_027", "Day 27"),
        ("_mina_028", "Day 28"),
        ("_mina_ep", "Epilog"),
        ("_mina_tips_001", "Tip 1"),
        ("_mina_tips_002", "Tip 2"),
        ("_mina_tips_003", "Tip 3"),
        ("_mina_tips_004", "Tip 4"),
        ("_mina_tips_005", "Tip 5"),
        ("_mina_tips_006", "Tip 6"),
        ("_mina_tips_007", "Tip 7"),
        ("_mina_tips_008", "Tip 8"),
        ("_mina_tips_009", "Tip 9"),
        ("_mina_tips_010", "Tip 10"),
        ("_mina_tips_011", "Tip 11"),
        ("_mina_tips_012", "Tip 12"),
        ("_mina_tips_013", "Tip 13"),
        ("staffroom", "Staffroom"),
    ],
    "matsuribayashi": [
        ("_mats_op", "Opening"),
        ("_mats_001", "1"),
        ("_mats_002", "2"),
        ("_mats_003", "3"),
        ("_mats_004", "4"),
        ("_mats_005", "5"),
        ("_mats_006", "6"),
        ("_mats_007", "7"),
        ("_mats_008", "8"),
        ("_mats_009", "9"),
        ("_mats_010", "10"),
        ("_mats_011", "11"),
        ("_mats_012", "12"),
        ("_mats_013", "13"),
        ("_mats_014", "14"),
        ("_mats_015", "15"),
        ("_mats_016", "16"),
        ("_mats_017", "17"),
        ("_mats_018", "18"),
        ("_mats_019", "19"),
        ("_mats_020", "20"),
        ("_mats_021", "21"),
        ("_mats_022", "22"),
        ("_mats_023", "23"),
        ("_mats_024", "24"),
        ("_mats_025", "25"),
        ("_mats_tips_01", "Tip 1"),
        ("_kakera01", "1"),
        ("_kakera02", "2"),
        ("_kakera03", "3"),
        ("_kakera04", "4"),
        ("_kakera05", "5"),
        ("_kakera06", "6"),
        ("_kakera07", "7"),
        ("_kakera08", "8"),
        ("_kakera09", "9"),
        ("_kakera10", "10"),
        ("_kakera11", "11"),
        ("_kakera12", "12"),
        ("_kakera13", "13"),
        ("_kakera14", "14"),
        ("_kakera15", "15"),
        ("_kakera16", "16"),
        ("_kakera17", "17"),
        ("_kakera18", "18"),
        ("_kakera19", "19"),
        ("_kakera20", "20"),
        ("_kakera21", "21"),
        ("_kakera22", "22"),
        ("_kakera23", "23"),
        ("_kakera24", "24"),
        ("_kakera25", "25"),
        ("_kakera26", "26"),
        ("_kakera27", "27"),
        ("_kakera28", "28"),
        ("_kakera29", "29"),
        ("_kakera30", "30"),
        ("_kakera31", "31"),
        ("_kakera32", "32"),
        ("_kakera33", "33"),
        ("_kakera34", "34"),
        ("_kakera35", "35"),
        ("_kakera36", "36"),
        ("_kakera37", "37"),
        ("_kakera38", "38"),
        ("_kakera39", "39"),
        ("_kakera40", "40"),
        ("_kakera41", "41"),
        ("_kakera42", "42"),
        ("_kakera43", "43"),
        ("_kakera44", "44"),
        ("_kakera45", "45"),
        ("_kakera46", "46"),
        ("_kakera47", "47"),
        ("_kakera48", "48"),
        ("_kakera49", "49"),
        ("_kakera50", "50.1"),
        ("_kakera50_02", "50.2"),
        ("_kakera51", "51"),
        ("_kakera52", "52"),
        ("kakera_miss", "Miss"),
        ("staffroom", "Staffroom"),
    ],
}

ACTOR_COLOR_RE = re.compile("<.*?</color>")
COLOR_RE = re.compile("=(.*?)>")
ACTOR_RE = re.compile(">(.*?)<")
SUBSCRIPT_CONDITION_RE = re.compile(
    r"GetGlobalFlag\(GCensor\)\s*(>=|<=|>|<|==)(\s*)(\d*)"
)
SUBSCRIPT_RE = re.compile(r"ModCallScriptSection\(\"(.*?)\",\"(.*?)\"\)")
DIALOG_CALL_RE = re.compile(r"void dialog(\d*)\(\)")

out_dir = "./out/"
chapter = ""
censor_level = 2
script_path = ""
voice_path = ""
extra_flag = False
html_body = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Higurashi (français)</title>
<style type="text/css">
body {
background: #000;
color: #ccc;
max-width: 640px;
margin: 0 auto;
}

h1 {
text-align: center;
}
a {
color: #8B0000;
text-decoration: underline;
}

div.speaker {
font-weight: bold;
font-size: 1.1rem;
margin-left: 1em;
text-decoration: underline;
}

div.guardian {
position: fixed;
left: 0px;
right:0px;
top:0px;
height:1px;
font-size: 4pt;
}
a.episode {
text-align: center;
font-size: 1.4rem;
}
nav ul {
text-align: center;
margin: 0 auto;
display: block;
}
nav li {
display: inline-block;
margin: 0 10px;
min-width: 160px;
}

nav li a {
font-weight: bold;
}
</style>
</head><body><div class="guardian">&nbsp;</div> """
html_body_tail = """
<script>
let lastScrollY = window.scrollY;
let lastScrollDirection = null;

window.addEventListener('scroll', () => {
  lastScrollDirection = window.scrollY > lastScrollY ? 'down' : 'up';
  lastScrollY = window.scrollY;
});

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    if (Object.keys(entry.target.dataset).length == 0) return;
    const direction = lastScrollDirection === 'down' ? 'up' : 'down';
    console.log({
      dataset: entry.target.dataset,
      direction: direction
    });
    if (entry.target.dataset.charas !== undefined) {
      window.activeCharas = entry.target.dataset.charas.split(',');
    }
    if (entry.target.dataset.bg !== undefined) {
      window.activeBg = entry.target.dataset.bg;
    }
    
  });
}, {
  root: null,
  rootMargin: '0px 0px -100% 0px', // 1px line at viewport top
  threshold: 0
});

document.querySelectorAll('p').forEach(el => {
  observer.observe(el);
});
</script>
</body></html>"""
html_table = '<div style="display:flex;flex-direction:column;" >'
index_file = "index.html"


def build_navigation(chapter, current_position):
  if chapter not in CHAPTERS:
    raise ValueError(f"wrong chapter {chapter}")
  enumerated = list(enumerate(CHAPTERS[chapter]))
  cur = list(filter(lambda x: x[1][0] == current_position, enumerated))
  if not cur:
    raise ValueError(f"wrong position in {chapter}: {current_position}")
  if len(cur) > 1:
    raise ValueError(f"duplicate position in {chapter}: {current_position}")
  cur_index, cur_chap = cur[0]
  first = cur_index == 0
  last = cur_index == (len(enumerated) - 1)
  prev = None
  nc = None
  if not first:
    prev = enumerated[cur_index - 1]
  if not last:
    nc = enumerated[cur_index + 1]
  prev_html = f'<li><a href="higurashi_{prev[1][0]}.html">{prev[1][1]}</a></li>' if prev else '<li>(first chapter)</li>'
  next_html = f'<li><a href="higurashi_{nc[1][0]}.html">{nc[1][1]}</a></li>' if nc else '<li>(last chapter)</li>'
  return f"""
<nav>
<ul>
{prev_html}
<li>{cur_chap[1]}</li>
{next_html}
</ul>
<ul>
<li><a href="index.html">Chapter index</a></li>
<li><a href="../index.html">List of chapters</a></li>
</ul>
</nav>
"""
# Calls a subscript by parsing the subscript file and extracting all relevant lines specified by the dialog_start
# Returns a list of all lines occuring in that dialog
def call_subscript(subscript_filename: str, dialog_start: str) -> list[str]:
    script_file = open(script_path + "{}.txt".format(subscript_filename), "r")
    lines = script_file.readlines()
    write_files = False
    output_lines = []

    for line in lines:
        if dialog_start in line:
            write_files = True
            continue
        if write_files:
            if DIALOG_CALL_RE.match(line):
                write_files = False
                break
            else:
                output_lines.append(line)
    script_file.close()
    return output_lines


# Checks whether a given line is a condition to call a subscript and evalutes that condition based on the set censor_level
# Returns the evaluation of the condition as a boolean
def evaluate_subscript_condition(line: str):
    condition_match = SUBSCRIPT_CONDITION_RE.search(line)
    condition = False
    if condition_match:
        relation = condition_match.group(1)
        operand = condition_match.group(3)
        match relation:
            case "==":
                condition = censor_level == int(operand)
            case "<=":
                condition = censor_level <= int(operand)
            case ">=":
                condition = censor_level >= int(operand)
            case "<":
                condition = censor_level < int(operand)
            case ">":
                condition = censor_level > int(operand)
    return condition


# Excract subscript filename and the dialogue function from a subscript call
def extract_subscript_args(line):
    subscript_match = SUBSCRIPT_RE.search(line)
    if subscript_match:
        return [subscript_match.group(1), subscript_match.group(2)]


# Parse actor and color into HTML
def color_to_html(input):
    color = COLOR_RE.findall(input)[0]
    character = ACTOR_RE.findall(input)[0]
    return '<div class="speaker" style="color: {}; font-weight: bold;">{}</div>'.format(
        color, character
    )


def remove_quotes(l: list) -> list:
  return [remove_quotes_s(a) for a in l]

def remove_quotes_s(s: str) -> str:
  return s.replace('"', '').strip()

def remove_frontback_quotes(s: str) -> str:
  "yeah dirty"
  return s.strip().replace('\\"', '|').strip('"').replace('|', '"')

# Parse Japanese "OutputLine" into an HTML paragraph
def line_to_html_paragraph(split_line, optional_bg=None, optional_charas=None):
    extra = ''
    line_text = split_line[1].split('",')[0]
    if optional_bg:
      extra += f' data-bg="{remove_quotes_s(optional_bg)}"'
    if optional_charas:
      extra += f' data-charas="{",".join(remove_quotes(optional_charas))}"'
    return f"<p{extra}>{remove_frontback_quotes(line_text)}</p>\n"


# Parse modded voice line "ModPlayVoice" into an HTML audio
def voice_to_html_audio(split_line):
    return ""
    audio_name = split_line[2].strip().replace('"', "")
    src = voice_path + audio_name + ".ogg"
    return """<audio controls preload="none">
            <source src="{}" type="audio/ogg">
            </audio>""".format(
        src
    )


# Parse a list of script lines into HTML
def parse_lines(lines: list[str], output_file: typing.IO):
    flag_readnext = False
    bg_to_attach = None
    charas_to_attach = []
    charas_dirty = False
    for lnum, line in enumerate(lines):
        stripped_line = line.strip().replace("\u3000", "")
        split_line = stripped_line.split(",", 1)
        split_line_full = stripped_line.split(",", 2)

        # Which background is active
        if stripped_line.startswith("DrawSceneWithMask"):
          bg_to_attach = split_line_full[0].split('"', 1)[1]
        elif stripped_line.startswith("DrawScene"):
          bg_to_attach = split_line_full[0].split('"', 1)[1]
        elif stripped_line.startswith('ModDrawCharacter'):
          charas_to_attach.append(split_line_full[2])
          charas_dirty = True
        elif stripped_line.startswith('FadeBustshot'):
          charas_to_attach = []
        # Text line (
        if stripped_line.startswith("OutputLine(NULL,") and TRANSLATE:
            flag_readnext = True
        elif stripped_line.startswith("OutputLine(NULL,"):
            output_file.write(line_to_html_paragraph(split_line, bg_to_attach, charas_to_attach if charas_dirty else []))
            charas_dirty = False
            bg_to_attach = None
            # charas_to_attach = []
        elif flag_readnext:
            output_file.write(line_to_html_paragraph(split_line, bg_to_attach, charas_to_attach if charas_dirty else []))
            charas_dirty = False
            bg_to_attach = None
            # charas_to_attach = []
            flag_readnext = False
        # Actor-color line
        actor = ACTOR_COLOR_RE.findall(line)
        if actor is not None and actor:
            if TRANSLATE:
              idx = 1
            else:
              idx = 0
            try:
              output_file.write(color_to_html(actor[idx]))
            except:
              print(output_file, actor, "error", idx, "lnum", lnum)
              raise

        # Voice line
        #if extra_flag and stripped_line.startswith("ModPlayVoiceLS"):
        #    output_file.write(voice_to_html_audio(split_line))

        # Call to subscript
        if evaluate_subscript_condition(stripped_line):
            subscript_args = extract_subscript_args(stripped_line)
            if len(subscript_args) == 2:
                subscript_lines = call_subscript(
                    subscript_args[0], subscript_args[1])
                parse_lines(subscript_lines, output_file)
            else:
                continue


if __name__ == "__main__":
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
            voice_path = ""
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
                "'{}' detected as chapter.\nExtracting WITH audio support.".format(
                    chapter
                )
            )
        else:
            print("The provided path does not seem to be valid!")
            exit(1)

    # Parse optional out directory arg
    if len(sys.argv) >= 3:
        out_dir = sys.argv[2].rstrip("/")
    os.makedirs(os.path.dirname(out_dir + "/"), exist_ok=True)

    for script_name in CHAPTERS[chapter]:
        output_file = open(
            "{}/higurashi_{}.html".format(out_dir, script_name[0]), "w")
        script_file = open(script_path + "{}.txt".format(script_name[0]), "r")

        html_table += '<a href="./higurashi_{}.html">{}</a>'.format(
            script_name[0], script_name[1]
        )
        output_file.write(html_body)
        output_file.write(build_navigation(chapter, script_name[0]))

        parse_lines(script_file.readlines(), output_file)

        output_file.write(build_navigation(chapter, script_name[0]))
        output_file.write(html_body_tail)
        output_file.close()
        script_file.close()

    main_file = open("{}/{}".format(out_dir, index_file), "w")
    main_file.write(html_body)
    main_file.write(chapter.capitalize())
    main_file.write(html_table)
    main_file.write('<a class="episode" href="../">All episodes</a>')
    main_file.write(html_body_tail)
    main_file.close()
