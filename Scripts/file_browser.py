import tkinter as tk
from tkinter import filedialog
import json
import os


def browse_wav_file(config_file="audio_config.json"):
    """
    Open a file dialog to select a WAV file and save the path to a JSON config file.

    Args:
        config_file (str): Path to the JSON file where the selected audio path will be saved.

    Returns:
        str | None: The selected file path, or None if no file was selected.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(
        title="Select a WAV audio file",
        initialdir="D:/",
        filetypes=[
            ("WAV files", "*.wav"),
            ("All files", "*.*")
        ]
    )

    root.destroy()

    if file_path:
        data = {"filePath": file_path}  # Match the key expected in your other script
        with open(config_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Selected and saved: {file_path}")
        return file_path

    print("No file selected")
    return None


if __name__ == "__main__":
    browse_wav_file()
