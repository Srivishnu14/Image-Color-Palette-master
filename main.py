# -------------------//// Note input pdf should contain text less than 2000 characters////-------------------#

# Environment variables
import os
import shutil

# for saving file locally in server
from werkzeug.utils import secure_filename

# Flask App
from flask import Flask, render_template, request

from colorthief import ColorThief

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')

file_name = None


def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":

        try:
            os.makedirs("static/file/")
        except FileExistsError:
            pass
        else:
            pass
        finally:
            data = request.files["file"]
            file_name = secure_filename(data.filename)
            data.save(os.path.join("static/file/", file_name))

            color_thief = ColorThief(f'static/file/{file_name}')
            dominant_color = color_thief.get_color(quality=1)
            palette = color_thief.get_palette(color_count=11)
            # print(dominant_color)
            # print(palette)

            hex_values = []
            for i in palette:
                value = rgb_to_hex(i[0], i[1], i[2])
                hex_values.append(value)
            # print(hex_values)
            return render_template("index.html", show=True, image=file_name, palette=palette, hex=hex_values,len=len(palette))

    try:
        shutil.rmtree('static/')
    except FileExistsError:
        pass
    else:
        print("delete")
        print("1")
    finally:
        return render_template("index.html", show=False)


if __name__ == "__main__":
    app.run(debug=False)
