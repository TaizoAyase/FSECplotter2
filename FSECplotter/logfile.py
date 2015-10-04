
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import numpy as np
import codecs
import re
import os
from section import Section

class LogFile:
  def __init__(self):
    self.sections = []
    self.file_name = None

  def parse(self, filename):
    self.__parse_logfile(filename)
    self.file_name, ext = os.path.basename(filename)
    return self

  def append_section(self, section):
    section.convert_to_npary()
    self.sections.append(section)
    return self.sections

  def find_section(self, section_name):
    secname = self.__sub_parenthesis(section_name)
    pat = re.compile(secname)
    ary_tmp = [x.name() for x in self.sections]
    index = [i for i, name in enumerate(ary_tmp) if pat.search(name)]
    return int(index[0])

  ### private methods

  def __parse_logfile(self, f_name):
    header_pattern = re.compile(r"\[.+\]")
    
    header_flag = False
    with codecs.open(f_name, "r", "shift_jis") as f:
      for line in f: 
        # search the header line
        if re.match(header_pattern, line):
          sec = Section(line)
          header_flag = True
          next
    
        # search the end of the section
        if re.match(r"^\s+$", line):
          if header_flag:
            header_flag = False
            self.append_section(sec)
            del sec
          next
        sec.append_data(line) if 'sec' in locals() else None

  def __sub_parenthesis(self, section_name):
    tmp = re.sub(r"\(", "\(", section_name)
    return re.sub(r"\)", "\)", tmp)



