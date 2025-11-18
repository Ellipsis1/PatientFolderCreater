from pathlib import Path

def get_patient_data_massinput():
    print("Paste all input from HopeRx, then press Enter a few times: ")

    lines = []
    empty_count = 0

    while empty_count < 2:
        line = input()
        if line.strip() == "":
            empty_count += 1
        else:
            empty_count = 0
            lines.append(line.strip())

    # filter to only non-empty lines
    lines = [line for line in lines if line]

    print(f"\nReceived {len(lines)} lines of data.")

    due_date = None
    center_name = None
    patient_line = None

    for i, line in enumerate(lines):
        #first line with / is due date
        if '/' in line and not due_date:
            # replace slashes with periods in duedate for folder creation
            due_date = line.replace("/", ".")
        # last line is patient name and id
        elif i == len(lines) - 1:
            patient_line = line.upper()

        elif line.isalpha() or (line[0].isupper()):  # Single word, capitalized = center
            center_name = line


    if patient_line:
        patient_parts = patient_line.strip().split()
        if len(patient_parts) >= 2:
            unique_id = patient_parts[-1]  # last element is ID
            patient_name = " ".join(patient_parts[:-1])  # everything else is the name
        else:
            patient_name = patient_line.strip()
            unique_id = "UNKNOWN"

    is_ios = input("Is IOS? (Y/N): ").strip().lower()

    #create the main folder name
    if is_ios == 'y':
        folder = f"{due_date} {patient_name} ({unique_id}) (ios) {center_name} Due {due_date} Hrx"
    else:
        folder = f"{due_date} {patient_name} ({unique_id}) {center_name} Due {due_date} Hrx"

    return folder

def get_patient_data_lineinput():
    print("Please input patient info below:")


    due_date = input("Enter Due date (format mm-dd-yy): ").strip()
    patient_name = input("Enter patient name: ").strip().upper()
    unique_id = input("Enter Unique ID: ").strip().upper()
    center_name = input("Enter Center Name: ").strip()
    is_ios = input("Is IOS? (Y/N): ").strip().lower()

    #replace hyphens with periods in duedate for folder creation
    due_date = due_date.replace("-", ".")

    #create the main folder name
    if is_ios == 'y':
        folder = f"{due_date} {patient_name} ({unique_id}) (ios) {center_name} Due {due_date} Hrx"
    else:
        folder = f"{due_date} {patient_name} ({unique_id}) {center_name} Due {due_date} Hrx"

    return folder

def create_patient_folder():
    """prompt user for infomation and create folders on desktop"""

    #Get inputs either as one mass input or individual
    input_type = input("Paste direct from HopeRx? (Y/N)").strip().lower()

    if input_type == "y":
        folder_name = get_patient_data_massinput()
    else:
        folder_name = get_patient_data_lineinput()


    #get desktop path and create full path
    desktop = Path.home() / "Desktop"
    main_folder_path = desktop / folder_name

    #create main folder and subfolders
    try:
        #create main folder
        main_folder_path.mkdir(exist_ok=True)
        print(f"Created folder: {folder_name}")

        #create subfolders
        subfolders = ["Design Files", "Design Screenshots", "STL"]
        for subfolder in subfolders:
            subfolder_path = main_folder_path / subfolder
            subfolder_path.mkdir(exist_ok=True)
            print(f"Created folder: {subfolder_path}")

        print(f"Folder structure successfully created at: {main_folder_path}")

    except Exception as e:
        print(f"\nError creating folder: {e}")

if __name__ == "__main__":
    while True:
        create_patient_folder()

        #ask if user wants to run again
        run_again = input("Do you want to run again? (y/n): ").strip().lower()

        if run_again != 'y':
            break

        print("\n" + "="*30 + "\n")




