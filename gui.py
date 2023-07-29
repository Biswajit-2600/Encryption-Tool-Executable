import ctypes
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


selected_file = False


def validate_file():
    global selected_file
    if selected_file:
        return selected_file
    else:
        messagebox.showwarning("No File!", "Please select a file to encrypt!")


def generate_keys():
    name = perform_action()
    try:
        # subprocess.run(["python", "Steganography_Tools_master/genkeys.py", name, "0"], check=True,
        #                stderr=subprocess.PIPE)
        if name is not None:
            paths = genkeys.make_key_files(name).split("#path#")
            # except subprocess.CalledProcessError as e:
            #     error_message = e.stderr.decode().strip().split("#path#")
            #     print(error_message)
            # if "Errno 2" in error_message[0]:
            #     messagebox.showerror("File Not Found!", "The Program for the generating the Key Files was NOT FOUND!")
            #     return
            if "directory_not_selected" in paths:
                messagebox.showwarning("No Directory Selected!",
                                       "You have not chosen any directory for saving the Key Files!")
                return
            elif "FileExistsError" in paths:
                confirm = messagebox.askyesno("Files Already Exist!",
                                              "The Key Files for the Given Username already exist!\n"
                                              "Do you want to OVERWRITE the Key Files?")
                if confirm:
                    # subprocess.run(
                    # ["python", "Steganography_Tools_master/genkeys.py", name, "1", error_message[1],
                    # error_message[2]],
                    #     check=True,
                    #     stderr=subprocess.PIPE)
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
    try:
        if selected_file:
            crypt.encrypt()
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


def update_up_image(path):
    file_name = path.split("/")[-1]
    change_image = PhotoImage(
        file="assets/frame0/file_change.png")
    display_text = "File Selected : %s" % file_name
    canvas.itemconfig(up_image, image=change_image)
    canvas.change_image = change_image
    canvas.itemconfig(up_rectangle_text, text=display_text, fill="#CEE6F3",
                      font=("Inter Black", 15 * 1),
                      width=300,
                      justify=LEFT,
                      tags="updated_text")


def open_file_dialog(event):
    global selected_file
    selected_file = filedialog.askopenfilename()
    if selected_file:
        update_up_image(selected_file)
    else:
        messagebox.showwarning("No File Selected!", "You have not selected any file!")


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
    415.0,
    330.0,
    anchor="nw",
    text="Drag & Drop / Click to Upload File",
    fill="#CEE6F3",
    font=("Inter Black", 15 * 1),
    width=300
)

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
    170.0,
    500.0,
    anchor="nw",
    text="The Decrypted File will be saved in the chosen folder.",
    fill="#071952",
    font=("Eloqua Display", 15 * 1)
)

canvas.create_text(
    200.0,
    530.0,
    anchor="nw",
    text="To use the web version of this app, ",
    fill="#071952",
    font=("Eloqua Display", 15 * 1)
)

click_text = canvas.create_text(
    512.0,
    530.0,
    anchor="nw",
    text="click here.",
    fill="#001AFF",
    font=("Eloqua Display", 15 * 1)
)

canvas.tag_bind(click_text, '<Enter>', lambda event: canvas.config(cursor="hand2"))
canvas.tag_bind(click_text, '<Leave>', lambda event: canvas.config(cursor=""))
canvas.tag_bind(click_text, "<Button-1>", open_link)


def on_close():
    window.destroy()
    sys.exit(0)


window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()
