
# Python File Organiser

This project is a Python script for organizing files in a user-specified directory. It categorizes files based on their extensions, using a user-provided JSON mapping of extensions to folder names. The script includes features like logging actions to a file, creating necessary directories, and an undo function to revert the last organization. It handles errors and skips unknown file types, providing a summary of its actions.

## Features

- **Directory Selection:** Users can choose from common directories like Desktop, Downloads, Documents, Music, Pictures, and Videos, or specify a custom directory.
- **Extension-Based Organization:** The script organizes files based on their extensions, which are defined in an external JSON file. Users must provide the path to this JSON file.
- **Logging:** All actions (file movements, errors, skipped files) are logged to fileOrganizer.log, providing a detailed record of the script's activity.
- **Dynamic Folder Creation:** If a folder for a specific file type doesn't exist, the script creates it automatically.
- **File Movement Tracking:** The script records each file movement, allowing for an undo operation.
- **Undo Feature:** Users have the option to undo the last organization, moving files back to their original locations.
- **Error Handling:** The script logs errors, such as issues in moving files or reading the extension mapping file, and skips files with unknown extensions.
- **Summary Statistics:** After organizing, it provides a summary of the number of files moved, skipped, and errors encountered.

## License

[MIT](https://choosealicense.com/licenses/mit/)

