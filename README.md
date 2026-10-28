# Sleep Advice Expert System (SleepWise)

A beginner-friendly Python desktop application built with Tkinter. It asks about sleep habits and applies simple **IF/THEN rules** to produce general sleep-hygiene suggestions, an educational sleep-habit alignment score, and a practical 7-day starter plan.

## Features

- Light medical-inspired interface: white cards, light blue and teal accents
- Detailed sleep-habits questionnaire
- Rule-based recommendations based on the selected answers
- Age-group-aware sleep-duration guidance
- Sleep-habit alignment score (educational feedback only)
- Personalized 7-day starter plan
- Warnings about when professional advice may be appropriate
- Save results as a `.txt` report
- No external Python packages required

## Requirements

- Python 3.10 or newer recommended
- Tkinter (usually included with standard Python on Windows)
- Visual Studio Code (VS Code)

## Run in VS Code on Windows

1. Extract the ZIP file into a folder, for example `sleep_advice_expert_system`.
2. Open VS Code.
3. Select **File → Open Folder** and choose that folder.
4. Open `main.py` in the Explorer panel.
5. Open **Terminal → New Terminal**.
6. Run this command:

   ```powershell
   python main.py
   ```

7. If `python` does not work, try the Python launcher:

   ```powershell
   py main.py
   ```

8. The SleepWise desktop window should open. Complete the questions, then click **Generate My Sleep Advice**.
9. On the **Your Results** tab, you can read the report and use **Save Report as TXT**.

### If you already use a virtual environment

You can run the app with the virtual environment's Python interpreter. For example:

```powershell
.\.venv\Scripts\python.exe main.py
```

## How the expert system works

The application uses rule-based logic rather than machine learning. For example:

- **IF** reported sleep is below the common range for the selected age group, **THEN** it suggests allowing more time for sleep and shifting bedtime gradually.
- **IF** caffeine is used near bedtime, **THEN** it suggests moving caffeine earlier.
- **IF** screens are used until bedtime, **THEN** it suggests a screen-free wind-down period.
- **IF** loud snoring or breathing pauses are reported, **THEN** it advises discussing these signs with a healthcare professional.

The score is a simple educational reflection of selected habits. It is **not** a clinical scale and cannot diagnose a sleep disorder.

## Troubleshooting

- **Python command not found:** install Python from the official Python website and enable the option to add Python to PATH, or try `py main.py`.
- **Tkinter error:** use a standard Windows Python installation that includes Tcl/Tk. On Windows, Tkinter normally ships with Python.
- **Window does not appear:** check the VS Code terminal for error messages and make sure the file is saved as `main.py`.

## Health disclaimer

SleepWise provides general educational sleep-hygiene information only. It is not medical advice, diagnosis, or treatment. Sleep problems that persist, worsen, or interfere with daily life should be discussed with a qualified healthcare professional. Seek urgent help for an emergency.
