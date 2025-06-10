import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QTextEdit, QPushButton,
    QFileDialog, QGridLayout, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt, QTimer
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("t5-base")
model = T5ForConditionalGeneration.from_pretrained("t5-base")

default_article = (
    "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines. "
    "These machines are designed to think and act like humans, and they can be trained to learn "
    "from experience and perform tasks such as problem-solving, speech recognition, decision-making, and language translation. "
    "AI has evolved rapidly over the last few decades and is now embedded in many areas of modern life, "
    "from personal assistants like Siri and Alexa to self-driving cars and healthcare diagnostics."
)

class Task1FinalLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.auto_mode = False
        self.setWindowTitle("Task 1 – Article Summarizer 💻")
        self.setGeometry(200, 100, 1080, 720)
        self.setWindowOpacity(0.96)
        self.setStyleSheet("background-color: rgba(30, 30, 30, 180);")
        self.init_ui()
        self.text_input.textChanged.connect(self.schedule_auto_generate)
        self.auto_timer = QTimer()
        self.auto_timer.setSingleShot(True)
        self.auto_timer.timeout.connect(self.auto_generate_trigger)

    def schedule_auto_generate(self):
        if self.auto_mode:
            self.auto_timer.start(1000)

    def auto_generate_trigger(self):
        if self.auto_mode:
            self.summarize_article()

    def init_ui(self):
        grid = QGridLayout()
        grid.setHorizontalSpacing(25)
        grid.setVerticalSpacing(15)
        grid.setContentsMargins(20, 20, 20, 20)
        self.setLayout(grid)

        title = QLabel("CODTECH INTERNSHIP – TASK 1 🧠")
        title.setFont(QFont("Algerian", 20))
        title.setStyleSheet("color: #00ffff;")
        title.setAlignment(Qt.AlignCenter)
        grid.addWidget(title, 0, 0, 1, 3)

        label = QLabel("PASTE OR UPLOAD ARTICLE: 📄")
        label.setFont(QFont("Algerian", 20))
        label.setStyleSheet("color: #00ffff;")
        label.setAlignment(Qt.AlignCenter)
        grid.addWidget(label, 1, 0)

        output_label = QLabel("SUMMARY OUTPUT: 📌 ")
        output_label.setFont(QFont("Algerian", 20))
        output_label.setStyleSheet("color: #00ffff;")
        output_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(output_label, 1, 2)

        self.text_input = QTextEdit()
        self.text_input.setFont(QFont("Lemon", 14))
        self.text_input.setText(default_article)
        self.text_input.setStyleSheet("""
            background-color: rgba(0, 0, 0, 140);
            color: #00ffee;
            border: 1px solid #00ffff;
        """)
        grid.addWidget(self.text_input, 2, 0, 2, 1)

        self.text_output = QTextEdit()
        self.text_output.setFont(QFont("Lemon", 14))
        self.text_output.setReadOnly(True)
        self.text_output.setStyleSheet("""
            background-color: rgba(0, 0, 0, 130);
            color: #00ff88;
            border: 1px solid #33ff99;
        """)
        grid.addWidget(self.text_output, 2, 2, 2, 1)

        upload_layout = QVBoxLayout()
        upload_layout.setAlignment(Qt.AlignCenter)

        self.upload_button = QPushButton("Choose Files (.txt ~10k words) 📁")
        self.upload_button.setFont(QFont("Lemon", 16))
        self.upload_button.setStyleSheet("background-color: #00ffff; color: black;")
        self.upload_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.upload_button.clicked.connect(self.load_txt_files)
        upload_layout.addWidget(self.upload_button)

        self.uploaded_files_label = QLabel("Uploaded Files: None 📄")
        self.uploaded_files_label.setFont(QFont("Lemon", 14))
        self.uploaded_files_label.setStyleSheet("color: #00ffff;")
        self.uploaded_files_label.setAlignment(Qt.AlignCenter)
        upload_layout.addWidget(self.uploaded_files_label)

        grid.addLayout(upload_layout, 4, 0, alignment=Qt.AlignCenter)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(12)
        button_layout.setAlignment(Qt.AlignCenter)

        self.toggle_button = QPushButton("▶ Auto Generate")
        self.toggle_button.setFont(QFont("Lemon", 14))
        self.toggle_button.setStyleSheet("background-color: #00ffff; color: black;")
        self.toggle_button.setFixedHeight(40)
        self.toggle_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggle_button.clicked.connect(self.toggle_mode)

        self.summarize_button = QPushButton("✨ Summarizer ✨")
        self.summarize_button.setFont(QFont("Lemon", 14))
        self.summarize_button.setStyleSheet("background-color: #00ffff; color: black;")
        self.summarize_button.setFixedHeight(40)
        self.summarize_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.summarize_button.clicked.connect(self.summarize_article)

        button_layout.addWidget(self.toggle_button)
        button_layout.addWidget(self.summarize_button)

        grid.addLayout(button_layout, 4, 2, alignment=Qt.AlignCenter)

    def load_txt_files(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Select .txt files", "", "Text Files (*.txt)")
        combined = self.text_input.toPlainText().strip()
        for file_path in paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    combined += "\n" + f.read()
            except Exception as e:
                print("Error reading file:", e)

        words = combined.split()
        if len(words) > 10000:
            combined = ' '.join(words[:10000])
        self.text_input.setText(combined)

        file_names = [f.split("/")[-1] for f in paths]
        if file_names:
            self.uploaded_files_label.setText("Uploaded Files: 📄" + ", ".join(file_names))
        else:
            self.uploaded_files_label.setText("Uploaded Files 📄: None")

        if self.auto_mode:
            self.summarize_article()

    def summarize_article(self):
        article = self.text_input.toPlainText().strip()
        if not article:
            return

        input_text = "summarize: " + article
        input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=1024, truncation=True)

        summary_ids = model.generate(
            input_ids,
            max_length=150,
            num_beams=4,
            no_repeat_ngram_size=3,
            repetition_penalty=2.5,
            length_penalty=1.5,
            early_stopping=True
        )

        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        self.animate_summary(summary)

    def animate_summary(self, text):
        self.text_output.clear()
        self._text = text
        self._index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._show_char)
        self.timer.start(20)

    def _show_char(self):
        if self._index < len(self._text):
            self.text_output.insertPlainText(self._text[self._index])
            self._index += 1
        else:
            self.timer.stop()

    def toggle_mode(self):
        self.auto_mode = not self.auto_mode
        if self.auto_mode:
            self.toggle_button.setText("⏸ Auto Generate (On)")
            self.summarize_button.setVisible(False)
            self.summarize_article()
        else:
            self.toggle_button.setText("▶ Auto Generate (Off)")
            self.summarize_button.setVisible(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Task1FinalLayout()
    window.show()
    sys.exit(app.exec_())