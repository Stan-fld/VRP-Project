from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas

from pdf.RoadMap import remove_img


class StatMap:
    file_name = "stats"
    canvas: Canvas
    offset = 800

    def __init__(self, file_name):
        self.file_name = file_name
        self.canvas = canvas.Canvas(f"{self.file_name}.pdf")

    def next_page(self):
        self.canvas.showPage()
        self.offset = 800

    def has_enough_room(self, height):
        return self.offset - height > 0

    def adjust_offset(self, added_height):
        if self.offset - added_height < 20:
            self.canvas.showPage()
            self.offset = 800
        else:
            self.offset -= added_height

    def add_img(self, fn):
        if self.has_enough_room(4 * inch):
            self.canvas.drawImage(f'{fn}.jpg', 0, self.offset - 4 * inch, height=4 * inch, preserveAspectRatio=True,
                                  mask='auto')
            remove_img(fn)
            self.adjust_offset(4 * inch+20)
        else:
            self.adjust_offset(4 * inch)
            self.add_img(fn)

    def add_txt(self, txt, centered=False):
        if self.has_enough_room(20):
            self.canvas.drawString(100, self.offset, txt)
            self.adjust_offset(20)
        else:
            self.adjust_offset(20)
            self.add_txt(txt, centered)

    def save(self):
        self.canvas.save()

