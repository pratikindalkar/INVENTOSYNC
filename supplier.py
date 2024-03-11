from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox  
import sqlite3
class SupplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1250x630+270+140")
        self.root.title("InventoSync ( Inventory Management System )")
        self.root.config(bg="white")
        self.root.focus_force()

        #--All Variables--#
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contactno=StringVar()

        #--SearchFrame--#
        #--Option--#
        lbl_Search=Label(self.root,text="Invoice no.",bg="white",font=("goudy old style",20))
        lbl_Search.place(x=750,y=110)

        txt_Search=Entry(self.root,textvariable=self.var_searchtxt,font=("goudy old style",20),bg="lightyellow").place(x=880,y=110,width=200)
        btn_Search=Button(self.root,text="Search",font=("goudy old style",15),bg="green",fg="white",cursor="hand2").place(x=1090,y=110,width=110,height=28)
        
        #--Title--#
        title=Label(self.root,text="Supplier Details",font=("goudy old style",25,"bold"),bg="darkgoldenrod",fg="white").place(x=50,y=25,width=1150,height=50)
        
        #--Content--#
        lbl_supplier_invoice=Label(self.root,text="Invoice No.",font=("goudy old style",25),bg="white").place(x=50,y=140)
        txt_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",25),bg="lightyellow").place(x=230,y=140,width=300)
        
        lbl_name=Label(self.root,text="Name",font=("goudy old style",25),bg="white").place(x=50,y=210)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",25),bg="lightyellow").place(x=230,y=210,width=300)

        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",25),bg="white").place(x=50,y=280)
        txt_contact=Entry(self.root,textvariable=self.var_contactno,font=("goudy old style",25),bg="lightyellow").place(x=230,y=280,width=300)
        lbl_desc=Label(self.root,text="Description",font=("goudy old style",25),bg="white").place(x=50,y=350)
        self.txt_desc=Text(self.root,font=("goudy old style",25),bg="lightyellow")
        self.txt_desc.place(x=230,y=350,width=500,height=150)
        

        #--Buttons--#
        btn_Save=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="royalblue",fg="white",cursor="hand2").place(x=200,y=550,width=120,height=35)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="slategrey",fg="white",cursor="hand2").place(x=340,y=550,width=120,height=35)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="olive",fg="white",cursor="hand2").place(x=480,y=550,width=120,height=35)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="crimson",fg="white",cursor="hand2").place(x=620,y=550,width=120,height=35)

        #--Supplier Details--#
        sup_frame=Frame(self.root,relief=RIDGE,bd=5)
        sup_frame.place(x=750,y=150,width=470,height=430)
        scolly=Scrollbar(sup_frame,orient=VERTICAL)
        scollx=Scrollbar(sup_frame,orient=HORIZONTAL)

        self.SupplierTable=ttk.Treeview(sup_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scolly.set,xscrollcommand=scollx.set)
        scollx.pack(side=BOTTOM,fill=X)
        scolly.pack(side=RIGHT,fill=Y)
        scollx.config(command=self.SupplierTable.xview)
        scolly.config(command=self.SupplierTable.yview)
        

        self.SupplierTable.heading("invoice",text="Invoice No.")
        self.SupplierTable.heading("name",text="Name")
        self.SupplierTable.heading("contact",text="Contact")
        self.SupplierTable.heading("desc",text="Description")
        self.SupplierTable["show"]="headings"

        self.SupplierTable.column("invoice",width=50)
        self.SupplierTable.column("name",width=100)
        self.SupplierTable.column("contact",width=100)
        self.SupplierTable.column("desc",width=350)
        self.SupplierTable.pack(fill=BOTH,expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()
    #--DataBase Connection Buttons--#
    def add(self):
        con = sqlite3.connect(database=r'INVENTOSYNC.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required!", parent=self.root)
            elif not self.var_sup_invoice.get().isdigit():
                messagebox.showerror("Error", "Invoice No. must be a valid number!", parent=self.root)
            else:
                if len(self.var_name.get()) < 2 or len(self.var_name.get()) > 50:
                    messagebox.showerror("Error", "Name should be between 3 to 50 characters!", parent=self.root)
                elif not self.var_contactno.get().isdigit() or len(self.var_contactno.get()) != 10:
                    messagebox.showerror("Error", "Contact must be a valid 10-digit number!", parent=self.root)
                else:
                    cur.execute("Select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                    row = cur.fetchone()
                    if row is not None:
                        messagebox.showerror("Error", "Invoice no. already assigned, try different", parent=self.root)
                    else:
                        cur.execute("Insert into supplier(invoice,name,contact,desc) values(?,?,?,?)", (
                            self.var_sup_invoice.get(),
                            self.var_name.get(),
                            self.var_contactno.get(),
                            self.txt_desc.get('1.0', END),
                        ))
                        con.commit()
                        messagebox.showinfo("Success", "Supplier Added Successfully", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def show(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            cur.execute("select * from supplier")
            rows=cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def get_data(self,ev):     
        f=self.SupplierTable.focus()
        content=(self.SupplierTable.item(f))
        row=content['values']
        #print(row)
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contactno.set(row[2])
        self.txt_desc.delete('1.0',END)
        self.txt_desc.insert(END,row[3])

    def update(self):
        con = sqlite3.connect(database=r'INVENTOSYNC.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice no. must be required!", parent=self.root)
            elif not self.var_sup_invoice.get().isdigit():
                messagebox.showerror("Error", "Invoice no. must be a valid number!", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", f"Invalid Invoice no.", parent=self.root)
                else:
                    # Additional Validation Checks
                    if len(self.var_name.get()) < 2 or len(self.var_name.get()) > 50:
                        messagebox.showerror("Error", "Name should be between 3 to 50 characters!", parent=self.root)
                    elif not self.var_contactno.get().isdigit() or len(self.var_contactno.get()) != 10:
                        messagebox.showerror("Error", "Contact must be a valid 10-digit number!", parent=self.root)
                    else:
                        cur.execute("Update supplier set name=?,contact=?,desc=? where invoice=?", (
                            self.var_name.get(),
                            self.var_contactno.get(),
                            self.txt_desc.get('1.0', END),
                            self.var_sup_invoice.get(),
                        ))
                        con.commit()
                        messagebox.showinfo("Success", "Supplier Updated Successfully", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice no. must be required!",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice no.",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Suppplier Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contactno.set("")
        self.txt_desc.delete('1.0',END)
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Invoice no. should be required",parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?",(self.var_searchtxt.get()))
                row=cur.fetchone()
                if row!=None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)
           

if __name__=="__main__":
    root=Tk()
    obj=SupplierClass(root)
    root.mainloop()