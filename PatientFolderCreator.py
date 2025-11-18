from pathlib import Path

def create_patient_folder():
    """prompt user for infomation and create folders on desktop"""

    #Get inputs
    print("Please input patient info below:")

    due_date = input("Enter Due date (format mm-dd-yy): ").strip()
    patient_name = input("Enter patient name: ").strip().upper()
    unique_id = input("Enter Unique ID: ").strip().upper()
    center_name = input("Enter Center Name: ").strip()
    is_ios = input("Is IOS? (Y/N): ").strip().upper()

    #replace hyphens with periods in duedate for folder creation
    due_date = due_date.replace("-", ".")

    #create the main folder name
    if is_ios:
        folder_name = f"{due_date} {patient_name} ({unique_id})- (ios) {center_name} Due {due_date} Hrx"
    else:
        folder_name = f"{due_date} {patient_name} ({unique_id})- {center_name} Due {due_date} Hrx"

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




