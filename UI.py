from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtUiTools import QUiLoader
from Viterbi import Viterbi
from SplitPinyin import getSplit


class MyForm(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('UI/main.ui')
        self.ui.lineEdit.returnPressed.connect(self.handleEnter)
        self.ui.textEdit_2.textChanged.connect(self.Select)
        self.v = Viterbi(['pi', 'A', 'B', 'STATE'])
        self.ans = []

    def handleEnter(self):
        text = self.ui.lineEdit.text()
        self.ui.textBrowser.clear()
        self.ui.textEdit_2.clear()
        self.ans = self.v.predict(getSplit(text))
        for i in range(1, min(10, len(self.ans))):
            self.ui.textBrowser.append("{}: {}".format(i, self.ans[i - 1][0]))
            self.ui.textBrowser.ensureCursorVisible()

    def Select(self):
        choose = self.ui.textEdit_2.toPlainText()
        if not choose:
            return
        if not '1' <= choose[0] <= '9':
            return
        self.ui.textEdit_2.setText('{}'.format(self.ans[int(choose[0]) - 1][0]))
        f = open('corpus/updated.txt', 'a+', encoding='utf-8')
        f.write('{} \n'.format(self.ans[int(choose[0]) - 1][0]))
        f.close()


if __name__ == '__main__':
    app = QApplication([])
    form = MyForm()
    form.ui.show()
    app.exec_()
