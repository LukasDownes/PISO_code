import customtkinter as ctk
import os # For reading files
import serial # For Transmitting via UART
import time # For delays


# Set appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Global variable for box size
box_size = "default"
box_quantity = "default"
box_type = "default"
file_name = "default"

# Initialize Serial Communication (Use Raspberry Pi UART /dev/serial0)
ser = serial.Serial(
    port='/dev/serial0', 
    baudrate=19200, 
    bytesize=serial.EIGHTBITS,  # 8-bit data
    parity=serial.PARITY_NONE,  # No parity
    stopbits=serial.STOPBITS_ONE,  # 1 stop bit
    timeout=1
)
time.sleep(2)  # Allow time for serial connection to initialize

# Function to update box size and refresh file list
def set_box_size(size):
    global box_size
    box_size = size
    print(f"Box size set to: {box_size}")

    # Show the file left frame after selecting a box size
    file_left_frame.place(relx=0.1, y=60)  # Make the frame visible when a size is selected

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
                file_button = ctk.CTkButton(file_left_frame, text=file_name, font=("Arial", 20), command=lambda f_path=file_path, f_name=file_name: read_and_print_file(f_path, f_name), width=320, height=50)
                file_button.pack(pady=5)

        print(f"Total number of files: {num_files}")
        file_size.configure(text=f"{num_files} files detected.")
    else:
        file_size.configure(text="No files found \n in the selected folder.")
    
    file_size.place(relx=0.3, y=300)
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
        box_num = ctk.CTkLabel(middle_option_frame, text=f"{box_quantity}", font=("Arial", 25,"bold"))
        box_num.place(relx=0.65, y=5)

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
    section_box_size = ctk.CTkLabel(right_section_frame, text=f"Box Size: {box_size}", font=("Arial", 25,"bold")) 
    section_box_size.place(x=10, y=15)

    # Update Box File
    section_box_type = ctk.CTkLabel(right_section_frame, text=f"Box Type: {box_type}", font=("Arial", 25,"bold")) 
    section_box_type.place(x=10, y=50)

    # Update Box qty
    section_box_qty = ctk.CTkLabel(right_section_frame, text=f"Box Qty: {box_quantity}", font=("Arial", 25,"bold"))
    section_box_qty.place(x=10, y=85)

def set_box_quantity(quantity):
    global box_quantity
    box_quantity = quantity

    current_section()

def transmit_file_contents():
    global box_quantity, box_type, box_size
    
    # Ensure a valid file and quantity are selected
    if box_quantity == "default" or box_type == "default" or box_size == "default":
        show_message("Please select box size, type, and quantity before starting.")
        return
    
    # Determine the file path based on box size and type
    base_path = f"/media/PISO/bootfs/PISO GUI/G-Code/{box_size.capitalize()}"
    file_path = os.path.join(base_path, f"{box_type}.txt")
    
    if not os.path.exists(file_path):
        show_message(f"File not found: {file_path}")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.readlines()  # Read all lines
        
        # Convert box_quantity to an integer
        try:
            quantity = int(box_quantity)
        except ValueError:
            show_message("Invalid box quantity. Please enter a number.")
            return
        
        for _ in range(quantity):
            for line in content:
                message = line.strip() + "\r"  # Format message
                ser.write(message.encode())  # Send over UART
                print(f"Sent: {message.strip()}")
                time.sleep(5)  # 5-second delay between each line
    
    except Exception as e:
        show_message(f"Error reading or sending file: {e}")

def show_message(msg):
    """Displays a message on the screen for 3 seconds."""
    message_label.config(text=msg)
    window.update()
    window.after(3000, lambda: message_label.config(text=""))  # Clear message after 3 seconds


# Create main window
window = ctk.CTk()
window.bind("<Escape>", lambda event: window.attributes('-fullscreen', False))
window.geometry('1280x800')
#window.title('PISO TEST MENU')
#window.attributes('-fullscreen', True)

# LEFT Top Frame
top_left_frame = ctk.CTkFrame(window, width=400, height=120)
top_left_frame.place(relx=0.01, rely=0.05)

# LEFT for sizes
size_title_label = ctk.CTkLabel(top_left_frame, text="Box Size", font=("Arial", 25, "bold"))
size_title_label.place(x=140, y=5)

# LEFT Frame for size buttons
size_left_frame = ctk.CTkFrame(top_left_frame, fg_color=('gray14'), width=360, height=80)
size_left_frame.place(relx=0.05, y=40)

# LEFT S/M/L Buttons
small_button = ctk.CTkButton(size_left_frame, text="Small",font=("Arial", 20), command=lambda: set_box_size("small"),width=120,height=60)
small_button.pack(side="left", pady=5)

medium_button = ctk.CTkButton(size_left_frame, text="Medium",font=("Arial", 20), command=lambda: set_box_size("medium"),width=120,height=60)
medium_button.pack(side="left", pady=5)

large_button = ctk.CTkButton(size_left_frame, text="Large",font=("Arial", 20), command=lambda: set_box_size("large"), width=120,height=60)
large_button.pack(side="left", pady=5)

# LEFT Bottom Left Frame
bottom_left_frame = ctk.CTkFrame(window, width=400, height=500)
bottom_left_frame.place(relx=0.01, rely=0.25)

# LEFT Title for files
file_title_label = ctk.CTkLabel(bottom_left_frame, text="Drawing Type", font=("Arial",25 , "bold"))
file_title_label.place(relx=0.25, y=10)

# LEFT Frame for file buttons
file_left_frame = ctk.CTkFrame(bottom_left_frame, fg_color=('gray14'), width=380, height=200)

# LEFT Label to show number of detected files
file_size = ctk.CTkLabel(bottom_left_frame, text="Please Select \n Box Size.", font=("Arial",20 , "underline"))
file_size.place(relx=0.30, y=200)

# MIDDLE options frame
middle_option_frame = ctk.CTkFrame(window, width=400, height= 200)
middle_option_frame.place(relx=0.35, rely=0.05)

# MIDDLE box qty
box_qty = ctk.CTkLabel(middle_option_frame, text="Box Quantity:", font=("Arial", 25,"bold"))
box_qty.place(relx=0.2, y=5)

# MIDDLE number count button
num_button = ctk.CTkButton(middle_option_frame, text="Enter Number",font=("Arial", 20,"bold"), command=open_number_pad, width=240, height=120)
num_button.place(relx=0.5, rely=0.6, anchor="center")

# MIDDLE stacks frame
middle_stack_frame = ctk.CTkFrame(window, width=400, height=250)
middle_stack_frame.place(relx=0.35, rely=0.35)

# MIDDLE stack Full button
full_stack_button = ctk.CTkButton(middle_stack_frame, text="Full Stack",font=("Arial", 20), command=lambda: set_box_quantity(12), width=190, height=50)
full_stack_button.place(relx=0.5, rely=0.15, anchor="center")

# MIDDLE stack 1/2 button
half_stack_button = ctk.CTkButton(middle_stack_frame, text="1/2 Stack",font=("Arial", 20), command=lambda: set_box_quantity(6), width=190, height=50) 
half_stack_button.place(relx=0.5, rely=0.48, anchor="center")

# MIDDLE stack 1/3 button
half_stack_button = ctk.CTkButton(middle_stack_frame, text="1/3 Stack",font=("Arial", 20), command=lambda: set_box_quantity(4), width=190, height=50) 
half_stack_button.place(relx=0.5, rely=0.81, anchor="center")

# MIDDLE Label for displaying messages
message_label = ctk.Label(window, text="", font=("Arial", 14), fg="black")
message_label.pack(pady=20)

# RIGHT selection frame
right_section_frame = ctk.CTkFrame(window, width=370, height=150)
right_section_frame.place(relx=0.70, rely=0.05)

# RIGHT start button frame
right_start_frame = ctk.CTkFrame(window, width=370, height=150)
right_start_frame.place(relx=0.70, rely=0.35)

# RIGHT start button
start_button = ctk.CTkButton(right_start_frame, text="START", font=("Arial", 25,"bold"),command=transmit_file_contents, width=360, height=140, fg_color="green")
start_button.place(relx=0.5, rely=0.5, anchor="center")


# RIGHT stop button frame
right_stop_frame = ctk.CTkFrame(window, width=370, height=150)
right_stop_frame.place(relx=0.70, rely=0.65)

# RIGHT stop button
stop_button = ctk.CTkButton(right_stop_frame, text="STOP", font=("Arial", 25,"bold"), command=lambda: print("Stop button pressed"), width=360, height=140, fg_color="red")
stop_button.place(relx=0.5, rely=0.5, anchor="center")





# Run main event loop
window.mainloop()
ser.close()
