import tkinter as tk
import re

# Autómata transitions
transitions = {
    'q0': {r'[a-zA-Z0-9]': 'q1', 'Fun': 'q4'},
    'q1': {r'[a-zA-Z0-9]': 'q1', r';': 'q2'},
    'q3': {},
    'q4': {r'[A-Z]': 'q5'},
    'q5': {r'[a-z]': 'q5', r'\[': 'q6'},
    'q6': {r'\]':'q7'},  
    'q7': {r'\(':'q8'},
    'q9': {r'\)':'q10'},
    'q10': {},
    'q11': {r'\[':'q6'}, 
    'q12': {r'\{':'q13'},
    'q13': {r'[0-9a-z]':'q16', r'\"':'q14'},
    'q14': {r'[a-z]':'q14',r'\"':'q15'},
    'q16': {r'[a-z0-9]':'q16'},
    'q17': {r'[0-9a-z]':'q19', r'\"':'q18'},
    'q18': {r'[a-z]':'q18',r'\"':'q20'},
    'q19': {r'[a-z]':'q19',r'\}':'q21'},
    'q20': {r'\}':'q21'},
    'q21': {r'\(':'q8'},
    'q22': {r'\{':'q23'},
    'q23': {r'[a-z0-9]':'q24'},
    'q24': {r'[a-z0-9]':'q24'},
    'q25': {r'[a-z0-9]':'q26'},
    'q26': {r'[a-z0-9]':'q26',r'\}':'q21'}
}

# Palabras clave para transiciones de múltiples caracteres
multi_char_transitions = {
    'q0': {'Fun': 'q4', 'Malph': 'q11','Vi':'q12','War':'q22'},
    'q2': {'string':'q3','int':'q3'},
    'q4': {'Malph': 'q11'},
    'q8': {'contenido':'q9'},
    'q15':{'>':'q17','<':'q17','==':'q17','=<':'q17','=>':'q17'},
    'q16':{'>':'q17','<':'q17','==':'q17','=<':'q17','=>':'q17'},
    'q24':{'>':'q25','<':'q25','==':'q25','=<':'q25','=>':'q25'},
}

# Function to handle transitions of each state.
def make_transition(state, input_char, buffer):
    # Manejar transiciones de múltiples caracteres
    if state in multi_char_transitions:
        buffer += input_char
        for word, next_state in multi_char_transitions[state].items():
            if buffer == word:
                return next_state, ''
            elif word.startswith(buffer):
                return state, buffer
        buffer = ''  # Reset buffer si no hay coincidencia

    # Transiciones de un solo carácter
    for pattern, next_state in transitions[state].items():
        if re.fullmatch(pattern, input_char):
            return next_state, ''
    return state, buffer  # Si no hay transición válida, retorna el estado actual

# Estilo de IDE: tema oscuro
color_fondo = "#282a36"  # Gris oscuro
color_texto = "#f8f8f2"  # Blanco cremoso
color_acento = "#44475a"  # Gris azulado
fuente_texto = ('Consolas', 12)  # Fuente común en los IDEs

# Initialize the GUI
root = tk.Tk()
root.title("Finite Automaton Simulator")
root.configure(bg=color_fondo)

state_label = tk.Label(root, text="Current State: q0", fg=color_texto, bg=color_fondo, font=fuente_texto)
state_label.pack(pady=20)

# Área de texto más grande para la entrada
input_text = tk.Text(root, height=5, width=40, fg=color_texto, bg=color_acento, font=fuente_texto)
input_text.pack(pady=20)

result_label = tk.Label(root, text="", fg=color_texto, bg=color_fondo, font=fuente_texto)
result_label.pack(pady=20)

def is_terminal_state(state):
    # Ajustar según las necesidades del autómata
    return state in ['q3', 'q10']

def process_input():
    global current_state
    input_string = input_text.get("1.0", "end-1c")
    current_state = 'q0'
    buffer = ''

    for char in input_string:
        # Ignorar espacios y saltos de línea
        if char in [' ', '\n', '\r']:
            continue

        current_state, buffer = make_transition(current_state, char, buffer)
        if current_state == 'q0' and buffer == '':
            break

    state_label.config(text=f"Current State: {current_state}")

    if is_terminal_state(current_state):
        result_label.config(text="Cadena Válida")
    else:
        result_label.config(text="Cadena Inválida")

process_button = tk.Button(root, text="Process", command=process_input, fg=color_texto, bg=color_acento, font=fuente_texto)
process_button.pack(pady=20)

current_state = 'q0'

root.mainloop()
