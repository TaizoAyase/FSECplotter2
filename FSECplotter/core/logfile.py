#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import numpy as np
import codecs
import re
import os
from .section import Section

class LogFile:
  def __init__(self):
    self.sections = []
    self.file_name = None # file basename without extension
    self.__flow_rate = None
    self.__no_of_detectors = None

  def parse(self, filename):
    self.__parse_logfile(filename)
    # remove extension from file basename
    filename, ext = os.path.splitext( os.path.basename(filename) )
    self.file_name = filename
    return self

  def append_section(self, section):
    section.convert_to_npary()
    self.sections.append(section)
    return self.sections

  # return section that match the RE of section_name
  def find_section(self, section_name):
    # first, replace "()" to "\(\)"
    secname = self.__sub_parenthesis(section_name)
    pat = re.compile(secname)
    name_ary = [x.name() for x in self.sections]
    index = [i for i, name in enumerate(name_ary) if pat.search(name)]
    if len(index) > 1:
      raise
    return self.sections[index[0]]

  # get flow rate from the file name of method file 
  # if cannot, raise Error
  def flowrate(self):
    # if already set, end...
    if self.__flow_rate:
      return self.__flow_rate

    methodfiles_ary = self.__get_params_ary("Original Files", "Method File")

    # search float in file name
    pat = re.compile(r"\d\.\d+")
    matched_str = pat.findall(methodfiles_ary[0])
    if matched_str:
      self.__flow_rate = float(matched_str[0])
      return self.__flow_rate
    else:
      raise NoMatchedFlowRateError

  # returns # of detectors and set it to self.__no_of_detectors
  def num_of_detector(self):
    num_detectors_ary = self.__get_params_ary("Configuration", "# of Detectors")
    self.__no_of_detectors = int(num_detectors_ary[0])
    return self.__no_of_detectors
    

  ### private methods

  def __parse_logfile(self, f_path):
    header_pattern = re.compile(r"\[.+\]")
    
    header_flag = False
    with codecs.open(f_path, "r", "shift_jis") as f:
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

  def __get_params_ary(self, section_name, param_name):
    params_ary = self.find_section(section_name).params()
    for par in params_ary:
      if param_name in par:
        rm_name_ary = par.copy()
        rm_name_ary.pop(0)
        return rm_name_ary


### exception
class NoMatchedFlowRateError(Exception):
  pass
