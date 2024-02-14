#!/usr/bin/python3
import tkinter as tk
from tkinter import filedialog

def remove_newline(strings):
    return [string.replace('\n', '') for string in strings]

def extract_lines_before_pop_pc(file_path):
    lines_before_pop_pc = []
    with open(file_path, 'r') as file:
        previous_line = ''
        for line in file:
            if 'pop pc' in line:
                lines_before_pop_pc.append(previous_line.strip())
            previous_line = line
    return lines_before_pop_pc

def find_matching_strings(list1, list2):
    result = []
    for string1 in list1:
        for string2 in list2:
            if string1 in string2:
                result.append(string2)
    return result

def open_rop_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        global ropfile
        ropfile = file_path
        rop_text.delete("1.0", tk.END)
        with open(ropfile, 'r') as file:
            rop_content = remove_newline(file.readlines())
            rop_text.insert(tk.END, '\n'.join(rop_content))

def open_disas_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        global disasfile
        disasfile = file_path
        disas_text.delete("1.0", tk.END)
        with open(disasfile, 'r') as file:
            disas_content = remove_newline(file.readlines())
            disas_text.insert(tk.END, '\n'.join(disas_content))

def compile_translate():
    rop = remove_newline(open(ropfile).readlines())
    lines_before_pop_pc = extract_lines_before_pop_pc(disasfile)
    matching_strings = find_matching_strings(rop, lines_before_pop_pc)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, '\n'.join(matching_strings))

root = tk.Tk()
root.title("String Matching")

ropfile = ""
disasfile = ""

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

rop_label = tk.Label(root, text="ROP File:")
rop_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

disas_label = tk.Label(root, text="Disas File:")
disas_label.grid(row=0, column=1, padx=5, pady=5, sticky='w')

rop_text = tk.Text(root, height=10, width=50)
rop_text.grid(row=1, column=0, padx=5, pady=5)

disas_text = tk.Text(root, height=10, width=50)
disas_text.grid(row=1, column=1, padx=5, pady=5)

result_label = tk.Label(root, text="Output:")
result_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

result_text = tk.Text(root, height=20, width=100)
result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()

