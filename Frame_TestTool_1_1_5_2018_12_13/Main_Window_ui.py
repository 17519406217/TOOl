import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QTcpSocket
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import socket
class Dsp_TestTool_Window(QWidget):
    def __init__(self):
        super(Dsp_TestTool_Window,self).__init__()
        self.initUI()
        self.showMaximized()  # 全屏

    def initUI(self):
        global win, curve
        Layout = QGridLayout(self)                  #网格布局
        Layout.setSpacing(20)
        Vertical = QVBoxLayout()                    #垂直布局
        Horizontal = QHBoxLayout()
        Horizontal_Variate_Log = QHBoxLayout()      #水平布局
        upside_Splitter = QSplitter(Qt.Horizontal)  #分隔器/水平布局
        bottom_Splitter = QSplitter(Qt.Horizontal)  #分隔器/水平布局
        VBox_Splitter = QSplitter(Qt.Vertical)      #分隔器/垂直布局
        self.mdiwindow = QMdiArea()

        self.Mainmenubar = QMenuBar(self)                   #创建菜单栏
        FileMeny = self.Mainmenubar.addMenu('文件&(P)')     #菜单栏选项
        Open_Project = QAction(QIcon("./images/打开.png"),'打开工程...', self)         #子选项创建
        Save_Project = QAction(QIcon("./images/保存.png"),'保存工程...', self)
        Save_as = QAction(QIcon("./images/另存为.png"),'另存为...', self)
        Esc = QAction('退出...', self)
        FileMeny.addAction(Open_Project)            #添加子选项
        FileMeny.addAction(Save_Project)
        FileMeny.addAction(Save_as)
        FileMeny.addAction(Esc)

        OperationMeny = self.Mainmenubar.addMenu('操作&(C)')
        Search_Sys = QAction(QIcon("./images/搜索.png"),'搜索系统', self)
        Refresh = QAction(QIcon("./images/刷新.png"),'刷新', self)
        Data_Export = QAction(QIcon("./images/导出.png"),'数据导出...', self)
        BooT = QAction('Boot', self)
        Reset = QAction(QIcon("./images/复位.png"),'复位', self)
        Send_Break_Off = QAction('发中断', self)
        Send_Signal= QAction(QIcon("./images/信号.png"),'发信号', self)
        OperationMeny.addAction(Search_Sys)
        OperationMeny.addAction(Refresh)
        OperationMeny.addAction(Data_Export)
        OperationMeny.addAction(BooT)
        OperationMeny.addAction(Reset)
        OperationMeny.addAction(Send_Break_Off)
        OperationMeny.addAction(Send_Signal)


        self.WindowMeny = self.Mainmenubar.addMenu('窗口&(W)')
        Text_Window = QAction(QIcon("./images/新建文本窗.png"),'新建文本窗', self)
        self.Graphic_Window = QAction(QIcon("./images/图形窗.png"),"新建图形窗", self)
        Window_Sort = QAction(QIcon("./images/排列.png"),'窗体排列', self)
        self.WindowMeny.addAction(Text_Window)
        self.WindowMeny.addAction(self.Graphic_Window)
        self.WindowMeny.addAction(Window_Sort)

        self.Graphic_Window.triggered.connect(self.Oscillogram)


        SetMeny = self.Mainmenubar.addMenu('设置&(S)')
        Sys_Set = QAction('系统设置', self)
        SetMeny.addAction(Sys_Set)
        HelpMeny = self.Mainmenubar.addMenu('帮助&(H)')

        self.Window_Scan_Equipment = QTreeWidget()                 #设备显示界面
        self.Window_Variate_View = QTableWidget(1,2)             #变量显示界面
        self.Window_Variate_View.setShowGrid(True)               #变量界面背景表格
        self.Window_Variate_View.setHorizontalHeaderLabels(['Key','Value'])
        self.Window_Variate_View.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)       #列宽是自动分配
        self.Window_Variate_View.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)#手动调整宽度
        self.Window_Variate_View.verticalHeader().setDefaultSectionSize(20)
        Window_Log_view = QTabWidget()                           #日志显示界面



        #工具栏
        self.tb = QToolBar(self)
        self.tb.setFixedHeight(28)
        self.New = QAction(QIcon("./images/新建.png"),"新建",self)
        self.tb.addAction(self.New)
        self.New.triggered.connect(self.New_Project)

        self.Open = QAction(QIcon("./images/打开.png"),"打开",self)
        self.tb.addAction(self.Open)

        self.Save = QAction(QIcon("./images/保存.png"),"保存",self)
        self.tb.addAction(self.Save)

        self.Reset = QAction(QIcon("./images/复位.png"),"复位",self)
        self.tb.addAction(self.Reset)

        self.Operation = QAction(QIcon("./images/运行程序.png"),"运行",self)
        self.tb.addAction(self.Operation)
        self.Operation.triggered.connect(self.slotStart)  # 启动socket

        self.Search = QAction(QIcon("./images/搜索.png"), "搜索系统", self)
        self.tb.addAction(self.Search)

        self.WindowMeny_Graphic = QAction(QIcon("./images//图形窗.png"),"新建图形窗",self)
        self.tb.addAction(self.WindowMeny_Graphic)
        self.WindowMeny_Graphic.triggered.connect(self.Oscillogram)

        self.socket_thread = Socket_worker()
        self.socket_thread.sinOut.connect(self.Show_Data)
        #设备显示界面
        self.Window_Scan_Equipment.setHeaderHidden(1)#隐藏表头
        self.root = QTreeWidgetItem(self.Window_Scan_Equipment)#添加节点

        self.root.setText(0,"ROOT")
        self.root.setIcon(0,QIcon("./images/节点选择.png"))

        child1 = QTreeWidgetItem(self.root)
        child1.setText(0,'child1')
        child1.setIcon(0,QIcon("./images/芯片.png"))
        #Qss样式表
        self.Window_Scan_Equipment.setStyleSheet("QTreeView{border-width:1px}"
                                                 "QTreeView{border-style:ridge}"
                                                 "QTreeView{border-color:gray}")
        self.Window_Variate_View.setStyleSheet("QTableWidget{border-width:3px}"
                                               "QTableWidget{border-style:ridge}"
                                               "QTableWidget{border-color:gray}")
        self.Mainmenubar.setStyleSheet("QMenuBar{border-width:0.1px}"
                                       "QMenuBar{border-style:inset}"
                                       "QMenuBar{border-color:gray}"
                                       "QMenuBar{background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(255,255,255) ,stop:1 rgb(176,196,222))}")
        self.mdiwindow.setStyleSheet("QMdiArea{border-width:3px}"
                                     "QMdiArea{border-style:inset}"
                                     "QMdiArea{border-color:gray}")
        self.tb.setStyleSheet("QToolBar{border-width:0.5px}"
                              "QToolBar{border-style:ridge}"
                              "QToolBar{border-color:gray}")
        Window_Log_view.addTab(QLabel("日志"), "日志 &L")
        Window_Log_view.addTab(QLabel("报告"), "报告 &Q")
        Window_Log_view.setTabPosition(QTabWidget.South)

        upside_Splitter.addWidget(self.Window_Scan_Equipment)                    #添加设备显示界面到分隔器布局中
        upside_Splitter.addWidget(self.mdiwindow)
        upside_Splitter.setStretchFactor(1,7)
        Horizontal.addWidget(upside_Splitter)                               #添加 设备显示界面 到水平布局中
        Vertical.addWidget(self.Mainmenubar)                                #将菜单栏和Horizontal布局添加到 vertical垂直布局中
        Vertical.addWidget(self.tb)
        Vertical.addLayout(Horizontal,1)

        Layout.addLayout(Vertical,2,0)                                      #参数说明 参数一为子布局 参数二是行 参数三列

        bottom_Splitter.addWidget(self.Window_Variate_View)                 #添加变量显示界面 到分割器布局中
        bottom_Splitter.addWidget(Window_Log_view)                          #添加日志显示界面 到分隔器布局中
        bottom_Splitter.setStretchFactor(0,3)
        bottom_Splitter.setStretchFactor(1,7)
        Horizontal_Variate_Log.addWidget(bottom_Splitter)                   #添加分隔器布局到水平布局中

        Layout.addLayout(Horizontal_Variate_Log,3,0,5,5)                    #参数说明# 参数一为 子布局 参数二是行 参数三列,参数四跨越行数，参数五跨越列数
        Layout.setSpacing(1)
        Layout.setContentsMargins(0,0,0,0)                                  #网格布局距离窗口四个方向距离

    def slotStart(self):

        #self.Operation.setEnabled(False)
        self.socket_thread.start()





#工作线程，将数据处理并发送到界面

class Socket_worker(QThread):
    sinOut = pyqtSignal(int)
    host_ip_addr = '192.168.2.110'
    port = 8080
    sock_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_send.connect((host_ip_addr, port))

    def __init__(self,parent=None):
        super(Socket_worker,self).__init__(parent)
        self.worling = True
    def run(self):

        while(1):
            if self.worling == 1:

                self.data_x = (qrand()%(54-0)) + 0#创建随机数
                self.sinOut.emit(self.data_x)#发送信号
                self.sleep(1)
            elif self.worling == 0:

                #self.sock_send.sendall(b'hi , server')
                data = self.sock_send.recv(10)
                self.sock_send.close()
                print(data)
                break




class COntrol_UI(Dsp_TestTool_Window):



    def __init__(self):
        super(COntrol_UI, self).__init__()

        self.setWindowTitle("DSP_TestTool")
        self.test_list = []
        self.Window_Scan_Equipment.setDragEnabled(True)
        self.Window_Variate_View.setAcceptDrops(True)


    def Show_Data(self):#intX

        Socket_worker.sock_send.sendall(b"request link...")
        #print(intX)
        #self.test_list.append(intX)
        #print(self.test_list)

        #改变worling值 停止线程
        import gc
        for obj in gc.get_objects():
            if isinstance(obj,Socket_worker):
                obj.worling = 0

    def New_Project(self):
        pass

    def Oscillogram(self,content):
        Sender = self.sender()
        #if content == self.Save or content == self.Graphic_Window:
        #print(Sender.text())
        if Sender.text() == "新建图形窗":
            win = pg.GraphicsWindow()
            win.setWindowIcon(QIcon("./images/图形窗.png"))
            win.setWindowTitle(u'Graphical View')
            win.resize(700, 450)
            x = [9,8,7,6,5,4,3,2,1,0]#np.linspace(-5 * np.pi, 5 * np.pi, 500)
            y3 = [0,1,2,3,4,5,6,7,8,9]#np.sinc(x)
            p3 = win.addPlot(left='Amplitude', bottom='x', title='Graphical View', colspan=2)
            for p, y, pen in zip([p3], [y3], ['y']):
                    #self.cstg = self.slotAdd()
                p.plot(x, y, pen=pen)
                p.showGrid(x=True, y=True)
                       #p.setRange(xRange=[-5 * np.pi, 5 * np.pi], yRange=[-2.3, 2.3], padding=0)
                    # pg.setConfigOptions(antialias=True)
                    # self.p6 = self.win.addPlot(title="Oscillogram")
                    # self.p6.showGrid(x=True, y=True)
                    # self.curve = self.p6.plot(pen='y')
                    # self.data = np.random.normal(size=(10, 1000))
                    # self.ptr = 0
                    #
                    #
                    # self.timer = QtCore.QTimer()
                    # self.timer.timeout.connect(self.Update)
                    # self.timer.start(50)
                    # self.win.setWindowTitle('Oscillogram')
        self.mdiwindow.addSubWindow(win)
        win.show()


    #持续刷新绘图界面
    def Update(self):
        global curve, data, p6
        self.curve.setData(self.data[self.ptr%10])
        if self.ptr == 0:
            self.p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
            #self.curve = self.p6.plot(pen='r')
        self.ptr += 1



if __name__ == "__main__":

    #if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):

    app = QApplication(sys.argv)
    form = COntrol_UI()

    sys.exit(app.exec_())