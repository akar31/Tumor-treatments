"""
tumortreatments.py 

Azra Karatan
Fall 2024
CS152-B Final Project

This program models the survival of patients with brain tumors according to their treatment types to determine which treatment is the most effective for brain tumors.

To run this program, execute it directly from the Mac terminal by typing cd desktop, then python3 tumortreatments.py
"""

import random
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Patient:
    # Parent class for patients
    def __init__(self, treatment_effect, tumor_size=10, growth_rate=1, time=0):
        self.tumor_size = tumor_size
        self.growth_rate = growth_rate
        self.treatment_effect = treatment_effect
        self.time = time  # in months

    """the The Gompertz Model function which's code did not calculate tumor growth correctly"""
    # def grow_tumor(self, carrying_capacity):
    #     """Simulates tumor growth using a simplified model"""
        
    #     # the Gompertz parameters

    #     K = 200  # Carrying capacity
    #     r = 0.1  # Growth rate
    #     t = 5    # Time
    #     e = 2.718281828459045  # Euler's number (e)
        
    #     # Update tumor size using the Gompertz formula
    #     self.tumor_size = K * (e ** (-r * t))


    def grow_tumor(self, carrying_capacity= 4):
            """Simulates tumor growth using the Gompertz model."""
            r = self.growth_rate  # Growth rate
            current_size = self.tumor_size  # Tumor size at the current time step
            
            # Update tumor size using the Gompertz model
            self.tumor_size *= 1.2
            print(self.tumor_size)

    def apply_treatment(self):
        """Apply treatment effect to reduce tumor size"""
        self.tumor_size *= self.treatment_effect


class ChemoPatient(Patient):
    def __init__(self):
        super().__init__(treatment_effect=0.3)


class RadioPatient(Patient):
    def __init__(self):
        super().__init__(treatment_effect=0.2)


class ChemoRadioPatient(Patient):
    def __init__(self):
        super().__init__(treatment_effect=0.1)


class NoTreatmentPatient(Patient):
    def __init__(self):
        super().__init__(treatment_effect=1)


# Global variable to track initial groups
initial = {"ChemoPatient": [], "RadioPatient": [], "ChemoRadioPatient": [], "NoTreatmentPatient": []}


def newPatient():
    """Creates a new patient and assigns a treatment group."""
    chance = random.random()
    if chance < 0.25:
        patient = ChemoPatient()
        initial["ChemoPatient"].append(patient)
    elif 0.25 <= chance < 0.5:
        patient = RadioPatient()
        initial["RadioPatient"].append(patient)
    elif 0.5 <= chance < 0.75:
        patient = ChemoRadioPatient()
        initial["ChemoRadioPatient"].append(patient)
    else:
        patient = NoTreatmentPatient()
        initial["NoTreatmentPatient"].append(patient)
    return patient


def initPopulation(populationsize):
    """Initializes the population with patients"""
    allPatients = []
    for _ in range(populationsize):
        patient = newPatient()
        allPatients.append(patient)
    return allPatients


def killPatients(parameters, patients):
    """Removes patients whose tumors exceed the carrying capacity"""
    survivors = []
    carrying_capacity = parameters[1]

    for patient in patients:
        if patient.tumor_size <= carrying_capacity:
            survivors.append(patient)

    survivalRate = len(survivors) / parameters[0]
    return survivors, survivalRate


def simulateYearAfter(parameters, patients):
    """Simulates tumor growth and treatment over a year"""
    for _ in range(12):
        for patient in patients:
            patient.time += 1
            patient.apply_treatment()
            patient.grow_tumor(parameters[1])

    patients, survivalRate = killPatients(parameters, patients)
    return patients, survivalRate


def calcResults(patients):
    """Calculates and returns the results for each treatment group"""
    groups = {
        "ChemoPatient": [],
        "RadioPatient": [],
        "ChemoRadioPatient": [],
        "NoTreatmentPatient": []}

    for patient in patients:
        treatment_name = type(patient).__name__
        if treatment_name in groups:
            groups[treatment_name].append(patient)

    # Calculate survival rates
    results = {}
    for treatment, group in groups.items():
        initial_count = len(initial[treatment])
        survived_count = len(group)
        if initial_count > 0:
            survival_rate = survived_count / initial_count
        else:
            survival_rate = 0
        results[treatment] = {
            'survival_rate': survival_rate,
            'survived_count': survived_count,
            'initial_count': initial_count }

    return results

def plot_results(results):
    """Plots a bar graph of survival rates across treatments"""
    treatments = list(results.keys())
    survival_rates = []
    for result in results.values():
        survival_rates.append(result['survival_rate'])

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.bar(treatments, survival_rates, color=['blue', 'red', 'hotpink', 'purple'])
    ax.set_title("Survival Rates by Treatment Type")
    ax.set_xlabel("Treatment")
    ax.set_ylabel("Survival Rate (%)")
    return fig


def runSimulation(population_size, carrying_capacity, output_box, graph_frame):
    """Runs the simulation and displays the results in the output box."""
    # Initialize parameters
    parameters = [population_size, carrying_capacity]
    patients = initPopulation(population_size)

    # Simulate tumor growth and treatment over a year
    patients, survivalRate = simulateYearAfter(parameters, patients)

    # Calculate results
    results = calcResults(patients)

    # Display text results
    results_text = "                     The results for each cancer treatment:\n"
    for treatment, data in results.items():
        results_text += f"The number of {treatment} patients survived: {data['survived_count']} out of {data['initial_count']} initial patients\n"
    results_text += f"\nFinal population size: {len(patients)}\n"
    results_text += f"Survival rate: {len(patients) / population_size:.2%}"

    # Display results in the output box
    output_box.config(state="normal")
    output_box.delete(1.0, tk.END)  # Clear previous output
    output_box.insert(tk.END, results_text)
    output_box.config(state="disabled")

    # Plot results
    fig = plot_results(results)
    # Embed the plot into the tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


def getTreatmentDescription(treatment_name):
    """Returns a descriptive message about each treatment to inform the patient of each treatment option they have."""
    descriptions = {
        "ChemoPatient": "Chemotherapy treatment targets rapidly growing cells, but may cause side effects such as nausea, hair loss, and fatigue.",
        "RadioPatient": "Radiation therapy uses high-energy rays to shrink or destroy the tumor, but it can cause fatigue, skin irritation, and long-term tissue damage.",
        "ChemoRadioPatient": "Combined chemotherapy and radiation therapy can be more effective but may cause increased side effects, such as severe fatigue and organ damage.",
        "NoTreatmentPatient": "No treatment option may result in faster tumor growth and lower survival chances."}
    
    return descriptions.get(treatment_name, "No description available.")


def main():
    """Main GUI application."""
    # Create the main window
    root = tk.Tk()
    root.title("Brain Tumor Treatment Simulation")

    # Input fields
    tk.Label(root, text="Number of Patients:").grid(row=0, column=0, padx=10, pady=5)
    population_entry = tk.Entry(root)
    population_entry.grid(row=0, column=1, padx=10, pady=5)


    # Button to start the simulation
    def start_simulation():
        try:
            population_size = int(population_entry.get())
            carrying_capacity = 1.5  # Defined by the programmer
            runSimulation(population_size, carrying_capacity, output_box, graph_frame)
        except ValueError:
            output_box.config(state="normal")
            output_box.delete(1.0, tk.END)
            output_box.insert(tk.END, "Please enter a valid population size.")
            output_box.config(state="disabled")

    tk.Button(root, text="Run Simulation", command=start_simulation).grid(row=1, column=0, columnspan=2, pady=10)

    # Output box
    output_box = tk.Text(root, wrap="word", state="disabled", width=90, height=9)
    output_box.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    # Frame for the graph
    graph_frame = tk.Frame(root)
    graph_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Treatment dropdown and description (moved after the graph and results)
    treatment_options = ["ChemoPatient", "RadioPatient", "ChemoRadioPatient", "NoTreatmentPatient"]
    treatment_var = tk.StringVar(value=treatment_options[0])  # Default value


    def show_treatment_description():
        selected_treatment = treatment_var.get()
        description = getTreatmentDescription(selected_treatment)
        treatment_description_label.config(text=description)

    treatment_dropdown = tk.OptionMenu(root, treatment_var, *treatment_options)
    treatment_dropdown.grid(row=4, column=0, padx=10, pady=5)

    # Label to display treatment description
    treatment_description_label = tk.Label(root, text="", width=110, height=3, anchor="w", justify="left")
    treatment_description_label.grid(row=4, column=1, padx=10, pady=5)

    # Button to show treatment description
    tk.Button(root, text="Show Treatment Description", command=show_treatment_description).grid(row=5, column=0, columnspan=2, pady=10)

    # Start the GUI loop
    root.mainloop()



if __name__ == "__main__":
    main()
