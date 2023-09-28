import tkinter as tk

def validar_automata(input_string, states):
    current_state = "q0"

    for char in input_string:
        try:
            if states[current_state][char]:
                current_state = states[current_state][char]
                resultado_label = tk.Label(ventana, text=current_state)
                resultado_label.pack()
        except KeyError:
            return {'success': False, 'message': f'Autómata no válido, error en el estado {current_state}'}
    
    if len(input_string) == 7:
        return {'success': False, 'message': f'Autómata no válido, error, tamaño de entrada invalido {current_state}'}

    return {'success': True, 'message': 'Autómata válido'}

def validar():
    input_text = entrada.get()
    resultado = validar_automata(input_text, states)
    resultado_label.config(text=f"Resultado: {resultado['message']}")


states = {
    'q0': {"1": 'q10', "9": 'q1'},
    'q1': {'-':'q2'},
    'q2': {'S':'q3'},
    'q3': {'V':'q4', 'W':'q4', 'X':'q4','Y':'q4','Z':'q4'},
    'q4':{'-':'q5'},
    'q5':{'0':'q6','1':'q9','2':'q9','3':'q9','4':'q9','5':'q9','6':'q9','7':'q9','8':'q9','9':'q9'},
    'q6':{'1':'q7','2':'q7','3':'q7','4':'q7','5':'q7','6':'q7','7':'q7','8':'q7','9':'q7',},
    'q7':{'W':'q8','X':'q8','Y':'q8','Z':'q8',},
    'q8':{},
    'q9':{'1':'q7','2':'q7','3':'q7','4':'q7','5':'q7','6':'q7','7':'q7','8':'q7','9':'q7'},
    'q10':{'-':'q11'},
    'q11':{'T':'q12'},
    'q12':{'A':'q13'},
    'q13':{'-':'q14'},
    'q14':{'0':'q15','1':'q18','2':'q18','3':'q18','4':'q18','5':'q18','6':'q18','7':'q18','8':'q18','9':'q18'},
    'q15':{'1':'q16','2':'q16','3':'q16','4':'q16','5':'q16','6':'q16','7':'q16','8':'q16','9':'q16'},
    'q16':{'A':'q17','B':'q17','C':'q17','D':'q17','E':'q17','F':'q17','G':'q17','H':'q17','I':'q17','J':'q17',
           'K':'q17','L':'q17','M':'q17','N':'q17','Ñ':'q17','O':'q17','P':'q17'},
    'q17':{},
    'q18':{'0':'q16','1':'q16','2':'q16','3':'q16','4':'q16','5':'q16','6':'q16','7':'q16','8':'q16','9':'q16'}
    
    
    
}

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Validador de Autómata")


ventana.geometry("400x500")


etiqueta = tk.Label(ventana, text="Ingresa el autómata:")
etiqueta.pack()


entrada = tk.Entry(ventana)
entrada.pack()


boton = tk.Button(ventana, text="Validar", command=validar)
boton.pack()


resultado_label = tk.Label(ventana, text="")
resultado_label.pack()

ventana.mainloop()