import sublime, sublime_plugin
import re

class Rtree2mdCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    bufferText = self.view.substr(sublime.Region(0, self.view.size()))
    mdText = ''
    lines = bufferText.splitlines()

    reH1 = re.compile(r"^(\d+)\s")
    reHm = re.compile(r"^((\t+)((\d+\.)+\d))\s")

    for line in lines:

      matchH1 = re.search(reH1,line)

      if (matchH1):
        if (mdText != ''):
          mdText += "\n"
        mdText += re.sub(r"^\d+\s",'#',line)
        mdText += "\n"
        continue

      matchHm = re.search(reHm,line)

      if (matchHm):
        mdText += "\n"
        mdText += line.replace(matchHm.group(1),'#' + ('#' * len(matchHm.group(2))))
        mdText += "\n"
        continue
      mdText += re.sub(r"\t+","",line)
      mdText += "\n"

    self.view.replace(edit, sublime.Region(0, self.view.size()), mdText)
