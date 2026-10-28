"""
Sleep Advice Expert System
==========================
A rule-based expert system (forward chaining) that gives general
sleep-hygiene advice based on the user's sleep habits.

Light, clinical "medical" theme built with Tkinter (included with Python).
Run:  python sleep_advice_expert_system.py

Disclaimer: this gives general wellness information, not a medical diagnosis.
"""

import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk, messagebox


# =====================================================================
# 1. THEME - light medical palette
# =====================================================================
THEME = {
    "bg":        "#F4FAFB",   # clinical off-white window background
    "card":      "#FFFFFF",   # cards and panels
    "primary":   "#0E7C86",   # medical teal
    "primary_d": "#095E66",   # darker teal (hover state)
    "accent":    "#E3F4F3",   # pale mint highlight
    "text":      "#1D3B45",   # dark slate text
    "muted":     "#6B8A93",   # secondary text
    "border":    "#D3E7EA",   # soft borders
    "high":      "#C62828",   # priority colours
    "medium":    "#B26A00",
    "low":       "#2E7D32",
}
FONT_TITLE = ("Arial", 18, "bold")
FONT_H2    = ("Arial", 13, "bold")
FONT_BODY  = ("Arial", 11)
FONT_BOLD  = ("Arial", 11, "bold")
FONT_SMALL = ("Arial", 9)


# =====================================================================
# 2. KNOWLEDGE BASE - questions and the facts each answer produces
# =====================================================================
QUESTIONS = [
    {
        "text": "What time do you usually go to bed?",
        "options": [
            ("Before 10:00 PM", ["bedtime_early"]),
            ("10:00 PM - 12:00 AM", ["bedtime_normal"]),
            ("After 12:00 AM (midnight)", ["bedtime_late"]),
        ],
    },
    {
        "text": "How many hours do you sleep on an average night?",
        "options": [
            ("Less than 5 hours", ["sleep_very_short"]),
            ("5 - 6 hours", ["sleep_short"]),
            ("7 - 9 hours", ["sleep_adequate"]),
            ("More than 9 hours", ["sleep_long"]),
        ],
    },
    {
        "text": "Do you wake up at about the same time every day, including weekends?",
        "options": [
            ("Yes, consistently", []),
            ("No, weekends differ by 2+ hours", ["irregular_schedule"]),
        ],
    },
    {
        "text": "Do you drink tea, coffee or cola in the afternoon or evening?",
        "options": [
            ("No", []),
            ("Yes, after 2:00 PM", ["caffeine_late"]),
        ],
    },
    {
        "text": "Do you use a phone, laptop or TV within 1 hour of going to bed?",
        "options": [("No", []), ("Yes", ["screens_before_bed"])],
    },
    {
        "text": "Do you drink alcohol or smoke within a few hours of bedtime?",
        "options": [("No", []), ("Yes", ["alcohol_before_bed"])],
    },
    {
        "text": "Do you take daytime naps longer than 30 minutes?",
        "options": [("No", []), ("Yes", ["long_naps"])],
    },
    {
        "text": "Is your bedroom usually noisy, bright or hot?",
        "options": [
            ("No, it is dark, quiet and cool", []),
            ("Yes", ["poor_environment"]),
        ],
    },
    {
        "text": "Do you eat a heavy meal within 2 hours of bedtime?",
        "options": [("No", []), ("Yes", ["heavy_meal_late"])],
    },
    {
        "text": "How often do you do physical activity (walking, exercise, sports)?",
        "options": [
            ("Most days (30+ minutes)", []),
            ("1 - 2 times a week", ["low_activity"]),
            ("Rarely or never", ["low_activity"]),
        ],
    },
    {
        "text": "Do you often lie awake worrying or feeling stressed at bedtime?",
        "options": [("No", []), ("Yes", ["stressed_at_bed"])],
    },
    {
        "text": "Do you feel sleepy or tired during the day, even after a full night's sleep?",
        "options": [("No", []), ("Yes", ["daytime_sleepiness"])],
    },
    {
        "text": "Does anyone say you snore loudly or stop breathing during sleep?",
        "options": [("No", []), ("Yes", ["snoring"])],
    },
]

# Human-readable names for the key findings shown in the report
PROFILE_LABELS = {
    "sleep_deprived":          "short sleep duration",
    "circadian_disruption":    "irregular sleep-wake (body clock) pattern",
    "possible_sleep_disorder": "daytime sleepiness together with snoring",
    "stress_insomnia_pattern": "stress-related difficulty sleeping",
}

PRIORITY_LABEL = {
    1: ("High priority", "high"),
    2: ("Recommended", "medium"),
    3: ("Helpful tip", "low"),
}


# =====================================================================
# 3. RULE BASE - IF <conditions> THEN <conclusion / advice>
# =====================================================================
@dataclass
class Rule:
    rid: str                 # unique rule id
    conditions: list         # facts that must ALL be true (IF part)
    conclusion: str = None   # new fact added to working memory (THEN part)
    advice: str = ""         # advice shown to the user (THEN part)
    category: str = ""
    priority: int = 3        # 1 = high, 2 = recommended, 3 = helpful tip


RULES = [
    # ---------- Intermediate (derived) facts ----------
    Rule("D1", ["sleep_very_short"], conclusion="sleep_deprived"),
    Rule("D2", ["sleep_short"], conclusion="sleep_deprived"),
    Rule("D3", ["bedtime_late", "irregular_schedule"],
         conclusion="circadian_disruption"),
    Rule("D4", ["daytime_sleepiness", "snoring"],
         conclusion="possible_sleep_disorder"),
    Rule("D5", ["stressed_at_bed", "sleep_deprived"],
         conclusion="stress_insomnia_pattern"),

    # ---------- Advice rules ----------
    Rule("R1", ["possible_sleep_disorder"], category="Medical referral", priority=1,
         advice="Daytime sleepiness together with loud snoring or breathing pauses can be "
                "a sign of a sleep-related breathing disorder such as sleep apnoea. Please "
                "consult a doctor or sleep specialist for an evaluation."),
    Rule("R2", ["stress_insomnia_pattern"], category="Stress and sleep", priority=1,
         advice="Stress and short sleep can feed each other. Set a daily 'worry time' earlier "
                "in the evening, practise slow breathing or muscle relaxation before bed, and "
                "if you cannot fall asleep after about 20 minutes, get up, do something calm in "
                "dim light, and return to bed only when sleepy."),
    Rule("R3", ["sleep_deprived"], category="Sleep duration", priority=1,
         advice="Most adults need 7 to 9 hours of sleep per night. Work backwards from your "
                "wake-up time and choose a bedtime that allows at least 7 hours of sleep."),
    Rule("R4", ["daytime_sleepiness", "sleep_adequate"], category="Medical referral", priority=2,
         advice="Feeling sleepy during the day despite 7 to 9 hours in bed may point to poor "
                "sleep quality or another health issue. If it continues, please see a doctor."),
    Rule("R5", ["circadian_disruption"], category="Body clock", priority=2,
         advice="Your body clock is likely out of step. Get bright daylight within an hour of "
                "waking, and keep meals and activity at regular times to anchor your sleep-wake rhythm."),
    Rule("R6", ["bedtime_late"], category="Sleep schedule", priority=2,
         advice="Going to bed late makes it harder to wake early. Move your bedtime earlier "
                "gradually, by about 15 to 30 minutes every few days, rather than all at once."),
    Rule("R7", ["irregular_schedule"], category="Sleep schedule", priority=2,
         advice="Wake up at about the same time every day, including weekends. Keep any weekend "
                "lie-in within about one hour of your weekday wake-up time."),
    Rule("R8", ["caffeine_late"], category="Stimulants", priority=2,
         advice="Avoid coffee, tea, cola and energy drinks for at least 6 hours before bed, "
                "since caffeine stays active in the body for several hours and can disrupt sleep."),
    Rule("R9", ["alcohol_before_bed"], category="Stimulants", priority=2,
         advice="Alcohol may make you drowsy at first, but it fragments sleep later in the night. "
                "Avoid alcohol and smoking in the 3 hours before bed."),
    Rule("R10", ["screens_before_bed"], category="Screens and light", priority=2,
         advice="Stop using phones, laptops and TVs 30 to 60 minutes before bed. Their bright light "
                "and mental stimulation can delay sleep. If you must use them, lower the brightness "
                "or enable night mode."),
    Rule("R11", ["poor_environment"], category="Bedroom environment", priority=2,
         advice="Make your bedroom dark, quiet and cool (around 18 °C / 65 °F). Use blackout "
                "curtains, earplugs or a fan, and keep the bed for sleep rather than for work."),
    Rule("R12", ["stressed_at_bed"], category="Stress and sleep", priority=2,
         advice="Build a calming wind-down routine 30 to 60 minutes before bed, such as reading, "
                "a warm shower, or writing tomorrow's to-do list to clear your mind."),
    Rule("R13", ["long_naps"], category="Daytime naps", priority=3,
         advice="Keep daytime naps short (about 20 to 30 minutes) and finish them before 3:00 PM "
                "so they do not reduce your sleep drive at night."),
    Rule("R14", ["heavy_meal_late"], category="Diet", priority=3,
         advice="Finish large meals at least 2 to 3 hours before bed. If you are hungry, a small, "
                "light snack is fine."),
    Rule("R15", ["low_activity"], category="Physical activity", priority=3,
         advice="Aim for about 30 minutes of physical activity on most days, such as brisk walking. "
                "Finish vigorous workouts at least 1 to 2 hours before bed."),
    Rule("R16", ["sleep_long"], category="Sleep duration", priority=3,
         advice="Regularly sleeping more than 9 hours can reflect poor sleep quality or an "
                "underlying health issue. If you still feel tired, please see a doctor."),
]


# =====================================================================
# 4. INFERENCE ENGINE - forward chaining
# =====================================================================
class SleepExpertSystem:
    """Applies rules repeatedly until no new facts can be derived."""

    def __init__(self, rules):
        self.rules = rules

    def infer(self, facts):
        known = set(facts)            # working memory
        fired, fired_ids = [], set()
        changed = True
        while changed:                # keep going while new facts appear
            changed = False
            for rule in self.rules:
                if rule.rid in fired_ids:
                    continue
                if all(cond in known for cond in rule.conditions):
                    fired_ids.add(rule.rid)
                    fired.append(rule)
                    if rule.conclusion:
                        known.add(rule.conclusion)
                    changed = True
        return known, fired

    def advise(self, answer_facts):
        """answer_facts: list of fact-lists, one per answered question."""
        facts = set()
        for group in answer_facts:
            facts.update(group)
        known, fired = self.infer(facts)
        advice = sorted((r for r in fired if r.advice), key=lambda r: r.priority)
        return advice, known


# =====================================================================
# 5. GRAPHICAL USER INTERFACE
# =====================================================================
class SleepAdviceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sleep Advice Expert System")
        self.geometry("780x640")
        self.minsize(700, 580)
        self.configure(bg=THEME["bg"])

        self.engine = SleepExpertSystem(RULES)
        self.current = 0
        self.choices = [None] * len(QUESTIONS)
        self.selected = tk.IntVar(value=-1)
        self.showing_results = False

        self._setup_style()
        self._build_header()
        self._build_footer()      # packed before body so it always stays visible
        self._build_body()
        self.show_question()

    # ---------- styling ----------
    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Teal.Horizontal.TProgressbar",
                        troughcolor=THEME["accent"], background=THEME["primary"],
                        bordercolor=THEME["border"], lightcolor=THEME["primary"],
                        darkcolor=THEME["primary"])
        style.configure("Teal.TButton", font=FONT_BOLD, padding=(18, 9),
                        background=THEME["primary"], foreground="white", borderwidth=0)
        style.map("Teal.TButton",
                  background=[("active", THEME["primary_d"]), ("disabled", THEME["border"])],
                  foreground=[("disabled", THEME["muted"])])
        style.configure("Ghost.TButton", font=FONT_BOLD, padding=(18, 9),
                        background=THEME["card"], foreground=THEME["primary"],
                        bordercolor=THEME["primary"], borderwidth=1)
        style.map("Ghost.TButton",
                  background=[("active", THEME["accent"]), ("disabled", THEME["bg"])],
                  foreground=[("disabled", THEME["muted"])])

    # ---------- layout ----------
    def _build_header(self):
        header = tk.Frame(self, bg=THEME["card"])
        header.pack(side="top", fill="x")

        logo = tk.Canvas(header, width=56, height=56, bg=THEME["card"], highlightthickness=0)
        logo.pack(side="left", padx=(24, 14), pady=14)
        logo.create_oval(2, 2, 54, 54, fill=THEME["primary"], outline="")
        logo.create_rectangle(23, 12, 33, 44, fill="white", outline="")   # medical cross
        logo.create_rectangle(12, 23, 44, 33, fill="white", outline="")

        titles = tk.Frame(header, bg=THEME["card"])
        titles.pack(side="left", pady=12)
        tk.Label(titles, text="Sleep Advice Expert System", font=FONT_TITLE,
                 bg=THEME["card"], fg=THEME["primary"]).pack(anchor="w")
        tk.Label(titles, text="General sleep-hygiene guidance based on your sleep habits",
                 font=FONT_SMALL, bg=THEME["card"], fg=THEME["muted"]).pack(anchor="w")

        tk.Frame(self, bg=THEME["border"], height=2).pack(side="top", fill="x")

    def _build_footer(self):
        footer = tk.Frame(self, bg=THEME["bg"])
        footer.pack(side="bottom", fill="x", padx=24, pady=(0, 20))
        self.back_btn = ttk.Button(footer, text="Back", style="Ghost.TButton",
                                   command=self.go_back)
        self.back_btn.pack(side="left")
        self.next_btn = ttk.Button(footer, text="Next", style="Teal.TButton",
                                   command=self.go_next)
        self.next_btn.pack(side="right")

    def _build_body(self):
        self.progress = ttk.Progressbar(self, style="Teal.Horizontal.TProgressbar",
                                        maximum=len(QUESTIONS))
        self.progress.pack(side="top", fill="x", padx=24, pady=(16, 0))

        self.step_label = tk.Label(self, font=FONT_SMALL, bg=THEME["bg"], fg=THEME["muted"])
        self.step_label.pack(side="top", anchor="w", padx=24, pady=(6, 8))

        self.card = tk.Frame(self, bg=THEME["card"], highlightbackground=THEME["border"],
                             highlightthickness=1)
        self.card.pack(side="top", fill="both", expand=True, padx=24, pady=(0, 12))

        # --- question view ---
        self.question_frame = tk.Frame(self.card, bg=THEME["card"])
        self.question_label = tk.Label(self.question_frame, font=FONT_H2, bg=THEME["card"],
                                       fg=THEME["text"], wraplength=680, justify="left")
        self.question_label.pack(anchor="w", padx=30, pady=(30, 18))
        self.options_frame = tk.Frame(self.question_frame, bg=THEME["card"])
        self.options_frame.pack(anchor="w", padx=30)

        # --- report view ---
        self.results_frame = tk.Frame(self.card, bg=THEME["card"])
        self.report = tk.Text(self.results_frame, wrap="word", font=FONT_BODY,
                              bg=THEME["card"], fg=THEME["text"], relief="flat",
                              borderwidth=0, padx=28, pady=18, cursor="arrow")
        scroll = ttk.Scrollbar(self.results_frame, command=self.report.yview)
        self.report.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.report.pack(side="left", fill="both", expand=True)

        self.report.tag_configure("h2", font=FONT_H2, foreground=THEME["primary"],
                                  spacing1=6, spacing3=6)
        self.report.tag_configure("cat", font=FONT_BOLD, foreground=THEME["text"], spacing1=8)
        self.report.tag_configure("body", font=FONT_BODY, foreground=THEME["text"],
                                  lmargin1=22, lmargin2=22, spacing3=4)
        self.report.tag_configure("high", font=FONT_SMALL, foreground=THEME["high"])
        self.report.tag_configure("medium", font=FONT_SMALL, foreground=THEME["medium"])
        self.report.tag_configure("low", font=FONT_SMALL, foreground=THEME["low"])
        self.report.tag_configure("muted", font=FONT_SMALL, foreground=THEME["muted"], spacing1=14)

    # ---------- navigation ----------
    def show_question(self):
        self.showing_results = False
        self.results_frame.pack_forget()
        self.question_frame.pack(fill="both", expand=True)

        q = QUESTIONS[self.current]
        self.progress["value"] = self.current
        self.step_label.config(text=f"Question {self.current + 1} of {len(QUESTIONS)}")
        self.question_label.config(text=q["text"])

        for widget in self.options_frame.winfo_children():
            widget.destroy()
        saved = self.choices[self.current]
        self.selected.set(-1 if saved is None else saved)
        for idx, (label, _facts) in enumerate(q["options"]):
            tk.Radiobutton(self.options_frame, text=label, value=idx, variable=self.selected,
                           font=FONT_BODY, bg=THEME["card"], fg=THEME["text"],
                           activebackground=THEME["accent"], activeforeground=THEME["text"],
                           selectcolor=THEME["accent"], highlightthickness=0, anchor="w",
                           cursor="hand2").pack(anchor="w", pady=7)

        self.back_btn.configure(text="Back", command=self.go_back)
        self.back_btn.state(["!disabled"] if self.current > 0 else ["disabled"])
        last = self.current == len(QUESTIONS) - 1
        self.next_btn.configure(text="Get my advice" if last else "Next", command=self.go_next)

    def go_next(self):
        choice = self.selected.get()
        if choice < 0:
            messagebox.showinfo("Please answer", "Please choose one option to continue.", parent=self)
            return
        self.choices[self.current] = choice
        if self.current < len(QUESTIONS) - 1:
            self.current += 1
            self.show_question()
        else:
            self.show_results()

    def go_back(self):
        if self.showing_results:
            self.current = len(QUESTIONS) - 1
            self.show_question()
        elif self.current > 0:
            if self.selected.get() >= 0:
                self.choices[self.current] = self.selected.get()
            self.current -= 1
            self.show_question()

    def show_results(self):
        self.showing_results = True
        answers = [QUESTIONS[i]["options"][c][1] for i, c in enumerate(self.choices)]
        advice, facts = self.engine.advise(answers)

        self.question_frame.pack_forget()
        self.results_frame.pack(fill="both", expand=True)
        self.progress["value"] = len(QUESTIONS)
        self.step_label.config(text="Your personalised sleep report")
        self._render_report(advice, facts)

        self.back_btn.configure(text="Review answers", command=self.go_back)
        self.back_btn.state(["!disabled"])
        self.next_btn.configure(text="Start over", command=self.restart)

    def restart(self):
        self.choices = [None] * len(QUESTIONS)
        self.current = 0
        self.show_question()

    # ---------- report ----------
    def _render_report(self, advice, facts):
        t = self.report
        t.config(state="normal")
        t.delete("1.0", "end")

        t.insert("end", "Your Sleep Profile\n", "h2")
        findings = [label for key, label in PROFILE_LABELS.items() if key in facts]
        if findings:
            t.insert("end", "Key findings: " + "; ".join(findings) + ".\n", "body")
        else:
            t.insert("end", "No major sleep risk factors were detected.\n", "body")

        if advice:
            t.insert("end", "\nPersonalised Sleep-Hygiene Advice\n", "h2")
            for n, rule in enumerate(advice, start=1):
                label, tag = PRIORITY_LABEL[rule.priority]
                t.insert("end", f"\n{n}. {rule.category}   ", "cat")
                t.insert("end", f"({label})\n", tag)
                t.insert("end", rule.advice + "\n", "body")
        else:
            t.insert("end", "\nYour answers reflect healthy sleep habits. "
                            "Keep up the good routine!\n", "body")

        t.insert("end", "\nThis is general wellness information, not a medical diagnosis. "
                        "If sleep problems continue for several weeks, please consult a doctor.",
                 "muted")
        t.config(state="disabled")
        t.yview_moveto(0)


# =====================================================================
# 6. ENTRY POINT
# =====================================================================
if __name__ == "__main__":
    app = SleepAdviceApp()
    app.mainloop()