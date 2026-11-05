import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from src.src.generator import CHARACTER_TYPES, generate_password
    from src.src.password_store import PASSWORDS_FILE, save_password
    from src.src.strength import (
        check_common_password,
        estimate_crack_time,
        password_strength,
    )
else:
    from .generator import CHARACTER_TYPES, generate_password
    from .password_store import PASSWORDS_FILE, save_password
    from .strength import check_common_password, estimate_crack_time, password_strength


class PasswordApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("560x740")
        self.root.minsize(500, 680)
        self._configure_style()

        self.length = tk.StringVar(value="20")
        self.profile = tk.StringVar(value="Strong - 20 characters")
        self.password = tk.StringVar()
        self.app_or_site = tk.StringVar()
        self.show_password = tk.BooleanVar(value=True)
        self.character_type_vars = {
            choice: tk.BooleanVar(value=True) for choice in CHARACTER_TYPES
        }

        self._build_ui()
        self.length.trace_add("write", self._sync_profile)
        self.password.trace_add("write", self._update_strength)
        self.root.bind("<Return>", lambda _event: self.generate())

    def _configure_style(self) -> None:
        style = ttk.Style(self.root)
        for theme in ("vista", "xpnative"):
            if theme in style.theme_names():
                style.theme_use(theme)
                break

        background = "#f3f6fa"
        style.configure(".", font=("Segoe UI", 10))
        style.configure("TFrame", background=background)
        style.configure("TLabel", background=background, foreground="#263445")
        style.configure("Title.TLabel", font=("Segoe UI", 21, "bold"), foreground="#17365d")
        style.configure("Subtitle.TLabel", foreground="#536579")
        style.configure("Section.TLabelframe", padding=14)
        style.configure(
            "Section.TLabelframe.Label",
            font=("Segoe UI", 10, "bold"),
            foreground="#17365d",
        )
        style.configure("TButton", padding=(12, 8))
        style.configure("Generate.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Strength.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("Estimate.TLabel", font=("Segoe UI", 10, "bold"))

    def _build_ui(self) -> None:
        content = ttk.Frame(self.root, padding=(28, 24))
        content.pack(fill="both", expand=True)

        ttk.Label(content, text="Password Generator", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            content,
            text="Create a strong password and review its estimated strength.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(4, 18))

        options = ttk.LabelFrame(
            content, text="Password options", style="Section.TLabelframe"
        )
        options.pack(fill="x")

        length_row = ttk.Frame(options)
        length_row.pack(fill="x", pady=(0, 12))
        ttk.Label(length_row, text="Length").grid(row=0, column=0, sticky="w")
        ttk.Spinbox(
            length_row,
            from_=1,
            to=128,
            textvariable=self.length,
            width=8,
            justify="center",
        ).grid(row=0, column=1, padx=(12, 20))
        ttk.Label(length_row, text="Quick choice").grid(row=0, column=2, sticky="w")
        self.profile_combo = ttk.Combobox(
            length_row,
            textvariable=self.profile,
            values=(
                "Balanced - 16 characters",
                "Strong - 20 characters",
                "Very strong - 24 characters",
                "Custom",
            ),
            state="readonly",
            width=25,
        )
        self.profile_combo.grid(row=0, column=3, sticky="ew", padx=(8, 0))
        self.profile_combo.bind("<<ComboboxSelected>>", self._apply_profile)
        length_row.columnconfigure(3, weight=1)
        ttk.Label(
            options,
            text="Choose a preset or enter any length from 1 to 128.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(0, 12))

        types_row = ttk.Frame(options)
        types_row.pack(fill="x")
        for choice, (name, _characters) in CHARACTER_TYPES.items():
            ttk.Checkbutton(
                types_row,
                text=name.title(),
                variable=self.character_type_vars[choice],
            ).pack(side="left", padx=(0, 12))

        ttk.Button(
            content,
            text="Generate password",
            style="Generate.TButton",
            command=self.generate,
        ).pack(fill="x", pady=(16, 14))

        password_frame = ttk.LabelFrame(
            content, text="Password", style="Section.TLabelframe"
        )
        password_frame.pack(fill="x")

        password_row = ttk.Frame(password_frame)
        password_row.pack(fill="x")
        self.password_entry = ttk.Entry(
            password_row,
            textvariable=self.password,
            show="",
            font=("Consolas", 13),
        )
        self.password_entry.pack(side="left", fill="x", expand=True)
        ttk.Checkbutton(
            password_row, text="Show", variable=self.show_password, command=self._toggle
        ).pack(side="left", padx=(8, 0))

        save_row = ttk.Frame(password_frame)
        save_row.pack(fill="x", pady=(12, 0))
        ttk.Label(save_row, text="App or site").pack(side="left")
        ttk.Entry(save_row, textvariable=self.app_or_site).pack(
            side="left", fill="x", expand=True, padx=(10, 10)
        )
        ttk.Button(save_row, text="Save password", command=self.save_current_password).pack(
            side="left"
        )

        actions = ttk.Frame(password_frame)
        actions.pack(fill="x", pady=(10, 0))
        ttk.Button(actions, text="Copy password", command=self.copy_password).pack(
            side="left"
        )
        ttk.Label(
            password_frame,
            text=(
                f"Saved in readable plain text at:\n{PASSWORDS_FILE}\n"
                "Anyone with access to this file can read the saved passwords."
            ),
            wraplength=480,
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(10, 0))

        result = ttk.Frame(content, padding=(2, 14, 2, 0))
        result.pack(fill="x")
        self.strength_label = ttk.Label(
            result, text="Strength: —", style="Strength.TLabel"
        )
        self.strength_label.pack(anchor="w")
        self.estimate_label = ttk.Label(
            result, text="Estimated offline cracking time: —", style="Estimate.TLabel"
        )
        self.estimate_label.pack(anchor="w", pady=(7, 0))
        self.warning_label = ttk.Label(
            result, text="", wraplength=490, style="Subtitle.TLabel"
        )
        self.warning_label.pack(anchor="w", pady=(8, 0))
        ttk.Label(
            result,
            text=(
                "Estimate assumes random characters and 10 billion guesses/second. "
                "Real attack speeds and human patterns vary widely."
            ),
            wraplength=490,
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(8, 0))

    def _apply_profile(self, _event: tk.Event) -> None:
        profile_lengths = {
            "Balanced - 16 characters": 16,
            "Strong - 20 characters": 20,
            "Very strong - 24 characters": 24,
        }
        selected_length = profile_lengths.get(self.profile.get())
        if selected_length is not None:
            self.length.set(str(selected_length))

    def _sync_profile(self, *_args: str) -> None:
        profile_lengths = {
            "16": "Balanced - 16 characters",
            "20": "Strong - 20 characters",
            "24": "Very strong - 24 characters",
        }
        self.profile.set(profile_lengths.get(self.length.get(), "Custom"))

    def generate(self) -> None:
        try:
            length = int(self.length.get())
        except ValueError:
            messagebox.showerror("Invalid length", "Enter a whole-number password length.")
            return
        if not 1 <= length <= 128:
            messagebox.showerror("Invalid length", "Choose a length from 1 to 128.")
            return

        choices = [
            choice
            for choice, selected in self.character_type_vars.items()
            if selected.get()
        ]
        try:
            self.password.set(generate_password(length, choices))
        except ValueError as error:
            messagebox.showerror("Cannot generate password", str(error))

    def copy_password(self) -> None:
        password = self.password.get()
        if not password:
            messagebox.showinfo("Nothing to copy", "Generate or enter a password first.")
            return

        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
        except tk.TclError as error:
            messagebox.showerror("Copy failed", f"Could not access the clipboard: {error}")
            return
        messagebox.showinfo("Copied", "Password copied to the clipboard.")

    def save_current_password(self) -> None:
        try:
            path = save_password(self.app_or_site.get(), self.password.get())
        except ValueError as error:
            messagebox.showerror("Cannot save password", str(error))
            return
        except OSError as error:
            messagebox.showerror(
                "Save failed",
                f"Could not write the password file:\n{error}",
            )
            return

        messagebox.showinfo(
            "Password saved",
            f"Saved the password for {self.app_or_site.get().strip()} to:\n{path}",
        )

    def _toggle(self) -> None:
        self.password_entry.configure(show="" if self.show_password.get() else "•")

    def _update_strength(self, *_args: str) -> None:
        password = self.password.get()
        if not password:
            self.strength_label.configure(text="Strength: —")
            self.estimate_label.configure(text="Estimated offline cracking time: —")
            self.warning_label.configure(text="")
            return

        strength = password_strength(password)
        self.strength_label.configure(text=f"Strength: {strength}")
        estimate = estimate_crack_time(password)
        self.estimate_label.configure(
            text=f"Estimated offline cracking time: {estimate}"
        )
        if check_common_password(password):
            self.warning_label.configure(
                text="Warning: This password is on the common-password list."
            )
        else:
            self.warning_label.configure(text="")


def main() -> None:
    root = tk.Tk()
    PasswordApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()