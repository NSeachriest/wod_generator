"""
Nathan Seachriest
26 May, 2023

WOD Generator
Program generates a random wod by combining several potential workout patterns
and exercises to target each muscle group in a full-body HIIT workout.
"""

import random
from tkinter import *
from tkinter import ttk

def exercise_category_selector(muscle_group):
    """
    Ensures that the workout cycles through different muscle groups.

    Parameters
    ----------
    muscle_group : TYPE
        DESCRIPTION.

    Returns
    -------
    exercise : LIST
        DESCRIPTION.

    """
    core_exercises_list = [
        ["Sit-ups", 30, 45, 60],
        ["Plank", 30, 40, 55],
        ["Hollow-rocks", 15, 25, 35],
        ["Hollow-hold", 30, 40, 55]
        ]
    upper_body_exercises_list = [
        ["Push-ups", 20, 30, 40],
        ["Pull-ups", 3, 8, 12],
        ["Inverted Rows", 15, 25, 35]
        ]
    leg_exercises_list = [
        ["Pistols", 10, 15, 25],
        ["Air Squats", 30, 40, 50]
        ]
    muscle_group = muscle_group % 3
    if muscle_group == 0:
        exercise = random.choice(core_exercises_list)
    elif muscle_group == 1:
        exercise = random.choice(upper_body_exercises_list)
    else:
        exercise = random.choice(leg_exercises_list)
    return exercise

def emom(muscle_group, desired_intensity):
    """
    EMOM structure:
    For X minutes do Y workout at the beginning of each minute, resting for
    the remainder of the minute

    Parameters
    ----------
    muscle_group : TYPE
        DESCRIPTION.

    Returns
    -------
    list
        DESCRIPTION.

    """
    exercise = exercise_category_selector(muscle_group)
    time = random.randint(4, 10)
    string = f"EMOM: {exercise[desired_intensity]} "
    if exercise[0] not in ['Plank', 'Hollow-hold']:
        string = string + f"{exercise[0]} for {time} minutes"
    else:
        string = string + f"second {exercise[0]} for {time} minutes"
    return [string, time]

def amrap(muscle_group):
    """
    AMRAP structure:
    Do as many reps as possible of a workout
    (may rest in the "up" position).

    Parameters
    ----------
    muscle_group : TYPE
        DESCRIPTION.

    Returns
    -------
    list
        DESCRIPTION.

    """
    exercise = exercise_category_selector(muscle_group)
    while exercise[0] == 'Plank' or exercise[0] == 'Hollow-hold':
        exercise = exercise_category_selector(muscle_group)
    return [f"AMRAP: {exercise[0]}", 2]

def tabata(muscle_group):
    """
    TABATA structure:
    20 seconds of work and 10 seconds of rest alternating for X minutes

    Parameters
    ----------
    muscle_group : TYPE
        DESCRIPTION.

    Returns
    -------
    list
        DESCRIPTION.

    """
    exercise = exercise_category_selector(muscle_group)
    time = random.randint(4, 8)
    return [f"TABATA: {exercise[0]} for {time} minutes", time]

def create_wod(user_input):
    """
    

    Parameters
    ----------
    user_input : LIST
        [Time limit, Desired intensity]

    Returns
    -------
    wod : TYPE
        DESCRIPTION.

    """
    PATTERNS = ["EMOM", "AMRAP", "TABATA"]
    time_limit = user_input[0]
    desired_intensity = user_input[1]
    muscle_group = 0
    total_time = 0
    wod = []
    while total_time <= time_limit:
        wod_pattern = random.choice(PATTERNS)
        if wod_pattern == 'EMOM':
            wod_plan = emom(muscle_group, desired_intensity)
            total_time += wod_plan[1]
            wod.append(wod_plan[0])
        elif wod_pattern == 'AMRAP':
            wod_plan = amrap(muscle_group)
            total_time += wod_plan[1]
            wod.append(wod_plan[0])
        else:
            wod_plan = tabata(muscle_group)
            total_time += wod_plan[1]
            wod.append(wod_plan[0])
        muscle_group += 1
    return wod

class GenerateUI:

    def __init__(self, root):
        root.title("WOD Generator")

        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        """
        

        Returns
        -------
        None.

        """

        self.time_limit = IntVar()
        time_entry = ttk.Entry(self.mainframe, width=7,
                               textvariable=self.time_limit)
        time_entry.grid(column=1, row=1, sticky=(S, E))
        ttk.Label(self.mainframe, text="Time limit (minutes)").grid(column=2,
                                                            row=1, sticky=W)
        self.desired_intensity = IntVar()
        intensity_easy = ttk.Radiobutton(self.mainframe, text='Beginner',
                                    variable=self.desired_intensity, value=1)
        intensity_medium = ttk.Radiobutton(self.mainframe, text='Intermediate',
                                    variable=self.desired_intensity, value=2)
        intensity_hard = ttk.Radiobutton(self.mainframe, text='Advanced',
                                    variable=self.desired_intensity, value=3)
        intensity_easy.grid(column=1, row=2, sticky=(N, W))
        intensity_medium.grid(column=2, row=2, sticky=(N, W))
        intensity_hard.grid(column=3, row=2, sticky=(N, W))

        generate_button = ttk.Button(self.mainframe, text="Generate",
                                     command=self.generate_wod)
        generate_button.grid(column=2, row=3, sticky=(N, S, E, W))

    def generate_wod(self):
        """
        

        Returns
        -------
        None.

        """
        try:
            time = self.time_limit.get()
            intensity = self.desired_intensity.get()
            wod = create_wod([time, intensity])
        except TypeError as error:
            print(error)
            wod = create_wod([30, 2])
        self.show_wod(wod)

    def show_wod(self, wod):
        """
        

        Returns
        -------
        None.

        """
        for widget in self.mainframe.grid_slaves():
            if isinstance(widget, ttk.Label):
                widget.grid_forget()
        ttk.Label(self.mainframe, text="Time limit (minutes)").grid(column=2,
                                                            row=1, sticky=W)
        for index, item in enumerate(wod):
            label = ttk.Label(self.mainframe, text=item)
            label.grid(column=0, row=index, sticky=(N, W))

def main():
    root = Tk()
    GenerateUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
