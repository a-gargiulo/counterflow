import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

import numpy as np

ATM_TO_PA = 101325.0
SEC_TO_MIN = 1.0 / 60.0
M3_TO_L = 1000.0
R_U = 8.314
FUELS = ["Ethylene", "Hydrogen"]
OXIDIZERS = ["Air", "Oxygen"]
F_DILUENTS = ["Nitrogen", "Helium"]
OX_DILUENTS = ["Nitrogen", "Helium"]
F_SHROUDS = ["Nitrogen", "Helium"]
OX_SHROUDS = ["Nitrogen", "Helium"]
M = {
    "air": 28.97e-03,
    "ethylene": 28.05e-03,
    "nitrogen": 28.00e-03,
    "oxygen": 32.00e-03,
}
WIN_X = 600
WIN_Y = 800
FONT = "Arial"
FS1 = 16
FS2 = 12


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        run_gui()
    else:
        run_console()


def run_gui():
    root = tk.Tk()
    root.grid_columnconfigure(0, weight=1)

    generate_window(root, "RFL Counterflow Burner")

    inputs = []
    inputs_label = tk.Label(root, text="Inputs", font=(FONT, FS1))
    inputs_label.grid(row=0, column=0, padx=10, sticky="w")
    inputs_frame = tk.Frame(root, borderwidth=5, relief="ridge")
    inputs_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
    inputs_frame.grid_columnconfigure(1, weight=1)
    inputs.append(add_field(inputs_frame, "normal", "Strain Rate:", "1/s", 0, 0))
    inputs.append(add_field(inputs_frame, "normal", "Nozzle Separation Distance:", "m", 1, 0))
    inputs.append(add_field(inputs_frame, "normal", "Pressure:", "atm", 2, 0))
    inputs.append(add_field(inputs_frame, "normal", "Temperature:", "K", 3, 0))
    inputs.append(add_dropdown(inputs_frame, "Fuel:", FUELS[0], FUELS, 4, 0))
    inputs.append(add_field(inputs_frame, "normal", "Fuel Mole Fraction:", "", 5, 0))
    inputs.append(add_dropdown(inputs_frame, "Fuel Diluent:", F_DILUENTS[0], F_DILUENTS, 6, 0))
    inputs.append(add_dropdown(inputs_frame, "Oxidizer:", OXIDIZERS[0], OXIDIZERS, 7, 0))
    inputs.append(add_field(inputs_frame, "normal", "Oxidizer Mole Fraction:", "", 8, 0))
    inputs.append(add_dropdown(inputs_frame, "Oxidizer Diluent:", OX_DILUENTS[0], OX_DILUENTS, 9, 0))
    inputs.append(add_dropdown(inputs_frame, "Fuel Shroud:", F_SHROUDS[0], F_SHROUDS, 10, 0))
    inputs.append(add_dropdown(inputs_frame, "Oxidizer Shroud:", OX_SHROUDS[0], OX_SHROUDS, 11, 0))
    inputs.append(add_field(inputs_frame, "normal", "Shroud Momentum Fraction:", "", 12, 0))

    outputs = []
    outputs_frame = tk.Frame(root, borderwidth=5, relief="ridge")
    outputs_frame.grid(row=13, column=0, padx=10, pady=5, sticky="ew")
    outputs_frame.grid_columnconfigure(1, weight=1)
    oxidizer_label = tk.Label(outputs_frame, text="Oxidizer Side", font=(FONT, FS1))
    oxidizer_label.grid(row=0, column=0, padx=10, sticky="w")
    oxidizer_frame = tk.Frame(outputs_frame, borderwidth=5, relief="ridge")
    oxidizer_frame.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
    oxidizer_frame.grid_columnconfigure(1, weight=1)
    fuel_label = tk.Label(outputs_frame, text="Fuel Side", font=(FONT, FS1))
    fuel_label.grid(row=2, column=0, padx=10, sticky="w")
    fuel_frame = tk.Frame(outputs_frame, borderwidth=5, relief="ridge")
    fuel_frame.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
    fuel_frame.grid_columnconfigure(1, weight=1)
    shroud_label = tk.Label(outputs_frame, text="Shroud", font=(FONT, FS1))
    shroud_label.grid(row=4, column=0, padx=10, sticky="w")
    shroud_frame = tk.Frame(outputs_frame, borderwidth=5, relief="ridge")
    shroud_frame.grid(row=5, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
    shroud_frame.grid_columnconfigure(1, weight=1)
    outputs.append(add_field(oxidizer_frame, "readonly", "Total:", "SLPM", 0, 0))
    outputs.append(add_field(oxidizer_frame, "readonly", "Oxidizer:", "SLPM", 1, 0))
    outputs.append(add_field(oxidizer_frame, "readonly", "Oxidizer Diluent:", "SLPM", 2, 0))
    outputs.append(add_field(fuel_frame, "readonly", "Total:", "SLPM", 0, 0))
    outputs.append(add_field(fuel_frame, "readonly", "Fuel:", "SLPM", 1, 0))
    outputs.append(add_field(fuel_frame, "readonly", "Fuel Diluent:", "SLPM", 2, 0))
    outputs.append(add_field(shroud_frame, "readonly", "Oxidizer Side:", "SLPM", 0, 0))
    outputs.append(add_field(shroud_frame, "readonly", "Fuel Side:", "SLPM", 1, 0))

    calculate_button = tk.Button(root, text="Calculate", command=lambda: generate_output(inputs, outputs))
    calculate_button.grid(row=12, column=0, sticky="ns")

    load_cached_inputs(inputs)

    root.mainloop()


def generate_window(root, title):
    pos_x = root.winfo_screenwidth() // 2 - WIN_X // 2
    pos_y = root.winfo_screenheight() // 2 - WIN_Y // 2
    root.geometry(f"{WIN_X}x{WIN_Y}+{pos_x}+{pos_y}")
    root.title(title)


def add_field(parent, state, label_str, unit_str, gr, gc):
    label1 = tk.Label(parent, text=label_str, font=(FONT, FS2))
    label1.grid(row=gr, column=gc, padx=5, sticky="w")
    if state.lower() == "readonly":
        readonly_var = tk.StringVar(value="")
        entry = tk.Entry(parent, textvariable=readonly_var, state=state)
        entry.grid(row=gr, column=gc + 1, padx=5, sticky="we")
    else:
        entry = tk.Entry(parent, state=state)
        entry.grid(row=gr, column=gc + 1, padx=5, sticky="we")
    label2 = tk.Label(parent, text=unit_str, font=(FONT, FS2))
    label2.grid(row=gr, column=gc + 2, padx=5, sticky="w")
    if state.lower() == "readonly":
        return (label1, entry, readonly_var, label2)
    return (label1, entry, label2)


def add_dropdown(parent, label, default_option, options, gr, gc):
    selected_option = tk.StringVar(parent)
    selected_option.set(default_option)
    dropdown_label = tk.Label(parent, text=label, font=(FONT, FS2))
    dropdown_label.grid(row=gr, column=gc, padx=5, sticky="w")
    dropdown_menu = tk.OptionMenu(parent, selected_option, *options)
    dropdown_menu.grid(row=gr, column=gc + 1, padx=5, sticky="we")
    return (selected_option, dropdown_label, dropdown_menu)


def cache_inputs(data):
    with open("counterflow.json", "w") as f:
        json.dump(data, f, indent=4)


def load_cached_inputs(inputs):
    if os.path.exists("counterflow.json"):
        with open("counterflow.json", "r") as f:
            data = json.load(f)
            set_cache(inputs, data, 0, 1, "a_g")
            set_cache(inputs, data, 1, 1, "L")
            set_cache(inputs, data, 2, 1, "p")
            set_cache(inputs, data, 3, 1, "T")
            set_cache(inputs, data, 4, 0, "fuel")
            set_cache(inputs, data, 5, 1, "X_f")
            set_cache(inputs, data, 6, 0, "fuel_diluent")
            set_cache(inputs, data, 7, 0, "oxidizer")
            set_cache(inputs, data, 8, 1, "X_ox")
            set_cache(inputs, data, 9, 0, "oxidizer_diluent")
            set_cache(inputs, data, 10, 0, "fuel_shroud")
            set_cache(inputs, data, 11, 0, "oxidizer_shroud")
            set_cache(inputs, data, 12, 1, "shroud_momentum_fraction")


def set_cache(inp, data, i, j, var):
    if isinstance(inp[i][j], tk.Entry):
        inp[i][j].delete(0, tk.END)
        inp[i][j].insert(0, data.get(var, ""))
    else:
        inp[i][j].set(data.get(var, ""))


def generate_output(inputs, outputs):
    for i in range(len(inputs)):
        if isinstance(inputs[i][1], tk.Entry):
            if inputs[i][1].get().strip() == "":
                messagebox.showwarning(
                    "WARNING",
                    "Some inputs are empty! Please fill-out all input fields.",
                )
                return 1
        else:
            if inputs[i][0].get().strip() == "":
                messagebox.showwarning(
                    "WARNING",
                    "Some inputs are empty! Please fill-out all input fields.",
                )
                return 1

    inp = {
        "a_g": float(inputs[0][1].get()),
        "L": float(inputs[1][1].get()),
        "p": float(inputs[2][1].get()),
        "T": float(inputs[3][1].get()),
        "fuel": inputs[4][0].get(),
        "X_f": float(inputs[5][1].get()),
        "fuel_diluent": inputs[6][0].get(),
        "oxidizer": inputs[7][0].get(),
        "X_ox": float(inputs[8][1].get()),
        "oxidizer_diluent": inputs[9][0].get(),
        "fuel_shroud": inputs[10][0].get(),
        "oxidizer_shroud": inputs[11][0].get(),
        "shroud_momentum_fraction": float(inputs[12][1].get()),
    }

    cache_inputs(inp)

    out = calculate_slpm(inp)

    outputs[0][2].set(str(round(out["SLPM_ox_total"], 5)))
    outputs[1][2].set(str(round(out["SLPM_ox"], 5)))
    outputs[2][2].set(str(round(out["SLPM_ox_diluent"], 5)))
    outputs[3][2].set(str(round(out["SLPM_f_total"], 5)))
    outputs[4][2].set(str(round(out["SLPM_f"], 5)))
    outputs[5][2].set(str(round(out["SLPM_f_diluent"], 5)))
    outputs[6][2].set(str(round(out["SLPM_ox_shroud"], 5)))
    outputs[7][2].set(str(round(out["SLPM_f_shroud"], 5)))

    return 0


def run_console():
    if os.path.exists("counterflow.json"):
        with open("counterflow.json", "r") as f:
            inp = json.load(f)
    else:
        print("ERROR: No input file found! Please provide a counterflow.json file.")

    out = calculate_slpm(inp)

    pretty_out = json.dumps(out, indent=4)
    print(pretty_out)


def calculate_slpm(inp):
    # Burner geometry
    D_i = 0.0065
    A_i = D_i**2 * np.pi / 4
    A_o = np.pi * ((0.01495 / 2) ** 2 - (0.00726 / 2) ** 2)

    out = {}

    # Oxidizer side
    v_ox_total = inp["L"] * inp["a_g"] / 4
    vdot_ox_total = v_ox_total * A_i
    out["SLPM_ox_total"] = vdot_to_slpm(vdot_ox_total, inp["p"] * ATM_TO_PA, inp["T"])

    v_ox = v_ox_total * inp["X_ox"]
    v_ox_diluent = v_ox_total * (1 - inp["X_ox"])
    vdot_ox = v_ox * A_i
    vdot_ox_diluent = v_ox_diluent * A_i
    out["SLPM_ox"] = vdot_to_slpm(vdot_ox, inp["p"] * ATM_TO_PA, inp["T"])
    out["SLPM_ox_diluent"] = vdot_to_slpm(vdot_ox_diluent, inp["p"] * ATM_TO_PA, inp["T"])

    # Fuel side
    M_ox_total = inp["X_ox"] * M[inp["oxidizer"].lower()] + (1 - inp["X_ox"]) * M[inp["oxidizer_diluent"].lower()]
    M_f_total = inp["X_f"] * M[inp["fuel"].lower()] + (1 - inp["X_f"]) * M[inp["fuel_diluent"].lower()]
    rho_f_total = inp["p"] * ATM_TO_PA * M_f_total / R_U / inp["T"]
    rho_ox_total = inp["p"] * ATM_TO_PA * M_ox_total / R_U / inp["T"]
    v_f_total = v_ox_total * float(np.sqrt(rho_ox_total / rho_f_total))
    vdot_f_total = v_f_total * A_i
    out["SLPM_f_total"] = vdot_to_slpm(vdot_f_total, inp["p"] * ATM_TO_PA, inp["T"])

    v_f = v_f_total * inp["X_f"]
    v_f_diluent = v_f_total * (1 - inp["X_f"])
    vdot_f = v_f * A_i
    vdot_f_diluent = v_f_diluent * A_i
    out["SLPM_f"] = vdot_to_slpm(vdot_f, inp["p"] * ATM_TO_PA, inp["T"])
    out["SLPM_f_diluent"] = vdot_to_slpm(vdot_f_diluent, inp["p"] * ATM_TO_PA, inp["T"])

    # Shrouds
    M_ox_shroud = M[inp["oxidizer_shroud"].lower()]
    rho_ox_shroud = inp["p"] * ATM_TO_PA * M_ox_shroud / R_U / inp["T"]
    v_ox_shroud = v_ox_total * float(np.sqrt(inp["shroud_momentum_fraction"] * rho_ox_total / rho_ox_shroud))
    vdot_ox_shroud = v_ox_shroud * A_o
    out["SLPM_ox_shroud"] = vdot_to_slpm(vdot_ox_shroud, inp["p"] * ATM_TO_PA, inp["T"])

    M_f_shroud = M[inp["fuel_shroud"].lower()]
    rho_f_shroud = inp["p"] * ATM_TO_PA * M_f_shroud / R_U / inp["T"]
    v_f_shroud = v_ox_shroud * float(np.sqrt(rho_ox_shroud / rho_f_shroud))
    vdot_f_shroud = v_f_shroud * A_o
    out["SLPM_f_shroud"] = vdot_to_slpm(vdot_f_shroud, inp["p"] * ATM_TO_PA, inp["T"])

    return out


def vdot_to_slpm(vdot: float, p: float, T: float) -> float:
    T_ref = 300.0
    p_ref = 101325.0
    ndot = p * vdot / R_U / T
    return ndot * R_U * T_ref * M3_TO_L / p_ref / SEC_TO_MIN


if __name__ == "__main__":
    main()
