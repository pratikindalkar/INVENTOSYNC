from tkinter import*
from PIL import ImageTk #pip install pillow
from tkinter import messagebox, Toplevel
import sqlite3
import os
from signup import SignUpClass
import emailPass
import smtplib
import time
class LoginSystem:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1920x1080+0+0")
        self.root.title("Login System ( Inventory Management System )")
        self.root.config(bg="white")

        self.otp=''

        #-- Image --#
        self.phoneImg=ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_phoneImg=Label(self.root,image=self.phoneImg,bd=0).place(x=280,y=90)

        #-- Login Frame --#
        self.employee_id=StringVar()
        self.password=StringVar()

        loginFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        loginFrame.place(x=750,y=130,width=350,height=460)

        title=Label(loginFrame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)
        
        lblUser=Label(loginFrame,text="Employee ID",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=100)
        txtUsername=Entry(loginFrame,textvariable=self.employee_id,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140,width=250,height=30)
        
        lblPass=Label(loginFrame,text="Password",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=190)
        txtPass=Entry(loginFrame,textvariable=self.password,font=("times new roman",15),bg="#ECECEC",show="*").place(x=50,y=230,width=250,height=30)

        btnLogin=Button(loginFrame,text="Log In",command=self.login,font=("Arial Rounded MT Bold",15),bg="#00B0F0",activebackground="#00B0F0",fg="white",activeforeground="white",cursor="hand2").place(x=50,y=300,width=250,height=40)

        hr=Label(loginFrame,bg="lightgray").place(x=50,y=370,width=250,height=2)
        or_=Label(loginFrame,text="OR",bg="white",fg="lightgray",font=("times new roman",15,"bold")).place(x=155,y=355)

        btnForget=Button(loginFrame,text="Forget Password?",command=self.forgetWindow,font=("times new roman",17),bg="white",fg="#00759E",bd=0,activebackground="white",activeforeground="#00759E").place(x=90,y=390)

        #-- Frame 2 --#
        registerFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        registerFrame.place(x=750,y=600,width=350,height=60)
        lbl_reg = Label(registerFrame, text="Don't have an account ? ", font=("times new roman", 18)).place(x=13, y=10)
        btnSignUp=Button(registerFrame,text="Sign Up",command=self.signup, font=("times new roman",16,"bold"),bg="white",cursor="hand2",fg="#00759E",bd=0,activebackground="white",activeforeground="#00759E").place(x=250,y=9)
        
        #-- Animation Imgaes --#
        self.im1=ImageTk.PhotoImage(file="images/im1.png")
        self.im2=ImageTk.PhotoImage(file="images/im2.png")
        self.im3=ImageTk.PhotoImage(file="images/im3.png")

        self.lbl_changeImage=Label(self.root,bg="white")
        self.lbl_changeImage.place(x=447,y=195,width=240,height=420)
        self.animate()

        
    #-- All Functions --#
    def signup(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=SignUpClass(self.new_win)

    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_changeImage.config(image=self.im)
        self.lbl_changeImage.after(2000,self.animate)

    def isEmployeeTableEmpty(self):
        try:
            con = sqlite3.connect(database=r'INVENTOSYNC.db')
            cur = con.cursor()
            cur.execute("select * from employee")
            rows = cur.fetchall()
            con.close()
            return len(rows) == 0
        except Exception as ex:
            print(f"Error checking if employee table is empty: {str(ex)}")
            return False

    def login(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        user = None
        try:
            if self.employee_id.get()=="" and self.password.get()=="":
                messagebox.showerror('Error',"All fields are Required",parent=self.root)
            else:
                # Check if the employee table is empty
                if self.isEmployeeTableEmpty():
                    messagebox.showerror('Error', "No employees in the system", parent=self.root)
                else:
                    cur.execute("select utype from employee where eid=? And pass=?",(self.employee_id.get(),self.password.get()))
                    user=cur.fetchone()
                    if user==None:
                        messagebox.showerror('Error',"Invalid USERNAME/PASSWORD?",parent=self.root)
                    else:
                        if user[0]=="Admin":
                            self.root.destroy()
                            os.system("python dashboard.py")
                        else:
                            self.root.destroy()
                            os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def forgetWindow(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror('Error',"Employee ID must be Required",parent=self.root)
            else:
                cur.execute("select email from employee where eid=?",(self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror('Error',"Invalid Employee ID,Try again",parent=self.root)
                else:
                    #-- Forget Window --#
                    self.var_otp=StringVar()
                    self.var_newPass=StringVar()
                    self.var_confPass=StringVar()
                    #-- Call SendEmail Function() --#
                    chk=self.sendEmail(email[0])
                    if chk=='f':
                        messagebox.showerror("Error","Connection Error,Try again",parent=self.root)
                    else:
                        self.forgetWin=Toplevel(self.root)
                        self.forgetWin.title('RESET PASSWORD')
                        self.forgetWin.geometry('400x350+500+100')
                        self.forgetWin.focus_force()

                        title=Label(self.forgetWin,text='Reset Password',font=('goudy old style',15,'bold'),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                        lblReset=Label(self.forgetWin,text="Enter OTP Sent on Registered Email",font=("times new roman",15)).place(x=20,y=60)
                        txtReset=Entry(self.forgetWin,textvariable=self.var_otp,font=("times new roman",15),bg="lightyellow").place(x=20,y=100,width=250,height=30)
                        self.btnReset=Button(self.forgetWin,text="SUBMIT",command=self.validateOtp,font=("times new roman",15),bg="lightblue")
                        self.btnReset.place(x=280,y=100,width=100,height=30)

                        lblnewPass=Label(self.forgetWin,text="Confirm Password",font=("times new roman",15)).place(x=20,y=160)
                        txtnewPass=Entry(self.forgetWin,textvariable=self.var_newPass,font=("times new roman",15),bg="lightyellow").place(x=20,y=190,width=250,height=30)

                        lblconfPass=Label(self.forgetWin,text=" New Password",font=("times new roman",15)).place(x=20,y=225)
                        txtconfPass=Entry(self.forgetWin,textvariable=self.var_confPass,font=("times new roman",15),bg="lightyellow").place(x=20,y=255,width=250,height=30)

                        self.btnUpdate=Button(self.forgetWin,text="Update",command=self.updatePassword,state=DISABLED,font=("times new roman",15),bg="lightblue")
                        self.btnUpdate.place(x=150,y=300,width=100,height=30)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def updatePassword(self):
        if self.var_newPass.get()=="" or self.var_confPass.get()=="":
            messagebox.showerror("Error","Password is Required",parent=self.forgetWin)
        elif self.var_newPass.get()!= self.var_confPass.get()=="":
            messagebox.showerror("Error","New Password & Confirm Password should be same",parent=self.forgetWin)
        else: 
            con=sqlite3.connect(database=r'INVENTOSYNC.db')
            cur=con.cursor()
            try:
                cur.execute("Update employee SET pass=? where eid=?",(self.var_newPass.get(),self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success","Password updated Successfully",parent=self.forgetWin)
                self.forgetWin.destroy()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)
                

    def validateOtp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btnUpdate.config(state=NORMAL)
            self.btnReset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP","Try Again",parent=self.forgetWin)

    def sendEmail(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=emailPass.email_
        pass_=emailPass.pass_
        s.login(email_,pass_)

        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        
        subj='InventoSync - Reset Password OTP'
        msg=f'Dear Sir/Madam, \n\nYour Reset OTP is {str(self.otp)}.\n\nWith Regards, \nInventoSync Team'
        msg="Subject : {}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'


root=Tk()
obj=LoginSystem(root)
root.mainloop()