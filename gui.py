import ctypes
import subprocess
from pathlib import Path
from tkinter import *
from tkinter import messagebox

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Dev\Python_Projects\Encryption Tool Windows\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


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
icon = PhotoImage(file="assets/favicon-32x32.png")
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
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    400.0,
    300.0,
    image=image_image_1
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

canvas.create_rectangle(
    370.0,
    128.0,
    750.0,
    418.0,
    fill="#1D5D9B",
    outline="#CEE6F3",
    dash=(10, 10),
    width=5
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    560.0,
    251.0,
    image=image_image_2
)

button_image_1 = PhotoImage(
    file="assets/frame0/button_1.png")
img_label = Label(image=button_image_1)

button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=46.0,
    y=360.0,
    width=250.0,
    height=55.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=46.0,
    y=292.0,
    width=250.0,
    height=55.0
)


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


def generate_keys():
    name = perform_action()
    try:
        subprocess.run(["python", "Steganography-Tools-master/genkeys.py", name, "0"], check=True,
                       stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode().strip()
        if "Errno 2" in error_message:
            messagebox.showerror("File Not Found!", "The Program for the generating the Key Files was NOT FOUND!")
            return
        elif "FileExistsError" in error_message:
            confirm = messagebox.askyesno("Files Already Exist!",
                                          "The Key Files for the Given Username already exist!\n"
                                          "Do you want to OVERWRITE the Key Files?")
            if confirm:
                subprocess.run(["python", "Steganography-Tools-master/genkeys.py", name, "1"], check=True,
                               stderr=subprocess.PIPE)
            else:
                return
    except TypeError:
        return
    except Exception as e:
        messagebox.showerror("Error!", "The Following Error was encountered : %s" % e)
        return
    messagebox.showinfo("Keys Generated Successfully!",
                        "\n Public and Private Key Files generated Successfully!\n"
                        "\n Files have been stored in the Chosen Directory\n"
                        "\n Keep the Private Key \"SAFE\" and \"SECRET\"\n"
                        "\n Share Public Key to perform Encryption and Decryption")


def erase_word(event):
    text = entry.get()

    index = entry.index(INSERT)
    while index > 0 and text[index - 1] != ' ':
        index -= 1

    entry.delete(index, INSERT)


button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: generate_keys(),
    relief="flat"
)
button_3.place(
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

canvas.create_text(
    415.0,
    352.0,
    anchor="nw",
    text="Drag & Drop / Upload File",
    fill="#CEE6F3",
    font=("Inter Black", 25 * -1)
)


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
    text="To use the web version of this app, click here.",
    fill="#071952",
    font=("Eloqua Display", 15 * 1)
)
window.resizable(False, False)
window.mainloop()
