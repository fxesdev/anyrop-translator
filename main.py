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

def find_matching_strings(list1, list2, list3):
    result = []
    found = False
    for string1 in list1:
        match_info = ''
        for string2 in list2:
            found = False
            for string3 in list3:
                if string1 in string2:
                    fstring2 = string2.split(' ')[1]
                    print(fstring2)
                    if fstring2 in string3:
                        extracted_chars = string3[33:39]
                        formatted_chars = extracted_chars[3:5] + ' ' + extracted_chars[1:3] + ' ' + 'x' + extracted_chars[0] + ' xx'
                        result.append(formatted_chars)
                        found = True
                        break
            if found: break
        else:
            result.append(string1)
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

def open_disasb_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        global disasbfile
        disasbfile = file_path
        disasb_text.delete("1.0", tk.END)
        with open(disasbfile, 'r') as file:
            disasb_content = remove_newline(file.readlines())
            disasb_text.insert(tk.END, '\n'.join(disasb_content))

def compile_translate():
    if not ropfile or not disasfile or not disasbfile:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Please select ROP file, Disassembly file, and Disassembly B file.")
        return
    
    rop = remove_newline(open(ropfile).readlines())
    disas_lines_before_pop_pc = extract_lines_before_pop_pc(disasfile)
    disasb_lines_before_pop_pc = extract_lines_before_pop_pc(disasbfile)
    
    matching_strings = find_matching_strings(rop, disas_lines_before_pop_pc, disasb_lines_before_pop_pc)
    
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, '\n'.join(matching_strings))

def about_popup():
    popup = tk.Toplevel(root)
    popup.title("AnyRop-Translator")
    
    version_content = ''
    readme_content = ''
    with open('version', 'r') as version_file:
        version_content = version_file.read()
    with open('README.md', 'r') as readme_file:
        readme_content = readme_file.read()

    lines = readme_content.split('\n')
    for line in lines:
        if line.startswith('#'):
            label = tk.Label(popup, text=line[1:], font=("Arial", 16, "bold"))
            label.pack(padx=10, pady=10)
        elif line.startswith('__') and line.endswith('__'):
            label = tk.Label(popup, text=line[2:-2], font=("Arial", 12, "bold"))
            label.pack(padx=10, pady=2)
        else:
            label = tk.Label(popup, text=line)
            label.pack(padx=10, pady=2)

root = tk.Tk()
root.title("AnyRop Translator")

menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open ROP File", command=open_rop_file)
file_menu.add_command(label="Open Disas File", command=open_disas_file)
file_menu.add_command(label="Open DisasB File", command=open_disasb_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

compile_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Compile", menu=compile_menu)
compile_menu.add_command(label="Translate", command=compile_translate)

about_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="About", command=about_popup)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(3, weight=1)

rop_label = tk.Label(root, text="ROP File:")
rop_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

disas_label = tk.Label(root, text="Disas File:")
disas_label.grid(row=0, column=1, padx=5, pady=5, sticky='w')

disasb_label = tk.Label(root, text="DisasB File:")
disasb_label.grid(row=0, column=2, padx=5, pady=5, sticky='w')

rop_text = tk.Text(root, height=10, width=30)
rop_text.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

disas_text = tk.Text(root, height=10, width=30)
disas_text.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

disasb_text = tk.Text(root, height=10, width=30)
disasb_text.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

result_label = tk.Label(root, text="Output:")
result_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

result_text = tk.Text(root, height=20, width=100)
result_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

root.mainloop()
