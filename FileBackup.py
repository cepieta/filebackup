import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
import shutil
import tkinter
from tkinter import filedialog

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("FileBackupUI.ui")[0]

dir_pathSrc = 'C:/'
dir_pathDest = 'D:/'
fileQueue = list()
folderQueue = list()
fileType = {}
fileCategory = 0

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.lineEditSrc.setText(dir_pathSrc)
        self.lineEditDest.setText(dir_pathDest)
        # GroupBox안에 있는 CheckBox에 기능 연결
        self.checkBoxAll.stateChanged.connect(self.groupchkFunction)
        self.pushButtonSrc.clicked.connect(self.btn_clickedSrc)
        self.pushButtonDest.clicked.connect(self.btn_clickedDest)
        self.pushButtonStart.clicked.connect(self.btn_clickedStart)

    # 모두 선택 체크 했을때 나머지 체크박스 모두 선택 혹은 비선택
    def groupchkFunction(self):
        if self.checkBoxAll.isChecked():
            self.checkBox1.setChecked(True)
            self.checkBox2.setChecked(True)
            self.checkBox3.setChecked(True)
            self.checkBox4.setChecked(True)
            self.checkBox5.setChecked(True)
            self.checkBox6.setChecked(True)
            self.checkBox7.setChecked(True)
            self.checkBox8.setChecked(True)
        else:
            self.checkBox1.setChecked(False)
            self.checkBox2.setChecked(False)
            self.checkBox3.setChecked(False)
            self.checkBox4.setChecked(False)
            self.checkBox5.setChecked(False)
            self.checkBox6.setChecked(False)
            self.checkBox7.setChecked(False)
            self.checkBox8.setChecked(False)

    # 백업 폴더 선택
    def btn_clickedSrc(self):
        root = tkinter.Tk()
        root.withdraw()
        global dir_pathSrc
        dir_pathSrc = filedialog.askdirectory(parent=root, initialdir="/", title='Please select a directory')
        if dir_pathSrc[-1:] != '/':
            dir_pathSrc += '/'
        print("\ndir_path : ", dir_pathSrc)
        self.lineEditSrc.setText(dir_pathSrc)

    # 대상 폴더 선택
    def btn_clickedDest(self):
        root = tkinter.Tk()
        root.withdraw()
        global dir_pathDest
        dir_pathDest = filedialog.askdirectory(parent=root, initialdir="/", title='Please select a directory')
        print("\ndir_path : ", dir_pathDest)
        self.lineEditDest.setText(dir_pathDest)

    # 백업 시작
    def btn_clickedStart(self):

        fileQueue.clear()
        folderQueue.clear()
        fileType.clear()

        self.matchType()
        #체크박스 변경 불가로 변경
        #self.disableCheckbox()

        global dir_pathSrc
        print(dir_pathSrc)
        # 백업 대상 폴더 내 목록 읽어 리스트에 저장
        try:
            file_list = os.listdir(dir_pathSrc)
        except:
            self.labelStatus.setText('접근 오류 발생!!')

        if dir_pathSrc[-1:] != '/':
            dir_pathSrc += '/'
        # 폴더큐와 파일큐에 따로 저장
        for fl in file_list:
            if (fl[0] == '$') or (fl[0] == '%'):
                continue
            if os.path.isdir(dir_pathSrc + fl):
                folderQueue.append(dir_pathSrc + fl)
            else:
                fileQueue.append(dir_pathSrc + fl)

        # print(fileQueue)
        # print(folderQueue)
        # 리스트에 저장된 목록을 BFS 방식으로 순회하며 복사
        while len(folderQueue) > 0:
            # 파일 큐에 있는 내용을 모두 복사
            for fl in fileQueue:
                destfolder = fileType.get(self.fileExt(fl))
                if destfolder:
                    self.copyFile(fl, destfolder)
            fileQueue.clear()

            try:
                # 폴더 큐에 있는 내용 중 첫번째 값을 가져와 그 폴더 내의 파일 리스트를 저장
                dir_pathSrc = folderQueue.pop(0)+'/'
                file_list = os.listdir(dir_pathSrc)

                # 가져온 파일 리스트를 파일과 폴더로 구분하여 저장
                for fl in file_list:
                    if (fl[0] == '$') or (fl[0] == '%'):
                        continue
                    if os.path.isdir(dir_pathSrc + fl):
                        folderQueue.append(dir_pathSrc + fl)
                    else:
                        fileQueue.append(dir_pathSrc + fl)
            except Exception as e:
                self.labelStatus.setText('폴더 접근 오류발생:' + dir_pathSrc)
                print('폴더 접근 오류발생:' + dir_pathSrc)

        self.labelStatus.setText('복사가 완료되었습니다.')

    # 파일 복사 함수
    def copyFile(self, fileName, folder):
        try:
            print('copy: ' + fileName)
            self.labelStatus.setText('복사중: ' + fileName)
            copyFolder = dir_pathDest + '/' + folder
            if not os.path.exists(copyFolder):
                os.makedirs(copyFolder)
            shutil.copy2(fileName, copyFolder)
        except Exception as e:
            self.labelStatus.setText('복사중 오류발생:' + fileName)
            print('복사중 오류발생:' + fileName + ' ' + e)

    def fileExt(self, fileName):
        idx = fileName.rfind('.')
        if idx == -1:
            return 'null'
        # print(fileName[idx:])
        return fileName[idx:]

    # 파일의 확장자와 일치하는지 확인하는 함수
    def matchType(self):
        global fileCategory
        fileType.clear()
        if self.checkBox1.isChecked():
            fileType['.hwp'] = '문서'
            fileType['.txt'] = '문서'
        if self.checkBox2.isChecked():
            fileType['.xls'] = '엑셀'
            fileType['.xlsx'] = '엑셀'
            fileType['.xlsm'] = '엑셀'
            fileType['.xlm'] = '엑셀'
        if self.checkBox3.isChecked():
            fileType['.png'] = '그림'
            fileType['.jpg'] = '그림'
            fileType['.bmp'] = '그림'
            fileType['.jpeg'] = '그림'
        if self.checkBox4.isChecked():
            fileType['.pdf'] = 'PDF'
        if self.checkBox5.isChecked():
            fileType['.py'] = '프로그램'
            fileType['.c'] = '프로그램'
            fileType['.cpp'] = '프로그램'
            fileType['.cs'] = '프로그램'
            fileType['.java'] = '프로그램'
        if self.checkBox6.isChecked():
            fileType['.avi'] = '동영상'
            fileType['.mpg'] = '동영상'
            fileType['.mp4'] = '동영상'
            fileType['.kmv'] = '동영상'
            fileType['.mkv'] = '동영상'
        if self.checkBox7.isChecked():
            fileType['.psd'] = '포토샵'
            fileType['.ai'] = '포토샵'
        if self.checkBox8.isChecked():
            fileType['.zip'] = '압축'
            fileType['.rar'] = '압축'
            fileType['.alz'] = '압축'

    def disableCheckbox(self):
        self.checkBoxAll.setCheckable(False)
        self.checkBox1.setCheckable(False)
        self.checkBox2.setCheckable(False)
        self.checkBox3.setCheckable(False)
        self.checkBox4.setCheckable(False)
        self.checkBox5.setCheckable(False)
        self.checkBox6.setCheckable(False)
        self.checkBox7.setCheckable(False)

    def enableCheckbox(self):
        self.checkBoxAll.setCheckable(True)
        self.checkBox1.setCheckable(True)
        self.checkBox2.setCheckable(True)
        self.checkBox3.setCheckable(True)
        self.checkBox4.setCheckable(True)
        self.checkBox5.setCheckable(True)
        self.checkBox6.setCheckable(True)
        self.checkBox7.setCheckable(True)


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    # 프로그램 화면을 보여주는 코드
    myWindow.show()
    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
