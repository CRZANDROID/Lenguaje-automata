import tkinter as tk
import re


transitions = {
    'q0': {r'[a-zA-Z0-9]': 'q1', 'Fun': 'q4'},
    'q1': {r'[a-zA-Z0-9]': 'q1', r';': 'q2'},
    'q3': {},
    'q4': {r'[A-Z]': 'q5'},
    'q5': {r'[a-z]': 'q5', r'\[': 'q6'},
    'q6': {r'\]': 'q7'},  
    'q7': {r'\(': 'q8'},
    'q9': {r'\)': 'q10'},
    'q10': {},
    'q11': {r'\[': 'q6'}, 
    'q12': {r'\{': 'q13'},
    'q13': {r'[0-9a-z]': 'q16', r'\"': 'q14'},
    'q14': {r'[a-z]': 'q14', r'\"': 'q15'},
    'q16': {r'[a-z0-9]': 'q16'},
    'q17': {r'[0-9a-z]': 'q19', r'\"': 'q18'},
    'q18': {r'[a-z]': 'q18', r'\"': 'q20'},
    'q19': {r'[a-z]': 'q19', r'\}': 'q21'},
    'q20': {r'\}': 'q21'},
    'q21': {r'\(': 'q8'},
    'q22': {r'\{': 'q23'},
    'q23': {r'[a-z0-9]': 'q24'},
    'q24': {r'[a-z0-9]': 'q24'},
    'q25': {r'[a-z0-9]': 'q26'},
    'q26': {r'[a-z0-9]': 'q26', r'\}': 'q21'}
}


multi_char_transitions = {
    'q0': {'Fun': 'q4', 'Malph': 'q11','Vi':'q12','War':'q22'},
    'q2': {'string':'q3','int':'q3'},
    'q4': {'Malph': 'q11'},
    'q8': {'contenido':'q9'},
    'q15':{'>':'q17','<':'q17','==':'q17','=<':'q17','=>':'q17'},
    'q16':{'>':'q17','<':'q17','==':'q17','=<':'q17','=>':'q17'},
    'q24':{'>':'q25','<':'q25','==':'q25','=<':'q25','=>':'q25'},
}
grammar_rules = {
    'q0': {r'[a-zA-Z0-9]': 'S -> AX1', 'q1': 'X1 -> BX2'},
    'q1': {r'[a-zA-Z0-9]': 'X1 -> BX2', r';': 'X2 -> PV'},
    'q2': {'string': 'V -> string', 'int': 'V -> int'}
}
state_stack = []
applied_rules = set()


def make_transition(state, input_char, buffer):
    global state_stack, applied_rules

    if state in multi_char_transitions:
        buffer += input_char
        for word, next_state in multi_char_transitions[state].items():
            if buffer == word:
                
                rule = grammar_rules.get(state, {}).get(word, f"{state} -> {next_state}")
                if rule and rule not in applied_rules:
                    state_stack.append(rule)
                    applied_rules.add(rule)
                print("Pila actualizada:", state_stack)
                return next_state, ''
            elif word.startswith(buffer):
                return state, buffer
        buffer = ''
    
    for pattern, next_state in transitions[state].items():
        if re.fullmatch(pattern, input_char):
            
            rule = grammar_rules.get(state, {}).get(pattern, f"{state} -> {next_state}")
            if rule and rule not in applied_rules:
                state_stack.append(rule)  
                applied_rules.add(rule)
                print("Pila actualizada:", state_stack)
            return next_state, ''
    return state, buffer


color_fondo = "#282a36"  
color_texto = "#f8f8f2"  
color_acento = "#44475a"  
fuente_texto = ('Consolas', 12)  


root = tk.Tk()
root.title("RiftCode")
root.configure(bg=color_fondo)

state_label = tk.Label(root, text="Estado actual: q0", fg=color_texto, bg=color_fondo, font=fuente_texto)
state_label.pack(pady=20)


input_text = tk.Text(root, height=5, width=40, fg=color_texto, bg=color_acento, font=fuente_texto)
input_text.pack(pady=20)

canvas = tk.Canvas(root, width=600, height=300, bg=color_fondo)
canvas.pack(side="left", fill="both", expand=True)



def draw_state(canvas, state, x, y, r=20):
    canvas.create_oval(x - r, y - r, x + r, y + r, fill=color_acento, outline=color_texto, tags=state)
    canvas.create_text(x, y, text=state, fill=color_texto)


def update_state_colors(canvas, visited_states, valid):
    color = "green" if valid else "red"
    for state in visited_states:
        canvas.itemconfig(state, fill=color)

result_label = tk.Label(root, text="", fg=color_texto, bg=color_fondo, font=fuente_texto)
result_label.pack(pady=20)

def is_terminal_state(state):
    
    return state in ['q3', 'q10']

stack_frame = tk.Frame(root)
stack_frame.pack(pady=20)


stack_display = tk.Text(stack_frame, height=10, width=40, fg="#8be9fd", bg=color_acento, font=fuente_texto, borderwidth=2, relief="groove")
stack_display.pack(side="left", fill="y")

scrollbar = tk.Scrollbar(stack_frame, command=stack_display.yview)
scrollbar.pack(side="right", fill="y")

stack_display.config(yscrollcommand=scrollbar.set)

def display_stack():
    stack_content = "\n".join(state_stack)
    stack_display.delete('1.0', tk.END)  
    stack_display.insert(tk.END, stack_content)  


def process_input():
    global current_state, applied_rules
    applied_rules.clear() 
    input_string = input_text.get("1.0", "end-1c")
    current_state = 'q0'
    buffer = ''
    canvas.delete("all")  
    visited_states = []
    x, y = 50, 50  

    
    state_stack.clear()


    for char in input_string:
        if char in [' ', '\n', '\r']:
            continue

        if current_state not in visited_states:
            draw_state(canvas, current_state, x, y)
            visited_states.append(current_state)
            y += 50
            if y > canvas.winfo_height() - 50:
                y = 50
                x += 100

        current_state, buffer = make_transition(current_state, char, buffer)
        if current_state == 'q0' and buffer == '':
            break

    state_label.config(text=f"Estado actual: {current_state}")
    is_valid = is_terminal_state(current_state)
    result_label.config(text="Cadena Válida" if is_valid else "Cadena Inválida")
    update_state_colors(canvas, visited_states, is_valid)

    display_stack()

    stack_label = tk.Label(root, text="", fg=color_texto, bg=color_fondo, font=fuente_texto)
    stack_label.pack(pady=20)

process_button = tk.Button(root, text="Process", command=process_input, fg=color_texto, bg=color_acento, font=fuente_texto)
process_button.pack(pady=20)

current_state = 'q0'

root.mainloop()
