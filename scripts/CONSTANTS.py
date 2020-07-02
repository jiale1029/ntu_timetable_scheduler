"""
CONSTANTS
    - This file contains the constants for the parsing of html timetables.
"""

COURSE_CODE: str = '<TD WIDTH="100"><B><FONT COLOR=#0000FF>[a-zA-Z0-9]{6}<\/FONT><\/B><\/TD>'
COURSE_TITLE: str = '<TD WIDTH="500"><B><FONT COLOR=#0000FF>.*<\/FONT><\/B><\/TD>'
COURSE_AU: str = '<TD WIDTH="50"><B><FONT COLOR=#0000FF>.*<\/FONT><\/B><\/TD>'
COURSE_REMARK: str = '<TD WIDTH="500"><B><FONT SIZE=2 COLOR=#FF00FF>.*<\/FONT><\/B><\/TD>'
