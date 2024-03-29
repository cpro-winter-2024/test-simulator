import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
from PIL import ImageTk, Image
import random
import question_db


class TestSimulator(tk.Frame):
    def __init__(self, root, question_database):
        super().__init__()  # Call init from superclass
        self.root = root
        self.question_db = question_database
        self.category_var = tk.StringVar()
        self.difficulty_var = tk.StringVar()
        self.num_questions_var = tk.IntVar()
        self.current_question_idx = 0
        self.correct_ans = 0
        self.selected_answer = tk.StringVar()
        # Welcome logo
        img = Image.open("C:/Users/joash/Desktop/01 CPRO Winter 2024/01 CPRO Git Repo/cpro-term1/01 Python/01 Lec/Project/logo.png")
        self.image = img.resize((250, 300))
        self.python_image = ImageTk.PhotoImage(self.image)
        self.tg_logo = tk.Label(root, image=self.python_image, bg="white")
        self.tg_logo.pack(padx=0, pady=20)
        # Welcome message
        # #0F9D58 Green
        # #4285F4 Blue
        # #DB4437 Red
        # #F4B400 Yellow
        self.welcome_label = tk.Label(root, text="Welcome to TestGenius:\nYour Test Simulator", font=("Helvetica 25 bold"), bg="white", fg="#666666")
        self.welcome_label.pack()
        self.authors_label = tk.Label(root, text="by Joash Daligcon, Aron Limos, and Lance Mirano\n", font=("Helvetica 10"), bg="white", fg="#838383")
        self.authors_label.pack()
        # Dropdown for selecting category
        font_cat_diff_numq = "Helvetica 12 bold"
        self.sel_categ_label = tk.Label(root, text="\nSelect a category:", font=(font_cat_diff_numq), bg="white", fg="#4285F4")
        self.sel_categ_label.pack()
        self.sel_categ_dropdown = ttk.Combobox(root, textvariable=self.category_var, state="readonly", font=("Helvetica 20"), width=10)
        self.sel_categ_dropdown["values"] = ("Culture", "Geography", "History", "Technology")
        self.sel_categ_dropdown.current(0)
        self.sel_categ_dropdown.pack()
        # Dropdown for selecting difficulty
        self.sel_diff_label = tk.Label(root, text="\nSelect a difficulty:", font=(font_cat_diff_numq), bg="white", fg="#DB4437")
        self.sel_diff_label.pack()
        self.sel_diff_dropdown = ttk.Combobox(root, textvariable=self.difficulty_var, state="readonly", font=("Helvetica 20"), width=10)
        self.sel_diff_dropdown["values"] = ("Easy", "Medium", "Hard")
        self.sel_diff_dropdown.current(0)
        self.sel_diff_dropdown.pack()
        # Dropdown for selecting number of questions
        self.num_questions_label = tk.Label(root, text="\nSelect number of questions:", font=(font_cat_diff_numq), bg="white", fg="#F4B400")
        self.num_questions_label.pack()
        self.num_questions_dropdown = ttk.Combobox(root, textvariable=self.num_questions_var, state="readonly", font=("Helvetica 20"), width=10)
        self.num_questions_dropdown["values"] = ("5", "10", "15", "20")
        self.num_questions_dropdown.current(0)
        self.num_questions_dropdown.pack()
        # Initialize Start button
        # style = ttk.Style()
        self.start_button = ttk.Button(root, text="Start Test", command=self.start_test)
        self.start_button.pack(padx=0, pady=25)
        # style.configure("start.button", font=("Verdana", 10))
        # Questions, choices, and buttons
        self.q_number_label = tk.Label(root, text="", font=("Helvetica 24 bold"), bg="white")
        self.q_number_label.pack()
        self.question_label = tk.Label(root, text="", wraplength=550, font=("Helvetica 20"), bg="white")
        self.question_label.pack()
        self.choice_buttons = []
        self.submit_button = ttk.Button(root, text="Submit Answer", command=self.submit_answer)

    def hide_welcome_screen(self):
        self.welcome_label.pack_forget()
        self.authors_label.pack_forget()
        self.sel_categ_label.pack_forget()
        self.sel_categ_dropdown.pack_forget()
        self.sel_diff_label.pack_forget()
        self.sel_diff_dropdown.pack_forget()
        self.num_questions_label.pack_forget()
        self.num_questions_dropdown.pack_forget()
        self.start_button.pack_forget()

    def start_test(self):
        # Hide welcome screen widgets
        self.hide_welcome_screen()
        # Get test settings
        self.category = self.category_var.get()
        self.difficulty = self.difficulty_var.get()
        self.num_questions = int(self.num_questions_var.get())
        # Prepare questions from category
        match (self.category):
            case "Culture":
                self.question_bank = self.question_db.qb_cul
                self.bg_hex = "#DB4437"
                self.fg_col = "white"
            case "Geography":
                self.question_bank = self.question_db.qb_geo
                self.bg_hex = "#0F9D58"
                self.fg_col = "white"
            case "History":
                self.question_bank = self.question_db.qb_his
                self.bg_hex = "#F4B400"
                self.fg_col = "black"
            case "Technology":
                self.question_bank = self.question_db.qb_tech
                self.bg_hex = "#4285F4"
                self.fg_col = "black"
            case _:
                pass
        # Randomize questions
        random.shuffle(self.question_bank)
        # Prepare questions according to difficulty
        self.sel_questions = []
        for qb in self.question_bank:
            if qb["difficulty"] == self.difficulty:
                self.sel_questions.append(qb)
        # Update display (category logo, bg color)
        img = Image.open(f"C:/Users/joash/Desktop/01 CPRO Winter 2024/01 CPRO Git Repo/cpro-term1/01 Python/01 Lec/Project/logo_{self.fg_col}.png")
        self.image = img.resize((250, 300))
        self.python_image = ImageTk.PhotoImage(self.image)
        self.tg_logo.config(image=self.python_image, bg=self.bg_hex)
        self.root.configure(bg=self.bg_hex)
        self.q_number_label.config(bg=self.bg_hex, fg=self.fg_col)
        self.question_label.config(bg=self.bg_hex, fg=self.fg_col)
        # Show questions
        self.show_question()

    def show_question(self):
        # Update question label to current question
        self.q_number_label.config(text=f"{self.category} ({self.difficulty})\nQuestion {self.current_question_idx + 1} of {self.num_questions}")
        self.question_label.config(text="\n" + self.sel_questions[self.current_question_idx]["question"] + "\n")
        # Clear radio buttons
        for radio_button in self.choice_buttons:
            radio_button.destroy()
        # Randomize choices
        self.choices = self.sel_questions[self.current_question_idx]["choices"]
        random.shuffle(self.choices)
        # Create radio buttons for choices
        style=ttk.Style()
        style.configure("TRadiobutton", background=self.bg_hex, font=("Helvetica 15"), foreground=self.fg_col)
        for choice in self.choices:
            radio_button = ttk.Radiobutton(self.root, text=choice, value=choice, variable=self.selected_answer, style="TRadiobutton")
            radio_button.pack(anchor=tk.N)
            self.choice_buttons.append(radio_button) # Store then destroy later
        # Set radio button to none
        self.selected_answer.set(None)
        # Show submit button
        self.submit_button.pack(padx=0, pady=25)

    def submit_answer(self):
        user_answer = self.selected_answer.get()
        correct_answer = self.sel_questions[self.current_question_idx]["answer"]
        if user_answer == correct_answer:
            self.correct_ans += 1
            showinfo(
                title = "Result",
                message = "Correct!"
            )
        else:
            showerror(
                title = "Result",
                message = f"Incorrect! The correct answer is: {correct_answer}."
            )
        # Go to next question
        self.current_question_idx += 1
        if self.current_question_idx < self.num_questions:
            self.submit_button.pack_forget()
            self.show_question()
        else:
            self.hide_question()
            showinfo(
                title = "End of Test",
                message = "You have completed the test. Press OK to see your score."
            )
            self.show_score()

    def hide_question(self):
        self.q_number_label.destroy()
        self.question_label.destroy()
        for radio_button in self.choice_buttons:
            radio_button.destroy()
        self.submit_button.destroy()

    def show_score(self):
        self.test_label = tk.Label(self.root, text=f"Test taken: {self.category} ({self.difficulty})", font=("Helvetica 21"), bg="white")
        self.test_label.pack()
        self.score_label = tk.Label(self.root, text="Your score is:", font=("Helvetica 20"), bg="white")
        self.score_label.pack()
        # Calculate score
        score_prcnt = 100 * (self.correct_ans / self.num_questions)
        self.score_prcnt_label = tk.Label(self.root, text=f"{score_prcnt:.2f}%", font=("Helvetica 24 bold"), bg="white")
        self.score_prcnt_label.pack()
        score_string = f"{str(self.correct_ans)} out of {str(self.num_questions)}"
        self.score_count = tk.Label(self.root, text=score_string, font=("Helvetica 21"), bg="white")
        self.score_count.pack()
        # Restart button
        self.restart_button = ttk.Button(self.root, text="Restart", command=self.restart)
        self.restart_button.pack()

    def restart(self):
        self.tg_logo.pack_forget()
        self.test_label.pack_forget()
        self.score_label.pack_forget()
        self.score_prcnt_label.pack_forget()
        self.score_count.pack_forget()
        self.restart_button.pack_forget()
        self.__init__(self.root, self.question_db)


def main():
    # Root window
    root = tk.Tk()
    root.title("TestGenius: Your Test Simulator")
    root.geometry("600x850")
    root.configure(bg="white")
    # root.resizable(False, False)
    # Create test simulator object
    gui = TestSimulator(root, question_db)
    gui.mainloop()


if __name__ == "__main__":
    main()