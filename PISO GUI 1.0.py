import customtkinter as ctk
import os

# Set appearance and theme
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("dark-blue")

# Create main window
window = ctk.CTk()
window.geometry('800x533')
window.title('PISO TEST MENU')

# Top Left Frame menu frame
top_left_frame = ctk.CTkFrame(window, width=200, height=80)
top_left_frame.place(relx=0.01, rely=0.05)

# Title for sizes
size_title_label = ctk.CTkLabel(top_left_frame, text="Box Size", font=("Arial", 16, "bold"))
size_title_label.place(x=70,y=5)

# Inner frame inside file_frame for sizes
size_left_frame = ctk.CTkFrame(top_left_frame, fg_color="blue", width=180, height=20)
size_left_frame.place(x=10, y=30) #prev y=10

# S/M/L Buttons within file_frame
small_button = ctk.CTkButton(size_left_frame, text="Small", command=lambda: print("Small Pressed"),fg_color=('DarkOrchid2'), width=60)
small_button.pack(side = "left",pady=5)

medium_button = ctk.CTkButton(size_left_frame, text="Medium", command=lambda: print("Medium Pressed"),fg_color=('DarkOrchid2'), width = 60)
medium_button.pack(side = "left",pady=5)

large_button = ctk.CTkButton(size_left_frame, text="Large", command=lambda: print("Large Pressed"),fg_color=('DarkOrchid2'), width = 60)
large_button.pack(side = "left",pady=5)




# Bottom Left Frame menu frame
bottom_left_frame = ctk.CTkFrame(window, width=200, height=350)
bottom_left_frame.place(relx=0.01, rely=0.25)

# Title for files
file_title_label = ctk.CTkLabel(bottom_left_frame, text="Drawing Type", font=("Arial", 16, "bold"))
file_title_label.place(x=45,y=10)

# Inner frame inside file_frame for files
file_left_frame = ctk.CTkFrame(bottom_left_frame, fg_color="blue", width=180, height=410)
file_left_frame.place(x=10, y=60) # prev y=60

# Creates the file buttons for every file 
path = 'D:\Mechatronics Year 4\ROBT 4491 Mechatronics Project\G-Code'
files = os.listdir(path)


num_files = 0
for file in files:
    num_files += 1
    file_name, file_extension = os.path.splitext(file)
    file_button = ctk.CTkButton(file_left_frame, text=file_name, command=lambda f=file_name: print(f"{f} pressed"), fg_color='DarkOrchid2',width=180)
    file_button.pack(pady=5)

print(f"Total number of files: {num_files}")

# Number of files
file_size = ctk.CTkLabel(bottom_left_frame, text=f"{num_files} files detected.", font=("Arial", 13))
file_size.place(x=55,y=320)

# Run the main event loop
window.mainloop()
