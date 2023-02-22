import sys
from PyQt6.QtWidgets import QApplication, QWidget, QSlider, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog
from PyQt6.QtGui import QIcon, QFont

from PyQt6.QtGui import QPalette
from PyQt6.QtGui import QColor
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from PyQt6.QtCore import QUrl
from PyQt6.QtCore import Qt


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WinAll")
        self.resize(400, 400)
        self.setFont(QFont("Candara", 12))

        self.dict_name = {}
        self.indexinglist = []
        self.is_playing = False
        self.player = QMediaPlayer()


        # Set the color scheme
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(14, 10, 49))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 25, 20))
        self.setPalette(palette)

        # Create a vertical layout for the widget
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create a horizontal layout for the add and delete buttons
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        # Create the Add button
        self.add_button = QPushButton("Add song", self)
        self.add_button.clicked.connect(self.add_song)
        self.add_button.setIcon(QIcon('plus_but.jpeg'))
        button_layout.addWidget(self.add_button)

        # Create the Delete button
        self.delete_button = QPushButton("Del song",self)
        self.delete_button.clicked.connect(self.del_song)
        self.delete_button.setIcon(QIcon('del.jpeg'))
        button_layout.addWidget(self.delete_button)

        # Create the Volume Slider
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.valueChanged[int].connect(self.changeValue)
        button_layout.addWidget(self.volume_slider)


        # Create a QListWidget for the songs
        self.song_list = QListWidget()
        self.song_list.clicked.connect(self.clicked)
        main_layout.addWidget(self.song_list)


        # Create a horizontal layout for the music controls
        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        # Create the Play button
        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect(self.play)
        self.play_button.setIcon(QIcon('play_but.jpeg'))
        control_layout.addWidget(self.play_button)

        # Create the Pause button
        self.pause_button = QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.pause_button.setIcon(QIcon('pause_but.jpeg'))
        control_layout.addWidget(self.pause_button)

        # Create the Stop button
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setIcon(QIcon('stop_but.jpeg'))
        control_layout.addWidget(self.stop_button)

        # Create the Next button
        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.next)
        self.next_button.setIcon(QIcon('next_but.jpeg'))
        control_layout.addWidget(self.next_button)

        # Create the Previous button
        self.previous_button = QPushButton("Previous", self)
        self.previous_button.clicked.connect(self.previous)
        self.previous_button.setIcon(QIcon('prev_but.jpeg'))
        control_layout.addWidget(self.previous_button)


    # Functions
    def changeValue(self, value):
        # Changing volume by QSlider
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.audioOutput().setVolume(value)
        self.current_volume = self.audio_output.volume()

    def clicked(self):
        #Choose song in list and return way to file
        self.name = (self.song_list.currentItem()).text()
        self.path_to_file = self.dict_name[self.name]
        return self.path_to_file

    def add_song(self):
        #Adding song to playlist
        self.temp_song = QFileDialog.getOpenFileName(self, 'Open file', '/', "Mp3 files (*.mp3)")  ###
        short_name = self.temp_song[0].split("/")[-1]
        if short_name not in self.dict_name:
            self.song_list.addItem(short_name)
            self.dict_name[short_name] = self.temp_song[0]
            self.indexinglist.append(short_name)
        return self.song_list, self.indexinglist

    def del_song(self):
        #Deleting song from playlist
        if self.name in self.indexinglist:
            self.indexinglist.remove(self.name)
            del self.dict_name[self.name]
            for item in self.song_list.selectedItems():
                self.song_list.takeItem(self.song_list.row(item))

    def play(self):
        #Playing
        self.is_playing = True
        try:
            self.player.setSource(QUrl(self.path_to_file))
            self.player.play()
            self.current_song_index = self.indexinglist.index(self.name)
        except:
            pass
        return self.current_song_index

    def toggle_pause(self):
        #Pausing
        try:
            if self.is_playing:
                self.player.pause()
                self.is_playing = False
                self.pause_button.setText("Resume")
            else:
                self.player.play()
                self.is_playing = True
                self.pause_button.setText("Pause")
        except:
            pass

    def stop(self):
        #Stoping
        self.player.stop()
        self.song_list.clearSelection()
        self.song_list.setCurrentItem(None)

    def previous(self):
        #Move back in playlist
        if self.current_song_index > 0:
            self.current_song_index -= 1
            self.name = self.indexinglist[self.current_song_index]
            self.path_to_file = self.dict_name[self.name]
            self.player.setSource(QUrl(self.path_to_file))
            self.player.play()
            self.song_list.setCurrentRow(self.current_song_index)
            self.song_list.item(self.current_song_index).setSelected(True)

    def next(self):
        #Move forward in playlist
        if self.current_song_index < len(self.indexinglist)-1:
            self.current_song_index += 1
            print(self.current_song_index)
        else:
            self.current_song_index = 0

        self.name = self.indexinglist[self.current_song_index]
        self.path_to_file = self.dict_name[self.name]
        self.player.setSource(QUrl(self.path_to_file))
        self.player.play()
        self.song_list.setCurrentRow(self.current_song_index)
        self.song_list.item(self.current_song_index).setSelected(True)


def main():

    app = QApplication(sys.argv)
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

