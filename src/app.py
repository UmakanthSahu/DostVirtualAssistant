from tkinter import *
import speech_recognition as sr
from chat import get_response,bot_name

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#FFFFFF"

FONT = "Calibri 14"
FONT_BOLD = "Calibri 15 bold"


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        #query = r.recognize_sphinx(audio)
        query = r.recognize_google(audio,language='eng-in')

        print(f'User said:{query}\n')
    except Exception as e:
        print(e,"error occurred... Sorry :(")
        return "None"
    return query

class ChatApplication:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
    
    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False,height=False)
        self.window.configure(width=650, height=550,bg=BG_COLOR)

        #Welcome head label
        head_label = Label(self.window, bg=BG_COLOR, fg= TEXT_COLOR,text="Welcome",font=FONT_BOLD,pady=10)
        head_label.place(relwidth=1)

        #divider 
        line = Label(self.window,width=450,bg=BG_GRAY)
        line.place(relwidth=1,rely=0.07,relheight=0.012)

        #Scroll bar
        scrollbar = Scrollbar(self.window) #
        scrollbar.pack(side="right",fill=Y)
        scrollbar.place(relheight=0.83,relx=0.974)
        
        #text widget 
        self.text_widget = Text(self.window,width=20,height=2,bg=BG_COLOR,fg=TEXT_COLOR,font=FONT,padx=5,pady=5,yscrollcommand=scrollbar.set)
        self.text_widget.pack(side="left")
        self.text_widget.place(relheight=0.745,relwidth=0.975,rely=0.08)
        scrollbar.configure(command=self.text_widget.yview)

        self.text_widget.configure(cursor="arrow",state=DISABLED)

        
        
        #Bottom Label
        bottom_label = Label(self.window,bg = BG_GRAY,height=80)
        bottom_label.place(relwidth=1,rely=0.825)

        #message entry box
        self.msg_entry = Entry(bottom_label,bg="#2C3E50",fg=TEXT_COLOR,font=FONT)
        self.msg_entry.place(relwidth=0.66,relheight=0.06,rely=0.008,relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>",self._on_enter_pressed)

        #voice button
        voice_button = Button(bottom_label, text="Speak", font=FONT_BOLD, width=20, bg=BG_GRAY,command=lambda:self._take_voice_input(None))
        voice_button.place(relx=0.68,rely=0.008,relheight=0.06,relwidth=0.15)

        #send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY, command=lambda:self._on_enter_pressed(None))
        send_button.place(relx=0.85,rely=0.008,relheight=0.06,relwidth=0.15)

        # self.fun()
        # time.sleep(5)
        # self._take_voice_input(None)
    
    def _fun(self):
        print(self)
        print(type(self.msg_entry))
        self.msg_entry.delete(0,END)
        self.msg_entry.insert(0,"DOST is Listening... Speak now...")
        

    def _take_voice_input(self,event):
        # self.msg_entry.delete(0,END)
        self._fun()
        msg = takeCommand().lower()
        self.msg_entry.delete(0,END)
        self._insert_message(msg,"You")



    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg,"You")

    def _insert_message(self,message,sender):
        if not message:
            return

        self.msg_entry.delete(0,END)
        msg = f'{sender}: {message}\n\n'
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END,msg)
        self.text_widget.configure(state=DISABLED)


        msg2 = f'{bot_name}: {get_response(message)}\n\n'
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END,msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)
        

if __name__ == "__main__":
    app = ChatApplication()
    app.run()
    # app.display_config_message()
    # time.sleep(10)


