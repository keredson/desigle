import pango, re

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
        'properties':{'foreground':'#888888','style':pango.STYLE_ITALIC,},
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
    ('latex_error', {
        'regex': re.compile('oZooxae4'), # dummy regex
        'properties':{'background':'#ffdddd',},
    }),
]


AUTOCOMPLETE = [
    '\\begin{}\n\\end{}',
    '\\begin{document}\n\\end{document}',
    '\\begin{comment}\n\\end{comment}',
    '\\begin{quote}\n\\end{quote}',
    '\\begin{quotation}\n\\end{quotation}',
    '\\begin{verse}\n\\end{verse}',
    '\\begin{enumerate}\n\\item\n\\end{enumerate}',
    '\\begin{itemize}\n\\item\n\\end{itemize}',
    '\\begin{description}\n\\item[]\n\\end{description}',
    '\\begin{table}\n\\end{table}',
    '\\begin{figure}\n\\end{figure}',
    '\\begin{equation}\n\\end{equation}',
    '\\begin{verbatim}\n\\end{verbatim}',
    '\\begin{center}\n\\end{center}',
    '\\begin{flushleft}\n\\end{flushleft}',
    '\\begin{flushright}\n\\end{flushright}',
    '\\begin{array}\n\\end{array}',
    '\\begin{tabular}\n\\end{tabular}',
]


BLANK_DOCUMENT = """\\documentclass{article}
\\begin{document}

\\centerline{\\large Welcome to DeSiGLE: Derek's Simple Gnome \\LaTeX\\ Editor! }

\\end{document}"""