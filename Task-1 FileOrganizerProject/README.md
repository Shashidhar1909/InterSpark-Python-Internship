# Python File Automation Script

## Project Title
File Automation Script using Python

## Objective
This project automates common file operations such as renaming, sorting, and cleaning files inside a folder.

## Features
- Rename files by adding a prefix
- Sort files into folders by extension
- Remove empty files
- Display files in a folder
- Handle invalid input safely
- Generate logs for every operation

## Technologies Used
- Python
- `os` module
- `shutil` module
- `logging` module
- Exception handling

## How to Run
1. Open the project folder in VS Code or any Python IDE.
2. Open terminal in the project directory.
3. Run the script:

```bash
python main.py
```

4. Enter the folder path where your files are located.
5. Choose an operation from the menu.

## Example Input
- Folder path: `C:\Users\YourName\Desktop\sample_files`
- Choice: `2` (Sort files by extension)

## Example Output
```text
Moved: report.pdf -> PDF/
Moved: notes.txt -> TXT/
Moved: image.jpg -> JPG/
Clean-up complete. Removed 1 empty file(s).
```

## Log File
All operations are saved in:
`logs/operations.log`

## Sample Use Case
Suppose a folder contains:
- `report.pdf`
- `notes.txt`
- `photo.jpg`
- `empty.txt`

After using the script:
- Files are sorted into extension folders
- Empty files can be deleted
- Files can be renamed with a prefix

## Deliverables for Internship
- Source code
- Sample input/output
- README file
- GitHub repository link
