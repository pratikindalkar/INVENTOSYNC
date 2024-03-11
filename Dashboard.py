import sqlite3
import os
import time
from tkinter import*
from tkinter import messagebox
from PIL import Image,ImageTk
from employee import EmployeeClass
from supplier import SupplierClass
from category import CategoryClass
from product import ProductClass
from billing import BillClass
from sales import SalesClass
class InventoSync:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1920x1080+0+0")
        self.root.title("InventoSync ( Inventory Management System )")
        self.root.config(bg="white")

        #---Title---#
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text=" InventoSync ",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="darkgoldenrod",fg="white").place(x=0,y=0,relwidth=1,height=70)

        #--Btn Logout--#
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="peachpuff",cursor="hand2").place(x=1350,y=10,height=50,width=150)

        #--Clock--#
        self.lbl_clock=Label(self.root,text="Welcome To InventoSync\t\t Date: DD-MM-YYYY\t\t Time: HH-MM-SS ",font=("times new roman",17),bg="gainsboro")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=40)

        #--Left Menu--#
        self.MenuLogo=Image.open("images/menu_im.png")
        self.MenuLogo=self.MenuLogo.resize((250,250))
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=115,width=275,height=675)  

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)

        self.icon_side=PhotoImage(file="images/side.png")
        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",25),bg="darkcyan").pack(side=TOP,fill=X)

        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,anchor="w",padx=15,font=("times new roman",23,"bold"),bd=3,bg="white",cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,image=self.icon_side,compound=LEFT,anchor="w",padx=15,font=("times new roman",23,"bold"),bd=3,bg="white",cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Category",command=self.category,image=self.icon_side,compound=LEFT,anchor="w",padx=15,font=("times new roman",23,"bold"),bd=3,bg="white",cursor="hand2").pack(side=TOP,fill=X)
        btn_product=Button(LeftMenu,text="Product",command=self.product,image=self.icon_side,compound=LEFT,anchor="w",padx=15,font=("times new roman",23,"bold"),bd=3,bg="white",cursor="hand2").pack(side=TOP,fill=X)
        btn_billing=Button(LeftMenu,text="Billing",command=self.bill,image=self.icon_side,compound=LEFT,anchor="w",padx=15,font=("times new roman",23,"bold"),bd=3,bg="white",cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,anchor="w",padx=15,font=("times new roman",23,"bold"),bd=3,bg="white",cursor="hand2").pack(side=TOP,fill=X)
        
        #--Content--#
        self.lbl_employee=Label(self.root,text="Total Employee\n [ 0 ]",bd=5,relief=RIDGE,bg="crimson",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=350,y=170,height=150,width=300)

        self.lbl_supplier=Label(self.root,text="Total Supplier\n [ 0 ]",bd=5,relief=RIDGE,bg="olive",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=750,y=170,height=150,width=300)

        self.lbl_category=Label(self.root,text="Total Category\n [ 0 ]",bd=5,relief=RIDGE,bg="slategrey",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=1150,y=170,height=150,width=300)

        self.lbl_product=Label(self.root,text="Total Product\n [ 0 ]",bd=5,relief=RIDGE,bg="royalblue",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_product.place(x=350,y=370,height=150,width=300)

        self.lbl_sales=Label(self.root,text="Total Sales\n [ 0 ]",bd=5,relief=RIDGE,bg="yellowgreen",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=750,y=370,height=150,width=300)

        self.updateContent()

        #--On Button__#
    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=EmployeeClass(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=SupplierClass(self.new_win)

    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=CategoryClass(self.new_win)
    
    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=ProductClass(self.new_win)
    
    def bill(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=BillClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=SalesClass(self.new_win)

    def updateContent(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f'Total Product\n [ {str(len(product))} ]')

            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f'Total Supplier\n [ {str(len(supplier))} ]')

            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f'Total category\n [ {str(len(category))} ]')

            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f'Total employee\n [ {str(len(employee))} ]')
            self.lbl_sales.config(text=f'Total sales\n [ {str(len(os.listdir('bill')))} ]')

            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome To InventoSync\t\t Date: {str(date_)}\t\t Time: {str(time_)} ")
            self.lbl_clock.after(200,self.updateContent)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")


if __name__=="__main__":
    root=Tk()
    obj=InventoSync(root)
    root.mainloop()