import datetime
import os

# --- Configuration ---
# Use a simple text file to store all readings. Each reading is one line.
DATA_FILE = 'bp_readings.txt'

# --- Functional Module 1: Classification Logic ---

def classify_reading(sys, dia):
    """
    Classifies the blood pressure reading based on standard guidelines.
    This logic fulfills a core functional module requirement.
    """
    if sys < 120 and dia < 80:
        return "Normal"
    elif 120 <= sys <= 129 and dia < 80:
        return "Elevated"
    elif 130 <= sys <= 139 or 80 <= dia <= 89:
        return "Hypertension Stage 1"
    elif sys >= 140 or dia >= 90:
        return "Hypertension Stage 2"
    else:
        # Should not be reached if validation works, but included for completeness.
        return "Unclassified (Error)"

# --- Helper Function: Get All Readings ---

def get_all_readings():
    """
    Reads all data from the text file into a list of lists (table format).
    Returns an empty list if the file is missing or empty.
    """
    if not os.path.exists(DATA_FILE):
        return []

    readings = []
    try:
        with open(DATA_FILE, mode='r') as file:
            for line in file:
                # Add the original line (used for deleting) and the parsed fields
                line_content = line.strip()
                fields = line_content.split(',')
                if len(fields) == 5:
                    # Storing the original line content is crucial for rewriting the file later
                    readings.append({'line': line_content, 'fields': fields})
        return readings
    except Exception as e:
        print(f"An error occurred while reading the data: {e}")
        return []

# --- Functional Module 2: Data Input and Creation (CREATE) ---

def get_valid_input(prompt):
    """
    Gets integer input from the user and handles basic input validation.
    """
    while True:
        try:
            value = int(input(prompt))
            # Basic range check to prevent obvious typos or impossible readings
            if 50 <= value <= 250:
                return value
            else:
                print("Error: Value seems out of typical range (50-250). Please try again.")
        except ValueError:
            print("Error: Please enter a valid whole number.")

def log_new_reading():
    """
    Collects user data, classifies it, and saves it as a new line in the text file.
    """
    print("\n--- Log New Reading (CREATE) ---")
    sys = get_valid_input("Enter Systolic (SYS) reading: ")
    dia = get_valid_input("Enter Diastolic (DIA) reading: ")
    pulse = get_valid_input("Enter Pulse (HR) reading: ")

    category = classify_reading(sys, dia)
    # Generate a simple timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Format the data into a single comma-separated string (no special CSV module needed)
    data_line = f"{timestamp},{sys},{dia},{pulse},{category}\n"

    # Write the data line to the text file in append mode ('a')
    try:
        with open(DATA_FILE, mode='a') as file:
            file.write(data_line)
        print(f"\nSUCCESS! Reading recorded ({sys}/{dia}) and classified as: {category}")
    except Exception as e:
        print(f"An error occurred while saving: {e}")

# --- Functional Module 3: Data Viewing and Analysis (READ) ---

def view_history():
    """
    Reads all data from the text file, displays it, and calculates summary statistics.
    """
    readings_data = get_all_readings()

    print("\n--- Blood Pressure History (READ) ---")

    if not readings_data:
        print("No readings recorded yet. Start by logging a new reading.")
        return

    # Print table headers
    print(f"{'INDEX':<5} {'TIMESTAMP':<20} {'SYS':<5} {'DIA':<5} {'PULSE':<5} {'CATEGORY':<25}")
    print("-" * 70)

    total_sys = 0
    total_dia = 0

    for index, item in enumerate(readings_data):
        # We now include an index for the user to select for deletion
        timestamp, sys_str, dia_str, pulse_str, category = item['fields']
        
        # Print the formatted row
        print(f"{index+1:<5} {timestamp:<20} {sys_str:<5} {dia_str:<5} {pulse_str:<5} {category:<25}")
        
        # Sum the values for statistics
        total_sys += int(sys_str)
        total_dia += int(dia_str)

    # Calculate and display Summary Statistics
    print("-" * 70)
    print(f"Total Readings: {len(readings_data)}")
    print(f"Overall Average BP: {total_sys / len(readings_data):.0f}/{total_dia / len(readings_data):.0f}")

# --- Functional Module 4: Data Management (DELETE) ---

def delete_reading():
    """
    Displays the history with an index and allows the user to select a reading to delete.
    """
    readings_data = get_all_readings()

    if not readings_data:
        print("\nCannot delete. No readings recorded yet.")
        return
    
    # First, display the history with indexes
    view_history()

    num_readings = len(readings_data)
    
    while True:
        try:
            choice = input(f"\nEnter the INDEX number to delete (1 to {num_readings}), or 0 to cancel: ")
            index_to_delete = int(choice)
            
            if index_to_delete == 0:
                print("Deletion cancelled.")
                return
            
            if 1 <= index_to_delete <= num_readings:
                # Python list index starts at 0, so subtract 1
                del readings_data[index_to_delete - 1] 
                break
            else:
                print(f"Invalid index. Please enter a number between 1 and {num_readings}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Rewrite the file with the remaining readings
    try:
        # Use 'w' mode to overwrite the entire file
        with open(DATA_FILE, mode='w') as file:
            for item in readings_data:
                # Add newline character back as it was stripped in the helper function
                file.write(item['line'] + '\n') 
        
        print(f"\nSUCCESS! Reading #{index_to_delete} has been deleted.")
        # Show the updated history immediately
        view_history() 

    except Exception as e:
        print(f"An error occurred while rewriting the file: {e}")

# --- Main Application Loop ---

def main():
    """The main function to run the console tracker application."""
    print("Welcome to the Blood Pressure Tracker (Simple Console App)")

    while True:
        print("\n--- Main Menu ---")
        print("1. Log New Reading (Create)")
        print("2. View History & Summary (Read)")
        print("3. Delete a Reading (Delete)") # New option
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            log_new_reading()
        elif choice == '2':
            view_history()
        elif choice == '3':
            delete_reading() # New function call
        elif choice == '4':
            print("Thank you for using the tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()