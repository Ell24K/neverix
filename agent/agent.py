import tkinter as tk
import socketio

SERVER_URL = "https://neverix-production.up.railway.app"

sio = socketio.Client(
    reconnection=True,
    reconnection_attempts=0
)

pc_id = "UNKNOWN"

root = tk.Tk()
root.withdraw()

def show_screen(title, message):
    root.deiconify()

    root.title(title)
    root.geometry("900x500")
    root.configure(bg="black")

    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(
        root,
        text=message,
        fg="#00ff66",
        bg="black",
        font=("Consolas", 26),
        justify="center"
    )

    label.pack(expand=True)

def restore():
    root.withdraw()

@sio.event
def connect():
    sio.emit("register-agent")

@sio.event
def disconnect():
    root.after(0, restore)

@sio.on("assigned-id")
def assigned_id(data):
    global pc_id
    pc_id = data["id"]

@sio.on("lab-full")
def lab_full():
    root.after(
        0,
        lambda: show_screen(
            "RPL CYBER LAB",
            "LAB CAPACITY FULL"
        )
    )

@sio.on("agent-command")
def agent_command(data):
    command = data.get("command")
    payload = data.get("payload")

    if command == "SHOW_BREACH":
        root.after(
            0,
            lambda: show_screen(
                "SYSTEM ALERT",
                "⚠ REMOTE SESSION DETECTED ⚠\n\n"
                "SIMULATION ACTIVE\n\n"
                f"TARGET: {pc_id}\n\n"
                "AUTHORIZED RPL DEMO"
            )
        )

    elif command == "MATRIX":
        root.after(
            0,
            lambda: show_screen(
                "RPL CYBER LAB",
                "01001000 01000001 01000011 01001011\n\n"
                "SIMULATION MODE"
            )
        )

    elif command == "SHOW_MESSAGE":
        root.after(
            0,
            lambda: show_screen(
                "MESSAGE",
                str(payload or "RPL CYBER LAB")
            )
        )

    elif command == "RESTORE":
        root.after(0, restore)

sio.connect(SERVER_URL)

root.mainloop()
