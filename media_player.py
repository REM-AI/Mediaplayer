import subprocess

from PyQt5.QtGui import QIcon, QFont, QKeySequence
from PyQt5.QtCore import QDir, Qt, QUrl, QSize, QTime
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, QMessageBox, 
        QShortcut,
        QLineEdit,QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QStatusBar)
from style_sheet import stylesheet

class window(QWidget):
    def __init__(self, parent=None):
        super(window, self).__init__(parent)
        self.init_ui()
        self.init_layout()
        self.init_signals()
        self.hot_keys()

    def init_ui(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget(self)

        # create a open button
        self.open_button = QPushButton()   
        self.open_button.setFixedSize(24, 24)
        self.open_button.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        self.open_button.setStyleSheet(stylesheet(self))
        self.open_button.clicked.connect(self.load_file)

        # create a info button
        self.info_button = QPushButton()
        self.info_button.setFixedSize(24, 24)
        self.info_button.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))
        self.info_button.setStyleSheet(stylesheet(self))
        self.info_button.clicked.connect(self.handleInfo)

        # create a play button
        self.play_button = QPushButton()
        self.play_button.setEnabled(False)
        self.play_button.setFixedSize(32, 32)
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.setStyleSheet(stylesheet(self))
        self.play_button.clicked.connect(self.play)
        
        # create a fullscreen button
        self.fullScreen_button = QPushButton()
        self.fullScreen_button.setFixedSize(32, 32)
        self.fullScreen_button.setIcon(QIcon.fromTheme("view-fullscreen"))
        self.fullScreen_button.setStyleSheet(stylesheet(self))
        self.fullScreen_button.clicked.connect(self.fullscreen_handler)

        # create a fullscreen videowidget button
        self.fullScreen_videowidget_button = QPushButton()
        self.fullScreen_videowidget_button.setFixedSize(32, 32)
        self.fullScreen_videowidget_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.fullScreen_videowidget_button.setStyleSheet(stylesheet(self))
        self.fullScreen_videowidget_button.clicked.connect(self.fullScreen_videowidget)
        self.fullScreen_videowidget_button.hide()

        # create a timeline slider
        self.timeline_slider = QSlider(Qt.Horizontal)
        self.timeline_slider.setFixedHeight(8)
        self.timeline_slider.setRange(0, 0)
        self.timeline_slider.setStyleSheet(stylesheet(self))
        self.timeline_slider.sliderMoved.connect(self.setPosition)

        # create a timeline lable
        self.timeline_label = QLineEdit('00:00:00')
        self.timeline_label.setReadOnly(True)
        self.timeline_label.setFixedSize(70, 32)
        self.timeline_label.setUpdatesEnabled(True)
        self.timeline_label.setStyleSheet(stylesheet(self))
        self.timeline_label.selectionChanged.connect(lambda: self.timeline_label.setSelection(0, 0))
        
        # create a end timeline lable  
        self.end_timeline_label = QLineEdit('00:00:00')
        self.end_timeline_label.setReadOnly(True)
        self.end_timeline_label.setFixedSize(70, 32)
        self.end_timeline_label.setUpdatesEnabled(True)
        self.end_timeline_label.setStyleSheet(stylesheet(self))
        self.end_timeline_label.selectionChanged.connect(lambda: self.end_timeline_label.setSelection(0, 0))

        # create a timeline forward button
        self.timeline_forward = QPushButton()
        self.timeline_forward.setFixedSize(32, 32)
        self.timeline_forward.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.timeline_forward.setStyleSheet(stylesheet(self))
        self.timeline_forward.clicked.connect(self.forward_timeline)

        # create a timeline forward button
        self.timeline_backward = QPushButton()
        self.timeline_backward.setFixedSize(32, 32)
        self.timeline_backward.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.timeline_backward.setStyleSheet(stylesheet(self))
        self.timeline_backward.clicked.connect(self.backward_timeline)

        # create a audio button
        self.audio_button = QPushButton()
        self.audio_button.setFixedSize(32, 32)
        self.audio_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.audio_button.setStyleSheet(stylesheet(self))
        self.audio_button.clicked.connect(self.set_mute)

        # create a audio slider
        self.audio_slider = QSlider(Qt.Horizontal)
        self.audio_slider.setFixedHeight(32)
        self.audio_slider.setRange(0,100)
        self.audio_slider.setValue(100)
        self.audio_slider.setStyleSheet(stylesheet(self))
        self.audio_slider.sliderMoved.connect(self.setvolume_slider)

        # create a photo tab
        self.photo_tab = QLabel("Photo")
        self.photo_tab.setStyleSheet(stylesheet(self))
        self.photo_tab.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.photo_tab.setMinimumWidth(100)

         # create a Video tab
        self.video_tab = QLabel("Video")
        self.video_tab.setStyleSheet(stylesheet(self))
        self.video_tab.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.video_tab.setMinimumWidth(100)

        # create a audio volume lable
        self.volume_value = QLabel('100', self)
        self.volume_value.setFixedSize(32, 32)
        self.volume_value.setStyleSheet(stylesheet(self))
        self.volume_value.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        # create a status bar
        self.statusBar = QStatusBar()
        self.statusBar.setFont(QFont("Noto Sans", 7))
        self.statusBar.setFixedHeight(12)
        self.statusBar.setStyleSheet(stylesheet(self))


        # create a info
        self.myinfo = """
©2021
Created By Hamim Ally


HotKeys:
    Mouse Wheel = Zoom
    UP = Volume Up
    DOWN = Volume Down + 
    LEFT = < 1 Minute
    RIGHT = > 1 Minute + 
    SHIFT+LEFT = < 10 Minutes
    SHIFT+RIGHT = > 10 Minutes"""

    def hot_keys(self):
        self.shortcut = QShortcut(QKeySequence("o"), self)
        self.shortcut.activated.connect(self.load_file)
        self.shortcut = QShortcut(QKeySequence(" "), self)
        self.shortcut.activated.connect(self.play)
        self.shortcut = QShortcut(QKeySequence("f"), self)
        self.shortcut.activated.connect(self.fullscreen_handler)
        self.shortcut = QShortcut(QKeySequence("i"), self)
        self.shortcut.activated.connect(self.handleInfo)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.shortcut.activated.connect(self.forward_timeline)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.shortcut.activated.connect(self.backward_timeline)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Up), self)
        self.shortcut.activated.connect(self.volumeUp)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Down), self)
        self.shortcut.activated.connect(self.volumeDown)    

    def init_layout(self):
        # create layout_A
        self.layout_A = QHBoxLayout()
        self.layout_A.setSpacing(0)
        self.layout_A.addWidget(self.open_button)
        self.layout_A.addWidget(self.photo_tab)
        self.layout_A.addWidget(self.video_tab)
        self.layout_A.addWidget(self.info_button)
        
        # create layout_B
        self.layout_B = QHBoxLayout()
        self.layout_B.setSpacing(0)
        self.layout_B.addWidget(self.play_button)
        self.layout_B.addWidget(self.timeline_backward)
        self.layout_B.addWidget(self.timeline_label)
        self.layout_B.addWidget(self.end_timeline_label)
        self.layout_B.addWidget(self.timeline_forward)
        self.layout_B.addWidget(self.audio_button)
        self.layout_B.addWidget(self.audio_slider)
        self.layout_B.addWidget(self.volume_value)
        self.layout_B.addWidget(self.fullScreen_button)
        self.layout_B.addWidget(self.fullScreen_videowidget_button)
        
        # create layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addLayout(self.layout_A)
        self.layout.addWidget(self.statusBar)
        self.layout.addWidget(self.videoWidget)
        self.layout.addWidget(self.timeline_slider)
        self.layout.addLayout(self.layout_B)

        self.setLayout(self.layout)

    def init_signals(self):
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.statusBar.showMessage("Ready")
    
    def load_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Selected media",".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi *.mkv)")

        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.play_button.setEnabled(True)
            self.statusBar.showMessage(fileName)
            self.play()
        
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.timeline_slider.setValue(position)
        mtime = QTime(0,0,0,0)
        mtime = mtime.addMSecs(self.mediaPlayer.position())
        self.timeline_label.setText(mtime.toString())

    def durationChanged(self, duration):
        self.timeline_slider.setRange(0, duration)
        mtime = QTime(0,0,0,0)
        mtime = mtime.addMSecs(self.mediaPlayer.duration())
        self.end_timeline_label.setText(mtime.toString())

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
    
    def forward_timeline(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 100*50)
    
    def backward_timeline(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 100*50)

    def volumeUp(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() + 1)
        self.volume_value.setText(str(self.mediaPlayer.volume()))
        self.audio_slider.setValue(self.mediaPlayer.volume())
        print("Volume: " + str(self.mediaPlayer.volume()))
    
    def volumeDown(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() - 1)
        self.volume_value.setText(str(self.mediaPlayer.volume()))
        self.audio_slider.setValue(self.mediaPlayer.volume())
        print("Volume: " + str(self.mediaPlayer.volume()))

    def setvolume_slider(self,value):
        self.mediaPlayer.setVolume(value)
        self.volume_value.setText(str(self.mediaPlayer.volume()))
        if value > 0:
            self.audio_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        else:
            self.audio_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
    
    def set_mute(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() == 0)
        self.audio_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
        print("muted")

    def mouseDoubleClickEvent(self, event):
        if self.windowState() & Qt.WindowFullScreen:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.open_button.show()
            self.info_button.show()
            self.statusBar.show()
            self.timeline_slider.show()
            self.play_button.show()
            self.timeline_label.show()
            self.end_timeline_label.show()
            self.timeline_forward.show()
            self.timeline_backward.show()
            self.audio_button.show()
            self.audio_slider.show()
            self.volume_value.show()
            self.fullScreen_button.show()
            self.fullScreen_videowidget_button.show()

            
    def fullScreen_videowidget(self):
        if self.windowState() & Qt.WindowFullScreen:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.showFullScreen()
            QApplication.setOverrideCursor(Qt.BlankCursor)
            print("Fullscreen entered")
            self.open_button.hide()
            self.info_button.hide()
            self.statusBar.hide()
            self.timeline_slider.hide()
            self.play_button.hide()
            self.timeline_label.hide()
            self.end_timeline_label.hide()
            self.timeline_forward.hide()
            self.timeline_backward.hide()
            self.audio_button.hide()
            self.audio_slider.hide()
            self.volume_value.hide()
            self.fullScreen_button.hide()
            self.fullScreen_videowidget_button.hide()

    def fullscreen_handler(self):
        if self.windowState() & Qt.WindowFullScreen:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.fullScreen_videowidget_button.show()
            self.showNormal()
            self.fullScreen_videowidget_button.hide()
            print("no Fullscreen")
        else:
            self.showFullScreen()
            self.fullScreen_videowidget_button.show()
            print("Fullscreen entered")

    def handleInfo(self):
        msg = QMessageBox.about(self, "QT5 Player", self.myinfo)

    def handleError(self):
        self.play_button.setEnabled(False)
        self.statusBar.showMessage("Error: " + self.mediaPlayer.errorString())

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    player = window()
    player.widescreen = True
    player.setGeometry(100, 300, 600, 380)
    player.setWindowTitle("Media Player")
    player.show()
    sys.exit(app.exec_())