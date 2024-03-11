from datetime import date
from tkinter import*                     
from PIL import Image,ImageTk    
from tkinter import ttk,messagebox
import sqlite3
class ProductClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1250x630+270+140")
        self.root.title("InventoSync ( Inventory Management System )")
        self.root.config(bg="white")
        self.root.focus_force()

        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar() 
        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()

        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()

        product_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_frame.place(x=10,y=10,width=500,height=600)

        #--Title--#
        title=Label(product_frame,text="Manage Product Details",font=("goudy old style",30),bg="darkgoldenrod",fg="white").pack(side=TOP,fill=X)
        
        #--Column 1--#
        lbl_category=Label(product_frame,text="Category",font=("goudy old style",30),bg="white").place(x=30,y=60)
        lbl_supplier=Label(product_frame,text="Supplier",font=("goudy old style",30),bg="white").place(x=30,y=125)
        lbl_product=Label(product_frame,text="Name",font=("goudy old style",30),bg="white").place(x=30,y=190)
        lbl_price=Label(product_frame,text="Price",font=("goudy old style",30),bg="white").place(x=30,y=257)
        lbl_qty=Label(product_frame,text="Quantity",font=("goudy old style",30),bg="white").place(x=30,y=322)
        lbl_status=Label(product_frame,text="Status",font=("goudy old style",30),bg="white").place(x=30,y=390)

        #--Column 2--#
        cmb_cat=ttk.Combobox(product_frame,textvariable=self.var_cat,values=self.cat_list,state='readonly',justify=CENTER,font=("goudy old style",20))
        cmb_cat.place(x=225,y=75,width=200)
        cmb_cat.current(0)

        cmb_sup=ttk.Combobox(product_frame,textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=CENTER,font=("goudy old style",20))
        cmb_sup.place(x=225,y=140,width=200)
        cmb_sup.current(0)


        txt_name=Entry(product_frame,textvariable=self.var_name,font=("goudy old style",20),bg="lightyellow").place(x=225,y=205,width=200)
        txt_price=Entry(product_frame,textvariable=self.var_price,font=("goudy old style",20),bg="lightyellow").place(x=225,y=270,width=200)
        txt_qty=Entry(product_frame,textvariable=self.var_qty,font=("goudy old style",20),bg="lightyellow").place(x=225,y=335,width=200)

        cmb_status=ttk.Combobox(product_frame,textvariable=self.var_status,values=("Active","Inactive"),state='readonly',justify=CENTER,font=("goudy old style",20))
        cmb_status.place(x=225,y=400,width=200)
        cmb_status.current(0)


        #--Buttons--#
        btn_Save=Button(product_frame,text="Save",command=self.add,font=("goudy old style",15),bg="royalblue",fg="white",cursor="hand2").place(x=10,y=500,width=105,height=50)
        btn_update=Button(product_frame,text="Update",command=self.update,font=("goudy old style",15),bg="slategrey",fg="white",cursor="hand2").place(x=135,y=500,width=105,height=50)
        btn_delete=Button(product_frame,text="Delete",command=self.delete,font=("goudy old style",15),bg="olive",fg="white",cursor="hand2").place(x=260,y=500,width=105,height=50)
        btn_clear=Button(product_frame,text="Clear",command=self.clear,font=("goudy old style",15),bg="crimson",fg="white",cursor="hand2").place(x=385,y=500,width=105,height=50)

        #--SearchFrame--#
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("goudy old style",25,"bold"),bd=2, relief=RIDGE,bg="white")
        SearchFrame.place(x=560,y=10,width=650,height=120)

        #--Option--#
        cmb_Search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Category","Supplier","Name"),state='readonly',justify=CENTER,font=("goudy old style",20))
        cmb_Search.place(x=13,y=18,width=200)
        cmb_Search.current(0)
 
        txt_Search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",20),bg="lightyellow").place(x=225,y=18,width=250)
        btn_Search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="green",fg="white",cursor="hand2").place(x=490,y=18,width=130)




        #--Product Details--#
        p_frame=Frame(self.root,relief=RIDGE,bd=5)
        p_frame.place(x=530,y=150,width=700,height=450)

        scolly=Scrollbar(p_frame,orient=VERTICAL)
        scollx=Scrollbar(p_frame,orient=HORIZONTAL)

        self.ProductTable=ttk.Treeview(p_frame,columns=("pid","Supplier","Category","Name","Price","Qty","Status"),yscrollcommand=scolly.set,xscrollcommand=scollx.set)
        scollx.pack(side=BOTTOM,fill=X)
        scolly.pack(side=RIGHT,fill=Y)
        scollx.config(command=self.ProductTable.xview)
        scolly.config(command=self.ProductTable.yview)
        

        self.ProductTable.heading("pid",text="PID")
        self.ProductTable.heading("Category",text="Category")
        self.ProductTable.heading("Supplier",text="Supplier")
        self.ProductTable.heading("Name",text="Name")
        self.ProductTable.heading("Price",text="Price")
        self.ProductTable.heading("Qty",text="QTY")
        self.ProductTable.heading("Status",text="Status")
        
        self.ProductTable["show"]="headings"

        self.ProductTable.column("pid",width=90)
        self.ProductTable.column("Category",width=100)
        self.ProductTable.column("Supplier",width=100)
        self.ProductTable.column("Name",width=100)
        self.ProductTable.column("Price",width=100)
        self.ProductTable.column("Qty",width=100)
        self.ProductTable.column("Status",width=100)
        self.ProductTable.pack(fill=BOTH,expand=1 )
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()

        #--DataBase Connection Buttons--#
    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            cur.execute("Select name from category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute("Select name from supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def add(self):
        con = sqlite3.connect(database=r'INVENTOSYNC.db')
        cur = con.cursor()
        try:
            if (
                self.var_cat.get() == "Select"
                or self.var_cat.get() == "Empty"
                or self.var_sup.get() == "Select"
                or self.var_name.get() == ""
                or self.var_price.get() == ""
                or self.var_qty.get() == ""
            ):
                messagebox.showerror("Error", "All fields are required!", parent=self.root)
            else:
                # Add validation for quantity and price
                try:
                    qty = float(self.var_qty.get())
                    price = float(self.var_price.get())
                except ValueError:
                    messagebox.showerror("Error", "Quantity and Price must be numeric values", parent=self.root)
                    return

                # Check if the quantity and price are greater than zero
                if qty <= 0 or price <= 0:
                    messagebox.showerror("Error", "Quantity and Price must be greater than zero", parent=self.root)
                    return

                cur.execute("Select * from product where Name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Product already Present, try different", parent=self.root)
                else:
                    cur.execute(
                        "Insert into product(Category,Supplier,name,price,qty,status) values(?,?,?,?,?,?)",
                        (
                            self.var_cat.get(),
                            self.var_sup.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),
                        ),
                    )
                    con.commit()
                    messagebox.showinfo("Success", f"Product  Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def show(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def get_data(self,ev):     
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']
        self.var_pid.set(row[0]),
        self.var_cat.set(row[2]),
        self.var_sup.set(row[1]),
        self.var_name.set(row[3]),
        self.var_price.set(row[4]),
        self.var_qty.set(row[5]),
        self.var_status.set(row[6]),
        

    def update(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Please select from the product list!",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    cur.execute("Update product set Category=?,Supplier=?,name=?,price=?,qty=?,status=? where pid=?",(
                                                self.var_cat.get(),
                                                self.var_sup.get(),
                                                self.var_name.get(),
                                                self.var_price.get(),
                                                self.var_qty.get(),
                                                self.var_status.get(),
                                                self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success",f"Product Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Select Product from the List!",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def clear(self):
        self.var_cat.set("Select"),
        self.var_sup.set("Select"),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_qty.set(""),
        self.var_status.set("Active"),
        self.var_pid.set("")
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
                cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

if __name__=="__main__":
    root=Tk()
    obj=ProductClass(root)
    root.mainloop()