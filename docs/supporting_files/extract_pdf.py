import fitz
from PIL import Image, ImageTk
import tkinter as tk

#change file path**
FILE_PATH = "sandbox/meeting_list.pdf"

with fitz.open(FILE_PATH) as doc:
    page = doc[0]

    (_, _, x_end, _) = page.cropbox

    names_rect = (198, 590, 600, 784)
    emails_rect = (198, 380, 600, 581)
    duration_rect = (93, 90, 114, 161)
    course_cod_rect = (65, 50, 88, 145)
    training_name_rect = (65, 245, 88, 742)
    company_name_rect = (90, 245, 115, 764)
    instructor_name_rect = (118, 245, 135, 767)
    dates_rect = (156, 20, 177, 380)

    # Creates rectangles
    # rects = page.search_for("Rúbrica")
    rects = [duration_rect]

    for rect in rects:
        print(rect)
        # adds anotation so we can display later
        page.add_rect_annot(rect)
    
    pix = page.get_pixmap()


# start tkinter and display rectangles created above
root = tk.Tk()
# set the mode depending on alpha
mode = "RGBA" if pix.alpha else "RGB"
img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
tkimg = ImageTk.PhotoImage(img)
l = tk.Label(image=tkimg)
l.pack()

root.mainloop()
