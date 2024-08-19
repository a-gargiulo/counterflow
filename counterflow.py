from typing import Dict
import sys

import numpy as np
import pprint
import tkinter as tk


atm2pa = 101325.0
sec2min = 1.0 / 60.0
mCubic2litre = 1000.0

R_u = 8.314
T_ref = 300.0
p_ref = 101325.0


# def M(element: str) -> float:
#     element = element.lower()
#     match element:
#         case "air":
#             return 28.9705e-3
#         case "ethylene":
#             return 28.05336e-3
#         case "nitrogen":
#             return 28.02e-3
#         case "oxygen":
#             return 31.998e-3


# def vdot2slpm_ig(Vdot: float, p: float, T: float) -> float:
#     ndot = p * Vdot / R_u / T
#     return ndot * R_u * T_ref * mCubic2litre / p_ref / sec2min


# def calculate_flow_rates(inp: Dict[str, float]) -> Dict[str, float]:
#     out = {}

#     out["v_ox_side"] = inp["L"] * inp["a_g"] / 4

#     A_i = inp["D_i"] ** 2 * np.pi / 4

#     # Oxidizer side flow (air + diluent)
#     Vdot_ox_side = out["v_ox_side"] * A_i
#     out["SLPM_ox_side"] = vdot2slpm_ig(Vdot_ox_side, inp["p"], inp["T"])

#     # Actual oxidizer flow
#     v_ox = out["v_ox_side"] * inp["X_ox"]
#     v_ox_dilut = out["v_ox_side"] * (1-inp["X_ox"])
#     Vdot_ox = v_ox * A_i
#     Vdot_ox_dilut = v_ox_dilut * A_i
#     out["SLPM_ox"] = vdot2slpm_ig(Vdot_ox, inp["p"], inp["T"])
#     out["SLPM_ox_dilut"] = vdot2slpm_ig(Vdot_ox_dilut, inp["p"], inp["T"])

#     # Fluel flow
#     if inp["X_ox"] == 0.21008 and inp["oxidizer_dilutant"].lower() == "nitrogen":
#         M_ox_side = M("air")
#     else:
#         M_ox_side = inp["X_ox"] * M(inp["oxidizer"]) + (
#             1 - inp["X_ox"]
#         ) * M(inp["oxidizer_dilutant"])

#     M_f_side = inp["X_f"] * M(inp["fuel"]) + (
#         1 - inp["X_f"]
#     ) * M(inp["fuel_dilutant"])

#     rho_f_side = inp["p"] / (R_u / M_f_side) / inp["T"]
#     rho_ox_side = inp["p"] / (R_u / M_ox_side) / inp["T"]

#     out["v_f_side"] = out["v_ox_side"] * float(np.sqrt(rho_ox_side / rho_f_side))
#     Vdot_f_side = out["v_f_side"] * A_i
#     out["SLPM_f_side"] = vdot2slpm_ig(Vdot_f_side, inp["p"], inp["T"])

#     v_f = out["v_f_side"] * inp["X_f"]
#     v_f_dilut = out["v_f_side"] * (1-inp["X_f"])
#     Vdot_f = v_f * A_i
#     Vdot_f_dilut = v_f_dilut * A_i
#     out["SLPM_f"] = vdot2slpm_ig(Vdot_f, inp["p"], inp["T"])
#     out["SLPM_f_dilut"] = vdot2slpm_ig(Vdot_f_dilut, inp["p"], inp["T"])



#     M_ox_shroud = M(inp["oxidizer_shroud"])
#     rho_ox_shroud = inp["p"] / (R_u / M_ox_shroud) / inp["T"]
#     v_ox_shroud = out["v_f_side"] * float(np.sqrt(rho_f_side / rho_ox_shroud))
#     A_o = np.pi * ((0.01495/2)**2-(0.00726/2)**2)
#     Vdot_ox_shroud = v_ox_shroud * A_o
#     out["SLPM_ox_shroud"] = vdot2slpm_ig(Vdot_ox_shroud, inp["p"], inp["T"])


#     return out


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--gui':
        run_gui()
    # else:
        # run_console()

# def resize_font(event, label):
    # Adjust font size based on window width
    # new_font_size = max(10, min(event.width // 20, 72))  # Example logic for resizing font
    # font = ("Arial", new_font_size)
    # label.config(font=font)

def run_gui():
    # Constants
    WIN_X = 800
    WIN_Y = 600

    root = tk.Tk()

    pos_x = root.winfo_screenwidth() // 2 - WIN_X // 2
    pos_y = root.winfo_screenheight() // 2 - WIN_Y // 2

    root.geometry(f"{WIN_X}x{WIN_Y}+{pos_x}+{pos_y}")

    root.title("RFL Counterflow Burner")
    
    inputs_label = tk.Label(root, text="Inputs:")
    inputs_label.grid(row=0, column=0, sticky="w")

    inputs_frame = tk.Frame(root, borderwidth=5, relief="ridge")
    inputs_frame.grid(row=1, column=0, sticky="ew")

    strain_label = tk.Label(inputs_frame, text="Strain Rate [1/s]:")
    strain_label.grid(row=0, column=0, sticky="w")
    strain_entry = tk.Entry(inputs_frame)
    strain_entry.grid(row=0, column=1, sticky="w")

    pressure_label = tk.Label(inputs_frame, text="Pressure [atm]:")
    pressure_label.grid(row=1, column=0, sticky="w")
    pressure_entry = tk.Entry(inputs_frame)
    pressure_entry.grid(row=1, column=1, sticky="w")


    # root.grid_columnconfigure(0, weight=1)
    # root.grid_rowconfigure(0, weight=0)


    # root.bind("<Configure>", resize_font)

    # root.bind("<Configure>", lambda event: resize_font(event, inputs_label))
    root.mainloop()






if __name__ == "__main__":
    main()
    # inputs = {
    #     "a_g": 363,
    #     "p": 4 * atm2pa,
    #     "T": 300,
    #     "fuel": "Ethylene",
    #     "fuel_dilutant": "Nitrogen",
    #     "fuel_shroud": "Nitrogen",
    #     "oxidizer": "Air",
    #     "oxidizer_dilutant": "Nitrogen",
    #     "oxidizer_shroud": "Nitrogen",
    #     "X_f": 0.6,
    #     "X_ox": 0.5,
    #     "L": 0.00545,
    #     "D_i": 0.0065,
    # }

    # result = calculate_flow_rates(inputs)
    # pprint.pprint(result)
