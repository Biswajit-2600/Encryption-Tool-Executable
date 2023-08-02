import ctypes
import os
import sys
import webbrowser
from pathlib import Path
from tkinter import *
from tkinter import messagebox, filedialog
from Steganography_Tools_master import (crypt, genkeys)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Dev\Python_Projects\Encryption_Tool_Windows\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def on_entry_focus_in(event):
    if entry.get() == placeholder_text:
        entry.delete(0, END)
        entry.config(fg='#071952')


def on_entry_focus_out(event):
    if not entry.get():
        entry.insert(0, placeholder_text)
        entry.config(fg='#071952')


def perform_action():
    input_string = entry.get()
    if input_string and input_string != placeholder_text:
        return input_string
    else:
        messagebox.showwarning("No Username!", "Please enter a username to generate keys!")


def perform_pop_up_action(this_entry, this_window):
    input_string = this_entry.get()
    if input_string and input_string != placeholder_text:
        return input_string
    else:
        messagebox.showwarning("Empty Input!", "Please enter a Choice!")
        this_window.destroy()
        ask_file_choice()


selected_file = False
key_selected_file = False


def validate_file():
    global selected_file
    if selected_file:
        return selected_file
    else:
        messagebox.showwarning("No File!", "Please select a file to encrypt!")


def make_key_files(user_name, key_size=1024):
    directory_window = Tk()
    directory_window.withdraw()

    selected_directory = filedialog.askdirectory()
    if not selected_directory:
        return "directory_not_selected"

    pub_file_path = f"{selected_directory}/{user_name}.pub"
    prv_file_path = f"{selected_directory}/{user_name}.prv"

    if os.path.exists(pub_file_path) and os.path.exists(prv_file_path):
        return "FileExistsError#path#%s#path#%s" % (pub_file_path, prv_file_path)
    else:
        genkeys.write_to_files(pub_file_path, prv_file_path, key_size)
        return ""


def register_file_choice(this_entry, this_window):
    global selected_file
    choice = perform_pop_up_action(this_entry, this_window)
    this_window.destroy()
    if choice == "1":
        selected_file = filedialog.askopenfilename(title="Choose File!")
        if selected_file:
            update_upload_data(selected_file)
        else:
            messagebox.showwarning("No File Selected!", "You have not selected any file!")
    elif choice == "2":
        open_key_file_dialog()
    else:
        messagebox.showwarning("Wrong Input!", "Input does NOT match any of the choices!")
        register_file_choice(this_entry, this_window)


def register_stego_choice(this_entry, this_window, val, file_type):
    choice = perform_pop_up_action(this_entry, this_window)
    this_window.destroy()
    if choice == "1":
        messagebox.showinfo("Select File!", "Select Image File in which data is to be encrypted!")
        stego_img_file = filedialog.askopenfilename(title="Select File!")
        crypt.encode_img_data(val, file_type, stego_img_file)
        messagebox.showinfo("Success!", "Message successfully Decrypted!")
    elif choice == "2":
        messagebox.showinfo("Select File!", "Select Text File in which data is to be encrypted!")
        stego_txt_file = filedialog.askopenfilename(title="Select File!")
        crypt.encode_txt_data(val, file_type, stego_txt_file)
        messagebox.showinfo("Success!", "Message successfully Decrypted!")
    elif choice == "3":
        messagebox.showinfo("Select File!", "Select Audio File in which data is to be encrypted!")
        stego_aud_file = filedialog.askopenfilename(title="Select File!")
        crypt.encode_aud_data(val, file_type, stego_aud_file)
        messagebox.showinfo("Success!", "Message successfully Decrypted!")
    elif choice == "4":
        messagebox.showinfo("Select File!", "Select Video File in which data is to be encrypted!")
        stego_vid_file = filedialog.askopenfilename(title="Select File!")
        crypt.encode_vid_data(val, file_type, stego_vid_file)
        messagebox.showinfo("Success!", "Message successfully Decrypted!")
    else:
        messagebox.showwarning("Wrong Input!", "Input does NOT match any of the choices!")
        register_file_choice(this_entry, this_window)


def ask_file_choice():
    input_window = Tk()
    input_window.title("Choose File!")
    input_window_width = 500
    input_window_height = 300

    input_x = (screen_width / 2) - (input_window_width / 2)
    input_y = (screen_height / 2) - (input_window_height / 2)

    input_window.geometry(f'{input_window_width}x{input_window_height}+{int(input_x)}+{int(input_y)}')

    label = Label(input_window, text="Choose File to Upload:\n1. File to Encrypt\n2. Key File",
                  font=("Inter Black", 20 * -1))
    label.pack()

    this_entry = Entry(input_window, font=custom_font)
    this_entry.place(x=175, y=80, width=160, height=20)
    ok_button = Button(input_window, text="Ok", command=lambda: register_file_choice(this_entry, input_window))
    ok_button.place(x=180, y=110, width=70, height=20)
    cancel_button = Button(input_window, text="Cancel", command=lambda: input_window.destroy())
    cancel_button.place(x=260, y=110, width=70, height=20)

    input_window.mainloop()


def ask_stego_choice(val, file_type):
    input_window = Tk()
    input_window.title("Choose File!")
    input_window_width = 500
    input_window_height = 300

    input_x = (screen_width / 2) - (input_window_width / 2)
    input_y = (screen_height / 2) - (input_window_height / 2)

    input_window.geometry(f'{input_window_width}x{input_window_height}+{int(input_x)}+{int(input_y)}')

    label = Label(input_window, text="***** CHOOSE THE STEGANOGRAPHY TECHNIQUE *****\n"
                                     "\n1. IMAGE STEGANOGRAPHY {Hiding Data in Image cover file}"
                                     "\n2. TEXT STEGANOGRAPHY {Hiding Data in Text cover file}"
                                     "\n3. AUDIO STEGANOGRAPHY {Hiding Data in Audio cover file}"
                                     "\n4. VIDEO STEGANOGRAPHY {Hiding Data in Video cover file}",
                  font=("Inter Black", 15 * -1))
    label.pack()

    this_entry = Entry(input_window, font=custom_font)
    this_entry.place(x=175, y=120, width=160, height=20)
    ok_button = Button(input_window, text="Ok",
                       command=lambda: register_stego_choice(this_entry, input_window, val, file_type))
    ok_button.place(x=180, y=150, width=70, height=20)
    cancel_button = Button(input_window, text="Cancel", command=lambda: input_window.destroy())
    cancel_button.place(x=260, y=150, width=70, height=20)

    input_window.mainloop()


def generate_keys():
    name = perform_action()
    try:
        if name is not None:
            paths = make_key_files(name).split("#path#")
            if "directory_not_selected" in paths:
                messagebox.showwarning("No Directory Selected!",
                                       "You have not chosen any directory for saving the Key Files!")
                return
            elif "FileExistsError" in paths:
                confirm = messagebox.askyesno("Files Already Exist!",
                                              "The Key Files for the Given Username "
                                              "already exist in the Chosen Directory!\n"
                                              "Do you want to OVERWRITE the Key Files?")
                if confirm:
                    genkeys.write_to_files(paths[1], paths[2])
                else:
                    return
            messagebox.showinfo("Keys Generated Successfully!",
                                "\n Public and Private Key Files generated Successfully!\n"
                                "\n Files have been stored in the Chosen Directory\n"
                                "\n Keep the Private Key \"SAFE\" and \"SECRET\"\n"
                                "\n Share Public Key to perform Encryption and Decryption")
    except Exception as e:
        messagebox.showerror("Error!", "The following Error was encountered while generating keys: %s" % e)
        return


def encrypt_file():
    up_file = validate_file()
    pub_key_path = key_selected_file

    try:
        if selected_file and key_selected_file:
            canvas.update_idletasks()
            encrypt_val, file_type = crypt.encrypt(pub_key_path, up_file)
            ask_stego_choice(encrypt_val.hex(), file_type)
            crypt.stego_encrypt_choices(encrypt_val.hex(), file_type)
        else:
            messagebox.showwarning("No Key File!", "Please provide the Key File!")
    except Exception as e:
        messagebox.showerror("Error!", "The following Error was encountered while encryption/decryption: %s" % e)
        return


def decrypt_file():
    pass
    # up_file = validate_file()
    # try:
    #     if selected_file:
    #         crypt.encrypt()
    # except Exception as e:
    #     messagebox.showerror("Error!", "The following Error was encountered while encryption/decryption: %s" % e)
    #     return


def update_upload_data(file_path):
    file_name = file_path.split("/")[-1]
    change_image = PhotoImage(
        file="assets/frame0/file_change.png")
    display_text = "File : %s" % file_name
    canvas.itemconfig(up_image, image=change_image)
    canvas.change_image = change_image
    canvas.itemconfig(up_rectangle_text, text=display_text, fill="#CEE6F3",
                      font=("Inter Black", 15 * 1),
                      width=300,
                      justify=LEFT,
                      tags="updated_text")


def update_key_file_data(pub_file_path):
    pub_file_name = pub_file_path.split("/")[-1]
    canvas.itemconfig(key_file_text, text="Key File : %s" % pub_file_name, fill="#CEE6F3",
                      font=("Inter Black", 15 * 1),
                      width=300,
                      justify=LEFT,
                      tags="updated_text")


def open_update_file_dialog():
    global selected_file
    selected_file = filedialog.askopenfilename(title="Choose File!")
    if selected_file:
        update_upload_data(selected_file)


def open_key_file_dialog():
    global key_selected_file
    if not key_selected_file:
        pub_key_path = filedialog.askopenfilename(title="Choose Key File!")
        key_selected_file = pub_key_path
        if pub_key_path:
            update_key_file_data(pub_key_path)
            return pub_key_path


def open_file_dialog(event):
    global selected_file
    if not selected_file or not key_selected_file:
        ask_file_choice()
    else:
        confirm_new_file = messagebox.askyesno("Files Already Selected!",
                                               "Files have already been selected.\n"
                                               "Do you want to select Another File?")
        if confirm_new_file:
            ask_file_choice()


def erase_word(event):
    text = entry.get()

    index = entry.index(INSERT)
    while index > 0 and text[index - 1] != ' ':
        index -= 1

    entry.delete(index, INSERT)


def create_rounded_rectangle(this_canvas, x1, y1, x2, y2, this_corner_radius, **kwargs):
    this_canvas.create_arc(x1, y1, x1 + 2 * this_corner_radius, y1 + 2 * this_corner_radius,
                           start=90, extent=90, **kwargs)
    this_canvas.create_arc(x2 - 2 * this_corner_radius, y1, x2, y1 + 2 * this_corner_radius,
                           start=0, extent=90, **kwargs)
    this_canvas.create_arc(x1, y2 - 2 * this_corner_radius, x1 + 2 * this_corner_radius, y2,
                           start=180, extent=90, **kwargs)
    this_canvas.create_arc(x2 - 2 * this_corner_radius, y2 - 2 * this_corner_radius, x2, y2,
                           start=270, extent=90, **kwargs)
    this_canvas.create_rectangle(x1 + this_corner_radius, y1, x2 - this_corner_radius, y2, **kwargs)
    this_canvas.create_rectangle(x1, y1 + this_corner_radius, x2, y2 - this_corner_radius, **kwargs)


def open_link(event):
    webbrowser.open("https://biswajit-2600.github.io/Encryption-Tool/")


def on_close():
    window.destroy()
    sys.exit(0)


window = Tk()

app_width = 800
app_height = 600

screen_height = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)

custom_font = ("Helvetica", 15, "bold")

window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
window.configure(bg="#FFFFFF")
window.title('Encryption Tool')
icon = PhotoImage(file="assets/favicon-32x32-black.png")
window.iconphoto(True, icon)

my_app_id = 'my_company.my_product.sub_product.version'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=600,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_bg_image = PhotoImage(
    file=relative_to_assets("bg_image.png"))
bg_image = canvas.create_image(
    400.0,
    300.0,
    image=image_bg_image
)

canvas.create_text(
    251.0,
    30.0,
    anchor="nw",
    text="** WELCOME **",
    fill="#CEE6F3",
    font=("Inter Black", 36 * -1)
)

canvas.create_rectangle(
    46.0,
    79.0,
    750.0,
    83.0,
    fill="#CEE6F3",
    outline="")

up_rectangle = canvas.create_rectangle(
    370.0,
    128.0,
    750.0,
    418.0,
    fill="#1D5D9B",
    outline="#CEE6F3",
    dash=(10, 10),
    width=5
)

canvas.tag_bind(up_rectangle, '<Enter>', lambda event: canvas.config(cursor="hand2"))
canvas.tag_bind(up_rectangle, '<Leave>', lambda event: canvas.config(cursor=""))
canvas.tag_bind(up_rectangle, '<Button-1>', open_file_dialog)

image_up_image = PhotoImage(
    file="assets/frame0/up_image.png")
up_image = canvas.create_image(
    560.0,
    230.0,
    image=image_up_image
)

canvas.tag_bind(up_image, '<Enter>', lambda event: canvas.config(cursor="hand2"))
canvas.tag_bind(up_image, '<Leave>', lambda event: canvas.config(cursor=""))
canvas.tag_bind(up_image, '<Button-1>', open_file_dialog)

button_image_1 = PhotoImage(
    file="assets/frame0/decrypt_btn.png")

decrypt_btn = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: decrypt_file(),
    cursor="hand2",
    relief="flat"
)
decrypt_btn.place(
    x=46.0,
    y=360.0,
    width=250.0,
    height=55.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("encrypt_btn.png"))
encrypt_btn = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: encrypt_file(),
    cursor="hand2",
    relief="flat"
)
encrypt_btn.place(
    x=46.0,
    y=292.0,
    width=250.0,
    height=55.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("gen_keys_btn.png"))
gen_keys_btn = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: generate_keys(),
    cursor="hand2",
    relief="flat"
)
gen_keys_btn.place(
    x=46.0,
    y=121.0,
    width=250.0,
    height=55.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    175.0,
    224.5,
    image=entry_image_1
)
placeholder_text = "ENTER USERNAME"
entry = Entry(
    bd=0,
    bg="#75C2F6",
    fg="#071952",
    font=custom_font,
    highlightthickness=0
)
entry.place(
    x=77.5,
    y=197.0,
    width=195.0,
    height=53.0
)
entry.insert(0, placeholder_text)
entry.bind("<FocusIn>", on_entry_focus_in)
entry.bind("<FocusOut>", on_entry_focus_out)
entry.bind("<Control-BackSpace>", erase_word)

up_rectangle_text = canvas.create_text(
    400.0,
    310.0,
    anchor="nw",
    text="Drag & Drop / Click to Upload File",
    fill="#CEE6F3",
    font=("Inter Black", 15 * 1),
    width=300
)

key_file_text = canvas.create_text(
    400.0,
    370.0,
    anchor="nw",
    text="",
    fill="#CEE6F3",
    font=("Inter Black", 15 * 1),
    width=300
)

canvas.tag_bind(key_file_text, '<Enter>', lambda event: canvas.config(cursor="hand2"))
canvas.tag_bind(key_file_text, '<Leave>', lambda event: canvas.config(cursor=""))
canvas.tag_bind(key_file_text, '<Button-1>', open_file_dialog)

canvas.tag_bind(up_rectangle_text, '<Enter>', lambda event: canvas.config(cursor="hand2"))
canvas.tag_bind(up_rectangle_text, '<Leave>', lambda event: canvas.config(cursor=""))
canvas.tag_bind(up_rectangle_text, '<Button-1>', open_file_dialog)

corner_radius = 20
create_rounded_rectangle(
    canvas,
    50.0,
    484.0,
    750.0,
    571.0,
    corner_radius,
    fill="#75C2F6",
    outline="")

canvas.create_text(
    225.0,
    500.0,
    anchor="nw",
    text="GUI design by Biswajit Panda \u00A9 2023.",
    fill="#071952",
    font=("Eloqua Display", 15 * 1)
)

canvas.create_text(
    190.0,
    530.0,
    anchor="nw",
    text="To use the Web Version of this app, ",
    fill="#071952",
    font=("Eloqua Display", 15 * 1)
)

click_text = canvas.create_text(
    510.0,
    530.0,
    anchor="nw",
    text="click here.",
    fill="#001AFF",
    font=("Eloqua Display", 15 * 1)
)

canvas.tag_bind(click_text, '<Enter>', lambda event: canvas.config(cursor="hand2"))
canvas.tag_bind(click_text, '<Leave>', lambda event: canvas.config(cursor=""))
canvas.tag_bind(click_text, "<Button-1>", open_link)

window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()
