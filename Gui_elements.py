import tkinter as tk


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



stack_frame = tk.Frame(root)
stack_frame.pack(pady=20)


stack_display = tk.Text(stack_frame, height=10, width=40, fg="#8be9fd", bg=color_acento, font=fuente_texto, borderwidth=2, relief="groove")
stack_display.pack(side="left", fill="y")

scrollbar = tk.Scrollbar(stack_frame, command=stack_display.yview)
scrollbar.pack(side="right", fill="y")

stack_display.config(yscrollcommand=scrollbar.set)





process_button = tk.Button(root, text="Process", fg=color_texto, bg=color_acento, font=fuente_texto)
process_button.pack(pady=20)

current_state = 'q0'