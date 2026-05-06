import tkinter as tk
from datetime import datetime
import time

# CONFIG
end = datetime(2100, 4, 27, 0, 0, 0)

PIN_REAL = "4321"
PIN_DECOY1 = "0000"
PIN_DECOY2 = "1111"

AUTO_LOCK = 20

# ROOT
root = tk.Tk()
root.title("Calculator")
root.geometry("400x600")
root.configure(bg="black")

font_big = ("Consolas", 30)
font_mid = ("Consolas", 16)
font_small = ("Consolas", 12)

input_value = ""
last_activity = time.time()

# ACTIVITY
def update_activity(event=None):
    global last_activity
    last_activity = time.time()

root.bind_all("<Key>", update_activity)
root.bind_all("<Button>", update_activity)

# CLEAR
def clear():
    for w in root.winfo_children():
        w.destroy()

# AUTO LOCK
def auto_lock():
    if time.time() - last_activity > AUTO_LOCK:
        calculator()
    root.after(2000, auto_lock)

# CALCULATOR
def calculator():
    global input_value
    input_value = ""

    clear()

    display = tk.Entry(root, font=("Consolas", 24), bd=0,
                       bg="black", fg="#00ffcc", justify="right")
    display.pack(fill="both", padx=10, pady=10)

    def press(val):
        global input_value
        if len(input_value) >= 12:
            input_value = ""
        input_value += str(val)
        display.delete(0, tk.END)
        display.insert(tk.END, input_value)

    def clear_input():
        global input_value
        input_value = ""
        display.delete(0, tk.END)

    def enter():
        global input_value

        code = "".join(filter(str.isdigit, input_value))[-4:]
        input_value = ""

        if code == PIN_REAL:
            vault()
            return
        elif code == PIN_DECOY1:
            decoy1()
            return
        elif code == PIN_DECOY2:
            decoy2()
            return

        try:
            result = str(eval(display.get()))
            display.delete(0, tk.END)
            display.insert(tk.END, result)
            input_value = result
        except:
            display.delete(0, tk.END)

    buttons = [
        "7","8","9","/",
        "4","5","6","*",
        "1","2","3","-",
        "0","C","=","+"
    ]

    frame = tk.Frame(root, bg="black")
    frame.pack()

    for i, b in enumerate(buttons):
        if b == "=":
            action = enter
        elif b == "C":
            action = clear_input
        else:
            action = lambda x=b: press(x)

        tk.Button(frame, text=b, command=action,
                  width=5, height=2,
                  bg="#111", fg="#00ffcc").grid(row=i//4, column=i%4)

# DECOYS
def decoy1():
    clear()
    tk.Label(root, text="SYSTEM STATUS", fg="#00ffcc", bg="black",
             font=("Consolas", 16)).pack(pady=20)
    tk.Label(root, text="ALL SYSTEMS NORMAL", fg="#00ffcc",
             bg="black").pack()
    tk.Button(root, text="BACK", command=calculator,
              bg="#111", fg="#00ffcc").pack(pady=20)

def decoy2():
    clear()
    tk.Label(root, text="NETWORK DATA", fg="#00ffcc", bg="black",
             font=("Consolas", 16)).pack(pady=20)
    tk.Label(root, text="STABLE", fg="#00ffcc",
             bg="black").pack()
    tk.Button(root, text="BACK", command=calculator,
              bg="#111", fg="#00ffcc").pack(pady=20)

# VAULT VISUAL
def vault():
    clear()

    title = tk.Label(root, text="VAULT TIMER",
                     fg="#00ffcc", bg="black", font=font_mid)
    title.pack(pady=10)

    main_time = tk.Label(root, fg="#00ffcc", bg="black", font=font_big)
    main_time.pack(pady=10)

    detail_time = tk.Label(root, fg="#00ffcc", bg="black", font=font_small)
    detail_time.pack(pady=5)

    # PROGRESS BAR
    canvas = tk.Canvas(root, width=300, height=20, bg="black", highlightthickness=1)
    canvas.pack(pady=15)
    bar = canvas.create_rectangle(0, 0, 0, 20, fill="#00ffcc")

    start = datetime.now()
    total = (end - start).total_seconds()

    def update():
        now = datetime.now()
        delta = end - now

        s = int(delta.total_seconds())
        m = s // 60
        h = m // 60
        d = h // 24

        hours = (h % 24)
        minutes = (m % 60)
        seconds = (s % 60)

        main_time.config(text=f"{d}D {hours}H")
        detail_time.config(text=f"{hours}H {minutes}M {seconds}S  |  {m}M {s}S")

        # progress
        elapsed = total - delta.total_seconds()
        percent = elapsed / total
        canvas.coords(bar, 0, 0, 300 * percent, 20)

        root.after(1000, update)

    def panic():
        decoy1()

    tk.Button(root, text="PANIC", command=panic,
              bg="#111", fg="#00ffcc").pack(pady=10)
    tk.Button(root, text="LOCK", command=calculator,
              bg="#111", fg="#00ffcc").pack(pady=5)

    update()

# START
calculator()
auto_lock()
root.mainloop()    