# GUI.py
from __future__ import annotations

import threading
import traceback
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from geometry.random_airfoil_generator import generator
from simulation.Openfoam import OpenFoam


def parse_angles(text: str) -> list[float]:
    """
    Parse angles from a string like:
      "0, 5, 10" or "0 5 10" or "0;5;10"
    Returns list[float].
    """
    if not text.strip():
        return []

    # Normalize separators to spaces
    normalized = (
        text.replace(",", " ")
            .replace(";", " ")
            .replace("\t", " ")
            .strip()
    )
    parts = [p for p in normalized.split(" ") if p.strip()]

    angles: list[float] = []
    for p in parts:
        angles.append(float(p))
    return angles


class AirfoilGeneratorGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Random Airfoil Generator (NACA 4-digit) — GUI")
        self.geometry("820x520")
        self.minsize(760, 480)

        # State
        self.base_dir_var = tk.StringVar(value="")
        self.origin_dir_var = tk.StringVar(value="")
        self.n_var = tk.StringVar(value="10")
        self.angles_var = tk.StringVar(
            value="0,45,90,135,180,225,270,315"
        )

        self._build_layout()

    def _build_layout(self) -> None:
        # --- Top frame: directories
        frm_dirs = tk.LabelFrame(self, text="Directories", padx=10, pady=10)
        frm_dirs.pack(fill="x", padx=10, pady=10)

        # Base
        tk.Label(frm_dirs, text="Base directory:").grid(row=0, column=0, sticky="w")
        ent_base = tk.Entry(frm_dirs, textvariable=self.base_dir_var, width=80)
        ent_base.grid(row=0, column=1, sticky="we", padx=(8, 8))
        tk.Button(frm_dirs, text="Browse...", command=self._browse_base).grid(row=0, column=2)

        # Origin
        tk.Label(frm_dirs, text="Origin (template) directory:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        ent_origin = tk.Entry(frm_dirs, textvariable=self.origin_dir_var, width=80)
        ent_origin.grid(row=1, column=1, sticky="we", padx=(8, 8), pady=(8, 0))
        tk.Button(frm_dirs, text="Browse...", command=self._browse_origin).grid(row=1, column=2, pady=(8, 0))

        frm_dirs.grid_columnconfigure(1, weight=1)

        # --- Middle frame: parameters
        frm_params = tk.LabelFrame(self, text="Parameters", padx=10, pady=10)
        frm_params.pack(fill="x", padx=10, pady=(0, 10))

        tk.Label(frm_params, text="N (airfoils):").grid(row=0, column=0, sticky="w")
        tk.Entry(frm_params, textvariable=self.n_var, width=12).grid(row=0, column=1, sticky="w", padx=(8, 20))

        tk.Label(frm_params, text="Angles (deg):").grid(row=0, column=2, sticky="w")
        tk.Entry(frm_params, textvariable=self.angles_var, width=40).grid(row=0, column=3, sticky="w", padx=(8, 0))
        tk.Label(
            frm_params,
            text='Example: "0, 5, 10"'
        ).grid(row=1, column=3, sticky="w", padx=(8, 0), pady=(4, 0))

        # --- Buttons
        frm_actions = tk.Frame(self)
        frm_actions.pack(fill="x", padx=10, pady=(0, 10))

        self.btn_run = tk.Button(frm_actions, text="Run generator", command=self._on_run, height=1)
        self.btn_run.pack(side="left")

        self.btn_foam = tk.Button(frm_actions, text="Run OpenFOAM", command=self._on_run_foam, height=1)
        self.btn_foam.pack(side="left", padx=(10, 0))

        tk.Button(frm_actions, text="Clear log", command=self._clear_log).pack(side="left", padx=(10, 0))

        # --- Log
        frm_log = tk.LabelFrame(self, text="Log", padx=10, pady=10)
        frm_log.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.log = scrolledtext.ScrolledText(frm_log, wrap="word", height=12)
        self.log.pack(fill="both", expand=True)

        self._log_line("Ready. Select Base and Origin directories, set N and angles, then Run.")

    def _browse_base(self) -> None:
        d = filedialog.askdirectory(title="Select base directory")
        if d:
            self.base_dir_var.set(d)

    def _browse_origin(self) -> None:
        d = filedialog.askdirectory(title="Select origin (template) directory")
        if d:
            self.origin_dir_var.set(d)

    def _clear_log(self) -> None:
        self.log.delete("1.0", tk.END)

    def _log_line(self, msg: str) -> None:
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
        self.update_idletasks()

    def _validate_inputs(self) -> tuple[int, list[float], Path, Path]:
        base_str = self.base_dir_var.get().strip()
        origin_str = self.origin_dir_var.get().strip()
        n_str = self.n_var.get().strip()
        angles_str = self.angles_var.get().strip()

        if not base_str:
            raise ValueError("Base directory is empty.")
        if not origin_str:
            raise ValueError("Origin directory is empty.")

        base = Path(base_str).expanduser().resolve()
        origin = Path(origin_str).expanduser().resolve()

        if not origin.exists():
            raise FileNotFoundError(f"Origin directory does not exist: {origin}")
        if not origin.is_dir():
            raise NotADirectoryError(f"Origin is not a directory: {origin}")

        try:
            n = int(n_str)
        except ValueError as e:
            raise ValueError("N must be an integer.") from e
        if n <= 0:
            raise ValueError("N must be > 0.")

        try:
            angles = parse_angles(angles_str)
        except ValueError as e:
            raise ValueError('Angles must be numbers, e.g. "0, 5, 10".') from e
        if len(angles) == 0:
            raise ValueError("Please provide at least one angle.")

        return n, angles, base, origin

    def _set_running(self, running: bool) -> None:
        state = "disabled" if running else "normal"
        self.btn_run.config(state=state)
        self.btn_foam.config(state=state)

    def _log_line_threadsafe(self, msg: str) -> None:
        # asegura que el log se actualiza en el hilo de Tkinter
        self.after(0, lambda: self._log_line(msg))

    # --------------------
    # DATA GENERATOR
    # -------------------- 

    def _on_run(self) -> None:
        try:
            n, angles, base, origin = self._validate_inputs()
        except Exception as e:
            messagebox.showerror("Input error", str(e))
            return

        self._set_running(True)
        self._log_line("------------------------------------------------------------")
        self._log_line(f"Starting generator:")
        self._log_line(f"  N      : {n}")
        self._log_line(f"  angles : {angles}")
        self._log_line(f"  base   : {base}")
        self._log_line(f"  origin : {origin}")
        self._log_line("------------------------------------------------------------")

        t = threading.Thread(
            target=self._run_generator_thread,
            args=(n, angles, base, origin),
            daemon=True
        )
        t.start()

    def _run_generator_thread(self, n: int, angles: list[float], base: Path, origin: Path) -> None:
        try:
            generator(N=n, angles=angles, base=base, origin=origin)
            self._log_line("✅ Done.")
        except Exception:
            self._log_line("❌ Error while running generator:")
            self._log_line(traceback.format_exc())
            messagebox.showerror("Execution error", "Generator failed. Check the log for details.")
        finally:
            # switch back to UI thread
            self.after(0, lambda: self._set_running(False))
    
    # --------------------
    # OPENFOAM
    # --------------------

    def _on_run_foam(self) -> None:
        base_str = self.base_dir_var.get().strip()
        if not base_str:
            messagebox.showerror("Input error", "Base directory is empty.")
            return

        base = Path(base_str).expanduser().resolve()
        if not base.exists() or not base.is_dir():
            messagebox.showerror("Input error", f"Base is not a valid directory:\n{base}")
            return

        self._set_running(True)
        self._log_line("------------------------------------------------------------")
        self._log_line("Starting OpenFOAM simulation:")
        self._log_line(f"  base   : {base}")
        self._log_line("------------------------------------------------------------")

        t = threading.Thread(
            target=self._run_foam_thread,
            args=(base,),
            daemon=True
        )
        t.start()

    def _run_foam_thread(self, base: Path) -> None:
        try:
            foam = OpenFoam(base)
            elapsed = foam.simulate()
            self._log_line_threadsafe(f"✅ OpenFOAM done. Execution time: {elapsed:.2f} s")
        except Exception:
            self._log_line_threadsafe("❌ Error while running OpenFOAM:")
            self._log_line_threadsafe(traceback.format_exc())
            self.after(0, lambda: messagebox.showerror("Execution error", "OpenFOAM failed. Check the log for details."))
        finally:
            self.after(0, lambda: self._set_running(False))


if __name__ == "__main__":
    app = AirfoilGeneratorGUI()
    app.mainloop()
