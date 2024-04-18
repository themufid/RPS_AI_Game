from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from reportlab.pdfgen import canvas

def ai_move():
    import random
    choices = ['Rock', 'Paper', 'Scissors']
    return random.choice(choices)

def generate_pdf(user_score, ai_score, history):
    filename = QFileDialog.getSaveFileName(None, "Save Score as PDF", "", "PDF Files (*.pdf)")[0]
    if filename:
        c = canvas.Canvas(filename)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(200, 800, "RPS AI Game")
        
        c.setFont("Helvetica", 14)
        c.drawString(50, 750, f"Your Score: {user_score}")
        c.drawString(50, 730, f"AI Score: {ai_score}")
        
        c.drawString(50, 700, "Game History:")
        y_pos = 680
        for line in history.split('\n'):
            c.drawString(50, y_pos, line)
            y_pos -= 20
        
        c.save()
        QMessageBox.information(None, "Success", "PDF saved successfully.")

class GameWindow(QWidget):
    def __init__(self, dashboard, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dashboard = dashboard
        
        self.user_score = 0
        self.ai_score = 0

        self.history = ""
        
        self.resize(800, 600)

        frame_geometry = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

        layout = QVBoxLayout()
        
        self.result_label = QLabel("Click your choice below")
        self.result_label.setFont(QFont("Arial", 14))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

        self.score_label = QLabel(f"Your Score: {self.user_score} | AI Score: {self.ai_score}")
        self.score_label.setFont(QFont("Arial", 12))
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.score_label)

        button_layout = QHBoxLayout()
        choices = ['Rock', 'Paper', 'Scissors']
        self.buttons = {}
        for choice in choices:
            button = QPushButton(choice)
            button.clicked.connect(lambda _, c=choice: self.play_game(c))
            button_layout.addWidget(button)
            self.buttons[choice] = button
        layout.addLayout(button_layout)

        home_button = QPushButton("Back to Home")
        home_button.clicked.connect(self.go_home)
        layout.addWidget(home_button)

        self.setLayout(layout)

    def play_game(self, user_choice):
        ai_choice = ai_move()
        result = self.determine_winner(user_choice, ai_choice)
        
        self.result_label.setText(f"AI chose: {ai_choice} - {result}")
        self.score_label.setText(f"Your Score: {self.user_score} | AI Score: {self.ai_score}")
        
        history_line = f"You chose: {user_choice}, AI chose: {ai_choice} - {result}"
        self.history += history_line + '\n'

    def determine_winner(self, user_choice, ai_choice):
        if user_choice == ai_choice:
            return "Draw"
        elif (user_choice == "Rock" and ai_choice == "Scissors") or \
             (user_choice == "Paper" and ai_choice == "Rock") or \
             (user_choice == "Scissors" and ai_choice == "Paper"):
            self.user_score += 1
            return "You Win"
        else:
            self.ai_score += 1
            return "AI Wins"
        
    def go_home(self):
        self.hide()
        self.dashboard.show()

    def get_scores_and_history(self):
        return self.user_score, self.ai_score, self.history

class Dashboard(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle("RPS AI Game (Rock Paper Scissors)")
        self.resize(800, 600)

        frame_geometry = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
        
        layout = QVBoxLayout()
        
        title_label = QLabel("Welcome to RPS AI Game!")
        title_label.setObjectName("title_label")
        title_label.setFont(QFont("Arial", 20))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        image_label = QLabel()
        image_label.setObjectName("image_label")
        image_path = "../RPS_AI_Game/assets/img/ai_game_trans.png"
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)
        
        welcome_label = QLabel("Enjoy the Rock Paper Scissors Game with AI! Click the button below to start.")
        welcome_label.setObjectName("welcome_label")
        welcome_label.setFont(QFont("Arial", 12))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)

        self.game_started = False
        self.start_button = QPushButton("Start Game")
        self.start_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_button)
        
        check_score_button = QPushButton("Check Last Score")
        check_score_button.clicked.connect(self.check_last_score)
        layout.addWidget(check_score_button)
        
        download_score_button = QPushButton("Download Score as PDF")
        download_score_button.clicked.connect(self.download_score)
        layout.addWidget(download_score_button)
        
        restart_button = QPushButton("Restart Game")
        restart_button.clicked.connect(self.restart_game)
        layout.addWidget(restart_button)
        
        quit_button = QPushButton("Quit Game")
        quit_button.clicked.connect(self.quit_game)
        layout.addWidget(quit_button)
        
        self.setLayout(layout)
        
        self.game_window = GameWindow(self)

    def start_game(self):
        if not self.game_started:
            self.start_button.setText("Resume Game")
            self.game_started = True
        
        self.hide()
        self.game_window.show()

    def check_last_score(self):
        user_score, ai_score, history = self.game_window.get_scores_and_history()
        msg = f"Your Score: {user_score}\nAI Score: {ai_score}\n\nGame History:\n{history}"
        QMessageBox.information(self, "Last Score", msg)
    
    def download_score(self):
        user_score, ai_score, history = self.game_window.get_scores_and_history()
        generate_pdf(user_score, ai_score, history)

    def restart_game(self):
        self.game_window.user_score = 0
        self.game_window.ai_score = 0
        self.game_window.history = ""
        self.game_started = False
        self.start_button.setText("Start Game")

        QMessageBox.information(self, "Success", "The game has been restarted")

    def quit_game(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet(open("style.qss").read())
    
    dashboard = Dashboard()
    dashboard.show()

    sys.exit(app.exec())
