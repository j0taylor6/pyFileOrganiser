import logging
import os
import shutil
import json

logging.basicConfig(filename='fileOrganizer.log', level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def get_base_directories():
    # This function returns common base directories
    # Note: You might need to adjust these paths based on the operating system
    home_path = os.path.expanduser('~')
    return {
        'Desktop': os.path.join(home_path, 'Desktop'),
        'Downloads': os.path.join(home_path, 'Downloads'),
        'Documents': os.path.join(home_path, 'Documents'),
        'Music': os.path.join(home_path, 'Music'),
        'Pictures': os.path.join(home_path, 'Pictures'),
        'Videos': os.path.join(home_path, 'Videos')
    }


def choose_directory():
    base_dirs = get_base_directories()
    print("Choose a directory to organize:")
    for i, key in enumerate(base_dirs.keys()):
        print(f"{i + 1}. {key}")

    print(f"{len(base_dirs) + 1}. Enter a custom directory")
    choice = int(input("Enter your choice: "))

    if choice in range(1, len(base_dirs) + 1):
        return list(base_dirs.values())[choice - 1]
    elif choice == len(base_dirs) + 1:
        return input("Enter the path of the custom directory: ")
    else:
        print("Invalid choice. Exiting.")
        exit()


def load_extension_mapping():
    jsonFile = input("Enter the directory for the extension mapping JSON: ")
    try:
        with open(jsonFile, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Extension mapping file not found.")
        exit()
    except json.JSONDecodeError:
        print("Error reading the extension mapping file.")
        exit()


file_movements = []


def fileOrganizer(path):
    global file_movements
    # Dictionary mapping file extensions to directory names
    extension_mapping = load_extension_mapping()

    count_moved = 0
    count_skipped = 0
    count_errors = 0

    for filename in os.listdir(path):
        extension = filename.split('.')[-1].lower()

        if extension in extension_mapping:
            folder_name = extension_mapping[extension]
            folder_path = os.path.join(path, folder_name)

            try:
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    logging.info(f"Created folder: {folder_path}")

                original_file_path = os.path.join(path, filename)
                new_file_path = os.path.join(folder_path, filename)
                shutil.move(original_file_path, new_file_path)

                # Record the movement for undo feature
                file_movements.append((original_file_path, new_file_path))

                logging.info(f"Moved: {filename} to {folder_path}")
                count_moved += 1
            except Exception as e:
                logging.error(f"Failed to move {filename}: {e}")
                count_errors += 1
        else:
            logging.info(f"Skipped: {filename} (Unknown extension)")
            count_skipped += 1

    # Print the summary statistics
    logging.info(f"Summary: Files Moved: {count_moved}, Files Skipped: {count_skipped}, Errors: {count_errors}")
    print(f"Summary:\nFiles Moved: {count_moved}\nFiles Skipped: {count_skipped}\nErrors: {count_errors}")


def undoLastOrganization():
    global file_movements
    if not file_movements:
        print("No organization actions to undo.")
        return

    for original_path, new_path in reversed(file_movements):
        try:
            if os.path.exists(new_path):
                shutil.move(new_path, original_path)
                print(f"Moved back: {new_path} to {original_path}")
            else:
                print(f"File not found for undo: {new_path}")
        except Exception as e:
            print(f"Error during undo: {e}")


dir_to_organize = choose_directory()
fileOrganizer(dir_to_organize)

log_file_name = 'fileOrganizer.log'
log_file_path = os.path.abspath(log_file_name)
print(f"The log file is located at: {log_file_path}")

undo_confirmation = input("Do you want to undo the last organization? (yes/no): ")
if undo_confirmation.lower() == 'yes':
    undoLastOrganization()
