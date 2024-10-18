from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, Qt

class MediaHandler:
    def __init__(self, media_data, parent_layout):
        self.media_data = media_data
        self.media_player = None
        self.video_widget = None
        self.layout = parent_layout
        self.setup_media()

    def setup_media(self):
        if isinstance(self.media_data, list):
            for media in self.media_data:
                self._add_media(media)
        else:
            self._add_media(self.media_data)

    def _add_media(self, media):
        if isinstance(media, str):
            if media.lower().endswith(('.mp4', '.avi', '.mov')):
                self._setup_video(media)
            else:
                self._setup_image(media)

    def _setup_video(self, media_path):
        self.video_widget = QVideoWidget()
        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setSource(QUrl.fromLocalFile(media_path))
        self.layout.addWidget(self.video_widget)

        play_button = QPushButton("播放/暂停")
        play_button.clicked.connect(self.play_pause_video)
        self.layout.addWidget(play_button)

    def _setup_image(self, media_path):
        image = QLabel()
        pixmap = QPixmap(media_path)
        if not pixmap.isNull():
            image.setPixmap(pixmap.scaled(300, 300))
        self.layout.addWidget(image)

    def play_pause_video(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def add_media(self, path, layout):
        if path.endswith(('.png', '.jpg', '.jpeg')):
            label = QLabel()
            pixmap = QPixmap(path)
            label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
            layout.addWidget(label)
        elif path.endswith(('.mp4', '.avi', '.mov')):
            label = QLabel("视频文件：" + path)
            layout.addWidget(label)
        else:
            label = QLabel("不支持的媒体类型：" + path)
            layout.addWidget(label)
