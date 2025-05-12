import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Right bar animation
class RightPanel(ctk.CTkFrame):
    def __init__(self, parent, start_pos, end_pos):
        super().__init__(master=parent, fg_color='grey14')

        # General attributes
        self.start_pos = start_pos  # Initial position
        self.end_pos = end_pos  # Target position
        self.width = abs(start_pos - end_pos)

        # Animation state
        self.pos = self.start_pos
        self.in_start_pos = True

        # Layout
        self.place(relx=self.start_pos, rely=0.05, relwidth=self.width, relheight=0.9)

    def animate(self):
        if self.in_start_pos:
            self.animate_in()
        else:
            self.animate_out()

    def animate_in(self):
        if self.pos > self.end_pos:
            self.pos -= 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_in)
        else:
            self.in_start_pos = False

    def animate_out(self):
        if self.pos < self.start_pos:
            self.pos += 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_out)  # Corrected method call
        else:
            self.in_start_pos = True


# Left bar animation
class LeftPanel(ctk.CTkFrame):
    def __init__(self, parent, start_pos, end_pos):
        super().__init__(master=parent, fg_color='grey14')

        # General attributes
        self.start_pos = start_pos  # Initial position
        self.end_pos = end_pos  # Target position
        self.width = abs(end_pos - start_pos)

        # Animation state
        self.pos = self.start_pos
        self.in_start_pos = True

        # Layout
        self.place(relx=self.start_pos, rely=0.05, relwidth=self.width, relheight=0.9)

    def animate(self):
        if self.in_start_pos:
            self.animate_in()
        else:
            self.animate_out()

    def animate_in(self):
        if self.pos < self.end_pos:  # Move right to the end position
            self.pos += 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_in)
        else:
            self.in_start_pos = False

    def animate_out(self):
        if self.pos > self.start_pos:  # Move left back to the start position
            self.pos -= 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_out)
        else:
            self.in_start_pos = True


# Main window
window = ctk.CTk()
window.geometry('800x533')
window.title('PISO TEST MENU')

# Menu Frame
menu_frame = ctk.CTkFrame(window, width=200, height=400, corner_radius=0)
menu_frame.place(relx=0.41, rely=0.6, anchor="nw")

# Menu Buttons
menu_title = ctk.CTkLabel(menu_frame, text="Menu", font=("Arial", 16))
menu_title.pack(pady=10)

new_button = ctk.CTkButton(menu_frame, text="New File", command=lambda: print("New File pressed"),fg_color=('DarkOrchid2'))
new_button.pack(pady=5)

exit_button = ctk.CTkButton(menu_frame, text="Exit", command=window.quit,fg_color=('DarkOrchid2'))
exit_button.pack(pady=5)

help_button = ctk.CTkButton(menu_frame, text="Help", command=lambda: print(help_menu_check_status.get()),fg_color=('DarkOrchid2'))
help_button.pack(pady=5)

# Checkbutton for Help Menu
help_menu_check_status = ctk.StringVar(value="off")
status_check = ctk.CTkCheckBox(menu_frame, text="Status", variable=help_menu_check_status, onvalue="on", offvalue="off")
status_check.pack(pady=5)


# Right Animated Widget
animated_right_panel = RightPanel(window, 1, 0.75)
ctk.CTkButton(animated_right_panel, text = 'Button 1',fg_color=('gray17')).pack(expand = True, fill = 'both', pady = 10)
ctk.CTkButton(animated_right_panel, text = 'Button 2',fg_color=('gray17')).pack(expand = True, fill = 'both', pady = 10)
ctk.CTkButton(animated_right_panel, text = 'Button 3',fg_color=('gray17')).pack(expand = True, fill = 'both', pady = 10)

# Left Animated Widget
animated_left_panel = LeftPanel(window, -0.25, 0)
ctk.CTkButton(animated_left_panel, text = 'Button 1', fg_color=('gray17')).pack(expand = True, fill = 'both', pady = 10)
ctk.CTkButton(animated_left_panel, text = 'Button 2', fg_color=('gray17')).pack(expand = True, fill = 'both', pady = 10)
ctk.CTkButton(animated_left_panel, text = 'Button 3', fg_color=('gray17')).pack(expand = True, fill = 'both', pady = 10)


# Toggle button for left side
button_x = 0.35
button_y = 0.45

button_left = ctk.CTkButton(window, text='Toggle left Sidebar', command=animated_left_panel.animate, fg_color=('grey14'))
button_left.place(relx=button_x, rely=button_y, anchor='center')

# Toggle button for right side
button_x = 0.65
button_y = 0.45

button_right = ctk.CTkButton(window, text='Toggle Right Sidebar', command=animated_right_panel.animate, fg_color=('gray14'))
button_right.place(relx=button_x, rely=button_y, anchor='center')



# Run the main event loop
window.mainloop()
