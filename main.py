import tkinter as tk
from tkinter import filedialog  # This imports filedialog module from tkinter

def remove_newline(strings):  # This defines a function to remove newline characters from strings
    return [string.replace('\n', '') for string in strings]

def extract_lines_before_pop_pc(file_path):  # This function extracts lines before "pop pc" from a file
    lines_before_pop_pc = []
    with open(file_path, 'r') as file:
        previous_line = ''
        for line in file:
            if 'pop pc' in line:
                lines_before_pop_pc.append(previous_line.strip())
            previous_line = line
    return lines_before_pop_pc

def find_matching_strings(list1, list2):  # This function finds matching strings between two lists
    result = []
    for string1 in list1:
        found_match = False
        for string2 in list2:
            if string1 in string2:
                # Extracting characters 34th to 39th and formatting them
                extracted_chars = string2[33:39]
                formatted_chars = extracted_chars[3:5] + ' ' + extracted_chars[1:3] + ' ' + 'x' + extracted_chars[0] + ' xx'
                result.append(formatted_chars)
                found_match = True
                break  # Stop processing list2 after finding a match
        if not found_match:
            # If no match was found in list2 for string1
            result.append("No match found for {}".format(string1))
    return result

def open_rop_file():  # This function opens a file dialog to select a ROP file
    file_path = filedialog.askopenfilename()
    if file_path:
        global ropfile
        ropfile = file_path
        rop_text.delete("1.0", tk.END)
        with open(ropfile, 'r') as file:
            rop_content = remove_newline(file.readlines())
            rop_text.insert(tk.END, '\n'.join(rop_content))

def open_disas_file():  # This function opens a file dialog to select a disassembly file
    file_path = filedialog.askopenfilename()
    if file_path:
        global disasfile
        disasfile = file_path
        disas_text.delete("1.0", tk.END)
        with open(disasfile, 'r') as file:
            disas_content = remove_newline(file.readlines())
            disas_text.insert(tk.END, '\n'.join(disas_content))

def compile_translate():  # This function compiles and translates the ROP and disassembly files
    rop = remove_newline(open(ropfile).readlines())
    lines_before_pop_pc = extract_lines_before_pop_pc(disasfile)
    matching_strings = find_matching_strings(rop, lines_before_pop_pc)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, '\n'.join(matching_strings))

def about_popup():  # This function creates a popup window displaying information about the program
    popup = tk.Toplevel(root)
    popup.title("AnyRop-Translator")
    
    version_content = ''
    readme_content = ''
    with open('version', 'r') as version_file:
        version_content = version_file.read()
    with open('readme.md', 'r') as readme_file:
        readme_content = readme_file.read()

    lines = readme_content.split('\n')
    for line in lines:
        if line.startswith('#'):  # This creates a label with big font size for lines starting with '#'
            label = tk.Label(popup, text=line[1:], font=("Arial", 16, "bold"))
            label.pack(padx=10, pady=10)
        elif line.startswith('__') and line.endswith('__'):  # This creates a bold label for lines enclosed in '__'
            label = tk.Label(popup, text=line[2:-2], font=("Arial", 12, "bold"))
            label.pack(padx=10, pady=2)
        else:  # This creates a label for other lines
            label = tk.Label(popup, text=line)
            label.pack(padx=10, pady=2)

root = tk.Tk()
root.title("AnyRop Translator")  # This sets the title of the main window

# Create menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Create File menu
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open ROP File", command=open_rop_file)
file_menu.add_command(label="Open Disas File", command=open_disas_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Create Compile menu
compile_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Compile", menu=compile_menu)
compile_menu.add_command(label="Translate", command=compile_translate)

# Create About menu
about_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="About", command=about_popup)

# Set up grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(3, weight=1)

# Create labels and text boxes
rop_label = tk.Label(root, text="ROP File:")
rop_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

disas_label = tk.Label(root, text="Disas File:")
disas_label.grid(row=0, column=1, padx=5, pady=5, sticky='w')

rop_text = tk.Text(root, height=10, width=50)
rop_text.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

disas_text = tk.Text(root, height=10, width=50)
disas_text.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

result_label = tk.Label(root, text="Output:")
result_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

result_text = tk.Text(root, height=20, width=100)
result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

root.mainloop()  # This starts the main event loop

