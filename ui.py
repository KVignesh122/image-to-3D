import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from run import convert_to_3d

file_path = ''

def open_image():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        # Load the image
        image = Image.open(file_path)
        width, height = image.size
        if width > height:
            fixed_size = (300, 200)  # Adjust the dimensions as needed
        else:
            fixed_size = (200, 300)
        resized_image = image.resize(fixed_size, Image.LANCZOS)
        # Display the image on the label
        img_label.image = ImageTk.PhotoImage(resized_image)
        img_label.config(image=img_label.image) 


def completion_msg(output_file):
    completion_window = tk.Toplevel(root)
    completion_window.title("Success")
    completion_label = tk.Label(completion_window, text=f"Conversion to 3D object completed. Saved to {output_file}")
    completion_label.pack(padx=20, pady=10)
    close_btn = tk.Button(completion_window, text="Close", command=completion_window.destroy)
    close_btn.pack(pady=5)
    return 


def process_image():
    global file_path
    if file_path == '':
        messagebox.showerror("Error", "Please select an image first.")
        return
    
    filename = text_entry.get()
    if '.' in str(filename):
        messagebox.showerror("Error", "Desired filename must not contain dots or file extension.\nNOTE: Inserting a desired filename is optional.")
        return
    
    v = selected_value.get()
    output_file = ''
    if v == "x":
        output_file = convert_to_3d(file_path, output_filename=filename)
    elif v == "Human":
        output_file = convert_to_3d(file_path, output_filename=filename, isHuman=True)
    elif v == "Full":
        output_file = convert_to_3d(file_path, output_filename=filename, isCloth=True)
    elif v == "Upper":
        output_file = convert_to_3d(file_path, output_filename=filename, isCloth=True, cloth_cat="upper")
    elif v == "Lower":
        output_file = convert_to_3d(file_path, output_filename=filename, isCloth=True, cloth_cat="lower")
    
    if output_file != '':
        return completion_msg(output_file)
    return  


# Create the main Tkinter window
root = tk.Tk()
root.title("2D Image to 3D Object Converter")

# Create a button to open the file dialog
upload_btn = tk.Button(root, text="Upload Image", command=open_image)
upload_btn.pack(pady=10)

# Create a label to display the uploaded image
img_label = tk.Label(root, text="[Uploaded image will be displayed here]")
img_label.pack()

selected_value = tk.StringVar(value="x")
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Create and pack the radio buttons in a row
radio_button = tk.Radiobutton(frame, text="Normal Convert", variable=selected_value, value="x")
radio_button.grid(row=0, column=0, padx=5)

radio_button = tk.Radiobutton(frame, text="Convert Human Only", variable=selected_value, value="Human")
radio_button.grid(row=0, column=1, padx=5)

radio_button = tk.Radiobutton(frame, text="Convert All Clothing Only", variable=selected_value, value="Full")
radio_button.grid(row=0, column=2, padx=5)

radio_button = tk.Radiobutton(frame, text="Convert Upper Clothing Only", variable=selected_value, value="Upper")
radio_button.grid(row=0, column=3, padx=5)

radio_button = tk.Radiobutton(frame, text="Convert Lower Clothing Only", variable=selected_value, value="Lower")
radio_button.grid(row=0, column=4, padx=5)

# Create a text field
text_label = tk.Label(root, text="Desired filename of generated 3D asset [OPTIONAL]:")
text_label.pack(pady=(20, 5))

text_entry = tk.Entry(root)
text_entry.pack()

# Create a button to create 3d object
upload_btn = tk.Button(root, text="Convert to 3D", command=process_image)
upload_btn.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
