import customtkinter as ctk
import os

# Set appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Global variable for box size
box_size = "default"
box_quantity = "default"
box_type = "default"
file_name = "default"

# Function to update box size and refresh file list
def set_box_size(size):
    global box_size
    box_size = size
    print(f"Box size set to: {box_size}")

    # Show the file left frame after selecting a box size
    file_left_frame.place(x=10, y=60)  # Make the frame visible when a size is selected

    # Call function to update file buttons dynamically
    update_file_buttons()

# Function to create file buttons dynamically
def update_file_buttons():
    global box_size
    global file_name
    # Clear previous file buttons in the existing frame
    for widget in file_left_frame.winfo_children():
        widget.destroy()

    # Set file path based on box size
    if box_size == "small":
        #path = r'D:\Mechatronics Year 4\ROBT 4491 Mechatronics Project\G-Code\Small'
        path = r'/media/PISO/bootfs/PISO GUI/G-Code/Small'
    elif box_size == "medium":
        #path = r'D:\Mechatronics Year 4\ROBT 4491 Mechatronics Project\G-Code\Medium'
        path = r'/media/PISO/bootfs/PISO GUI/G-Code/Medium'

    elif box_size == "large":
        #path = r'D:\Mechatronics Year 4\ROBT 4491 Mechatronics Project\G-Code\Large'
        path = r'/media/PISO/bootfs/PISO GUI/G-Code/Large'

    else:
        path = ""

    # Check if the path exists
    if os.path.exists(path):
        files = os.listdir(path)
        num_files = 0

        for file in files:
            file_name, file_extension = os.path.splitext(file)
            file_path = os.path.join(path, file)

            def read_and_print_file(f_path=file_path, f_name=file_name):
                """ Reads and prints the content of the selected file. """
                global box_type
                box_type = f_name  # Update global variable with selected file name

                try:
                    with open(f_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print(f"\nContents of {f_path}:\n{content}\n" + "-" * 50)
                except Exception as e:
                    print(f"Error reading {f_path}: {e}")

                # Updates current section
                current_section()


            # Create buttons only for .txt files
            if file_extension == ".txt":
                num_files += 1
                file_button = ctk.CTkButton(file_left_frame, text=file_name, command=lambda f_path=file_path, f_name=file_name: read_and_print_file(f_path, f_name), width=180)
                file_button.pack(pady=5)

        print(f"Total number of files: {num_files}")
        file_size.configure(text=f"{num_files} files detected.")
    else:
        file_size.configure(text="No files found in the selected folder.")
    
    file_size.place(x=55, y=300)
    current_section()

# Box Quantity
def open_number_pad():
    global num_pad_window
    global box_num  

    # Push window to front & ensures only 1 window is created
    if 'num_pad_window' in globals() and num_pad_window.winfo_exists():
        num_pad_window.lift()
        num_pad_window.focus_force()
        return 

    # Create a new window for the number pad
    num_pad_window = ctk.CTkToplevel(window)
    num_pad_window.geometry("300x400")
    num_pad_window.title("Enter a Number")

    # Numpad window is forced to the front
    def bring_window_to_front():
        num_pad_window.lift()
        num_pad_window.focus_force()
    num_pad_window.after(100, bring_window_to_front)

    # Number window
    num_entry = ctk.CTkEntry(num_pad_window, font=("Arial", 16), width=200)
    num_entry.grid(row=0, column=0, columnspan=3, pady=20)

    # Function that prints value box_quantity is the num value, box_num is the label
    def handle_number_input():
        global box_quantity
        box_quantity = num_entry.get()

        # Destroy the old number if it exists
        if 'box_num' in globals() and box_num is not None:
            box_num.destroy()

        # Print box number quantity
        box_num = ctk.CTkLabel(middle_option_frame, text=f"{box_quantity}", font=("Arial", 16,"bold"))
        box_num.place(x=150, y=5)

        print(f"Number entered: {box_quantity}")
        current_section() # Updates the section box qty
        num_pad_window.destroy()  # Close the number pad window
        del globals()['num_pad_window']  # Clean up the window reference

    # Number pad buttons 
    buttons = [
        '1', '2', '3',
        '4', '5', '6',
        '7', '8', '9',
        'Submit', '0'
    ]
    
    row, col = 1, 0  # Start placing buttons from row 1, column 0
    for button in buttons:
        # Offset the '0' button
        if button == '0':
            row = 4
            col = 1  

        # Offset the 'Submit' button
        elif button == 'Submit':
            row = 4
            col = 2

        # Regular button placement
        else:
            if col > 2:
                col = 0
                row += 1

        # Create the number pad button
        num_button = ctk.CTkButton(num_pad_window, text=button, 
                                   command=lambda b=button: num_entry.delete(0, 'end') or num_entry.insert(len(num_entry.get()), b) if b != 'Submit' else handle_number_input(),
                                   width=90, height=60)
        num_button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        col += 1
        if col > 2:
            col = 0
            row += 1


def current_section():
    global box_size
    global box_quantity
    global box_type
    
    # Clear previous labels
    for widget in right_section_frame.winfo_children():
        widget.destroy()

    # Update Box size 
    section_box_size = ctk.CTkLabel(right_section_frame, text=f"Box Size: {box_size}", font=("Arial", 16,"bold")) 
    section_box_size.place(x=10, y=5)

    # Update Box File
    section_box_type = ctk.CTkLabel(right_section_frame, text=f"Box Type: {box_type}", font=("Arial", 16,"bold")) 
    section_box_type.place(x=10, y=30)

    # Update Box qty
    section_box_qty = ctk.CTkLabel(right_section_frame, text=f"Box Qty: {box_quantity}", font=("Arial", 16,"bold"))
    section_box_qty.place(x=10, y=55)

def set_box_quantity(quantity):
    global box_quantity
    box_quantity = quantity

    current_section()


# Create main window
window = ctk.CTk()
window.geometry('800x533')
window.title('PISO TEST MENU')

# LEFT Top Frame
top_left_frame = ctk.CTkFrame(window, width=200, height=80)
top_left_frame.place(relx=0.01, rely=0.05)

# LEFT for sizes
size_title_label = ctk.CTkLabel(top_left_frame, text="Box Size", font=("Arial", 16, "bold"))
size_title_label.place(x=70, y=5)

# LEFT Frame for size buttons
size_left_frame = ctk.CTkFrame(top_left_frame, fg_color=('gray14'), width=180, height=20)
size_left_frame.place(x=10, y=30)

# LEFT S/M/L Buttons
small_button = ctk.CTkButton(size_left_frame, text="Small", command=lambda: set_box_size("small"),width=60)
small_button.pack(side="left", pady=5)

medium_button = ctk.CTkButton(size_left_frame, text="Medium", command=lambda: set_box_size("medium"),width=60)
medium_button.pack(side="left", pady=5)

large_button = ctk.CTkButton(size_left_frame, text="Large", command=lambda: set_box_size("large"), width=60)
large_button.pack(side="left", pady=5)

# LEFT Bottom Left Frame
bottom_left_frame = ctk.CTkFrame(window, width=200, height=350)
bottom_left_frame.place(relx=0.01, rely=0.25)

# LEFT Title for files
file_title_label = ctk.CTkLabel(bottom_left_frame, text="Drawing Type", font=("Arial", 16, "bold"))
file_title_label.place(x=45, y=10)

# LEFT Frame for file buttons
file_left_frame = ctk.CTkFrame(bottom_left_frame, fg_color=('gray14'), width=180, height=200)

# LEFT Label to show number of detected files
file_size = ctk.CTkLabel(bottom_left_frame, text="Please Select \n Box Size.", font=("Arial", 13, "underline"))
file_size.place(x=55, y=100)

# MIDDLE options frame
middle_option_frame = ctk.CTkFrame(window, width=200, height=160)
middle_option_frame.place(relx=0.35, rely=0.05)

# MIDDLE box qty
box_qty = ctk.CTkLabel(middle_option_frame, text="Box Quantity:", font=("Arial", 16,"bold"))
box_qty.place(x=40, y=5)

# MIDDLE number count button
num_button = ctk.CTkButton(middle_option_frame, text="Enter Number", command=open_number_pad, width=190, height=100)
num_button.place(relx=0.5, rely=0.6, anchor="center")

# MIDDLE stacks frame
middle_stack_frame = ctk.CTkFrame(window, width=200, height=250)
middle_stack_frame.place(relx=0.35, rely=0.4)

# MIDDLE stack Full button
full_stack_button = ctk.CTkButton(middle_stack_frame, text="Full Stack", command=lambda: set_box_quantity(12), width=190, height=50)
full_stack_button.place(relx=0.5, rely=0.15, anchor="center")

# MIDDLE stack 1/2 button
half_stack_button = ctk.CTkButton(middle_stack_frame, text="1/2 Stack", command=lambda: print("Half stack has been pressed"), width=190, height=50) 
half_stack_button.place(relx=0.5, rely=0.48, anchor="center")

# MIDDLE stack 1/3 button
half_stack_button = ctk.CTkButton(middle_stack_frame, text="1/3 Stack", command=lambda: print("Third stack has been pressed"), width=190, height=50) 
half_stack_button.place(relx=0.5, rely=0.81, anchor="center")

# RIGHT selection frame
right_section_frame = ctk.CTkFrame(window, width=200, height=150)
right_section_frame.place(relx=0.70, rely=0.05)

# RIGHT start button frame
right_start_frame = ctk.CTkFrame(window, width=200, height=150)
right_start_frame.place(relx=0.70, rely=0.35)

# RIGHT start button
start_button = ctk.CTkButton(right_start_frame, text="START", font=("Arial", 16,"bold"), command=lambda: print("Start button pressed"), width=180, height=130, fg_color="green")
start_button.place(relx=0.5, rely=0.5, anchor="center")

# RIGHT stop button frame
right_stop_frame = ctk.CTkFrame(window, width=200, height=150)
right_stop_frame.place(relx=0.70, rely=0.65)

# RIGHT stop button
stop_button = ctk.CTkButton(right_stop_frame, text="STOP", font=("Arial", 16,"bold"), command=lambda: print("Stop button pressed"), width=180, height=130, fg_color="red")
stop_button.place(relx=0.5, rely=0.5, anchor="center")





# Run main event loop
window.mainloop()
