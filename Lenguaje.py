from Grammar_transitions import *
from Gui_elements import *

state_stack = []
applied_rules = set()

def make_transition(state, input_char, buffer):
    global state_stack, applied_rules

    
    if state in multi_char_transitions:
        buffer += input_char
        for word, next_state in multi_char_transitions[state].items():
            if buffer == word:
                
                rule = grammar_rules.get(state, {}).get(word, None)
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
           
            rule = grammar_rules.get(state, {}).get(pattern, None)
            if rule and rule not in applied_rules:
                state_stack.append(rule)
                applied_rules.add(rule)
                print("Pila actualizada:", state_stack)
            return next_state, buffer

    return state, buffer

def is_terminal_state(state):
    
    return state in ['q3', 'q10']

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

    reached_terminal = False 

    for char in input_string:
        if char in [' ', '\n', '\r']:
            continue

        
        if is_terminal_state(current_state):
            reached_terminal = True

        
        if reached_terminal:
            break

        if current_state not in visited_states:
            draw_state(canvas, current_state, x, y)
            visited_states.append(current_state)
            y += 50
            if y > canvas.winfo_height() - 50:
                y = 50
                x += 100

        current_state, buffer = make_transition(current_state, char, buffer)

    
    state_label.config(text=f"Estado actual: {current_state}")
    
    
    is_valid = is_terminal_state(current_state) and not reached_terminal
    result_label.config(text="Cadena Válida" if is_valid else "Cadena Inválida")
    update_state_colors(canvas, visited_states, is_valid)

    display_stack()


    stack_label = tk.Label(root, text="", fg=color_texto, bg=color_fondo, font=fuente_texto)
    stack_label.pack(pady=20)

process_button.config(command=process_input)

root.mainloop()