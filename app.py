# Imports
import smtplib
import socket
import ssl
from email.mime.text import MIMEText
from tkinter import *
from tkinter import messagebox

socket.setdefaulttimeout(20)

large_font = ("Verdana", 12)


class Project(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.container = Frame(self)

        self.container.pack(side='top', fill='both', expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (EmailInput, EmailMessage):
            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')

            self.show_frame(EmailInput)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class EmailInput(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        controller.geometry("800x600")

        Password = None

        # Entry's
        self.password = Entry(self, width=45, show="*")

        # Labels
        self.title = Label(self, text="Enter your email password", font=large_font)
        self.password_label = Label(self, text="Enter your email password", font=large_font)

        # Button
        self.store_password = Button(self, text="Store Password", font=large_font, command=self.cache_password)
        self.next_page = Button(self, text="Messages", font=large_font, command=lambda: controller.show_frame(EmailMessage))

        # Placements
        self.title.pack()

        self.password_label.place(x=40, y=258)
        self.password.place(x=270, y=260)

        self.store_password.place(x=325, y=350)
        self.next_page.place(x=345, y=390)

    def cache_password(self):
        try:
            global Password
            Password = str(self.password.get())

        except EXCEPTION as e:
            print(e)

        finally:
            if self.password.get() == '':
                print("Nothing was added.")
            self.password.delete(0, END)


class EmailMessage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Labels
        self.title = Label(self, text="Enter the information", font=large_font)
        self.message_label = Label(self, text="Type the message \n you want to send", font=large_font)
        self.password_label = Label(self, text="Enter Password", font=large_font)
        self.receipts_email_label = Label(self, text="Receipts email address", font=large_font)
        self.sender_email_label = Label(self, text="Your email address", font=large_font)

        # Entry's
        self.message = Entry(self, width=45)
        self.password = Entry(self, width=45, show='*')
        self.receipts_email = Entry(self, width=45)
        self.sender_email = Entry(self, width=45)

        # Buttons
        self.send_message = Button(self, text="Send Message", command=self.Send)
        self.back = Button(self, text='Back', command=lambda: controller.show_frame(EmailInput))

        # Placements
        self.title.pack()

        self.sender_email_label.place(x=50, y=160)
        self.sender_email.place(x=270, y=160)

        self.receipts_email_label.place(x=40, y=188)
        self.receipts_email.place(x=270, y=191)

        self.password_label.place(x=50, y=268)
        self.password.place(x=270, y=270)

        self.message_label.place(x=50, y=218)
        self.message.place(x=270, y=230)

        self.send_message.place(x=340, y=320)

    def Send(self):
        password = Password
        if str(self.password.get()) == password:
            # Message and Server Variables
            smtp_ssl_host = "smtp.gmail.com"
            smtp_port = 587
            # Message
            msg = MIMEText(str(self.message.get()))
            msg['From'] = self.sender_email.get()
            msg['Subject'] = 'sent from python project'
            msg['To'] = str(self.receipts_email.get())
            # Server
            mail_server = smtplib.SMTP(smtp_ssl_host, smtp_port)
            mail_server.ehlo()
            mail_server.starttls(context=ssl.create_default_context())
            mail_server.login(str(self.sender_email.get()), str(self.password.get()))
            mail_server.sendmail(str(self.sender_email.get()), str(self.receipts_email.get()), msg.as_string())
            if mail_server == smtplib.SMTPAuthenticationError:
                email_false = messagebox.showerror(title="False Email", message="login information is incorrect")
                if email_false == "ok":
                    pass
            if self.message.get() == "":
                no_message = messagebox.showinfo(title="No message", message="No message was entered")
                if no_message == "ok":
                    pass
            if mail_server is not smtplib.SMTPException:
                email_sent = messagebox.showinfo(title="Sent", message="Your has been email sent to recipient")
                if email_sent == 'ok':
                    pass
            mail_server.quit()

            self.sender_email.delete(0, END)
            self.receipts_email.delete(0, END)
            self.message.delete(0, END)
            self.password.delete(0, END)

        else:
            return print("Password is incorrect or no password was entered")


if __name__ == '__main__':
    app = Project()
    app.mainloop()
