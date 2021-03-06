import os, pango, re, sys

RUN_FROM_DIR = os.path.abspath(os.path.dirname(sys.argv[0])) + '/'


LATEX_TAGS = [
    ('math', {
        'regex': re.compile('\$.*?\$'),
        'properties':{'foreground':'#006600',},
    }),
    ('math2', {
        'regex': re.compile('\$\$.*?\$\$'),
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
    ('search_highlight', {
        'regex': re.compile('oZooxae4'), # dummy regex
        'properties':{'background':'#ffffbb',},
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
    '\\author{}',
    '\\title{}',
    '\\date{}',
    '\\maketitle',
    '\\pagestyle{}',
    '\\part{}',
    '\\chapter{}',
    '\\section{}',
    '\\subsection{}',
    '\\ref{}',
    '\\pageref{}',
    '\\footnote{}',
    '\\caption{}',
    '\\textrm{}',
    '\\textsf{}',
    '\\texttt{}',
    '\\textmd{}',
    '\\textbf{}',
    '\\textup{}',
    '\\textit{}',
    '\\textsl{}',
    '\\textsc{}',
    '\\emph{}',
    '\\textnormal{}',
    '\\underline{}',
    '\\tiny',
    '\\scriptsize',
    '\\footnotesize',
    '\\small',
    '\\normalsize',
    '\\large',
    '\\kill',
    '\\pagebreak',
    '\\noindent',
    '\\today',
    '\\hspace{l}',
    '\\vspace{l}',
    '\\rule{w}{h}',
    '\\hline',
    '\\cline{x-y}',
    '\\leftarrow',
    '\\Leftarrow',
    '\\longleftarrow',
    '\\Longleftarrow',
    '\\rightarrow',
    '\\Rightarrow',
    '\\longrightarrow',
    '\\Longrightarrow',
    '\\leftrightarrow',
    '\\Leftrightarrow',
    '\\longleftrightarrow',
    '\\uparrow',
    '\\downarrow',
    '\\Uparrow',
    '\\nearrow ',
    '\\searrow ',
    '\\swarrow ',
    '\\nwarrow ',
    '\\hat{o}',
    '\\widehat{oo}',
    '\\check{o}',
    '\\tilde{o}',
    '\\widetilde{oo}',
    '\\acute{o}',
    '\\grave{o}',
    '\\dot{o}',
    '\\ddot{o}',
    '\\breve{o}',
    '\\bar{o}',
    '\\vec{o}',
    '\\pm',
    '\\mp',
    '\\times',
    '\\div',
    '\\ast',
    '\\star',
    '\\bullet',
    '\\circ',
    '\\cdot',
    '\\leq',
    '\\ll',
    '\\subset',
    '\\geq',
    '\\gg',
    '\\equiv',
    '\\sim',
    '\\simeq',
    '\\approx',
    '\\neq',
    '\\per',
    '\\propto',
    '\\alpha',
    '\\beta',
    '\\gamma',
    '\\delta',
    '\\epsilon',
    '\\varepsilon',
    '\\zeta',
    '\\eta',
    '\\theta',
    '\\vartheta',
    '\\iota',
    '\\kappa',
    '\\lambda',
    '\\mu',
    '\\nu',
    '\\xi',
    '\\pi',
    '\\varpi',
    '\\rho',
    '\\varrho',
    '\\sigma',
    '\\varsigma',
    '\\tau',
    '\\upsilon',
    '\\phi',
    '\\varphi',
    '\\chi',
    '\\psi',
    '\\omega',
    '\\aleph',
    '\\hbar',
    '\\imath',
    '\\jmath',
    '\\ell',
    '\\wp',
    '\\Re',
    '\\Im',
    '\\prime',
    '\\nabla',
    '\\surd',
    '\\angle',
    '\\forall',
    '\\exists',
    '\\backslash',
    '\\partial',
    '\\infty',
    '\\triangle',
    '\\Box',
    '\\Diamond',
    '\\flat',
    '\\natural',
    '\\sharp',
    '\\clubsuit',
    '\\diamondsuit',
    '\\heartsuit',
    '\\spadesuit',
    '\\dag',
    '\\ddag',
    '\\S',
    '\\P',
    '\\copyright',
    '\\pounds',
    '\\arccos',
    '\\arcsin',
    '\\arctan',
    '\\cos',
    '\\cosh',
    '\\cot',
    '\\coth',
    '\\csc',
    '\\deg',
    '\\det',
    '\\dim',
    '\\exp',
    '\\gcd',
    '\\hom',
    '\\inf',
    '\\ker',
    '\\lg',
    '\\lim',
    '\\liminf',
    '\\limsup',
    '\\ln',
    '\\log',
    '\\max',
    '\\min',
    '\\sec',
    '\\sin',
    '\\sinh',
    '\\sup',
    '\\tan',
    '\\tanh',
    '\\bmod',
    '\\pmod{}',
    '\\sum',
    '\\prod',
    '\\coprod',
    '\\int',
    '\\oint',
    '\\bigcup',
    '\\bigcap',
    '\\bigvee',
    '\\bigwedge',
    '\\bigodot',
    '\\bigotimes',
    '\\bigoplus',
    '\\biguplus',
    '\\boldmath',
    '\\cdots',
    '\\ddots',
    '\\frac',
    '\\ldots',
    '\\overbrace',
    '\\overline',
    '\\sqrt',
    '\\stackrel',
    '\\underbrace',
    '\\underline',
    '\\vdots',
    '\\item',
    '\\item[]',
]

SYMLIST = [ x.strip() for x in open( RUN_FROM_DIR + 'SYMLIST', 'r' ).readlines() ]

#AUTOCOMPLETE_PLUS = list( set(AUTOCOMPLETE).union( set(SYMLIST) ) )
AUTOCOMPLETE_PLUS = list( set(AUTOCOMPLETE) )
AUTOCOMPLETE_PLUS.sort()


BLANK_DOCUMENT = """\\documentclass{article}
\\begin{document}

\\centerline{\\large Welcome to DeSiGLE: Derek's Simple Gnome \\LaTeX\\ Editor! }

\\end{document}"""