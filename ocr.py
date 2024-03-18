import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import boto3

my_w = tk.Tk()
my_w.geometry("450x400")
my_w.title("AWS Textract")

l1 = tk.Label(my_w, text="Upload an Image", width=30, font=('times', 18, 'bold'))
l1.pack()

def upload_file():
    # Initialize AWS Textract client
    aws_mag_con = boto3.session.Session(profile_name="Aditya")
    client = aws_mag_con.client(service_name='textract', region_name='us-east-1')

    # Open file dialog to select image
    f_types = [('Jpg Files', "*.jpg")]
    filename = filedialog.askopenfilename(filetypes=f_types)
    if not filename:
        return  # User canceled selection

    # Open image
    img = Image.open(filename)

    # Resize image
    img_resized = img.resize((400, 200))

    # Convert image to PhotoImage for displaying in tkinter
    img_tk = ImageTk.PhotoImage(img_resized)

    # Display image
    b2 = tk.Button(my_w, image=img_tk)
    b2.image = img_tk  # Keep a reference to prevent garbage collection
    b2.pack()

    # Get image bytes
    with open(filename, 'rb') as imgfile:
        imgbytes = imgfile.read()

    # Call Textract to detect text
    response = client.detect_document_text(Document={'Bytes': imgbytes})
    for item in response['Blocks']:
        if item['BlockType'] == "WORD":
            print(item['Text'])

# Button to trigger file upload and text detection
b1 = tk.Button(my_w, text="Upload File & See what it has!!!", width=30, command=upload_file)
b1.pack()

my_w.mainloop()