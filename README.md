# Password Generator

A Windows-style desktop app for generating passwords, checking their estimated
strength, and optionally saving them with an app or site name.

## Features

- Generate passwords using letters, digits, punctuation, or any combination.
- Include at least one character from every selected character type.
- Choose a preset length or enter a custom length from 1 to 128 characters.
- Check the strength of a generated or manually entered password.
- Show an approximate offline brute-force time.
- Reveal or mask the password and copy it to the clipboard.
- Optionally save a password with its app or site name in a local text file.

## Requirements

- Windows
- Python 3.9 or later with Tkinter available

The app uses only Python's standard library; no third-party packages are
required.

## Run the app

Open PowerShell in the project folder and run:

```powershell
python src\src\main.py
```

If `python` is not recognized, try `py src\src\main.py` or install Python and
ensure the Python launcher is available.

## Use

1. Choose a preset or enter a password length from 1 to 128.
2. Select one or more character types: letters, digits, and/or punctuation.
3. Select **Generate password**. The app creates a password and displays its
   strength and estimated cracking time.
4. Optionally edit the password field to check another password, toggle
   **Show**, or select **Copy password**.
5. To save it, enter the app or site name and select **Save password**.

The selected password length must be at least the number of selected character
types, so every selected type can be included.

## Password storage warning

Saving is optional. When you select **Save password**, the app appends one JSON
record per line to:

```text
saved_passwords\passwords.txt
```

This file is **unencrypted plain text**. Anyone who can access the file, the
project folder, or a copy or backup of it can read the saved passwords. The
`saved_passwords` folder is listed in `.gitignore` to help prevent accidental
Git commits, but this does not protect the file on your computer. For real
credentials, use a reputable encrypted password manager instead.

Copied passwords may also remain in the system clipboard or clipboard history.

## Strength and cracking-time estimates

The strength label is a simple heuristic based on password length and whether
it contains uppercase letters, lowercase letters, digits, and punctuation. It
is not a security audit. The app also warns when a password matches its small,
built-in common-password list; not appearing on that list does not mean a
password is safe.

The cracking-time estimate assumes a random password and 10 billion guesses per
second, and estimates the average search time. Actual attack speeds vary, and
human-chosen passwords or reused passwords can be much easier to guess. Treat
the estimate as illustrative, not a guarantee.

## Development and testing

There is currently no automated test suite or separate build/install step.
The application can be launched directly with the command above.

## License

No license has been specified.
