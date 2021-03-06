
import re


class StringRefinery:

    _text: str

    def __init__(self, txt: str = None):
        if txt is not None:
            self.setText(txt)

    def refineElemTxt(self, txt: str):
        """
        Removes editorial Marks, numbers, \n, \t, and excess whitespace from
        given string. Whitespace removal is called last and matches regex for
        neighboring whitespaces.
        Procedure: First replace "unwished" elems through whitespace ...> then remove multiple
        whitespace through one.
        :param txt: the String to refine.
        :return: String without unnecessary whitespace/numbers/tabs/page-breaks/parenthesis.
        """
        # first replace unwanted elems through whitespace
        txt = self.replEditorMarks(txt)
        txt = self.replNumbers(txt)
        txt = self.replPunctuation(txt)
        txt = txt.replace("\n", " ")
        txt = txt.replace("\t", " ")

        # at last remove too much whitespace via regex
        txt = txt.strip()
        txt = re.sub(" +", " ", txt)
        return txt

    def replEditorMarks(self, txt: str):
        txt = txt.replace("[", " ")
        txt = txt.replace("]", " ")  # quite specific for my current project(maybe not good here)
        return txt

    def replNumbers(self, txt: str):
        remNumbs: str = re.sub("[\d]+", " ", txt)
        return remNumbs

    def replPunctuation(self, text: str):
        txt: str = re.sub("[,.:;]", " ", text)
        return txt

    def getText(self):
        return self._text

    def setText(self, txt: str):
        if len(txt) == 0:
            raise ValueError(str(self.__class__) + ": An empty string was given for refinement.")

        self._text = txt

