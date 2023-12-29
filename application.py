from tkinter import *
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import Tk, PhotoImage, ttk, Toplevel
from PIL import Image, ImageTk
import os
from stegano import lsb
from PIL import Image, ImageTk

def open_text_encryption_window():
    #Window Setup
    text_window = tk.Tk()
    text_window.title("Text Encryption")
    text_window.geometry("700x500+250+180")
    text_window.resizable(False,False)

    def atbash_cipher(text):
        result = ""
        for char in text:
            if char.isalpha():
                base = 'a' if char.islower() else 'A'
                end = 'z' if char.islower() else 'Z'
                mirrored_char = chr(ord(end) - (ord(char) - ord(base)))
                result += mirrored_char
            else:
                result += char
        return result
    
    def caesar_cipher(text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                base = 'a' if char.islower() else 'A'
                result += chr((ord(char) - ord(base) + shift) % 26 + ord(base))
            else:
                result += char
        return result
    
    def on_cipher_choice():
        choice = cipher_var.get()
        if choice == 'Caesar':
            show_caesar_key_entry()
        elif choice == 'Atbash':
            show_atbash_button()
        else:
            messagebox.showinfo("Info", "Please choose 'Caesar' or 'Atbash'.")

        
    def show_caesar_key_entry():
        key_window = tk.Toplevel(text_window)
        key_window.title("Enter Caesar Key")

        # Set the position of the key entry window
        x_position = text_window.winfo_x() + 50  # You can adjust this value based on your preference
        y_position = text_window.winfo_y() + 50  # You can adjust this value based on your preference
        key_window.geometry(f"+{x_position}+{y_position}")

        key_entry_label = tk.Label(key_window, text="Enter the Caesar cipher key:")
        key_entry_label.pack()

        key_entry = tk.Entry(key_window)
        key_entry.pack()

        # Modified binding to close the key window and display Encode/Decode button
        key_entry.bind("<Return>", lambda event: on_caesar_key_entered(key_window, key_entry.get()))

    def on_caesar_key_entered(key_window, key):
        try:
            key = int(key)

            # Check if the key is within the range 1 to 26
            if 1 <= key <= 26:
                text = input_text.get("1.0", tk.END).strip()

                if action_var.get() == 'Encrypt':
                    result = caesar_cipher(text, key)
                elif action_var.get() == 'Decrypt':
                    result = caesar_cipher(text, -key)

                # Close the key window
                key_window.destroy()

                # Display the encode/decode button on the main window
                encode_decode_button.config(command=lambda: on_caesar_encode_decode(text, key))
                encode_decode_button.grid(row=4, column=0, padx=10, pady=10)

            else:
                # Show an error message if the key is not within the valid range
                messagebox.showerror("Error", "Invalid key. Please enter a key between 1 and 26.")

        except ValueError:
            # Show an error message if the entered value is not an integer
            messagebox.showerror("Error", "Invalid key. Please enter an integer.")


    def on_caesar_encode_decode(text, key):
        if action_var.get() == 'Encrypt':
            result = caesar_cipher(text, key)
        elif action_var.get() == 'Decrypt':
            result = caesar_cipher(text, -key)

        result_text.config(state=tk.NORMAL)  # Enable the text widget for editing
        result_text.delete(1.0, tk.END)  # Clear previous text
        result_text.insert(tk.END, result)
        result_text.config(state=tk.DISABLED)  # Disable the text widget for editing

    def show_atbash_button():
        encode_decode_button.config(command=lambda: on_atbash_cipher(input_text.get("1.0", tk.END)))
        encode_decode_button.grid(row=4, column=0, padx=10, pady=10)

    def on_atbash_cipher(text):
        result = atbash_cipher(text)
        result_text.config(state=tk.NORMAL)  # Enable the text widget for editing
        result_text.delete(1.0, tk.END)  # Clear previous text
        result_text.insert(tk.END, result)
        result_text.config(state=tk.DISABLED)  # Disable the text widget for editing
       
    # Encode/Decode dropdown
    action_var = tk.StringVar()
    action_var.set('Encrypt')
    action_dropdown = ttk.Combobox(text_window, textvariable=action_var, values=['Encrypt', 'Decrypt'], state='readonly')
    action_dropdown.grid(row=0, column=0, padx=10, pady=10)

    # Text entry
    input_text = tk.Text(text_window, height=8, width=83)
    input_text.grid(row=1, column=0, padx=10, pady=10)

    # Cipher choice (Caesar/Atbash) dropdown
    cipher_var = tk.StringVar()
    cipher_var.set('Caesar')
    cipher_dropdown = ttk.Combobox(text_window, textvariable=cipher_var, values=['Caesar', 'Atbash'], state='readonly')
    cipher_dropdown.grid(row=2, column=0, padx=10, pady=10)

    # Button to proceed with chosen cipher
    cipher_button = tk.Button(text_window, text="Proceed", font="Verdana 9", command=on_cipher_choice)
    cipher_button.grid(row=3, column=0, padx=10, pady=10)

    # Encode/Decode button (hidden initially)
    encode_decode_button = tk.Button(text_window, text="Encode/Decode",font="Verdana 9")
    encode_decode_button.grid_forget()

    # Result display
    result_text = tk.Text(text_window,  height=8, width=83, state=tk.DISABLED)
    result_text.grid(row=5, column=0, padx=10, pady=10)

    text_window.mainloop()



def open_image_encryption_window():
    image_window = Toplevel()
    image_window.title("Image Encryption")
    image_window.geometry("700x500+250+180")
    image_window.resizable(False, False)
    image_window.configure(bg="black")
    

    def showimage():
        global filename, img  # Declare img as a global variable
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select Image File",
            filetype=(("PNG file", "*.png"), ("JPG file", "*.jpg"), ("All file", ".txt"))
        )
        img = Image.open(filename)
        img = ImageTk.PhotoImage(img)
        lbl.configure(image=img, width=250, height=250)
        lbl.image = img

    def Hide():
        global secret
        message = text1.get(1.0, END)
        try:
            secret = lsb.hide(str(filename), message)
            messagebox.showinfo("Success", "Data successfully hidden in the image!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def Show():
        clear_message=lsb.reveal(filename)
        text1.delete(1.0, END)
        text1.insert(END, clear_message)

    def save():
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            secret.save(save_path)
            messagebox.showinfo("Success", f"Image successfully saved as '{save_path}'")

    Label(image_window,text="STEGANOGRAPHY", bg="black",fg="white",font="Verdana 23 bold").place(x=200,y=20)
    # First Frame
    f = Frame(image_window, bd=3, bg="#353839", width=330, height=280, relief=GROOVE)
    f.place(x=10, y=110)
    # Title for the First Frame
    Label(image_window, text="Your Picture:", fg="white", bg="black", font="Arial 12 bold").place(x=10, y=80)
    lbl = Label(f, bg="black")
    lbl.place(x=40, y=10)
    
    # Second Frame
    frame2 = Frame(image_window, bd=3, width=330, height=280, bg="white", relief=GROOVE)
    frame2.place(x=360, y=110)
    
    # Title for the Second Frame
    Label(image_window, text="Your Text:", fg="white", bg="black", font="Arial 12 bold").place(x=360, y=80)
    text1 = Text(frame2, font="Roboto 10", bg="white", fg="black", relief=GROOVE, wrap=WORD)
    text1.place(x=0, y=0, width=320, height=245)

    scrollbar1 = Scrollbar(frame2)
    scrollbar1.place(x=320, y=0, height=245)

    scrollbar1.configure(command=text1.yview)
    text1.configure(yscrollcommand=scrollbar1.set)

    #Third Frame
    frame3=Frame(image_window, bd=3,bg="black",width=330,height=100)
    frame3.place(x=10,y=370)

    Button(frame3,text="Upload Image", width=10,height=2,font="arial 14 bold", command=showimage).place(x=20,y=30)
    Button(frame3,text="Save Image", width=10,height=2,font="arial 14 bold", command=save).place(x=180,y=30)
    Label(frame3, text="Picture, Image, Photo File", bg="black",fg="#c0c0c0").place(x=20,y=5)

    #Fourth Frame
    frame4=Frame(image_window, bd=3,bg="black",width=330,height=100)
    frame4.place(x=360,y=370)

    Button(frame4,text="Hide Data", width=10,height=2,font="arial 14 bold", command=Hide).place(x=20,y=30)
    Button(frame4,text="Show Data", width=10,height=2,font="arial 14 bold", command=Show).place(x=180,y=30)
    Label(frame4, text="Picture, Image, Photo File", bg="black",fg="#c0c0c0").place(x=20,y=5)

    image_window.mainloop()

root = Tk()
root.title("Secret Cipher")
root.geometry("700x500+250+180")
root.resizable(False, False)
root.configure(bg="black")

# icon
image_icon = PhotoImage(file="crypt.png")
root.iconphoto(False, image_icon)

# logo
original_image = Image.open("crypt.png")
resized_image = original_image.resize((100, 100), Image.ANTIALIAS)  # Replace width and height with desired dimensions
logo = ImageTk.PhotoImage(resized_image)
Label(root, text="CRYPTOGRAPHY", bg="black", fg="white", font="Verdana 23 bold").place(x=210, y=80)
Label(root, image=logo, bg="black").place(x=300, y=180)

# Buttons
button_width = 15
button_height = 2

text_encryption_button = Button(root, text="Text Encryption", font="Verdana 9 bold", command=open_text_encryption_window, bg="green", fg="white", width=button_width, height=button_height)
text_encryption_button.place(x=290, y=350)

image_encryption_button = Button(root, text="Image Encryption",font="Verdana 9 bold", command=open_image_encryption_window, bg="green", fg="white", width=button_width, height=button_height)
image_encryption_button.place(x=290, y=400)

root.mainloop()
