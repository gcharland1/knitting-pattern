import cv2
import numpy as np

class ImageHandler:

    def __init__(self, save = False):
        self.work_dir = "./"
        self.image_file = None
        self.original_img = None
        self.resized_img = None
        self.resized_width = None
        self.recolored_img = None
        self.save = save

    def get_simplified_image(self, work_dir, image_file, width, colors = None):
        self.work_dir = work_dir
        self.image_file = image_file
        original_img = self.read_image(work_dir, image_file)
        resized_img = self.resize(original_img, width)
        if self.save:
            cv2.imwrite(f"{work_dir}resized_{image_file}", resized_img)

        if type(colors) == type(np.array([])):
            recolored_img = self.simplify_colors(resized_img, colors)
            if self.save:
                cv2.imwrite(f"{work_dir}recolored_{image_file}", recolored_img)

            return recolored_img

        return resized_img

    def read_image(self, dir, file):
        img = cv2.imread(dir + file)
        return img

    def resize(self, img, width = 0, height = 0):
        original_height, original_width, channels = img.shape

        if width == 0 and height == 0:
            print('At least one dimension is needed in order to resize')
            return
        elif width == 0:
            width = original_width  * height // original_height
        elif height == 0:
            height = original_height * width // original_width

        scale = [height/original_height, width/original_width]
        resized_img = cv2.resize(img, (0, 0), fx = scale[1], fy = scale[0], interpolation=cv2.INTER_NEAREST).astype(np.uint8)

        return resized_img

    def simplify_colors(self, img, colors):
        recolored_img = np.zeros(img.shape)
        height, width, channels = img.shape
        if width > 300:
            print('Working with large file. Might take a while...')

        n_colors = colors.shape[0]
        distance = np.zeros(n_colors)
        for i in range(height):
            for j in range(width):
                pixel = img[i][j]
                for c in range(n_colors):
                    dist = np.sqrt(np.sum(np.square(pixel - colors[c])))
                    distance[c] = dist

                index = np.where(distance == np.amin(distance))[0][0]
                recolored_img[i][j] = colors[index]

        return recolored_img.astype(np.uint8)

    def scale_image(self, img, scale):
        kron_dims = np.ones([scale, scale, 1])
        return np.kron(img, kron_dims)  # scales each axis by kron_dims value

    def add_lines(self, img, line_thickness, line_interval, color = np.array([0, 0, 0]), em_interval=10):
        img_height, img_width, channels = img.shape

        for r in range(line_interval, img_height, line_interval):
            lower_index = r - line_thickness // 2
            upper_index = lower_index + line_thickness
            img[lower_index:upper_index, :, :] = color

        for c in range(line_interval, img_width, line_interval):
            lower_index = c - line_thickness//2
            upper_index = lower_index + line_thickness
            img[:, lower_index:upper_index, :] = color

        return img

    def add_border(self, img, border_width, border_color = (0, 0, 0)):
        img_height, img_width, channels = img.shape
        border_img_shape = (img_height + 2*border_width, img_width + 2*border_width, channels)
        borders = np.zeros(border_img_shape) + border_color
        borders[border_width:-border_width,border_width:-border_width,:] = img
        return borders

    def add_stitch_labels(self, img, pattern_shape, pixel_size, padding, font=cv2.FONT_HERSHEY_SIMPLEX, font_size=1, font_color=(0, 0, 0), font_thickness=None):
        n_rows, n_stitches = pattern_shape
        img_height, img_width, _ = img.shape
        h_rows = np.zeros((pixel_size, pixel_size*n_stitches, 3)) + [255, 255, 255]
        y_pos = pixel_size - padding
        for s in range(n_stitches):
            x_pos = (s)*pixel_size + padding
            h_rows = cv2.putText(h_rows, str(s + 1), (x_pos, y_pos), font, font_size, font_color, font_thickness)

        img = np.insert(img, 0, h_rows, axis=0)
        img = np.insert(img, -1, h_rows, axis=0)

        img_height, img_width, _ = img.shape
        v_rows = np.zeros((pixel_size * (n_rows+2), pixel_size, 3)) + [255, 255, 255]
        x_pos = padding
        for r in range(n_rows):
            y_pos = (r + 2) * pixel_size - padding
            v_rows = cv2.putText(v_rows, str(r + 1), (x_pos, y_pos), font, font_size, font_color, font_thickness)

        v_rows = np.transpose(v_rows, (1, 0, 2))
        img = np.insert(img, 0, v_rows, axis=1)
        img = np.insert(img, -1, v_rows, axis=1)

        return img

    def generate_pattern_image(self, work_dir, img_file, n_stitches, colors, line_thk=2):
            print('Generating image')
            img = self.get_simplified_image(work_dir, img_file, n_stitches, colors)

            n_rows, _, _ = img.shape
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_size = 0.5
            font_thickness = None
            font_color = (0, 0, 0)
            text_padding = 3 + line_thk
            max_number = max(img.shape) + 1
            max_text_width, max_text_height = cv2.getTextSize(str(max_number), font, font_size, font_thickness)[0]
            pixel_width = max(max_text_width, max_text_height) + 2 * text_padding
            scaled_img = self.scale_image(img, pixel_width)
            border_img = self.add_stitch_labels(scaled_img, (n_rows, n_stitches), pixel_width, text_padding, font, font_size, font_color, font_thickness)

            _, _, channels = border_img.shape
            line_color = np.zeros(channels) + 100
            print('adding lines...')
            lined_img = self.add_lines(border_img, line_thk, pixel_width, line_color)

            pattern_img = lined_img.astype(np.uint8)
            cv2.imwrite(f"{work_dir}patron_{img_file}", pattern_img)

            return pattern_img, img

    def set_save(self, save):
        self.save = save

if __name__ == "__main__":
    handler = ImageHandler(True)
    c1 = [0, 0, 0]
    c2 = [0, 200, 0]
    c3 = [255, 255, 100]
    colors = np.array([c1, c2, c3])
    n_stitches = 150
    lines_img, simple_img = handler.generate_pattern_image('./input/', 'test.png', n_stitches, colors)
    print('Done!')