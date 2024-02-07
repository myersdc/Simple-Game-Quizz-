import tkinter as tk
from tkinter import messagebox
import random
import difflib

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz App")
        self.master.geometry("600x400")
        self.master.configure(bg="#f0f0f0")

        self.questions = {
            "easy": {
                "Qual é a capital do Brasil?": "Brasília",
                "Quem escreveu 'Dom Quixote'?": "Miguel de Cervantes",
                "Quantos planetas existem no sistema solar?": "Oito"
            },
            "medium": {
                "Quem pintou a Mona Lisa?": "Leonardo da Vinci",
                "Qual é o maior animal terrestre?": "Elefante africano",
                "Quantos lados tem um quadrado?": "Quatro"
            },
            "hard": {
                "Qual é a fórmula química da água?": "H2O",
                "Quem descobriu a penicilina?": "Alexander Fleming",
                "Qual é o maior oceano do mundo?": "Oceano Pacífico"
            }
        }

        self.current_difficulty = tk.StringVar(master)
        self.current_difficulty.set("easy")

        self.theme_mode = tk.StringVar(master)
        self.theme_mode.set("light")

        self.theme_button = tk.Button(master, text="🌞", command=self.toggle_theme, font=("Arial", 12), bg="#f0f0f0", bd=0)
        self.theme_button.place(relx=1, rely=0, anchor="ne")

        self.difficulty_label = tk.Label(master, text="Escolha a dificuldade:", font=("Arial", 14, "bold"), bg="#f0f0f0")
        self.difficulty_label.pack()

        self.difficulty_menu = tk.OptionMenu(master, self.current_difficulty, "easy", "medium", "hard")
        self.difficulty_menu.config(font=("Arial", 12), bg="#fff", bd=0)
        self.difficulty_menu.pack(pady=5)

        self.start_button = tk.Button(master, text="Iniciar", command=self.start_quiz, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", bd=0)
        self.start_button.pack(pady=5)

        self.progress_label = tk.Label(master, text="", font=("Arial", 12, "italic"), bg="#f0f0f0")
        self.progress_label.pack()

        self.score_label = tk.Label(master, text="", font=("Arial", 12, "italic"), bg="#f0f0f0")
        self.score_label.pack()

        self.feedback_label = tk.Label(master, text="", font=("Arial", 12), bg="#f0f0f0")
        self.feedback_label.pack()

        self.question_label = tk.Label(master, text="", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        self.question_label.pack()

        self.answer_entry = tk.Entry(master, font=("Arial", 12), bg="#fff", bd=1, highlightthickness=0)
        self.answer_entry.pack(fill=tk.X, padx=10, pady=5)

        self.submit_button = tk.Button(master, text="Responder", command=self.submit_answer, font=("Arial", 12, "bold"), bg="#008CBA", fg="white", bd=0)
        self.submit_button.pack(pady=5)

        self.remaining_time = 0
        self.timer_label = tk.Label(master, text="", font=("Arial", 12), bg="#f0f0f0")
        self.timer_label.pack()

    def toggle_theme(self):
        if self.theme_mode.get() == "light":
            self.theme_mode.set("dark")
            self.theme_button.config(text="🌛")
            self.master.configure(bg="#333")
            self.difficulty_label.config(bg="#333", fg="#fff")
            self.progress_label.config(bg="#333", fg="#fff")
            self.score_label.config(bg="#333", fg="#fff")
            self.feedback_label.config(bg="#333", fg="#fff")
            self.question_label.config(bg="#333", fg="#fff")
            self.answer_entry.config(bg="#444", fg="#fff", bd=1, highlightthickness=0)
            self.submit_button.config(bg="#008CBA", fg="white")
            self.timer_label.config(bg="#333", fg="#fff")
        else:
            self.theme_mode.set("light")
            self.theme_button.config(text="🌞")
            self.master.configure(bg="#f0f0f0")
            self.difficulty_label.config(bg="#f0f0f0", fg="#333")
            self.progress_label.config(bg="#f0f0f0", fg="#333")
            self.score_label.config(bg="#f0f0f0", fg="#333")
            self.feedback_label.config(bg="#f0f0f0", fg="#333")
            self.question_label.config(bg="#f0f0f0", fg="#333")
            self.answer_entry.config(bg="#fff", fg="#333", bd=1, highlightthickness=1, highlightcolor="#ccc")
            self.submit_button.config(bg="#4CAF50", fg="white")
            self.timer_label.config(bg="#f0f0f0", fg="#333")

    def start_quiz(self):
        self.questions_set = self.questions[self.current_difficulty.get()]
        self.score = 0
        self.remaining_questions = list(self.questions_set.keys())
        self.update_question()

    def update_question(self):
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")
        if self.remaining_questions:
            self.current_question = random.choice(self.remaining_questions)
            self.remaining_questions.remove(self.current_question)
            self.question_label.config(text=self.current_question, fg="#333")
            self.progress_label.config(text="Progresso: {}/{}".format(self.score, len(self.questions_set)), fg="#333")
            self.score_label.config(text="Score: {}".format(self.score), fg="#333")
            self.start_timer()
        else:
            self.end_quiz()

    def start_timer(self):
        self.remaining_time = 20
        self.update_timer()

    def update_timer(self):
        if self.remaining_time >= 0:
            self.timer_label.config(text="Tempo restante: {}s".format(self.remaining_time), fg="#333")
            self.remaining_time -= 1
            self.master.after(1000, self.update_timer)
        else:
            self.submit_answer()

    def submit_answer(self):
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = self.questions_set[self.current_question].lower()
        if difflib.SequenceMatcher(None, user_answer, correct_answer).ratio() >= 0.8:
            self.score += 1
            self.feedback_label.config(text="Correto!", fg="#4CAF50")
        else:
            self.feedback_label.config(text="Incorreto! Resposta correta: {}".format(correct_answer), fg="#FF5733")
        self.update_question()

    def end_quiz(self):
        messagebox.showinfo("Fim do Quiz", "Parabéns! Você completou o quiz.\nScore: {}/{}".format(self.score, len(self.questions_set)))
        self.progress_label.config(text="")
        self.score_label.config(text="")
        self.question_label.config(text="")
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")
        self.timer_label.config(text="")
        self.start_button.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
