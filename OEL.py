from tkinter import *
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import Tk, PhotoImage, ttk, Toplevel
from PIL import Image, ImageTk
import os
from stegano import lsb
from PIL import Image, ImageTk



def open_text_encryption_window():

    # Atbash Cipher: A simple substitution cipher where each letter is replaced with its mirror image in the alphabet.
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

    # Caesar Cipher: A substitution cipher where each letter is shifted by a fixed number of positions in the alphabet.
    def caesar_cipher(text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                base = 'a' if char.islower() else 'A'
                result += chr((ord(char) - ord(base) + shift) % 26 + ord(base))
            else:
                result += char
        return result

    # Baconian Cipher: A substitution cipher where each letter is represented by a series of binary digits.
    def baconian_cipher(text, is_encrypt=True):
        lookup = {'A': 'aaaaa', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa',
                  'F': 'aabab', 'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'J': 'abaab',
                  'K': 'ababa', 'L': 'ababb', 'M': 'abbaa', 'N': 'abbab', 'O': 'abbba',
                  'P': 'abbbb', 'Q': 'baaaa', 'R': 'baaab', 'S': 'baaba', 'T': 'baabb',
                  'U': 'babaa', 'V': 'babab', 'W': 'babba', 'X': 'babbb', 'Y': 'bbaaa', 'Z': 'bbaab'}

        result = ""
        text = text.upper()
        for char in text:
            if char.isalpha():
                result += lookup[char] if is_encrypt else char
            else:
                result += char
        return result

    def baconian_cipher(text, is_encrypt=True):
    # Baconian Cipher: A substitution cipher where each letter is represented by a series of binary digits.

    # Define a dictionary for the Baconian cipher, mapping each letter to its binary representation.
        lookup = {'A': 'aaaaa', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa',
                'F': 'aabab', 'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'J': 'abaab',
                'K': 'ababa', 'L': 'ababb', 'M': 'abbaa', 'N': 'abbab', 'O': 'abbba',
                'P': 'abbbb', 'Q': 'baaaa', 'R': 'baaab', 'S': 'baaba', 'T': 'baabb',
                'U': 'babaa', 'V': 'babab', 'W': 'babba', 'X': 'babbb', 'Y': 'bbaaa', 'Z': 'bbaab'}

        # Initialize an empty string to store the result.
        result = ""
        
        # Convert the input text to uppercase for consistency.
        text = text.upper()

        # Iterate through each character in the input text.
        for char in text:
            # Check if the character is an alphabet letter.
            if char.isalpha():
                # If encrypting, append the binary representation from the lookup table; otherwise, keep the original character.
                result += lookup[char] if is_encrypt else char
            else:
                # If the character is not an alphabet letter, keep it unchanged.
                result += char

        # Return the final result.
        return result


    def decrypt_baconian(message):
        lookup = {'aaaaa': 'A', 'aaaab': 'B', 'aaaba': 'C', 'aaabb': 'D', 'aabaa': 'E',
                'aabab': 'F', 'aabba': 'G', 'aabbb': 'H', 'abaaa': 'I', 'abaab': 'J',
                'ababa': 'K', 'ababb': 'L', 'abbaa': 'M', 'abbab': 'N', 'abbba': 'O',
                'abbbb': 'P', 'baaaa': 'Q', 'baaab': 'R', 'baaba': 'S', 'baabb': 'T',
                'babaa': 'U', 'babab': 'V', 'babba': 'W', 'babbb': 'X', 'bbaaa': 'Y', 'bbaab': 'Z'}

        decipher = ''
        i = 0

        # emulating a do-while loop
        while True:
            # condition to run decryption till
            # the last set of ciphertext
            if(i < len(message)-4):
                # extracting a set of ciphertext
                # from the message
                substr = message[i:i + 5]
                # checking for space as the first
                # character of the substring
                if(substr[0] != ' '):
                    '''
                    This statement gets us the key(plaintext) using the values(ciphertext)
                    Just the reverse of what we were doing in encrypt function
                    '''
                    decipher += lookup[substr]
                    i += 5  # to get the next set of ciphertext

                else:
                    # adds space
                    decipher += ' '
                    i += 1  # index next to the space
            else:
                break  # emulating a do-while loop

        return decipher
    def on_atbash_cipher(text):
        # Perform Atbash cipher encryption on the input text.
        result = atbash_cipher(text)

        # Enable the result_text widget for editing.
        result_text.config(state=tk.NORMAL)

        # Clear the contents of result_text.
        result_text.delete(1.0, tk.END)

        # Insert the encrypted/decrypted result into result_text.
        result_text.insert(tk.END, result)

        # Disable the result_text widget to prevent further editing.
        result_text.config(state=tk.DISABLED)

    def on_baconian_cipher(text):
        # Get the user's choice for encryption or decryption.
        choice = action_var.get()

        # Check the choice and perform either encryption or decryption.
        if choice == 'Encrypt':
            result = baconian_cipher(text)
        elif choice == 'Decrypt':
            result = decrypt_baconian(text)  # You need to implement the decryption function for Baconian cipher.
        else:
            # If the user didn't choose either 'Encrypt' or 'Decrypt', show an information message.
            messagebox.showinfo("Info", "Please choose 'Encrypt' or 'Decrypt'.")
            return

        # Enable the result_text widget for editing.
        result_text.config(state=tk.NORMAL)

        # Clear the contents of result_text.
        result_text.delete(1.0, tk.END)

        # Insert the encrypted/decrypted result into result_text.
        result_text.insert(tk.END, result)

        # Disable the result_text widget to prevent further editing.
        result_text.config(state=tk.DISABLED)

    def on_encode_decode_button_pressed():
        # Get the input text from the input_text widget.
        text = input_text.get("1.0", tk.END).strip()

        # Check if the input text is empty.
        if not text:
            messagebox.showinfo("Info", "Please enter text before pressing the Encode/Decode button.")
            return

        # Get the user's choice of cipher.
        choice = cipher_var.get()

        # Check the choice and take appropriate actions.
        if choice == 'Caesar':
            show_caesar_key_entry()
        elif choice == 'Atbash':
            on_atbash_cipher(text)
        elif choice == 'Baconian':
            on_baconian_cipher(text)
        else:
            # If the user didn't choose 'Caesar', 'Atbash', or 'Baconian', show an information message.
            messagebox.showinfo("Info", "Please choose 'Caesar', 'Atbash', or 'Baconian'.")

    def show_caesar_key_entry():
        # Create a new window for entering the Caesar key.
        key_window = tk.Toplevel(text_window)
        key_window.title("Enter Caesar Key")

        # Set the position of the key window relative to the main window.
        x_position = text_window.winfo_x() + 90
        y_position = text_window.winfo_y() + 90
        key_window.geometry(f"+{x_position}+{y_position}")

        # Create a label for instructing the user to enter the Caesar key.
        key_entry_label = tk.Label(key_window, text="Enter the Caesar cipher key:")
        key_entry_label.pack()

        # Create an entry widget for entering the Caesar key.
        key_entry = tk.Entry(key_window)
        key_entry.pack()

        # Bind the 'Return' key to the function on_caesar_key_entered.
        key_entry.bind("<Return>", lambda event: (on_caesar_key_entered(key_window, key_entry.get()), key_window.destroy()))


    def on_caesar_key_entered(key_window, key):
        try:
            # Convert the entered key to an integer.
            key = int(key)

            # Check if the key is within the valid range (1 to 26).
            if 1 <= key <= 26:
                # Get the input text from the input_text widget.
                text = input_text.get("1.0", tk.END).strip()

                # Check the selected action ('Encrypt' or 'Decrypt') and perform the Caesar cipher operation.
                if action_var.get() == 'Encrypt':
                    result = caesar_cipher(text, key)
                elif action_var.get() == 'Decrypt':
                    result = caesar_cipher(text, -key)  # Decryption by using a negative shift.

                # Close the key entry window.
                key_window.destroy()

                # Enable the result_text widget for editing.
                result_text.config(state=tk.NORMAL)

                # Clear the contents of result_text.
                result_text.delete(1.0, tk.END)

                # Insert the encrypted/decrypted result into result_text.
                result_text.insert(tk.END, result)

                # Disable the result_text widget to prevent further editing.
                result_text.config(state=tk.DISABLED)
            else:
                # Show an error message for an invalid key outside the range 1 to 26.
                messagebox.showerror("Error", "Invalid key. Please enter a key between 1 and 26.")
        except ValueError:
            # Show an error message for a non-integer key.
            messagebox.showerror("Error", "Invalid key. Please enter an integer.")

    # GUI setup
    text_window = Toplevel()
    text_window.title("Text Encryption")
    text_window.geometry("800x600+200+150")
    text_window.resizable(False, False)
    text_window.configure(bg="#808080")
    image_icon2 = PhotoImage(file="crypt.png")
    text_window.iconphoto(False, image_icon2)

    # Labels, dropdowns, and buttons setup...

    text_window.mainloop()





def open_image_encryption_window():
    # Create a new window for image encryption.
    image_window = Toplevel()
    image_window.title("Image Encryption")
    image_window.geometry("700x500+250+180")
    image_window.resizable(False, False)
    image_window.configure(bg="black")
    image1_icon = PhotoImage(file="crypt.png")
    image_window.iconphoto(False, image1_icon)

    # Function to select and display an image.
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

    # Function to hide data in the selected image.
    def Hide():
        global secret
        message = text1.get(1.0, END)
        try:
            secret = lsb.hide(str(filename), message)
            messagebox.showinfo("Success", "Data successfully hidden in the image!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Function to reveal hidden data from the selected image.
    def Show():
        try:
            clear_message = lsb.reveal(filename)
            text1.delete(1.0, END)
            text1.insert(END, clear_message)
        except Exception as e:
            # Add an info message when no message is found in the photo
            nodata_message = "No hidden message found in the photo."
            messagebox.showinfo("Info", nodata_message)

    # Function to save the modified image.
    def save():
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            secret.save(save_path)
            messagebox.showinfo("Success", f"Image successfully saved as '{save_path}'")

    # Labels, frames, and buttons setup...
    # (Comments for these sections are not included for brevity, as they are similar to the previous code.)

    image_window.mainloop()


# Create the main window
root = Tk()
root.title("Secret Cipher")
root.geometry("700x500+250+180")
root.resizable(False, False)
root.configure(bg="black")

# Set the window icon
image_icon = PhotoImage(file="crypt.png")
root.iconphoto(False, image_icon)

# Load and resize the logo image
original_image = Image.open("crypt.png")
resized_image = original_image.resize((100, 100), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(resized_image)

# Display the program title and logo
Label(root, text="Secret Cipher", bg="black", fg="#0892d0", font="Verdana 23 italic bold").place(x=230, y=30)
Label(root, text="CRYPTOGRAPHY", bg="black", fg="white", font="Verdana 20 bold").place(x=220, y=80)
Label(root, image=logo, bg="black").place(x=300, y=180)

# Buttons for text and image encryption
button_width = 15
button_height = 2

# Button to open the text encryption window
text_encryption_button = Button(root, text="Text Encryption", font="Verdana 9 bold", command=open_text_encryption_window, bg="green", fg="white", width=button_width, height=button_height)
text_encryption_button.place(x=290, y=350)

# Button to open the image encryption window
image_encryption_button = Button(root, text="Image Encryption", font="Verdana 9 bold", command=open_image_encryption_window, bg="green", fg="white", width=button_width, height=button_height)
image_encryption_button.place(x=290, y=400)

# Start the GUI main loop
root.mainloop()
