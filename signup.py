from datetime import date
from tkinter import*                     
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import re
import datetime
from datetime import datetime
class SignUpClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+255+138")
        self.root.title("InventoSync ( Inventory Management System )")
        self.root.config(bg="white")
        self.root.focus_force()

        #--All Variables--#
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_empid=StringVar()
        self.var_name=StringVar()
        self.var_email=StringVar()
        self.var_address=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_password=StringVar()
        self.var_contactno=StringVar()
        self.var_doj=StringVar()
        self.var_utype=StringVar()
        self.var_sal=StringVar()

        
        #--Title--#
        title=Label(self.root,text="Employee Registration",font=("goudy old style",20),bg="darkgoldenrod",fg="white").place(x=50,y=30,width=1000)
        
        #--Content--#
        lbl_empid=Label(self.root,text="Emp Id",font=("goudy old style",20),bg="white").place(x=50,y=100)
        lbl_gender=Label(self.root,text="Gender",font=("goudy old style",20),bg="white").place(x=380,y=100)
        lbl_contact=Label(self.root,text="Contact No",font=("goudy old style",20),bg="white").place(x=720,y=100)
        txt_empid=Entry(self.root,textvariable=self.var_empid,font=("goudy old style",20),bg="lightyellow").place(x=150,y=100,width=180)
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=("Select","Male","Female","Other"),state='readonly',justify=CENTER,font=("goudy old style",20))
        cmb_gender.place(x=500,y=100,width=180)
        cmb_gender.current(0)
        txt_contact=Entry(self.root,textvariable=self.var_contactno,font=("goudy old style",20),bg="lightyellow").place(x=870,y=100,width=180)


        lbl_name=Label(self.root,text="Name",font=("goudy old style",20),bg="white").place(x=50,y=180)
        lbl_dob=Label(self.root,text="D.O.B",font=("goudy old style",20),bg="white").place(x=380,y=180)
        lbl_doj=Label(self.root,text="D.O.J",font=("goudy old style",20),bg="white").place(x=720,y=180)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",20),bg="lightyellow").place(x=150,y=180,width=180)
        txt_dob=Entry(self.root,textvariable=self.var_dob,font=("goudy old style",20),bg="lightyellow").place(x=500,y=180,width=180)
        txt_doj=Entry(self.root,textvariable=self.var_doj,font=("goudy old style",20),bg="lightyellow").place(x=870,y=180,width=180)

        lbl_email=Label(self.root,text="Email",font=("goudy old style",20),bg="white").place(x=50,y=260)
        lbl_pass=Label(self.root,text="Password",font=("goudy old style",20),bg="white").place(x=380,y=260)
        lbl_utype=Label(self.root,text="UserType",font=("goudy old style",20),bg="white").place(x=720,y=260)
        txt_email=Entry(self.root,textvariable=self.var_email,font=("goudy old style",20),bg="lightyellow").place(x=150,y=260,width=180)
        txt_pass=Entry(self.root,textvariable=self.var_password,font=("goudy old style",20),bg="lightyellow").place(x=500,y=260,width=180)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=("Admin","Employee"),state='readonly',justify=CENTER,font=("goudy old style",20))
        cmb_utype.place(x=870,y=260,width=180)
        cmb_utype.current(0)

        lbl_addr=Label(self.root,text="Address",font=("goudy old style",20),bg="white").place(x=50,y=330)
        lbl_sal=Label(self.root,text="Salary",font=("goudy old style",20),bg="white").place(x=500,y=330)
        self.txt_addr=Text(self.root,font=("goudy old style",20),bg="lightyellow")
        self.txt_addr.place(x=150,y=330,width=300,height=60)
        txt_sal=Entry(self.root,textvariable=self.var_sal,font=("goudy old style",20),bg="lightyellow").place(x=600,y=330,width=180)
        

        #-- Buttons --#
        btn_Save=Button(self.root,text="Submit",command=self.add,font=("goudy old style",15),bg="royalblue",fg="white",cursor="hand2").place(x=450,y=425,width=200,height=50)

       
    #--DataBase Connection Buttons--#
    def add(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            if self.var_empid.get()=="":
                messagebox.showerror("Error","Employee ID must be required!",parent=self.root)
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", self.var_email.get()):
                messagebox.showerror("Error", "Invalid email format", parent=self.root)
            elif datetime.strptime(self.var_dob.get(), "%Y-%m-%d").year >= 2004:
                messagebox.showerror("Error", "Date of Birth must be before 2004", parent=self.root)  
            elif len(self.var_password.get()) < 3:
                messagebox.showerror("Error", "Password should be at least 3 characters long", parent=self.root)
            elif not self.var_contactno.get().isdigit() or len(self.var_contactno.get()) != 10:
                    messagebox.showerror("Error", "Contact must be a valid 10-digit number", parent=self.root)              
            else:
                cur.execute("Select * from employee where eid=?",(self.var_empid.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Employee ID already assigned, try different",parent=self.root)
                else:
                    cur.execute("Insert into employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                                                self.var_empid.get(),
                                                self.var_name.get(),
                                                self.var_email.get(),
                                                self.var_gender.get(),
                                                self.var_contactno.get(),

                                                self.var_dob.get(),
                                                self.var_doj.get(),
                                                
                                                self.var_password.get(),
                                                self.var_utype.get(),
                                                self.txt_addr.get('1.0',END),
                                                self.var_sal.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success",f"Employee Added Successfully",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

        
if __name__=="__main__":
    root=Tk()
    obj=SignUpClass(root)
    root.mainloop()