import re

LATEX_TAGS = [
    ('math', {
        'regex': re.compile('\$.*\$'),
        'properties':{'foreground':'#008800',},
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
        'regex': re.compile('[{}[\]].*?[{}[\]]'),
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
