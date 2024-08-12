# main_script.py

import sys
import os
import cv2
import numpy as np
from PIL import Image, ImageOps
import moviepy.editor as mp
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
                             QProgressBar, QLineEdit, QMessageBox, QComboBox, QFormLayout)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal

import custom_styles

def custom_posterize(image, bits):
    num_colors = 2 ** bits
    img_array = np.array(image)
    img_array = img_array / 255.0
    img_array = np.floor(img_array * (num_colors - 1))
    img_array = (img_array / (num_colors - 1)) * 255
    return Image.fromarray(img_array.astype('uint8'))

def convert_frame_to_style(frame, bits, style_name):
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img_resized = img.resize((256, 240), Image.NEAREST)

    if bits <= 8:
        img_posterized = ImageOps.posterize(img_resized, bits)
    else:
        img_posterized = custom_posterize(img_resized, bits)

    if style_name:
        palette = custom_styles.get_palette(style_name)
        if palette:
            palette_img = Image.new('P', (1, 1))
            palette_img.putpalette(palette * 16)
            img_style = img_posterized.convert('RGB').quantize(palette=palette_img)
        else:
            img_style = img_posterized
    else:
        img_style = img_posterized

    return cv2.cvtColor(np.array(img_style.convert('RGB')), cv2.COLOR_RGB2BGR)

def convert_image_to_style(input_image_path, output_image_path, bits, style_name):
    try:
        img = Image.open(input_image_path)
        img_style = convert_frame_to_style(np.array(img), bits, style_name)
        img_style_pil = Image.fromarray(cv2.cvtColor(img_style, cv2.COLOR_BGR2RGB))
        img_style_pil.save(output_image_path, format='png')
    except Exception as e:
        raise e

def convert_video_to_style(input_video_path, output_video_path, bits, style_name, progress_signal):
    try:
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            raise Exception("Erro ao abrir o vídeo de entrada.")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        temp_video_path = 'temp_converted_video.mp4'
        out = cv2.VideoWriter(temp_video_path, fourcc, fps, (256, 240))

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_style = convert_frame_to_style(frame, bits, style_name)
            out.write(frame_style)

            frame_count += 1
            progress = (frame_count / total_frames) * 100
            progress_signal.emit(int(progress))

        cap.release()
        out.release()

        combine_audio_video(input_video_path, temp_video_path, output_video_path)

        os.remove(temp_video_path)

    except Exception as e:
        raise e

def combine_audio_video(input_video_path, temp_video_path, output_video_path):
    original_video = mp.VideoFileClip(input_video_path)
    converted_video = mp.VideoFileClip(temp_video_path)

    audio = original_video.audio

    final_video = converted_video.set_audio(audio)

    final_video.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

class ConvertThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, input_path, output_path, bits, style_name, is_image):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.bits = bits
        self.style_name = style_name
        self.is_image = is_image

    def run(self):
        try:
            with open(os.devnull, 'w') as fnull:
                sys.stdout = fnull
                sys.stderr = fnull
                if self.is_image:
                    convert_image_to_style(self.input_path, self.output_path, self.bits, self.style_name)
                else:
                    convert_video_to_style(self.input_path, self.output_path, self.bits, self.style_name, self.progress)
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
            self.finished.emit()
        except Exception as e:
            QMessageBox.critical(None, "Erro", str(e))

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Jasper Retro Converter'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        layout = QVBoxLayout()
        self.setLayout(layout)

        header_layout = QVBoxLayout()
        self.label_welcome = QLabel("Jasper Retro Converter", self)
        self.label_welcome.setAlignment(Qt.AlignCenter)
        self.label_welcome.setFont(QFont('Arial', 24, QFont.Bold))
        self.label_welcome.setStyleSheet("color: #333;")
        header_layout.addWidget(self.label_welcome)
        layout.addLayout(header_layout)

        form_layout = QFormLayout()
        self.label_bits = QLabel("Número de Bits:")
        self.entry_bits = QLineEdit()
        self.entry_bits.setPlaceholderText("Digite o número de bits (1-64)")
        form_layout.addRow(self.label_bits, self.entry_bits)

        self.label_style = QLabel("Escolha o Estilo:")
        self.style_combobox = QComboBox()
        self.style_combobox.addItems(["Nenhum Estilo"] + list(custom_styles.default_palettes.keys()))
        form_layout.addRow(self.label_style, self.style_combobox)

        self.file_type_combobox = QComboBox()
        self.file_type_combobox.addItems(["Vídeo", "Imagem"])
        form_layout.addRow(QLabel("Tipo de Arquivo:"), self.file_type_combobox)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.button_convert = QPushButton('Converter')
        self.button_convert.clicked.connect(self.start_conversion)
        button_layout.addWidget(self.button_convert)

        self.button_load_jrc = QPushButton('Carregar Estilo .jrc')
        self.button_load_jrc.clicked.connect(self.load_custom_jrc)
        button_layout.addWidget(self.button_load_jrc)

        layout.addLayout(button_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar)

    def load_custom_jrc(self):
        jrc_file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo .jrc", filter="Arquivos .jrc (*.jrc)")
        if jrc_file_path:
            try:
                name, palette = custom_styles.load_custom_palette(jrc_file_path)
                custom_styles.add_custom_palette(name, palette)
                self.style_combobox.addItem(name)
                QMessageBox.information(self, "Sucesso", "Estilo carregado com sucesso!")
            except ValueError as e:
                QMessageBox.critical(self, "Erro ao Carregar Estilo", str(e))

    def start_conversion(self):
        file_type = self.file_type_combobox.currentText()
        is_image = file_type == "Imagem"

        input_path, _ = QFileDialog.getOpenFileName(self, f"Selecionar {file_type} de Entrada", filter="Todos os Arquivos (*.*)")
        if not input_path:
            QMessageBox.warning(self, "Aviso", f"Nenhum {file_type} selecionado. Por favor, selecione um {file_type}.")
            return

        output_path, _ = QFileDialog.getSaveFileName(self, f"Salvar {file_type} de Saída", filter=f"{'Imagens (*.png)' if is_image else 'Vídeos (*.mp4)'}")
        if not output_path:
            QMessageBox.warning(self, "Aviso", f"Nenhum local para salvar o {file_type} foi selecionado. Por favor, selecione um local.")
            return

        if is_image and not output_path.lower().endswith('.png'):
            output_path += '.png'
        elif not is_image and not output_path.lower().endswith('.mp4'):
            output_path += '.mp4'

        try:
            bits = int(self.entry_bits.text())
            if bits <= 0 or bits > 64:
                QMessageBox.critical(self, "Erro", "O número de bits deve estar entre 1 e 64.")
                return

            style_name = self.style_combobox.currentText()
            self.thread = ConvertThread(input_path, output_path, bits, style_name, is_image)
            self.thread.progress.connect(self.update_progress)
            self.thread.finished.connect(self.conversion_finished)
            self.thread.start()

        except ValueError:
            QMessageBox.critical(self, "Erro", "Por favor, insira um número válido de bits.")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def conversion_finished(self):
        QMessageBox.information(self, "Concluído", "Conversão concluída com sucesso.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.showMaximized()  # Define a janela para tela cheia
    sys.exit(app.exec_())
