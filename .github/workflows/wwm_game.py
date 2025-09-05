import tkinter as tk
from tkinter import messagebox, filedialog, Toplevel
import json
import random

class WWMGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Wer wird Millionär?")
        self.root.geometry("700x500")

        # Spielvariablen
        self.questions = []
        self.current_question = None
        self.used_50_50 = False
        self.used_phone = False
        self.used_audience = False
        self.level = 0

        # Gewinnstufen
        self.money_levels = [
            "50 €", "100 €", "200 €", "300 €", "500 €",
            "1.000 €", "2.000 €", "4.000 €", "8.000 €", "16.000 €",
            "32.000 €", "64.000 €", "125.000 €", "500.000 €", "1.000.000 €"
        ]

        # UI: Frage
        self.label = tk.Label(root, text="Bitte lade einen Fragen-Ordner!", font=("Arial", 16), wraplength=650)
        self.label.pack(pady=20)

        # Antwort-Buttons
        self.buttons = []
        for i in range(4):
            btn = tk.Button(root, text=f"Antwort {i+1}", font=("Arial", 14), width=50, command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.buttons.append(btn)

        # Joker
        self.joker_frame = tk.Frame(root)
        self.joker_frame.pack(pady=10)

        self.btn_50 = tk.Button(self.joker_frame, text="50:50", command=self.use_50_50)
        self.btn_50.grid(row=0, column=0, padx=10)

        self.btn_phone = tk.Button(self.joker_frame, text="Telefonjoker", command=self.use_phone_joker)
        self.btn_phone.grid(row=0, column=1, padx=10)

        self.btn_audience = tk.Button(self.joker_frame, text="Publikumsjoker", command=self.use_audience_joker)
        self.btn_audience.grid(row=0, column=2, padx=10)

        # Gewinnleiter
        self.ladder_frame = tk.Frame(root)
        self.ladder_frame.pack(side="right", padx=20)

        self.ladder_labels = []
        for i, money in enumerate(reversed(self.money_levels)):
            lbl = tk.Label(self.ladder_frame, text=money, font=("Arial", 12))
            lbl.pack(anchor="e")
            self.ladder_labels.append(lbl)

        # Fragen laden Button
        self.btn_load = tk.Button(root, text="Fragen laden", command=self.load_questions)
        self.btn_load.pack(pady=10)

    def load_questions(self):
        file = filedialog.askopenfilename(title="Fragen-Datei wählen", filetypes=[("JSON Dateien", "*.json")])
        if not file:
            return
        with open(file, "r", encoding="utf-8") as f:
            self.questions = json.load(f)

        random.shuffle(self.questions)
        self.questions = self.questions[:15]

        self.level = 0
        self.used_50_50 = False
        self.used_phone = False
        self.used_audience = False
        self.next_question()

    def update_ladder(self):
        for i, lbl in enumerate(self.ladder_labels):
            lbl.config(bg="SystemButtonFace", fg="black")
        if self.level < len(self.money_levels):
            idx = len(self.money_levels) - 1 - self.level
            self.ladder_labels[idx].config(bg="gold", fg="black")

    def next_question(self):
        if self.level >= 15:
            messagebox.showinfo("Jackpot!", "Glückwunsch! Du hast 1.000.000 € gewonnen!")
            self.root.quit()
            return

        self.current_question = self.questions[self.level]
        self.label.config(text=f"Frage {self.level+1}: {self.current_question['frage']}")
        answers = self.current_question["antworten"]
        random.shuffle(answers)
        self.correct_answer = self.current_question["loesung"]

        for i, ans in enumerate(answers):
            self.buttons[i].config(text=ans, state="normal")

        self.update_ladder()

    def check_answer(self, idx):
        chosen = self.buttons[idx].cget("text")
        if chosen == self.correct_answer:
            messagebox.showinfo("Richtig!", f"Gut gemacht! Du hast {self.money_levels[self.level]} erreicht.")
            self.level += 1
            self.next_question()
        else:
            safe_money = self.get_safe_level()
            messagebox.showerror("Falsch!", f"Leider falsch. Richtige Antwort war: {self.correct_answer}\n\nDu gehst mit {safe_money} nach Hause.")
            self.root.quit()

    def get_safe_level(self):
        if self.level >= 10:
            return "16.000 €"
        elif self.level >= 5:
            return "500 €"
        else:
            return "0 €"

    def use_50_50(self):
        if self.used_50_50:
            return
        self.used_50_50 = True
        wrong_answers = [btn for btn in self.buttons if btn.cget("text") != self.correct_answer]
        to_disable = random.sample(wrong_answers, 2)
        for btn in to_disable:
            btn.config(state="disabled")

    def use_phone_joker(self):
        if self.used_phone:
            return
        self.used_phone = True
        messagebox.showinfo("Telefonjoker", f"Dein Freund sagt: Die richtige Antwort ist '{self.correct_answer}'.")
        self.next_question()

    def use_audience_joker(self):
        if self.used_audience:
            return
        self.used_audience = True

        votes = {}
        remaining = 100
        answers = [btn.cget("text") for btn in self.buttons]

        correct_votes = random.randint(40, 70)
        votes[self.correct_answer] = correct_votes
        remaining -= correct_votes

        wrong_answers = [a for a in answers if a != self.correct_answer]
        for i, ans in enumerate(wrong_answers):
            if i < len(wrong_answers) - 1:
                v = random.randint(0, remaining)
                votes[ans] = v
                remaining -= v
            else:
                votes[ans] = remaining

        win = Toplevel(self.root)
        win.title("Publikumsjoker")
        win.geometry("400x300")

        tk.Label(win, text="Publikumsumfrage:", font=("Arial", 14)).pack(pady=10)
        for ans in answers:
            frame = tk.Frame(win)
            frame.pack(fill="x", padx=20, pady=5)
            percent = votes[ans]
            tk.Label(frame, text=f"{ans}: {percent}%", width=20, anchor="w").pack(side="left")
            bar = tk.Frame(frame, bg="blue", width=percent*3, height=20)
            bar.pack(side="left")


if __name__ == "__main__":
    root = tk.Tk()
    game = WWMGame(root)
    root.mainloop()
