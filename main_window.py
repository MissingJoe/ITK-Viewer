#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @Author Fivethousand
    @Date 2021/4/30 13:53
    @Describe 
    @Version 1.0
"""
import time

from Display_widget import Display_widget
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPalette, QFont, QCursor,QTextCharFormat,QColor,QTextCursor,QTextBlockFormat
from PyQt5.QtWidgets import QMainWindow, QMenu, QTreeWidgetItem, QLabel, QSizePolicy, QTreeWidget, QFileDialog, QWidget, \
    QProgressBar,QRadioButton,QPushButton,QTextEdit
from PyQt5 import QtCore
import sys
from Slices_Viewer_Widget import Slice_Viewer_Widget
from Signal_Central_Process_Unit import SCPU
from VTK_Viewer_widget import VTK_Viewer_widget
from Drop_Tree_Widget import Drop_Tree_Widget
import numpy as np
from Switch_Button import SwitchBtn
class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.init_widgets()
        self.init_UI()
        self.init_connection()
    def init_widgets(self):
        self.Display_Widget=Display_widget()
        # self.Display_Widget.load_data('D://changhai//ct//tumor_CT//P1219041803//c_2.nii.gz')

    def init_UI(self):
        self.setWindowIcon(QIcon("GUI-resourses/FT-icon.png"))
        self.setWindowTitle("胰腺肿瘤在线诊断系统")
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        #self.main_widget.setObjectName('main_widget')
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        self.main_widget.setLayout(self.main_layout)
        #self.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.resize(1200,800)
        self.left_widget= QtWidgets.QWidget()  # 创建窗口左部件
        self.left_layout=QtWidgets.QGridLayout()
        self.left_widget.setLayout(self.left_layout)
        self.main_layout.addWidget(self.left_widget, 0, 0)
        self.main_layout.addWidget(self.Display_Widget,0,1)

        self.create_file_import_components()

        # 创建结果显示区域
        self.create_result_display()

        self.left_pbar_container_widget=QtWidgets.QWidget(self.left_widget)
        self.pbar = QProgressBar(self.left_widget)
        self.model_btn=QRadioButton(self.left_widget)
        self.model_btn.setText("CLS")
        self.left_layout.addWidget(self.pbar,21,1,1,9)
        self.left_layout.addWidget(self.model_btn,21,0,1,1)
        self.left_layout.setSpacing(20)
        # self.left_layout.addWidget(self.left_pbar_container_widget)
        # self.left_treewidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.model_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        #self.left_pbar_container_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.left_pbar_container_layout= QtWidgets.QHBoxLayout()
        # self.left_pbar_container_widget.setLayout(self.left_pbar_container_layout)
        # self.left_pbar_container_layout.addWidget(self.pbar)


       # self.model_btn=SwitchBtn(self.left_pbar_container_widget)
#        self.left_pbar_container_layout.addWidget(self.model_btn)
        #self.pbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def init_connection(self):
        # self.left_treewidget.file_text_signal.connect(self.handle_drop_file)
        self.model_btn.toggled.connect(self.handle_model_btn_clicked)
        self.Display_Widget.pbar_signal.connect(self.progress_bar_effect)

    def create_file_import_components(self):
        # 1. 导入数据
        self.data_button = QPushButton("导入数据", self.left_widget)
        self.data_button.clicked.connect(lambda: self.load_data_file(self.data_text, "数据文件 (*.nii *.nii.gz)"))
        self.data_text = QTextEdit(self.left_widget)
        self.data_text.setReadOnly(True)
        self.data_text.setFixedHeight(60)

        # 2. 导入数据标签
        self.label_button = QPushButton("导入数据标签", self.left_widget)
        self.label_button.clicked.connect(lambda: self.load_lable_file(self.label_text, "标签文件 (*.nii *.nii.gz)"))
        self.label_text = QTextEdit(self.left_widget)
        self.label_text.setReadOnly(True)
        self.label_text.setFixedHeight(60)

        # 3. 导入模型
        self.model_button = QPushButton("导入模型", self.left_widget)
        self.model_button.clicked.connect(lambda: self.load_model_file(self.model_text, "模型文件 (*.pt)"))
        self.model_text = QTextEdit(self.left_widget)
        self.model_text.setReadOnly(True)
        self.model_text.setFixedHeight(60)

        # 将组件添加到左侧布局
        self.left_layout.addWidget(self.data_button, 0, 0, 1, 10)  # 导入数据按钮
        self.left_layout.addWidget(self.data_text, 1, 0, 1, 10)  # 数据文件文本框
        self.left_layout.addWidget(self.label_button, 2, 0, 1, 10)  # 导入数据标签按钮
        self.left_layout.addWidget(self.label_text, 3, 0, 1, 10)  # 数据标签文本框
        self.left_layout.addWidget(self.model_button, 4, 0, 1, 10)  # 导入模型按钮
        self.left_layout.addWidget(self.model_text, 5, 0, 1, 10)  # 模型文件文本框

    def create_result_display(self):
        # 创建结果显示区域
        self.result_label = QLabel("分类结果", self.left_widget)  # 分类结果标签
        self.result_text = QTextEdit(self.left_widget)  # 结果显示文本框
        self.result_text.setReadOnly(True)
        self.result_text.setFixedHeight(100)

        # 将结果显示区域添加到左侧布局
        self.left_layout.addWidget(self.result_label, 6, 0, 1, 2)  # 分类结果标签
        self.left_layout.addWidget(self.result_text, 6, 2, 1, 8)  # 结果显示文本框

    def load_data_file(self, text_widget, filter_str):
        # 打开文件对话框，选择文件
        default_path = r'C:\Users\Administrator\Desktop\data'
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", default_path, filter_str)
        if file_path:
            text_widget.setText(file_path)  # 将文件路径显示在文本框中
            self.Display_Widget.load_data(file_path=file_path)
            data = 1
            if data is not None:
                print("数据读取成功！")
            else:
                print("数据读取失败！")

    def load_lable_file(self, text_widget, filter_str):
        # 打开文件对话框，选择文件
        default_path = r'C:\Users\Administrator\Desktop\data'
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", default_path, filter_str)
        if file_path:
            text_widget.setText(file_path)  # 将文件路径显示在文本框中
            self.Display_Widget.load_label_data(file_path)
            data = 1
            if data is not None:
                print("标签读取成功！")
            else:
                print("标签读取失败！")

    def load_model_file(self, text_widget, filter_str):
        # 打开文件对话框，选择文件
        default_path = r'C:\Users\Administrator\Desktop\data'
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", default_path, filter_str)
        if file_path:
            text_widget.setText(file_path)  # 将文件路径显示在文本框中
            # data = self.read_file(file_path)
            data = 1
            if data is not None:
                print("模型读取成功！")
            else:
                print("模型读取失败！")


    def handle_model_btn_clicked(self):
        if self.model_btn.isChecked()==True:            #do segmentation
            self.result_text.clear()
            self.Display_Widget.rt_si()
            # 创建 QTextCharFormat 对象
            format = QTextCharFormat()
            format.setFontWeight(QFont.Bold)  # 设置加粗
            format.setFontPointSize(18)  # 设置字体大小为 16
            format.setForeground(QColor("blue"))  # 设置字体颜色为蓝色
            format1 = QTextCharFormat()
            format1.setFontWeight(QFont.Bold)  # 设置加粗
            format1.setFontPointSize(18)  # 设置字体大小为 16
            format1.setForeground(QColor("red"))  # 设置字体颜色为蓝色

            block_format = QTextBlockFormat()
            block_format.setAlignment(Qt.AlignCenter)  # 设置文本居中对齐

            # 获取 QTextCursor 对象
            cursor = self.result_text.textCursor()

            # 设置块格式
            # cursor.setBlockFormat(block_format)

            # 插入加粗、指定大小和颜色的文本
            cursor.insertText("诊断结果：PDAC \n", format)  # 插入 "Hello"
            cursor.insertText("不确定性：0.03", format1)  # 插入 "world"

            # 将光标移动到文本末尾
            self.result_text.moveCursor(QTextCursor.End)
            self.result_text.setStyleSheet(
                """
                QTextEdit {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                """
            )
        else:
            self.result_text.clear()

    def FixSize(self):
        self.setFixedSize(1500,1000)


    def progress_bar_effect(self):              # just for show
        for i in range(100):
            self.pbar.setValue(i+1)
            time.sleep(0.01)


if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        myWin = MainWindow()
        myWin.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        myWin.show()
        myWin.FixSize()
        sys.exit(app.exec_())