import json
import os
from set_a2f import client


CONFIG_FILE = os.path.join(
    r"D:\Unreal Projects\AvatarCPP7\Scripts", "audio_config.json"
)


def load_audio_config(config_file=CONFIG_FILE):
    """Load audio configuration JSON and return the file path."""
    with open(config_file, "r") as f:
        data = json.load(f)
    return data.get("filePath")


def play_audio(file_path):
    """Play the given audio file with Audio2Face client."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Playing: {file_path}")
    filename = os.path.basename(file_path)

    client.set_track(client.players_available, filename)
    print("Playing track...")
    client.play_track(client.players_available)


def play_saved_audio():
    """Main wrapper: load audio config and play track in Audio2Face."""
    try:
        selected_file = load_audio_config()
        if not selected_file:
            raise KeyError("filePath not found in config")

        play_audio(selected_file)

    except FileNotFoundError:
        print("No audio file selected yet. Please run file_browser.py first.")
    except KeyError as e:
        print(f"Invalid config file (missing {e}). Please run file_browser.py.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    play_saved_audio()
