import re

LATEX_TAGS = [
    ('math', {
        'regex': re.compile('\$.*?\$'),
        'properties':{'foreground':'#006600',},
    }),
    ('command', {
        'regex': re.compile('[\\\\]\\w*[\\\\]?'),
        'properties':{'foreground':'#000088',},
    }),
    ('comment', {
        'regex': re.compile('%.*'),
        'properties':{'foreground':'#888888',},
    }),
    ('bracket_contents', {
        'regex': re.compile('[{}[\]].*?[^\\\\][{}[\]]'),
        'properties':{'foreground':'#440088',},
    }),
    ('bracket', {
        'regex': re.compile('[{}[\]]'),
        'properties':{'foreground':'#880000',},
    }),
    ('symbol', {
        'regex': re.compile('[=<>&-]'),
        'properties':{'foreground':'#888800',},
    }),
]


BLANK_DOCUMENT = """\\documentclass{article}
\\begin{document}

\\centerline{\\large Welcome to DeSiGLE: Derek's Simple Gnome \\LaTeX\\ Editor! }

\\end{document}"""