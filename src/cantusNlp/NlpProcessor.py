
import src.cantusNlp.utils.FileReader as FileReader
import src.cantusNlp.utils.XReader as Xreader
import src.cantusNlp.utils.StringRefinery as StringRefinery
import src.cantusNlp.utils.CltkOperator as CltkOperator


class NlpProcessor:

    _dirPath: str
    _textMap: dict

    _xreader: Xreader
    _fileReader: FileReader
    _cltk: CltkOperator
    _strRefiner: StringRefinery

    def __init__(self, dirPath: str):
        self._dirPath = dirPath

        self._xreader = Xreader.XReader()
        self._fileReader = FileReader.FileReader(self._dirPath)
        self._cltk = CltkOperator.CltkOperator()
        self._strRefiner = StringRefinery.StringRefinery()

        self._textMap = {}  # initialize here

    def _addToMap(self, key: str, content: str):
        self._textMap[key] = content

    def loadCorpus(self, elemToIgnore: str = None):
        """
        Uses the intern dirPath variable given at instantiation to locate the diretory
        of the xml files. Build the access to the individual files via concatinating dirpath
        and name of the xml-files. Uses the XReader class to retrieve the TEI-body as text.
        Stores retrieved corpus in the dictionary ...> filename.xml as key-value.
        :param elemToIgnore: Can optionally define a tag to be ignored for the read in of
        the tei-body.
        :return: nothing
        """
        fileNameList = self._fileReader.listFiles()
        for fileName in fileNameList:
            # trying getting all the body texts.
            path = self._dirPath + fileName

            # .txt or .xml
            if fileName.endswith(".xml"):
                xTree = self._xreader.readXml(path)
                bodyTxt = self._xreader.getTeiBodyText(xTree, elemToIgnore)
            elif fileName.endswith(".txt"):
                bodyTxt = self._fileReader.readTxt(path)
            else:
                raise TypeError("LoadCorpus only supports .txt and .xml files. Given file was: " + path)

            self._textMap[fileName] = bodyTxt

    def lemmatizeCorpus(self):

        cltk = self._cltk
        map: dict[str] = self.getTextMap()

        for key in map:
            text = map[key]
            text = self._strRefiner.refineElemTxt(text)
            text = cltk.wtokenizeLatin(text)
            text = cltk.lemmatizeLat(text)
            text = cltk.removeLatStopWords(text)
            map[key] = text

        return map


    def getText(self, fileName: str):
        """
        Accesses the intern dictionary in which the read in corpora are saved under their
        filename as key-value. Value calls dictionary[key] ...> to access the data.
        :param fileName: The Name of the file read in is stored as key in the intern dictionary. With
        the filename the read in corpus is accessible.
        :return: the internally saved corpus
        """
        corpus: str = self._textMap[fileName]
        return corpus

    def getTextMap(self):
        return self._textMap

