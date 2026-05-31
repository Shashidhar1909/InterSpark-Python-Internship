import os
import shutil
import logging
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "operations.log")


def setup_logging() -> None:
    """Create log directory and configure logging."""
    os.makedirs(LOG_DIR, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def list_files(folder_path: str) -> list[str]:
    """Return a list of files (not folders) in the given directory."""
    return [
        item for item in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, item))
    ]


def rename_files(folder_path: str, prefix: str) -> None:
    """Rename all files in a folder by adding a prefix."""
    files = list_files(folder_path)
    if not files:
        print("No files found to rename.")
        logging.info("No files found to rename in %s", folder_path)
        return

    for filename in files:
        old_path = os.path.join(folder_path, filename)
        new_name = f"{prefix}{filename}"
        new_path = os.path.join(folder_path, new_name)

        # Avoid overwriting an existing file
        counter = 1
        name, ext = os.path.splitext(new_name)
        while os.path.exists(new_path):
            new_name = f"{name}_{counter}{ext}"
            new_path = os.path.join(folder_path, new_name)
            counter += 1

        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")
        logging.info("Renamed file '%s' to '%s'", filename, new_name)


def sort_files_by_extension(folder_path: str) -> None:
    """Move files into folders based on extension."""
    files = list_files(folder_path)
    if not files:
        print("No files found to sort.")
        logging.info("No files found to sort in %s", folder_path)
        return

    for filename in files:
        source_path = os.path.join(folder_path, filename)
        _, ext = os.path.splitext(filename)
        ext = ext.lower().lstrip(".") or "no_extension"

        destination_folder = os.path.join(folder_path, ext.upper())
        os.makedirs(destination_folder, exist_ok=True)

        destination_path = os.path.join(destination_folder, filename)

        counter = 1
        name, extension = os.path.splitext(filename)
        while os.path.exists(destination_path):
            destination_path = os.path.join(
                destination_folder, f"{name}_{counter}{extension}"
            )
            counter += 1

        shutil.move(source_path, destination_path)
        print(f"Moved: {filename} -> {ext.upper()}/")
        logging.info("Moved file '%s' to folder '%s'", filename, destination_folder)


def remove_empty_files(folder_path: str) -> None:
    """Delete empty files in the folder."""
    files = list_files(folder_path)
    if not files:
        print("No files found to clean.")
        logging.info("No files found to clean in %s", folder_path)
        return

    removed = 0
    for filename in files:
        path = os.path.join(folder_path, filename)
        try:
            if os.path.getsize(path) == 0:
                os.remove(path)
                removed += 1
                print(f"Deleted empty file: {filename}")
                logging.info("Deleted empty file '%s'", filename)
        except OSError as exc:
            logging.error("Error reading file '%s': %s", filename, exc)
            print(f"Could not process {filename}: {exc}")

    print(f"Clean-up complete. Removed {removed} empty file(s).")
    logging.info("Clean-up complete. Removed %d empty file(s).", removed)


def show_menu() -> None:
    print("\n=== Python File Automation Script ===")
    print("1. Rename files with prefix")
    print("2. Sort files by extension")
    print("3. Remove empty files")
    print("4. Show files in folder")
    print("5. Exit")


def show_files(folder_path: str) -> None:
    files = list_files(folder_path)
    if not files:
        print("No files found.")
        logging.info("No files found in %s", folder_path)
        return

    print("\nFiles in folder:")
    for file in files:
        print(f"- {file}")
    logging.info("Listed %d file(s) in %s", len(files), folder_path)


def main() -> None:
    setup_logging()
    logging.info("Program started")

    print("File Automation Project")
    print("This tool can rename, sort, and clean files using the os module.\n")

    try:
        folder_path = input("Enter folder path: ").strip()

        if not folder_path:
            raise ValueError("Folder path cannot be empty.")

        if not os.path.exists(folder_path):
            raise FileNotFoundError("The given folder does not exist.")

        if not os.path.isdir(folder_path):
            raise NotADirectoryError("The given path is not a folder.")

        while True:
            show_menu()
            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                prefix = input("Enter prefix for new file names: ").strip()
                if not prefix:
                    print("Prefix cannot be empty.")
                    continue
                rename_files(folder_path, prefix)

            elif choice == "2":
                sort_files_by_extension(folder_path)

            elif choice == "3":
                remove_empty_files(folder_path)

            elif choice == "4":
                show_files(folder_path)

            elif choice == "5":
                print("Exiting program.")
                logging.info("Program exited by user")
                break

            else:
                print("Invalid choice. Please select a number between 1 and 5.")

    except Exception as exc:
        logging.exception("Unhandled error: %s", exc)
        print(f"Error: {exc}")

    finally:
        logging.info("Program ended")


if __name__ == "__main__":
    main()
