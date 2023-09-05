import random
import string
import customtkinter as CTk
from PIL import Image


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.minsize(500, 250)
        self.root.geometry("600x300")
        self.root.title("Pass Sentinel")
        self.root.iconbitmap("assets/locked.ico")

        CTk.set_appearance_mode("system")
        CTk.set_default_color_theme("green")

        # Change theme button
        self.theme_image = CTk.CTkImage(
            dark_image=Image.open("assets/sun.png"),
            light_image=Image.open("assets/moon.png"),
        )
        self.theme_button = CTk.CTkButton(
            self.root, command=self.change_theme, text="", image=self.theme_image
        )
        self.theme_button.place(
            relx=0.05, rely=0.08, relheight=0.15, relwidth=0.08, anchor="nw"
        )

        # Password frame and label
        self.password_frame = CTk.CTkFrame(self.root)
        self.password_frame.place(
            relx=0.14, rely=0.08, relheight=0.15, relwidth=0.74, anchor="nw"
        )

        self.password_var = CTk.StringVar(value="Your password will be shown here.")
        self.password_label = CTk.CTkLabel(
            self.password_frame, textvariable=self.password_var, font=("Consolas", 14)
        )
        self.password_label.place(
            relx=0.01, rely=0.01, relheight=0.95, relwidth=0.98, anchor="nw"
        )

        # Copy button
        self.copy_image = CTk.CTkImage(Image.open("assets/copy.png"))
        self.copy_button = CTk.CTkButton(
            self.root, command=self.copy_password, text="", image=self.copy_image
        )
        self.copy_button.place(
            relx=0.89, rely=0.08, relheight=0.15, relwidth=0.08, anchor="nw"
        )

        # Checkboxes and check frame
        self.check_frame = CTk.CTkFrame(self.root)
        self.check_frame.place(
            relx=0.05, rely=0.3, relheight=0.6, relwidth=0.3, anchor="nw"
        )

        self.specials_check_var = CTk.BooleanVar(value=True)
        self.digits_check_var = CTk.BooleanVar(value=True)
        self.lowercase_check_var = CTk.BooleanVar(value=True)
        self.uppercase_check_var = CTk.BooleanVar(value=True)

        self.specials_box = self.create_checkbox(
            self.check_frame, self.specials_check_var, "Specials #-$"
        )
        self.specials_box.place(relx=0.1, rely=0.12, anchor="nw")

        self.digits_box = self.create_checkbox(
            self.check_frame, self.digits_check_var, "Numbers 0-9"
        )
        self.digits_box.configure(command=self.enable_digits)
        self.digits_box.place(relx=0.1, rely=0.32, anchor="nw")

        self.lowercase_box = self.create_checkbox(
            self.check_frame, self.lowercase_check_var, "Lowercase a-z"
        )
        self.specials_box.configure(command=self.enable_specials)
        self.lowercase_box.place(relx=0.1, rely=0.54, anchor="nw")

        self.uppercase_box = self.create_checkbox(
            self.check_frame, self.uppercase_check_var, "Uppercase A-Z"
        )
        self.uppercase_box.place(relx=0.1, rely=0.76, anchor="nw")

        # Sliders for lengths
        self.slider_frame = CTk.CTkFrame(self.root)
        self.slider_frame.place(
            relx=0.4, rely=0.3, relheight=0.4, relwidth=0.57, anchor="nw"
        )

        self.total_length = CTk.CTkSlider(
            self.slider_frame,
            from_=4,
            to=52,
            command=lambda e: self.update_label(
                self.total_length, self.total_length_label, "Total Length"
            ),
        )
        self.total_length.set(12)
        self.total_length.place(relx=0.99, rely=0.12, relwidth=0.6, anchor="ne")

        self.total_length_label = CTk.CTkLabel(
            self.slider_frame, text="Total Length: 12"
        )
        self.total_length_label.place(relx=0.05, rely=0.1, anchor="nw")

        self.min_numbers = CTk.CTkSlider(
            self.slider_frame,
            from_=0,
            to=self.total_length.get(),
            command=lambda e: self.update_label(
                self.min_numbers, self.min_numbers_label, "Min Numbers"
            ),
        )
        self.min_numbers.set(3)
        self.min_numbers.place(relx=0.99, rely=0.42, relwidth=0.6, anchor="ne")

        self.min_numbers_label = CTk.CTkLabel(self.slider_frame, text="Min Numbers: 3")
        self.min_numbers_label.place(relx=0.05, rely=0.4, anchor="nw")

        self.min_specials = CTk.CTkSlider(
            self.slider_frame,
            from_=0,
            to=self.total_length.get(),
            command=lambda e: self.update_label(
                self.min_specials, self.min_specials_label, "Min Specials"
            ),
        )
        self.min_specials.set(3)
        self.min_specials.place(relx=0.99, rely=0.72, relwidth=0.6, anchor="ne")

        self.min_specials_label = CTk.CTkLabel(
            self.slider_frame, text="Min Specials: 3"
        )
        self.min_specials_label.place(relx=0.05, rely=0.7, anchor="nw")

        # Password function and button
        self.generate_button = CTk.CTkButton(
            self.root,
            text="Generate Password",
            text_color="black",
            command=self.generate_password,
            font=("Calibri", 18),
        )
        self.generate_button.place(
            relx=0.4, rely=0.75, relwidth=0.45, relheight=0.15, anchor="nw"
        )

        # About me button
        self.info_img = CTk.CTkImage(Image.open("assets/info.png"))
        self.info_button = CTk.CTkButton(
            self.root, command=self.about_me, text="", image=self.info_img
        )
        self.info_button.place(
            relx=0.87, rely=0.75, relwidth=0.1, relheight=0.15, anchor="nw"
        )

    def create_checkbox(self, parent, var, text):
        """Set all default configurations for a checkbox"""
        checkbox = CTk.CTkCheckBox(
            parent,
            variable=var,
            onvalue=True,
            offvalue=False,
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            text=text,
            checkmark_color="black",
        )
        return checkbox

    def enable_digits(self):
        """enable or disable digits slider based on numbers checkbox"""
        if self.digits_check_var.get():
            self.min_numbers.configure(state="normal", button_color="#2FA572")
        else:
            self.min_numbers.configure(state="disable", button_color="gray")
            self.min_numbers.set(0)
            self.update_label(self.min_numbers, self.min_numbers_label, "Min Numbers")

    def enable_specials(self):
        """enable or disable specials slider based on specials checkbox"""
        if self.specials_check_var.get():
            self.min_specials.configure(state="normal", button_color="#2FA572")
        else:
            self.min_specials.configure(state="disable", button_color="gray")
            self.min_specials.set(0)
            self.update_label(
                self.min_specials, self.min_specials_label, "Min Specials"
            )

    def change_theme(self):
        """Change current theme of the app"""
        if CTk.get_appearance_mode() == "Dark":
            CTk.set_appearance_mode("light")
        else:
            CTk.set_appearance_mode("dark")

    def update_label(self, slider, label, text):
        """Update labels according to slider values"""
        label.configure(text=f"{text}: {int(slider.get())}")
        if slider != self.total_length:
            slider.configure(to=self.total_length.get())

    def copy_password(self):
        """Copy the password shown in password_label"""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.password_var.get())
        self.root.update()

    def generate_password(self):
        """generate a random password based on checkboxes and length sliders"""
        # Define character sets
        lowercase_chars = (
            string.ascii_lowercase if self.lowercase_check_var.get() else ""
        )
        uppercase_chars = (
            string.ascii_uppercase if self.uppercase_check_var.get() else ""
        )
        digit_chars = string.digits if self.digits_check_var.get() else ""
        special_chars = string.punctuation if self.specials_check_var.get() else ""

        length = int(self.total_length.get())
        min_puncts = int(self.min_specials.get())
        min_digits = int(self.min_numbers.get())

        # Check if minimum digit and special character requirements are met
        if length < min_digits + min_puncts:
            self.password_var.set(
                "Sum of min numbers and min specials\ncan not be larger than length!"
            )
            return

        # Check if at least one of the checkboxes is selected
        if not (lowercase_chars or uppercase_chars or digit_chars or special_chars):
            self.password_var.set("Check at least one of the boxes!")
            return

        # Calculate the number of characters to use from each set
        num_digits = (
            random.randint(
                min_digits, max(min_digits, length - min_puncts - length // 3)
            )
            if digit_chars
            else 0
        )
        num_specials = (
            random.randint(
                min_puncts, max(min_puncts, length - num_digits - length // 3)
            )
            if special_chars
            else 0
        )
        num_lowercase = (
            random.randint(0, length - num_digits - num_specials)
            if lowercase_chars
            else 0
        )
        num_uppercase = (
            random.randint(0, length - num_digits - num_specials - num_lowercase)
            if uppercase_chars
            else 0
        )

        # Generate the password
        password = (
            "".join(random.choices(lowercase_chars, k=num_lowercase))
            + "".join(random.choices(uppercase_chars, k=num_uppercase))
            + "".join(random.choices(digit_chars, k=num_digits))
            + "".join(random.choices(special_chars, k=num_specials))
        )

        # Fill in the remaining characters with a random choice from all available characters
        remaining_length = length - len(password)
        remaining_chars = (
            lowercase_chars + uppercase_chars + digit_chars + special_chars
        )
        password += "".join(random.choices(remaining_chars, k=int(remaining_length)))

        # Shuffle the password to make it random
        password_list = list(password)
        random.shuffle(password_list)
        self.password_var.set("".join(password_list))

    def about_me(self):
        """Display developer information and a QR code."""
        info_window = CTk.CTkToplevel(self.root)
        info_window.resizable(False, False)
        info_window.geometry("400x150")
        info_window.title("About Me")

        # Make the top-level window stay on top of the main window
        info_window.wm_attributes("-topmost", 1)

        qr_img = CTk.CTkImage(
            Image.open("assets/qrlight.png"),
            Image.open("assets/qrdark.png"),
            size=(140, 140),
        )
        CTk.CTkLabel(info_window, image=qr_img, text="", height=500, width=500).place(
            relx=0, rely=0.05, relheight=0.9, relwidth=0.5, anchor="nw"
        )
        CTk.CTkLabel(info_window, text=" Chamrobit ", font=("Pacifico", 18)).place(
            relx=0.7, rely=0.2, anchor="c"
        )
        CTk.CTkLabel(
            info_window, text="chamrobit@gmail.com", font=("Prompt Medium", 14)
        ).place(relx=0.7, rely=0.45, anchor="c")
        CTk.CTkLabel(
            info_window, text="chamrobit@outlook.com", font=("Prompt Medium", 14)
        ).place(relx=0.7, rely=0.6, anchor="c")
        CTk.CTkLabel(info_window, text="Version: 1.0.1", font=("Consolas", 14)).place(
            relx=0.7, rely=0.8, anchor="c"
        )


if __name__ == "__main__":
    window = CTk.CTk()
    app = PasswordGeneratorApp(window)
    window.mainloop()
