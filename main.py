# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from image_handler import ImageHandler
from pattern_writer import PatternWriter
import numpy as np
from PIL import ImageTk, Image
import tkinter
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import messagebox

class app:
    font_name = "Helvetica"
    font_size = "12"
    font = f"{font_name} {font_size}"
    bold_font = font + ' bold'
    button_font_color = "#eeeeee"
    button_color = "#333333"
    preview_width=300
    preview_height=300

    def __init__(self, path = "./"):
        self.work_dir = path
        self.file_name = ''
        self.handler = ImageHandler(False)
        self.writer = PatternWriter()
        self.color_palette_rgb = []
        self.color_palette_hex = []
        self.color_buttons = []
        self.colors = []

        self.plain_img = None
        self.has_previewed = False

        self.root = tkinter.Tk()
        self.setup_gui()
        self.root.mainloop()

    def setup_gui(self):
        self.root.minsize(350, 200)
        self.root.title("Générateur de patrons")
        self.input_frame = tkinter.Frame(self.root)
        self.preview_frame = tkinter.Frame(self.root, bg="#000000")
        self.output_frame = tkinter.Frame(self.root)

        self.file_section = tkinter.Frame(self.input_frame)
        self.file_label = tkinter.Label(self.file_section,
                                        font=self.font,
                                        text="Fichier de l'image: ")
        self.file_name_label = tkinter.Label(self.file_section,
                                             borderwidth=1,
                                             font=self.font,
                                             relief='sunken',
                                             justify=tkinter.LEFT,
                                             anchor='w',
                                             width=30,
                                             height=1,
                                             text='Sélectioner une image...')
        self.file_open_button = tkinter.Button(self.file_section,
                                               font=self.font,
                                               text='Ouvrir...',
                                               width=10,
                                               height=1,
                                               bg=self.button_color,
                                               fg=self.button_font_color,
                                               command=self.open_file)
        self.file_label.pack(side=tkinter.LEFT, padx=2, pady=3)
        self.file_name_label.pack(side=tkinter.LEFT, padx=2, pady=3)
        self.file_open_button.pack(side=tkinter.RIGHT, padx=2, pady=3)
        self.file_section.pack(fill="both", pady=5, padx=5)

        self.knitting_section = tkinter.Frame(self.input_frame)
        self.knitting_width_label = tkinter.Label(self.knitting_section,
                                                  font=self.font,
                                                  text="Nombre de mailles: ")
        self.knitting_width_entry = tkinter.Entry(self.knitting_section)
        self.knitting_width_label.pack(side=tkinter.LEFT, padx=2, pady=3)
        self.knitting_width_entry.pack(side=tkinter.LEFT, padx=2, pady=3)
        self.knitting_section.pack(fill="x", pady=5, padx=5)

        self.palette_section = tkinter.Frame(self.input_frame)
        self.instruction_label = tkinter.Label(self.palette_section,
                                               text="(Cliquer une couleur pour la supprimer)",
                                               font=self.font)
        self.add_color_button = tkinter.Button(self.palette_section,
                                               text='Ajouter une couleur',
                                               font=self.font,
                                               bg=self.button_color,
                                               fg=self.button_font_color,
                                               command=self.add_color)
        self.instruction_label.pack(side=tkinter.LEFT, fill="both", padx=3, pady=3)
        self.add_color_button.pack(side=tkinter.RIGHT, fill="both", padx=3, pady=3)
        self.palette_section.pack(fill="both", pady=5)

        self.color_palette_frame = tkinter.Frame(self.input_frame, height=15)
        self.color_palette_frame.pack(fill="both", padx=5, pady=3)

        self.compute_filler = tkinter.Label(self.output_frame)
        self.preview_button = tkinter.Button(self.output_frame,
                                             font=self.bold_font,
                                             fg=self.button_font_color,
                                             bg="#4040aa",
                                             text="Afficher l'appercu",
                                             command=self.show_preview)
        self.compute_button = tkinter.Button(self.output_frame,
                                             font=self.bold_font,
                                             fg=self.button_font_color,
                                             bg="#40aa40",
                                             text='Créer Patron',
                                             command=self.compute)
        self.save_files = tkinter.BooleanVar()
        self.save_files_checkbox = tkinter.Checkbutton(self.output_frame,
                                                       text="Enregistrer l'image du patron?",
                                                       font=self.font,
                                                       var=self.save_files)


        self.compute_filler.pack(fill="both", pady=3)
        self.preview_button.pack(anchor='e', padx=5, pady=10)
        self.save_files_checkbox.pack(side=tkinter.LEFT, padx=5)
        self.compute_button.pack(fill="both", side=tkinter.RIGHT, anchor='e', padx=5, pady=10)

        self.preview_canvas = tkinter.Canvas(self.preview_frame,
                                             width=self.preview_width,
                                             height=self.preview_height,
                                             bg="#101010",
                                             borderwidth=4)
        self.preview_canvas.pack(fill='both')

        self.input_frame.grid(column=0, row=0, sticky='nw')
        self.output_frame.grid(column=0, row=1, sticky='se')
        self.preview_frame.grid(column=1, row=0, rowspan=2)

    def open_file(self):
        path_to_file = filedialog.askopenfilename(initialdir=self.work_dir)
        self.file_name = path_to_file.split("/")[-1]
        self.work_dir = "/".join(path_to_file.split("/")[:-1]) + "/"
        self.file_name_label.config(text=self.file_name)

    def add_color(self):
        rgb, hex = colorchooser.askcolor()
        if not rgb == None:
            self.color_palette_rgb.append(rgb)
            self.color_palette_hex.append(hex)
            self.color_buttons.append(tkinter.Button(self.color_palette_frame,
                                                       bg=hex,
                                                       width=2,
                                                       height=1,
                                                       borderwidth=3,
                                                       relief='sunken',
                                                       command=lambda:self.delete_color(hex)))
            self.color_buttons[-1].pack(side=tkinter.LEFT, padx=3, pady=3)

    def delete_color(self, hex_color):
        index = self.color_palette_hex.index(hex_color)
        self.color_buttons[index].pack_forget()
        self.color_buttons.pop(index)
        self.color_palette_hex.pop(index)
        self.color_palette_rgb.pop(index)

    def show_preview(self):
        preview, n_stitches, colors = self.can_preview()
        if preview:
            self.handler.set_save(False)
            self.compute_image(n_stitches, colors)
            img = Image.fromarray(np.flip(self.plain_img, axis=2)).copy()
            w_scale = self.preview_width/img.width
            h_scale = self.preview_height/img.height
            scale = min(h_scale, w_scale)
            new_size = (int(img.width*scale), int(img.height*scale))
            img = img.resize(new_size, resample=0)
            tk_img = ImageTk.PhotoImage(image=img)
            if self.has_previewed:
                self.preview_canvas.itemconfig(self.preview_img_id, image=tk_img)
            else:
                self.preview_img_id = self.preview_canvas.create_image(self.preview_width//2, self.preview_height//2, image=tk_img)
                self.has_previewed = True

            self.preview_canvas.image = tk_img

    def can_preview(self):
        preview = True
        colors = None
        n_stitches = self.preview_width
        message = ''
        if self.file_name == '':
            message += "Aucun fichier d'ouvert.\n"
            preview = False
        else:
            if self.knitting_width_entry.get().isnumeric():
                n_stitches = int(self.knitting_width_entry.get())

            if np.shape(self.color_palette_rgb)[0] < 2:
                message += "Le pattron doit être composé d'au moins 2 couleurs.\n"
                message += "L'image sera affichée dans ses couleurs originales pour l'instant\n"
            else:
                colors = np.flip(np.array(self.color_palette_rgb, dtype='int32'))


        if not message == '':
            messagebox.showinfo("Erreur", message)

        return preview, n_stitches, colors

    def can_compute(self):
        compute = True
        message = ''
        if self.file_name == '':
            message += "Aucun fichier d'ouvert.\n"
            compute = False

        if not self.knitting_width_entry.get().isnumeric():
            message += "Le nombre de mailles doit être un chiffre.\n"
            compute = False

        if np.shape(self.color_palette_rgb)[0] < 2:
            message += "Le pattron doit être composé d'au moins 2 couleurs.\n"
            compute = False

        if not compute:
            messagebox.showinfo("Erreur", message)

        return compute

    def compute_image(self, n_stitches, colors):
        self.plain_img = self.handler.get_simplified_image(self.work_dir, self.file_name, n_stitches, colors)

    def compute(self):
        if self.can_compute():
            n_stitches = int(self.knitting_width_entry.get())
            colors = np.flip(np.array(self.color_palette_rgb, dtype='int32'))

            if self.save_files.get():
                self.pattern_image, self.plain_image = self.handler.generate_pattern_image(self.work_dir,
                                                                                           self.file_name, n_stitches,
                                                                                           colors)
            else:
                self.compute_image(n_stitches, colors)

            pattern_file_name = "patron_" + ".".join(self.file_name.split(".")[:-1])
            pattern_file = self.writer.write_pattern(self.plain_img, colors, self.work_dir, pattern_file_name)
            messagebox.showinfo('Terminé!', f'Pattron créé. Ouvrez {pattern_file} pour le consulter')

if __name__ == '__main__':
    app()
