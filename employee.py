from datetime import date
from datetime import datetime
from tkinter import*                     
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import re
class EmployeeClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1250x630+270+140")
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

        #--SearchFrame--#
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("goudy old style",17,"bold"),bd=2, relief=RIDGE,bg="white")
        SearchFrame.place(x=300,y=20,width=600,height=80)

        #--Option--#
        cmb_Search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Name","Email","Contact"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_Search.place(x=10,y=10,width=200)
        cmb_Search.current(0)

        txt_Search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=225,y=10)
        btn_Search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="green",fg="white",cursor="hand2").place(x=440,y=9,width=130,height=30)
        
        #--Title--#
        title=Label(self.root,text="Employee Details",font=("goudy old style",20),bg="darkgoldenrod",fg="white").place(x=50,y=120,width=1150)
        
        #--Content--#
        lbl_empid=Label(self.root,text="Emp Id",font=("goudy old style",20),bg="white").place(x=50,y=170)
        lbl_gender=Label(self.root,text="Gender",font=("goudy old style",20),bg="white").place(x=350,y=170)
        lbl_contact=Label(self.root,text="Contact No",font=("goudy old style",20),bg="white").place(x=750,y=170)
        txt_empid=Entry(self.root,textvariable=self.var_empid,font=("goudy old style",20),bg="lightyellow").place(x=150,y=170,width=180)
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=("Select","Male","Female","Other"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_gender.place(x=500,y=170,width=180)
        cmb_gender.current(0)
        txt_contact=Entry(self.root,textvariable=self.var_contactno,font=("goudy old style",20),bg="lightyellow").place(x=910,y=170,width=180)


        lbl_name=Label(self.root,text="Name",font=("goudy old style",20),bg="white").place(x=50,y=240)
        lbl_dob=Label(self.root,text="D.O.B",font=("goudy old style",20),bg="white").place(x=350,y=240)
        lbl_doj=Label(self.root,text="D.O.J",font=("goudy old style",20),bg="white").place(x=750,y=240)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",20),bg="lightyellow").place(x=150,y=240,width=180)
        txt_dob=Entry(self.root,textvariable=self.var_dob,font=("goudy old style",20),bg="lightyellow").place(x=500,y=240,width=180)
        txt_doj=Entry(self.root,textvariable=self.var_doj,font=("goudy old style",20),bg="lightyellow").place(x=910,y=240,width=180)

        lbl_email=Label(self.root,text="Email",font=("goudy old style",20),bg="white").place(x=50,y=310)
        lbl_pass=Label(self.root,text="Password",font=("goudy old style",20),bg="white").place(x=350,y=310)
        lbl_utype=Label(self.root,text="UserType",font=("goudy old style",20),bg="white").place(x=750,y=310)
        txt_email=Entry(self.root,textvariable=self.var_email,font=("goudy old style",20),bg="lightyellow").place(x=150,y=310,width=180)
        txt_pass=Entry(self.root,textvariable=self.var_password,font=("goudy old style",20),bg="lightyellow").place(x=500,y=310,width=180)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=("Admin","Employee"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_utype.place(x=910,y=310,width=180)
        cmb_utype.current(0)

        lbl_addr=Label(self.root,text="Address",font=("goudy old style",20),bg="white").place(x=50,y=380)
        lbl_sal=Label(self.root,text="Salary",font=("goudy old style",20),bg="white").place(x=500,y=380)
        self.txt_addr=Text(self.root,font=("goudy old style",20),bg="lightyellow")
        self.txt_addr.place(x=150,y=380,width=300,height=60)
        txt_sal=Entry(self.root,textvariable=self.var_sal,font=("goudy old style",20),bg="lightyellow").place(x=600,y=380,width=180)
        

        #--Buttons--#
        btn_Save=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="royalblue",fg="white",cursor="hand2").place(x=500,y=425,width=110,height=28)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="slategrey",fg="white",cursor="hand2").place(x=640,y=425,width=110,height=28)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="olive",fg="white",cursor="hand2").place(x=780,y=425,width=110,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="crimson",fg="white",cursor="hand2").place(x=920,y=425,width=110,height=28)

        #--Employee Details--#
        emp_frame=Frame(self.root,relief=RIDGE,bd=5)
        emp_frame.place(x=0,y=475,relwidth=1,height=150)

        scolly=Scrollbar(emp_frame,orient=VERTICAL)
        scollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.EmployeeTable=ttk.Treeview(emp_frame,columns=("eid","name","email","gender","contact","dob","doj","pass","utype","address","salary"),yscrollcommand=scolly.set,xscrollcommand=scollx.set)
        scollx.pack(side=BOTTOM,fill=X)
        scolly.pack(side=RIGHT,fill=Y)
        scollx.config(command=self.EmployeeTable.xview)
        scolly.config(command=self.EmployeeTable.yview)
        

        self.EmployeeTable.heading("eid",text="EMP ID")
        self.EmployeeTable.heading("name",text="Name")
        self.EmployeeTable.heading("email",text="Email")
        self.EmployeeTable.heading("gender",text="Gender")
        self.EmployeeTable.heading("contact",text="Contact")
        self.EmployeeTable.heading("dob",text="D.O.B")
        self.EmployeeTable.heading("doj",text="D.O.J")
        self.EmployeeTable.heading("pass",text="Password")
        self.EmployeeTable.heading("utype",text="User Type")
        self.EmployeeTable.heading("address",text="Address")
        self.EmployeeTable.heading("salary",text="Salary")
        self.EmployeeTable["show"]="headings"

        self.EmployeeTable.column("eid",width=90)
        self.EmployeeTable.column("name",width=100)
        self.EmployeeTable.column("email",width=100)
        self.EmployeeTable.column("gender",width=100)
        self.EmployeeTable.column("contact",width=100)
        self.EmployeeTable.column("dob",width=100)
        self.EmployeeTable.column("doj",width=100)
        self.EmployeeTable.column("pass",width=100)
        self.EmployeeTable.column("utype",width=100)
        self.EmployeeTable.column("address",width=100)
        self.EmployeeTable.column("salary",width=100)
        self.EmployeeTable["show"]="headings"
        self.EmployeeTable.pack(fill=BOTH,expand=1 )
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()
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
    def show(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            cur.execute("select * from employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def get_data(self,ev):     
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        print(row)  
        self.var_empid.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contactno.set(row[4])

        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
                                                        
        self.var_password.set(row[7])
        self.var_utype.set(row[8])
        self.txt_addr.delete('1.0',END)
        self.txt_addr.insert(END,row[9])
        self.var_sal.set(row[10]) 

    def update(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            if self.var_empid.get()=="":
                messagebox.showerror("Error","Employee ID must be required!",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_empid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    cur.execute("Update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",(
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
                                                self.var_empid.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success",f"Employee Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            if self.var_empid.get()=="":
                messagebox.showerror("Error","Employee ID must be required!",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_empid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from employee where eid=?",(self.var_empid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def clear(self):
        self.var_empid.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contactno.set("")

        self.var_dob.set("")
        self.var_doj.set("")
                                                        
        self.var_password.set(" ")
        self.var_utype.set("Admin")
        self.txt_addr.delete('1.0',END)
        self.var_sal.set("")
        self.var_searchby.set("Select")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search By Option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)
        
if __name__=="__main__":
    root=Tk()
    obj=EmployeeClass(root)
    root.mainloop()