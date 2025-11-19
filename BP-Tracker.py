# --- Configuration ---
# Use a simple text file to store all readings. Each reading is one line.
DATA_FILE = 'bp_readings.txt'

# The entire application logic is contained within this main block.
if __name__ == "__main__":
    print("Welcome to the Blood Pressure Tracker (Single Block Console App - No Imports)")

    while True:
        # --- Main Menu Display ---
        print("\n--- Main Menu ---")
        print("1. Log New Reading (CREATE)")
        print("2. View History & Summary (READ)")
        print("3. Update/Edit a Reading (UPDATE)")
        print("4. Delete a Reading (DELETE)")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        # ----------------------------------------------------------------------
        # OPTION 1: LOG NEW READING (CREATE)
        # ----------------------------------------------------------------------
        if choice == '1':
            print("\n--- Log New Reading (CREATE) ---")
            
            # --- Input for Date (No Imports) ---
            timestamp = input("Enter today's date (e.g., YYYY-MM-DD): ")
            
            # --- Input and Validation for Systolic (Inline Logic) ---
            sys = 0
            while True:
                value_str = input("Enter Systolic (SYS) reading: ")
                if value_str.isdigit():
                    sys = int(value_str)
                    if 50 <= sys <= 250:
                        break
                    else:
                        print("Error: Value seems out of typical range (50-250). Try again.")
                else:
                    print("Error: Please enter a valid whole number (digits only).")

            # --- Input and Validation for Diastolic (Inline Logic) ---
            dia = 0
            while True:
                value_str = input("Enter Diastolic (DIA) reading: ")
                if value_str.isdigit():
                    dia = int(value_str)
                    if 50 <= dia <= 250:
                        break
                    else:
                        print("Error: Value seems out of typical range (50-250). Try again.")
                else:
                    print("Error: Please enter a valid whole number (digits only).")

            # --- Input and Validation for Pulse (Inline Logic) ---
            pulse = 0
            while True:
                value_str = input("Enter Pulse (HR) reading: ")
                if value_str.isdigit():
                    pulse = int(value_str)
                    if 50 <= pulse <= 250:
                        break
                    else:
                        print("Error: Value seems out of typical range (50-250). Try again.")
                else:
                    print("Error: Please enter a valid whole number (digits only).")


            # --- Classification Logic (Inline) ---
            category = ""
            if sys < 120 and dia < 80:
                category = "Normal"
            elif 120 <= sys <= 129 and dia < 80:
                category = "Elevated"
            elif 130 <= sys <= 139 or 80 <= dia <= 89:
                category = "Hypertension Stage 1"
            elif sys >= 140 or dia >= 90:
                category = "Hypertension Stage 2"
            else:
                category = "Unclassified (Error)"

            # Data line format: DATE,SYS,DIA,PULSE,CATEGORY
            data_line = f"{timestamp},{sys},{dia},{pulse},{category}\n"

            # --- File Writing (Inline Logic) ---
            with open(DATA_FILE, mode='a') as file:
                file.write(data_line)
            
            print(f"\nSUCCESS! Reading recorded ({sys}/{dia}) and classified as: {category}")

        # ----------------------------------------------------------------------
        # OPTION 2: VIEW HISTORY & SUMMARY (READ)
        # ----------------------------------------------------------------------
        elif choice == '2':
            # --- File Reading (Inline Logic) ---
            readings_data = []
            try: 
                 with open(DATA_FILE, mode='r') as file:
                    for line in file:
                        line_content = line.strip()
                        fields = line_content.split(',')
                        if len(fields) == 5:
                            readings_data.append({'line': line_content, 'fields': fields})
            except FileNotFoundError:
                 pass
            
            print("\n--- Blood Pressure History (READ) ---")

            if not readings_data:
                print("No readings recorded yet. Please use Option 1 to log your first reading.")
                continue

            # Print table headers
            print(f"{'INDEX':<5} {'DATE':<20} {'SYS':<5} {'DIA':<5} {'PULSE':<5} {'CATEGORY':<25}")
            print("-" * 70)

            total_sys = 0
            total_dia = 0

            for index, item in enumerate(readings_data):
                timestamp, sys_str, dia_str, pulse_str, category = item['fields']
                
                print(f"{index+1:<5} {timestamp:<20} {sys_str:<5} {dia_str:<5} {pulse_str:<5} {category:<25}")
                
                total_sys += int(sys_str)
                total_dia += int(dia_str)

            # Display Summary Statistics
            print("-" * 70)
            print(f"Total Readings: {len(readings_data)}")
            print(f"Overall Average BP: {total_sys / len(readings_data):.0f}/{total_dia / len(readings_data):.0f}")

        # ----------------------------------------------------------------------
        # OPTION 3: UPDATE/EDIT A READING (UPDATE)
        # ----------------------------------------------------------------------
        elif choice == '3':
            # --- File Reading (Inline Logic) ---
            readings_data = []
            try: 
                 with open(DATA_FILE, mode='r') as file:
                    for line in file:
                        line_content = line.strip()
                        fields = line_content.split(',')
                        if len(fields) == 5:
                            readings_data.append({'line': line_content, 'fields': fields})
            except FileNotFoundError:
                 pass

            if not readings_data:
                print("\nCannot update. No readings recorded yet. Please use Option 1 first.")
                continue 
            
            # --- Display History (Inline Logic) ---
            print("\n--- Select Reading to UPDATE ---")
            
            print(f"{'INDEX':<5} {'DATE':<20} {'SYS':<5} {'DIA':<5} {'PULSE':<5} {'CATEGORY':<25}")
            print("-" * 70)
            for index, item in enumerate(readings_data):
                timestamp, sys_str, dia_str, pulse_str, category = item['fields']
                print(f"{index+1:<5} {timestamp:<20} {sys_str:<5} {dia_str:<5} {pulse_str:<5} {category:<25}")
            print("-" * 70)

            # --- Get Valid Index Input (Inline Logic) ---
            num_readings = len(readings_data)
            index_to_update = -1
            
            while not (0 <= index_to_update <= num_readings):
                choice_str = input(f"Enter the INDEX number to update (1 to {num_readings}), or 0 to cancel: ")
                
                if choice_str.isdigit():
                    index_to_update = int(choice_str)
                    
                    if index_to_update == 0:
                        print("Update cancelled.")
                        break
                    
                    if 1 <= index_to_update <= num_readings:
                        break
                    else:
                        print(f"Invalid index. Please enter a number between 1 and {num_readings}.")
                else:
                    print("Invalid input. Please enter a number.")
            
            if index_to_update == 0:
                 continue

            # --- Get New Data (Inline Logic) ---
            index = index_to_update - 1
            print(f"\n--- Editing Reading #{index_to_update} ---")
            
            # Preserve existing date or prompt for a new one
            new_timestamp = input(f"Enter NEW date ({readings_data[index]['fields'][0]}): ")
            if not new_timestamp:
                new_timestamp = readings_data[index]['fields'][0]
                
            # Input and Validation for new SYS (Inline Logic) ---
            new_sys = 0
            while True:
                value_str = input("Enter NEW Systolic (SYS) reading: ")
                if value_str.isdigit():
                    new_sys = int(value_str)
                    if 50 <= new_sys <= 250:
                        break
                    else:
                        print("Error: Value seems out of typical range (50-250). Try again.")
                else:
                    print("Error: Please enter a valid whole number (digits only).")

            # Input and Validation for new DIA (Inline Logic) ---
            new_dia = 0
            while True:
                value_str = input("Enter NEW Diastolic (DIA) reading: ")
                if value_str.isdigit():
                    new_dia = int(value_str)
                    if 50 <= new_dia <= 250:
                        break
                    else:
                        print("Error: Value seems out of typical range (50-250). Try again.")
                else:
                    print("Error: Please enter a valid whole number (digits only).")

            # Input and Validation for new PULSE (Inline Logic) ---
            new_pulse = 0
            while True:
                value_str = input("Enter NEW Pulse (HR) reading: ")
                if value_str.isdigit():
                    new_pulse = int(value_str)
                    if 50 <= new_pulse <= 250:
                        break
                    else:
                        print("Error: Value seems out of typical range (50-250). Try again.")
                else:
                    print("Error: Please enter a valid whole number (digits only).")

            # --- Classification Logic (Inline) ---
            new_category = ""
            if new_sys < 120 and new_dia < 80:
                new_category = "Normal"
            elif 120 <= new_sys <= 129 and new_dia < 80:
                new_category = "Elevated"
            elif 130 <= new_sys <= 139 or 80 <= new_dia <= 89:
                new_category = "Hypertension Stage 1"
            elif new_sys >= 140 or new_dia >= 90:
                new_category = "Hypertension Stage 2"
            else:
                new_category = "Unclassified (Error)"
            
            # Recreate the data line
            new_data_line = f"{new_timestamp},{new_sys},{new_dia},{new_pulse},{new_category}"
            
            # Update the reading in the list
            readings_data[index]['line'] = new_data_line
            readings_data[index]['fields'] = new_data_line.split(',')

            # --- File Rewriting (Inline Logic) ---
            with open(DATA_FILE, mode='w') as file:
                for item in readings_data:
                    file.write(item['line'] + '\n')
            
            print(f"\nSUCCESS! Reading #{index_to_update} updated to {new_sys}/{new_dia} and classified as: {new_category}")


        # ----------------------------------------------------------------------
        # OPTION 4: DELETE A READING (DELETE)
        # ----------------------------------------------------------------------
        elif choice == '4':
            # --- File Reading (Inline Logic) ---
            readings_data = []
            try: 
                 with open(DATA_FILE, mode='r') as file:
                    for line in file:
                        line_content = line.strip()
                        fields = line_content.split(',')
                        if len(fields) == 5:
                            readings_data.append({'line': line_content, 'fields': fields})
            except FileNotFoundError:
                 pass
            
            if not readings_data:
                print("\nCannot delete. No readings recorded yet. Please use Option 1 first.")
                continue 
            
            # --- Display History (Inline Logic) ---
            print("\n--- Select Reading to DELETE ---")
            
            print(f"{'INDEX':<5} {'DATE':<20} {'SYS':<5} {'DIA':<5} {'PULSE':<5} {'CATEGORY':<25}")
            print("-" * 70)
            for index, item in enumerate(readings_data):
                timestamp, sys_str, dia_str, pulse_str, category = item['fields']
                print(f"{index+1:<5} {timestamp:<20} {sys_str:<5} {dia_str:<5} {pulse_str:<5} {category:<25}")
            print("-" * 70)

            # --- Get Valid Index Input (Inline Logic) ---
            num_readings = len(readings_data)
            index_to_delete = -1
            
            while not (0 <= index_to_delete <= num_readings):
                choice_str = input(f"Enter the INDEX number to delete (1 to {num_readings}), or 0 to cancel: ")
                
                if choice_str.isdigit():
                    index_to_delete = int(choice_str)
                    
                    if index_to_delete == 0:
                        print("Deletion cancelled.")
                        break
                    
                    if 1 <= index_to_delete <= num_readings:
                        break
                    else:
                        print(f"Invalid index. Please enter a number between 1 and {num_readings}.")
                else:
                    print("Invalid input. Please enter a number.")
            
            if index_to_delete == 0:
                continue

            # Remove the reading from the list
            del readings_data[index_to_delete - 1] 
            
            # --- File Rewriting (Inline Logic) ---
            with open(DATA_FILE, mode='w') as file:
                for item in readings_data:
                    file.write(item['line'] + '\n')
            
            print(f"\nSUCCESS! Reading #{index_to_delete} has been deleted.")
            
            # --- Display History Again (Inline Logic) ---
            # Re-read data after deletion (technically redundant but safe)
            readings_data_after_delete = []
            try: 
                 with open(DATA_FILE, mode='r') as file:
                    for line in file:
                        line_content = line.strip()
                        fields = line_content.split(',')
                        if len(fields) == 5:
                            readings_data_after_delete.append({'line': line_content, 'fields': fields})
            except FileNotFoundError:
                 pass

            print("\n--- UPDATED Blood Pressure History ---")
            
            if not readings_data_after_delete:
                print("The history is now empty.")
            else:
                print(f"{'INDEX':<5} {'DATE':<20} {'SYS':<5} {'DIA':<5} {'PULSE':<5} {'CATEGORY':<25}")
                print("-" * 70)
                for index, item in enumerate(readings_data_after_delete):
                    timestamp, sys_str, dia_str, pulse_str, category = item['fields']
                    print(f"{index+1:<5} {timestamp:<20} {sys_str:<5} {dia_str:<5} {pulse_str:<5} {category:<25}")
                print("-" * 70)
        
        # ----------------------------------------------------------------------
        # OPTION 5: EXIT
        # ----------------------------------------------------------------------
        elif choice == '5':
            print("Thank you for using the tracker. Goodbye!")
            break
        
        # ----------------------------------------------------------------------
        # INVALID CHOICE
        # ----------------------------------------------------------------------
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
