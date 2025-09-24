import subprocess
import threading
import os
import time


def execute_audio2face_threaded():
    """Launch Audio2Face in a separate thread to avoid blocking Unreal Engine."""

    def run_batch_file():
        """Run the Audio2Face batch file without blocking execution."""
        bat_file_path = (
            r"C:\Users\EjadaAi\AppData\Local\ov\pkg\audio2face-2023.2.0\audio2face_headless.bat"
        )

        if not os.path.exists(bat_file_path):
            print(f"[ERROR] Batch file not found: {bat_file_path}")
            return False

        try:
            print(f"[INFO] Executing: {bat_file_path}")

            process = subprocess.Popen(
                [bat_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True,
            )

            print("[INFO] Audio2Face batch file started in background")
            print(f"[INFO] Process ID: {process.pid}")

            return True

        except Exception as e:
            print(f"[ERROR] Failed to start Audio2Face: {e}")
            return False

    thread = threading.Thread(target=run_batch_file, daemon=True)
    thread.start()
    print("[INFO] Audio2Face execution started in background thread")


def execute_audio2face_blocking():
    """Launch Audio2Face and wait until it finishes (blocking execution)."""
    bat_file_path = (
        r"C:\Users\EjadaAi\AppData\Local\ov\pkg\audio2face-2023.2.0\audio2face_headless.bat"
    )

    if not os.path.exists(bat_file_path):
        print(f"[ERROR] Batch file not found: {bat_file_path}")
        return False

    try:
        print(f"[INFO] Executing: {bat_file_path}")

        result = subprocess.run(
            [bat_file_path], capture_output=True, text=True, shell=True
        )

        if result.stdout:
            print("[OUTPUT]")
            print(result.stdout)

        if result.stderr:
            print("[ERROR OUTPUT]")
            print(result.stderr)

        if result.returncode == 0:
            print("[INFO] Batch file executed successfully")
            return True
        else:
            print(f"[ERROR] Execution failed with return code: {result.returncode}")
            return False

    except Exception as e:
        print(f"[ERROR] Failed to execute Audio2Face: {e}")
        return False


def execute_audio2face():
    """Default entry point — uses threaded execution for Unreal Engine."""
    return execute_audio2face_threaded()


if __name__ == "__main__":
    execute_audio2face()

    # Delay to ensure Audio2Face is initialized before running set_a2f.py
    time.sleep(3)