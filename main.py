"""Sleep Advice Expert System

A beginner-friendly, rule-based Tkinter desktop application that provides
educational sleep-hygiene suggestions. It does not diagnose medical conditions.
Uses only Python's standard library.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime


# ---------------------------- Theme constants ---------------------------- #
BG = "#F3F8FC"
CARD = "#FFFFFF"
NAVY = "#174B67"
BLUE = "#DDEFF8"
TEAL = "#258F91"
TEAL_DARK = "#1D7376"
TEXT = "#263B48"
MUTED = "#647D8A"
BORDER = "#D8E7EE"
PALE_TEAL = "#E6F6F4"
PALE_GOLD = "#FFF4D9"


class SleepAdviceApp:
    """Main application window and simple rule-based expert system."""

    def __init__(self, root):
        self.root = root
        self.root.title("Sleep Advice Expert System | SleepWise")
        self.root.geometry("1080x820")
        self.root.minsize(900, 680)
        self.root.configure(bg=BG)

        self.answers = {}
        self.report_text = ""
        self.variables = {}

        self.setup_styles()
        self.create_header()
        self.create_notebook()
        self.create_assessment_tab()
        self.create_results_tab()
        self.create_footer()

    # ------------------------------- UI ---------------------------------- #
    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background=BG)
        style.configure("Card.TFrame", background=CARD)
        style.configure("TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("HeaderTitle.TLabel", background=BLUE, foreground=NAVY,
                        font=("Segoe UI", 21, "bold"))
        style.configure("HeaderSub.TLabel", background=BLUE, foreground=MUTED,
                        font=("Segoe UI", 10))
        style.configure("Section.TLabel", background=CARD, foreground=NAVY,
                        font=("Segoe UI", 12, "bold"))
        style.configure("Question.TLabel", background=CARD, foreground=TEXT,
                        font=("Segoe UI", 10))
        style.configure("Small.TLabel", background=BG, foreground=MUTED,
                        font=("Segoe UI", 9))
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", padding=(18, 9), font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", CARD), ("!selected", BLUE)],
                  foreground=[("selected", NAVY), ("!selected", MUTED)])
        style.configure("TCombobox", padding=6, fieldbackground=CARD, foreground=TEXT)
        style.configure("TSpinbox", padding=5, fieldbackground=CARD, foreground=TEXT)
        style.configure("Primary.TButton", background=TEAL, foreground="#FFFFFF",
                        padding=(16, 10), font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("Primary.TButton", background=[("active", TEAL_DARK), ("pressed", TEAL_DARK)])
        style.configure("Secondary.TButton", background=BLUE, foreground=NAVY,
                        padding=(13, 9), font=("Segoe UI", 9, "bold"), borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#CCE5F2")])

    def create_header(self):
        header = tk.Frame(self.root, bg=BLUE, padx=24, pady=18,
                          highlightbackground=BORDER, highlightthickness=1)
        header.pack(fill="x", padx=16, pady=(14, 10))

        top_line = tk.Frame(header, bg=BLUE)
        top_line.pack(fill="x")
        tk.Label(top_line, text="SLEEPWISE  |  WELLNESS TOOL", bg=BLUE, fg=TEAL_DARK,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ttk.Label(header, text="Sleep Advice Expert System", style="HeaderTitle.TLabel").pack(anchor="w", pady=(5, 2))
        ttk.Label(header, text="Understand your sleep habits. Build a healthier bedtime routine.",
                  style="HeaderSub.TLabel").pack(anchor="w")

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=16, pady=(0, 8))
        self.assessment_tab = ttk.Frame(self.notebook)
        self.results_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.assessment_tab, text="  Sleep Assessment  ")
        self.notebook.add(self.results_tab, text="  Your Results  ")

    def create_assessment_tab(self):
        # Scrollable questionnaire keeps the full form usable on smaller screens.
        outer = tk.Frame(self.assessment_tab, bg=BG)
        outer.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=self.canvas.yview)
        self.form_frame = tk.Frame(self.canvas, bg=BG)
        self.form_window = self.canvas.create_window((0, 0), window=self.form_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.form_frame.bind("<Configure>", self.on_form_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.add_section(
            "1. About your sleep",
            "Choose the options that best describe your usual sleep pattern.",
            [
                ("age_group", "Age group", ["Child (6–12 years)", "Teen (13–17 years)",
                                             "Adult (18–64 years)", "Older adult (65+ years)"],
                 "Adult (18–64 years)"),
                ("sleep_hours", "Average hours of sleep per night", None, "7.5"),
            ],
        )
        self.add_section(
            "2. Schedule & nighttime routine",
            "Regular timing and pre-bed habits can affect how easily you settle down.",
            [
                ("bedtime_consistency", "How regular is your bedtime?",
                 ["Consistent (within 30 minutes)", "Varies by 30–60 minutes",
                  "Varies by more than 1 hour"], "Consistent (within 30 minutes)"),
                ("wake_consistency", "Do you wake up at about the same time each day?",
                 ["Usually", "Sometimes", "Rarely"], "Usually"),
                ("screens", "Do you use a phone, computer, or TV in the last hour before bed?",
                 ["No screens in the last hour", "Some screen use", "Screens until bedtime"],
                 "Some screen use"),
                ("caffeine", "When do you usually have caffeine (coffee, tea, cola, energy drinks)?",
                 ["None or morning only", "Afternoon", "Evening or near bedtime"],
                 "None or morning only"),
                ("naps", "What best describes your naps?",
                 ["No naps", "Short (20 minutes or less, early afternoon)",
                  "Longer than 20 minutes", "Late afternoon or evening"], "No naps"),
            ],
        )
        self.add_section(
            "3. Lifestyle & sleep environment",
            "Small changes to your routine and bedroom may support better sleep.",
            [
                ("exercise", "How often are you physically active?",
                 ["Most days", "Some days", "Rarely"], "Some days"),
                ("stress", "How often do stress or worries make it hard to relax at bedtime?",
                 ["Rarely", "Sometimes", "Often"], "Sometimes"),
                ("room", "What is your bedroom like at night?",
                 ["Dark, quiet, and comfortably cool", "Some issues with light, noise, or temperature",
                  "Often bright, noisy, or too warm"], "Dark, quiet, and comfortably cool"),
            ],
        )
        self.add_section(
            "4. Sleep quality & daytime signs",
            "These questions help identify when general tips may not be enough.",
            [
                ("night_waking", "How often do you wake during the night?",
                 ["Rarely or once", "About twice", "Three or more times"], "Rarely or once"),
                ("refreshed", "How often do you feel refreshed after waking?",
                 ["Usually", "Sometimes", "Rarely"], "Usually"),
                ("snoring", "Has anyone noticed loud snoring, gasping, or pauses in your breathing?",
                 ["No", "Yes", "Not sure"], "No"),
                ("daytime_impact", "How much does poor sleep affect your daytime activities?",
                 ["No major effect", "Some tiredness or concentration difficulty",
                  "Major effect on daily tasks"], "No major effect"),
                ("duration", "How long have sleep difficulties been happening?",
                 ["Not currently having difficulties", "Less than 2 weeks", "2 weeks to 3 months",
                  "More than 3 months"], "Not currently having difficulties"),
            ],
        )

        note = tk.Frame(self.form_frame, bg=PALE_GOLD, padx=14, pady=12,
                        highlightbackground="#F1DDA4", highlightthickness=1)
        note.pack(fill="x", padx=12, pady=(0, 12))
        tk.Label(note, text="Please note", bg=PALE_GOLD, fg="#775D19",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(note, text="This tool provides general educational suggestions, not a diagnosis or a substitute for medical care.",
                 bg=PALE_GOLD, fg="#775D19", wraplength=850, justify="left",
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(3, 0))

        buttons = tk.Frame(self.form_frame, bg=BG)
        buttons.pack(fill="x", padx=12, pady=(0, 18))
        ttk.Button(buttons, text="Generate My Sleep Advice", style="Primary.TButton",
                   command=self.generate_report).pack(side="left")
        ttk.Button(buttons, text="Reset Answers", style="Secondary.TButton",
                   command=self.reset_form).pack(side="left", padx=(10, 0))

    def add_section(self, title, subtitle, questions):
        card = tk.Frame(self.form_frame, bg=CARD, padx=18, pady=15,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", padx=12, pady=(12, 0))
        ttk.Label(card, text=title, style="Section.TLabel").pack(anchor="w")
        tk.Label(card, text=subtitle, bg=CARD, fg=MUTED, font=("Segoe UI", 9),
                 wraplength=850, justify="left").pack(anchor="w", pady=(3, 12))

        for row_index, (key, prompt, options, default) in enumerate(questions):
            row = tk.Frame(card, bg=CARD)
            row.pack(fill="x", pady=5)
            row.grid_columnconfigure(0, weight=1)
            tk.Label(row, text=prompt, bg=CARD, fg=TEXT, font=("Segoe UI", 10),
                     anchor="w", justify="left", wraplength=470).grid(
                         row=0, column=0, sticky="ew", padx=(0, 18))

            if key == "sleep_hours":
                var = tk.StringVar(value=default)
                widget = ttk.Spinbox(row, from_=0, to=16, increment=0.5,
                                     textvariable=var, width=12, format="%.1f")
            else:
                var = tk.StringVar(value=default)
                widget = ttk.Combobox(row, textvariable=var, values=options,
                                      state="readonly", width=37)
            widget.grid(row=0, column=1, sticky="e")
            self.variables[key] = var

    def on_form_configure(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfigure(self.form_window, width=event.width)

    def on_mousewheel(self, event):
        # Windows mouse-wheel support. Ignore scroll events outside the form tab.
        try:
            if self.notebook.select() == str(self.assessment_tab):
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except (tk.TclError, ZeroDivisionError):
            pass

    def create_results_tab(self):
        wrapper = tk.Frame(self.results_tab, bg=BG, padx=14, pady=14)
        wrapper.pack(fill="both", expand=True)
        self.results_heading = tk.Label(wrapper, text="Your personalized sleep-habit report will appear here",
                                        bg=BG, fg=NAVY, font=("Segoe UI", 15, "bold"),
                                        anchor="w", justify="left", wraplength=900)
        self.results_heading.pack(fill="x", pady=(0, 10))
        self.results_subtitle = tk.Label(wrapper, text="Complete the assessment and select “Generate My Sleep Advice.”",
                                         bg=BG, fg=MUTED, font=("Segoe UI", 10), anchor="w")
        self.results_subtitle.pack(fill="x", pady=(0, 10))
        text_frame = tk.Frame(wrapper, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        text_frame.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical")
        self.results_box = tk.Text(text_frame, wrap="word", font=("Segoe UI", 10),
                                   bg=CARD, fg=TEXT, padx=18, pady=16,
                                   relief="flat", borderwidth=0,
                                   yscrollcommand=scrollbar.set, spacing1=2, spacing3=5)
        scrollbar.configure(command=self.results_box.yview)
        self.results_box.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.results_box.insert("1.0", "Your report will include:\n\n• A sleep-habit alignment score\n• Suggestions based on your answers\n• A simple 7-day improvement plan\n• Guidance on when to consider professional advice\n\nThis is an educational tool, not a medical assessment.")
        self.results_box.configure(state="disabled")

        actions = tk.Frame(wrapper, bg=BG)
        actions.pack(fill="x", pady=(12, 0))
        ttk.Button(actions, text="Save Report as TXT", style="Primary.TButton",
                   command=self.save_report).pack(side="left")
        ttk.Button(actions, text="Back to Assessment", style="Secondary.TButton",
                   command=lambda: self.notebook.select(self.assessment_tab)).pack(side="left", padx=(10, 0))

    def create_footer(self):
        tk.Label(self.root, text="SleepWise • General sleep-hygiene education • Not for diagnosis or emergencies",
                 bg=BG, fg=MUTED, font=("Segoe UI", 8)).pack(pady=(0, 8))

    # ------------------------- Expert-system rules ----------------------- #
    def collect_answers(self):
        answers = {key: var.get().strip() for key, var in self.variables.items()}
        try:
            hours = float(answers["sleep_hours"])
        except (ValueError, TypeError):
            raise ValueError("Please enter your average sleep duration as a number, such as 7.5.")
        if not 0 <= hours <= 16:
            raise ValueError("Sleep duration must be between 0 and 16 hours.")
        answers["sleep_hours_num"] = hours
        return answers

    @staticmethod
    def get_sleep_target(age_group):
        if age_group == "Child (6–12 years)":
            return 9, 12, "9–12 hours"
        if age_group == "Teen (13–17 years)":
            return 8, 10, "8–10 hours"
        if age_group == "Older adult (65+ years)":
            return 7, 9, "7–9 hours"
        return 7, 9, "7–9 hours"

    def evaluate_rules(self, a):
        """Return a score, personalized advice and safety flags based on IF/THEN rules."""
        score = 100
        advice = []
        priorities = []
        safety_notes = []
        lower, upper, target_text = self.get_sleep_target(a["age_group"])
        hours = a["sleep_hours_num"]

        # Rule group 1: age-appropriate sleep duration.
        if hours < lower - 1:
            score -= 22
            item = (1, "Protect enough time for sleep",
                    f"You report about {hours:g} hours per night. For your age group, a commonly recommended range is {target_text}. Try moving bedtime earlier in small steps (15–20 minutes at a time) while keeping your wake-up time steady.")
            advice.append(item[2])
            priorities.append(item)
        elif hours < lower:
            score -= 14
            item = (2, "Add a little more sleep time",
                    f"Your reported sleep is slightly below the usual {target_text} range for your age group. Consider setting aside 15–30 extra minutes for sleep and observe how you feel.")
            advice.append(item[2])
            priorities.append(item)
        elif hours > upper + 1:
            score -= 7
            advice.append(f"You report about {hours:g} hours of sleep. Sleep needs vary, but regularly needing much more than the usual {target_text} range—especially if you remain tired—may be worth discussing with a healthcare professional.")
        elif hours > upper:
            score -= 3
            advice.append(f"Your reported sleep is above the usual {target_text} range for your age group. Individual needs differ; focus on whether you feel rested and whether your schedule works well.")
        else:
            advice.append(f"Your reported sleep duration is within the commonly recommended {target_text} range for your age group. Keeping this amount consistent may help.")

        # Rule group 2: schedule regularity.
        if a["bedtime_consistency"] == "Varies by more than 1 hour":
            score -= 10
            entry = (2, "Keep bedtime more regular",
                     "Your bedtime varies by more than an hour. Choose a realistic bedtime window and shift your schedule gradually instead of making a large sudden change.")
            advice.append(entry[2]); priorities.append(entry)
        elif a["bedtime_consistency"] == "Varies by 30–60 minutes":
            score -= 5
            entry = (5, "Make bedtime more consistent",
                     "Try keeping bedtime within roughly the same 30-minute window on most days, including weekends when practical.")
            advice.append(entry[2]); priorities.append(entry)

        if a["wake_consistency"] == "Rarely":
            score -= 8
            entry = (2, "Anchor your wake-up time",
                     "Your wake-up time often changes. Pick a practical wake time and keep it similar each day; this can make it easier to build a steady sleep rhythm.")
            advice.append(entry[2]); priorities.append(entry)
        elif a["wake_consistency"] == "Sometimes":
            score -= 4
            entry = (5, "Steady your wake-up time",
                     "Try to keep your wake-up time similar on school/work days and days off. Adjust the schedule gradually if needed.")
            advice.append(entry[2]); priorities.append(entry)

        # Rule group 3: stimulants, screens, and naps.
        if a["screens"] == "Screens until bedtime":
            score -= 8
            entry = (3, "Create a screen-free wind-down",
                     "Screens continue until bedtime. When possible, put devices away for the last 30–60 minutes and choose a calm activity such as reading, gentle stretching, or quiet music.")
            advice.append(entry[2]); priorities.append(entry)
        elif a["screens"] == "Some screen use":
            score -= 4
            entry = (6, "Reduce late screen time",
                     "Try reducing phone, computer, or TV use during the last 30–60 minutes before bed, particularly if it keeps you alert or delays bedtime.")
            advice.append(entry[2]); priorities.append(entry)

        if a["caffeine"] == "Evening or near bedtime":
            score -= 10
            entry = (2, "Move caffeine earlier",
                     "Caffeine in the evening can make it harder to fall asleep. Try avoiding it for at least several hours before bedtime; sensitivity varies by person.")
            advice.append(entry[2]); priorities.append(entry)
        elif a["caffeine"] == "Afternoon":
            score -= 5
            entry = (5, "Check your caffeine cut-off time",
                     "If you have trouble sleeping, experiment with having coffee, strong tea, cola, or energy drinks earlier in the day. Caffeine can affect people for several hours.")
            advice.append(entry[2]); priorities.append(entry)

        if a["naps"] == "Longer than 20 minutes":
            score -= 4
            entry = (6, "Review nap length",
                     "Long naps can reduce sleepiness at bedtime for some people. Try a shorter, earlier nap—or skip naps if they make nighttime sleep harder.")
            advice.append(entry[2]); priorities.append(entry)
        elif a["naps"] == "Late afternoon or evening":
            score -= 6
            entry = (3, "Move naps earlier",
                     "Late naps may make it harder to feel sleepy at bedtime. If you need a nap, try keeping it short and earlier in the afternoon.")
            advice.append(entry[2]); priorities.append(entry)

        # Rule group 4: activity, relaxation, and environment.
        if a["exercise"] == "Rarely":
            score -= 5
            entry = (6, "Add gentle daytime movement",
                     "Consider a walk or another activity that suits your ability on most days. Daytime movement can support wellbeing; avoid intense exercise close to bedtime if it makes you feel alert.")
            advice.append(entry[2]); priorities.append(entry)
        elif a["exercise"] == "Some days":
            entry = (7, "Keep movement part of your routine",
                     "Continue building regular daytime movement in a way that feels comfortable and safe for you.")
            priorities.append(entry)

        if a["stress"] == "Often":
            score -= 8
            entry = (2, "Build a calming bedtime routine",
                     "Worries often make it hard to relax. Try 10–20 minutes of slow breathing, gentle stretching, writing tomorrow's to-do list earlier in the evening, or another calming routine.")
            advice.append(entry[2]); priorities.append(entry)
        elif a["stress"] == "Sometimes":
            score -= 4
            entry = (5, "Make space to unwind",
                     "Try a brief relaxing routine before bed, such as slow breathing, a warm shower, gentle stretching, or writing down worries and next steps earlier in the evening.")
            advice.append(entry[2]); priorities.append(entry)

        if a["room"] == "Often bright, noisy, or too warm":
            score -= 6
            entry = (3, "Improve the sleep environment",
                     "Make the room as dark, quiet, and comfortably cool as practical. Blackout curtains, an eye mask, reducing noise, or adjusting bedding may help if available.")
            advice.append(entry[2]); priorities.append(entry)
        elif a["room"] == "Some issues with light, noise, or temperature":
            score -= 3
            entry = (6, "Make one bedroom adjustment",
                     "Identify the biggest issue—light, noise, or temperature—and try one manageable change to make your room more comfortable for sleep.")
            advice.append(entry[2]); priorities.append(entry)

        # Rule group 5: sleep quality and possible reasons for seeking support.
        if a["night_waking"] == "Three or more times":
            score -= 5
            advice.append("Frequent awakenings can have many causes. Notice whether noise, temperature, late caffeine, stress, or another pattern is involved. Seek professional advice if this continues or affects daytime life.")
        elif a["night_waking"] == "About twice":
            score -= 2
            advice.append("If you wake during the night, keep lights low and choose a calm activity if you cannot return to sleep. Avoid checking the time repeatedly if it makes you worried.")

        if a["refreshed"] == "Rarely":
            score -= 5
            advice.append("You rarely feel refreshed. Track sleep timing and daytime energy for a couple of weeks. If this continues despite enough time for sleep, consider discussing it with a healthcare professional.")
        elif a["refreshed"] == "Sometimes":
            advice.append("Notice which nights leave you feeling more rested; a simple sleep diary may help you spot patterns in timing, caffeine, naps, or stress.")

        if a["snoring"] == "Yes":
            safety_notes.append("If loud snoring, gasping, or pauses in breathing have been noticed, arrange a conversation with a healthcare professional. These signs deserve assessment, especially with daytime sleepiness.")
        elif a["snoring"] == "Not sure":
            safety_notes.append("If you suspect loud snoring, gasping, or pauses in breathing, consider asking a trusted person what they notice and discuss concerns with a healthcare professional.")

        if a["daytime_impact"] == "Major effect on daily tasks":
            safety_notes.append("Because sleep is having a major effect on everyday activities, seek advice from a healthcare professional rather than relying on sleep tips alone. Avoid driving or operating machinery when very sleepy.")
        elif a["daytime_impact"] == "Some tiredness or concentration difficulty":
            safety_notes.append("If tiredness or concentration problems persist, worsen, or interfere with daily life, consider talking with a healthcare professional.")

        if a["duration"] == "More than 3 months":
            safety_notes.append("Sleep difficulties lasting more than three months are worth discussing with a healthcare professional, particularly if they affect your daytime functioning.")
        elif a["duration"] == "2 weeks to 3 months":
            safety_notes.append("If sleep difficulties continue for several weeks or affect your daytime functioning, consider seeking professional advice.")

        score = max(0, min(100, score))
        return score, target_text, advice, priorities, safety_notes

    # -------------------------- Report generation ------------------------ #
    def generate_report(self):
        try:
            a = self.collect_answers()
        except ValueError as error:
            messagebox.showerror("Check your answer", str(error))
            return

        self.answers = a
        score, target_text, advice, priorities, safety_notes = self.evaluate_rules(a)
        if score >= 85:
            band = "Strong sleep-habit alignment"
            summary = "Many of your reported habits are supportive. Keep the routines that are working and make small adjustments where useful."
        elif score >= 65:
            band = "Some habits could be improved"
            summary = "You have a helpful starting point. Pick one or two suggestions and practise them consistently before adding more changes."
        else:
            band = "Several habits may benefit from attention"
            summary = "Start with small, realistic changes rather than trying to change everything at once. If sleep problems continue or affect daily life, seek professional guidance."

        lines = [
            "SLEEPWISE — PERSONAL SLEEP-HABIT REPORT",
            "=" * 48,
            f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            f"Age group: {a['age_group']}",
            f"Reported sleep: {a['sleep_hours_num']:g} hours per night",
            f"Commonly recommended range for this age group: {target_text}",
            "",
            f"SLEEP-HABIT ALIGNMENT SCORE: {score}/100",
            f"Result: {band}",
            "Note: This is an educational rule-based score, not a medical score or diagnosis.",
            "",
            "YOUR SUMMARY",
            "-----------",
            summary,
            "",
            "SUGGESTIONS BASED ON YOUR ANSWERS",
            "----------------------------------",
        ]
        for index, tip in enumerate(advice, start=1):
            lines.append(f"{index}. {tip}")

        # Generate a 7-day plan: highest-priority triggered rules first, then healthy basics.
        plan = self.build_seven_day_plan(a, priorities)
        lines.extend(["", "YOUR 7-DAY STARTER PLAN", "-----------------------"])
        for day, task in enumerate(plan, start=1):
            lines.append(f"Day {day}: {task}")

        if safety_notes:
            lines.extend(["", "WHEN TO CONSIDER PROFESSIONAL ADVICE", "------------------------------------"])
            for note in safety_notes:
                lines.append(f"• {note}")
        else:
            lines.extend(["", "WHEN TO SEEK SUPPORT", "--------------------",
                          "If sleep problems persist, worsen, or interfere with daytime life, consider speaking with a healthcare professional. Seek urgent help for an emergency."])

        lines.extend([
            "",
            "SIMPLE TRACKING TIP",
            "-------------------",
            "For the next 7 days, note your bedtime, wake-up time, approximate sleep duration, caffeine timing, and how rested you feel. Look for patterns instead of expecting instant perfection.",
            "",
            "IMPORTANT DISCLAIMER",
            "--------------------",
            "SleepWise provides general educational sleep-hygiene information only. It cannot diagnose, treat, or rule out a sleep disorder and is not a substitute for advice from a qualified healthcare professional.",
        ])
        self.report_text = "\n".join(lines)

        self.results_heading.configure(text=f"Your result: {score}/100 — {band}")
        self.results_subtitle.configure(text="Your advice and 7-day plan are based on the habits you selected.")
        self.results_box.configure(state="normal")
        self.results_box.delete("1.0", "end")
        self.results_box.insert("1.0", self.report_text)
        self.results_box.configure(state="disabled")
        self.notebook.select(self.results_tab)

    def build_seven_day_plan(self, answers, priorities):
        """Build a practical plan using high-priority triggered rules first."""
        # Deduplicate tasks while retaining the most important rule first.
        priorities = sorted(priorities, key=lambda item: item[0])
        tasks = []
        seen = set()
        for _priority, title, task in priorities:
            normalized = task.strip()
            if normalized not in seen:
                tasks.append(normalized)
                seen.add(normalized)
            if len(tasks) == 7:
                break

        standard_tasks = [
            "Choose a realistic wake-up time and keep it similar each day.",
            "Create a 20–30 minute wind-down routine before bed.",
            "Make your sleep space as dark, quiet, and comfortable as practical.",
            "Review the week in a short sleep diary and keep the one change that helped most.",
            "Allow enough time for sleep for your age group; shift bedtime gradually if needed.",
            "Keep caffeine earlier in the day if it affects your sleep.",
            "Reduce late-night screen use and choose a calming alternative.",
        ]
        for task in standard_tasks:
            if len(tasks) >= 7:
                break
            if task not in seen:
                tasks.append(task)
                seen.add(task)
        return tasks[:7]

    def reset_form(self):
        defaults = {
            "age_group": "Adult (18–64 years)",
            "sleep_hours": "7.5",
            "bedtime_consistency": "Consistent (within 30 minutes)",
            "wake_consistency": "Usually",
            "screens": "Some screen use",
            "caffeine": "None or morning only",
            "naps": "No naps",
            "exercise": "Some days",
            "stress": "Sometimes",
            "room": "Dark, quiet, and comfortably cool",
            "night_waking": "Rarely or once",
            "refreshed": "Usually",
            "snoring": "No",
            "daytime_impact": "No major effect",
            "duration": "Not currently having difficulties",
        }
        for key, value in defaults.items():
            self.variables[key].set(value)
        self.answers = {}
        self.report_text = ""
        messagebox.showinfo("Reset complete", "Your answers have been reset to the default choices.")

    def save_report(self):
        if not self.report_text:
            messagebox.showinfo("No report yet", "Please generate your sleep advice before saving the report.")
            return
        path = filedialog.asksaveasfilename(
            title="Save SleepWise Report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="sleepwise_report.txt",
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as report_file:
                report_file.write(self.report_text)
            messagebox.showinfo("Report saved", f"Your report was saved successfully:\n{path}")
        except OSError as error:
            messagebox.showerror("Could not save report", f"The report could not be saved.\n\n{error}")


def main():
    root = tk.Tk()
    SleepAdviceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
