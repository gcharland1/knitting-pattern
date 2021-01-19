class PatternWriter:

    def __init__(self, work_dir = "/", file_name = 'Patron.html'):
        self.file_name = file_name
        self.work_dir = work_dir

    def get_color_index(self, pixel, colors):
        index = 0
        for c in colors:
            if (pixel == c).all():
                return index
            index += 1

    def set_output_file_name(self, output_name):
        if len(output_name.split('.')) > 1:
            output_name = '.'.join([output_name.split('.'), 'html'])

        self.file_name = output_name + '.html'

    def write_html_headers(self):
        with open(self.work_dir + self.file_name, 'w') as pattern:
            pattern.write('<html style="font-family:Helvetica;">\n<body>\n')

    def write_html_footers(self):
        with open(self.work_dir + self.file_name, 'a') as pattern:
            pattern.write('</body>\n</html>\n')

    def write_pattern_header(self, bgr_colors, row_count, stitch_count):
        color_letters = []
        for i in range(bgr_colors.shape[0]):
            color_letters.append(chr(65 + i))


        with open(self.work_dir + self.file_name, 'a') as pattern:
            pattern.write("<h1>Détails de l'ouvrage</h1>\n")
            pattern.write(f'<h4>Nombre de mailles: {stitch_count}</h4>')
            pattern.write(f'<h4>Nombre de rangs: {row_count}</h4>')
            pattern.write("<h4>Couleurs de l'ouvrage</h4>\n<ul>\n")
            for c in range(bgr_colors.shape[0]):
                b, g, r = bgr_colors[c]
                color_box = f'<span style="background-color:rgb({r},{g},{b});color:rgb({r},{g},{b});">CETTE COULEUR</span>'
                pattern.write(f"<li><b>{color_letters[c]}</b> = {color_box}</li>\n")
            pattern.write('</ul>\n<hr><hr>')

        return color_letters

    def write_pattern_rows(self, img, colors, color_letters):
        with open(self.work_dir + self.file_name, 'a') as pattern:
            pattern.write("<h1>L'ouvrage, rang par rang</h1>")
            pattern_width = img.shape[1]
            row_count = 0
            for row in img[::-1]:
                row_count += 1
                pattern_line = f"<p><b>R.{str(row_count).ljust(6)}: </b>"
                stitch_count = 0
                color = row[0]
                letter = color_letters[self.get_color_index(color, colors)]
                index = 0
                while index < pattern_width:
                    if (row[index] == color).all():
                        stitch_count += 1
                        index += 1
                    else:
                        pattern_line += f"<b>{letter}:</b> {stitch_count}m. ,"
                        color = row[index]
                        letter = color_letters[self.get_color_index(color, colors)]
                        stitch_count = 0

                pattern_line += f"<b>{letter}:</b> {stitch_count}m."
                pattern.write(pattern_line + "\n")

    def write_pattern(self, img, colors, output_dir="", output_file=""):
        if not output_dir == "":
            self.work_dir = output_dir
        if not output_file == "":
            self.set_output_file_name(output_file)

        n_rows, n_stitches, _ = img.shape
        self.write_html_headers()
        color_letters = self.write_pattern_header(colors, n_rows, n_stitches)
        self.write_pattern_rows(img, colors, color_letters)
        self.write_html_footers()
        return self.file_name


