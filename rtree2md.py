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

class Rtreeheader2listCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    textSelection = [a for a in self.view.sel()][0]
    resultText = ''
    startFlag = 0
    baseHeaderLevel = 0
    lines = self.view.substr(textSelection).splitlines()
    baseHeadCheckRe = re.compile(r"^(\#+)\s")
    listLabelArr = ['-','*']

    for line in lines:

      if (line == '' and startFlag == 0):
        resultText += "\n"
        continue

      if (line == ''):
        continue

      matchHead = re.search(baseHeadCheckRe,line)

      if (matchHead):
        if (startFlag == 0):
          baseHeaderLevel = len(matchHead.group(1))
          startFlag = 1

        listLevel = len(matchHead.group(1)) - baseHeaderLevel

        if (listLevel < 0):
          resultText += "\n"
          resultText += line
          resultText += "\n"
          continue

        resultText += "\t" * listLevel
        resultText += listLabelArr[(listLevel + 1) % 2]
        resultText += " "
        resultText += re.sub(r"\#+","",line)
        resultText += "\n"
        continue

      resultText += line
      resultText += "\n"

    print(resultText)
    self.view.replace(edit, textSelection, resultText)

