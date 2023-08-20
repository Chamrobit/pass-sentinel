import random
import string
import customtkinter as CTk
from PIL import Image

# Window configurations
root = CTk.CTk()
root.minsize(500, 250)
root.geometry('600x300')
root.title('Pass Sentinel')
root.iconbitmap('locked.ico')

CTk.set_appearance_mode('system')
CTk.set_default_color_theme('green')

# Password frame and label
password_frame = CTk.CTkFrame(root)
password_frame.place(relx=0.05, rely=0.08, relheight=0.15, relwidth=0.82, anchor='nw')

password_var = CTk.StringVar(value='Your password will be shown here.')
password_label = CTk.CTkLabel(password_frame, textvariable=password_var, font=('Consolas', 14))
password_label.place(relx=0.01, rely=0.01, relheight=0.95, relwidth=0.98, anchor='nw')

# Copy button
def copy_password():
    """Copy the password shown in password_label"""
    root.clipboard_clear()
    root.clipboard_append(password_var.get())
    root.update()


copy_image = CTk.CTkImage(Image.open('copy.png'))
copy_button = CTk.CTkButton(root, command=copy_password, text='', image=copy_image)
copy_button.place(relx=0.88, rely=0.08, relheight=0.15, relwidth=0.09, anchor='nw')

# Checkboxes and check frame
check_frame = CTk.CTkFrame(root)
check_frame.place(relx=0.05, rely=0.3, relheight=0.6, relwidth=0.3, anchor='nw')


def create_checkbox(parent, var, text):
    """Set all default configurations for a checkbox"""
    checkbox = CTk.CTkCheckBox(parent, variable=var, onvalue=True, offvalue=False, checkbox_width=20,
                               checkbox_height=20, border_width=2, text=text, checkmark_color='black')
    return checkbox


def enable_digits():
    """enable or disable digits slider based on numbers checkbox"""
    if digits_check_var.get():
        min_numbers.configure(state='normal', button_color='#2FA572')
    else:
        min_numbers.configure(state='disable', button_color='gray')
        min_numbers.set(0)
        update_label(min_numbers, min_numbers_label, 'Min Numbers')


def enable_specials():
    """enable or disable specials slider based on specials checkbox"""
    if specials_check_var.get():
        min_specials.configure(state='normal', button_color='#2FA572')
    else:
        min_specials.configure(state='disable', button_color='gray')
        min_specials.set(0)
        update_label(min_specials, min_specials_label, 'Min Specials')


specials_check_var = CTk.BooleanVar(value=True)
digits_check_var = CTk.BooleanVar(value=True)
lowercase_check_var = CTk.BooleanVar()
uppercase_check_var = CTk.BooleanVar()

specials_box = create_checkbox(check_frame, specials_check_var, 'Specials #-$')
specials_box.place(relx=0.1, rely=0.12, anchor='nw')

digits_box = create_checkbox(check_frame, digits_check_var, 'Numbers 0-9')
digits_box.configure(command=enable_digits)
digits_box.place(relx=0.1, rely=0.32, anchor='nw')

lowercase_box = create_checkbox(check_frame, lowercase_check_var, 'Lowercase a-z')
specials_box.configure(command=enable_specials)
lowercase_box.place(relx=0.1, rely=0.54, anchor='nw')

uppercase_box = create_checkbox(check_frame, uppercase_check_var, 'Uppercase A-Z')
uppercase_box.place(relx=0.1, rely=0.76, anchor='nw')

# Sliders for lengths
slider_frame = CTk.CTkFrame(root)
slider_frame.place(relx=0.4, rely=0.3, relheight=0.4, relwidth=0.57, anchor='nw')


def update_label(slider, label, text):
    """Update labels according to slider values"""
    label.configure(text=f'{text}: {int(slider.get())}')
    if slider != total_length:
        slider.configure(to=total_length.get())


total_length = CTk.CTkSlider(slider_frame, from_=4, to=52, command=lambda e: update_label(total_length, total_length_label, 'Total Length'))
total_length.set(12)
total_length.place(relx=0.99, rely=0.12, relwidth=0.6, anchor='ne')

total_length_label = CTk.CTkLabel(slider_frame, text='Total Length: 12')
total_length_label.place(relx=0.05, rely=0.1, anchor='nw')

min_numbers = CTk.CTkSlider(slider_frame, from_=0, to=total_length.get(), command=lambda e: update_label(min_numbers, min_numbers_label, 'Min Numbers'))
min_numbers.set(3)
min_numbers.place(relx=0.99, rely=0.42, relwidth=0.6, anchor='ne')

min_numbers_label = CTk.CTkLabel(slider_frame, text='Min Numbers: 3')
min_numbers_label.place(relx=0.05, rely=0.4, anchor='nw')

min_specials = CTk.CTkSlider(slider_frame, from_=0, to=total_length.get(), command=lambda e: update_label(min_specials, min_specials_label, 'Min Specials'))
min_specials.set(3)
min_specials.place(relx=0.99, rely=0.72, relwidth=0.6, anchor='ne')

min_specials_label = CTk.CTkLabel(slider_frame, text='Min Specials: 3')
min_specials_label.place(relx=0.05, rely=0.7, anchor='nw')

# Password function and button
def generate_password():
    """generate a random password bassed on checkboxes and length sliders"""
    # Define character sets
    lowercase_chars = string.ascii_lowercase if lowercase_check_var.get() else ''
    uppercase_chars = string.ascii_uppercase if uppercase_check_var.get() else ''
    digit_chars = string.digits if digits_check_var.get() else ''
    special_chars = string.punctuation if specials_check_var.get() else ''

    length = int(total_length.get())
    min_puncts = int(min_specials.get())
    min_digits = int(min_numbers.get())

    # Check if minimum digit and special character requirements are met
    if length < min_digits + min_puncts:
        password_var.set('Sum of min numbers and min specials can not be larger than length!')
        return

    # Check if at least one of the checkboxes are selected
    if not (lowercase_chars or uppercase_chars or digit_chars or special_chars):
        password_var.set('Check at least one of the boxes!')
        return

    # Calculate the number of characters to use from each set
    num_digits = random.randint(min_digits, max(min_digits, length-min_puncts-length//3)) if digit_chars else 0
    num_specials = random.randint(min_puncts, max(min_puncts, length-num_digits-length//3)) if special_chars else 0
    num_lowercase = random.randint(0, length-num_digits-num_specials) if lowercase_chars else 0
    num_uppercase = random.randint(0, length-num_digits-num_specials-num_lowercase) if uppercase_chars else 0

    # Generate the password
    password = (
        ''.join(random.choices(lowercase_chars, k=num_lowercase)) +
        ''.join(random.choices(uppercase_chars, k=num_uppercase)) +
        ''.join(random.choices(digit_chars, k=num_digits)) +
        ''.join(random.choices(special_chars, k=num_specials))
    )

    # Fill in the remaining characters with a random choice from all available characters
    remaining_length = length - len(password)
    remaining_chars = lowercase_chars + uppercase_chars + digit_chars + special_chars
    password += ''.join(random.choices(remaining_chars, k=int(remaining_length)))

    # Shuffle the password to make it random
    password_list = list(password)
    random.shuffle(password_list)
    password_var.set(''.join(password_list))

generate_button = CTk.CTkButton(root, text='Generate Password', text_color='black', command=generate_password, font=('Calibri', 18))
generate_button.place(relx=0.4, rely=0.75, relwidth=0.45, relheight=0.15, anchor='nw')

# about me page
def about_me():
    info_window = CTk.CTkToplevel(root)
    info_window.resizable(False, False)
    info_window.geometry('400x150')
    info_window.title('About Me')

    qr_img = CTk.CTkImage(Image.open('qrlight.png'), Image.open('qrdark.png'), size=(140, 140))
    CTk.CTkLabel(info_window, image=qr_img, text='', height=500, width=500).place(relx=0, rely=0.05, relheight=0.9, relwidth=0.5, anchor='nw')
    CTk.CTkLabel(info_window, text=' Chamrobit ', font=('Pacifico', 18)).place(relx=0.7, rely=0.2, anchor='c')
    CTk.CTkLabel(info_window, text='chamrobit@gmail.com', font=('Prompt Medium', 14)).place(relx=0.7, rely=0.45, anchor='c')
    CTk.CTkLabel(info_window, text='chamrobit@outlook.com', font=('Prompt Medium', 14)).place(relx=0.7, rely=0.6, anchor='c')
    CTk.CTkLabel(info_window, text='Version: 1.0.0', font=('Consolas', 14)).place(relx=0.7, rely=0.8, anchor='c')

info_img = CTk.CTkImage(Image.open('info.png'))
info_button = CTk.CTkButton(root, command=about_me, text='', image=info_img)
info_button.place(relx=0.87, rely=0.75, relwidth=0.1, relheight=0.15, anchor='nw')

root.mainloop()
