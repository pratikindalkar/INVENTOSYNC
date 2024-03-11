from tkinter import*
from PIL import Image,ImageTk          
from tkinter import ttk,messagebox
import sqlite3
class CategoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1250x630+270+140")
        self.root.title("InventoSync ( Inventory Management System )")
        self.root.config(bg="white")
        self.root.focus_force()
        #--Title--#
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        #--Title--#
        lbl_title=Label(self.root,text="Manage Product Category",font=("goudy old style",30),bg="darkgoldenrod",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_name=Label(self.root,text="Enter Category Name",font=("goudy old style",30),bg="white").place(x=50,y=120)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",25),bg="lightyellow").place(x=50,y=200,width=300)

        btn_add=Button(self.root,text="ADD",command=self.add,font=("goudy old style",20),bg="royalblue",fg="white",cursor="hand2").place(x=360,y=200,width=160,height=40)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",20),bg="red",fg="white",cursor="hand2").place(x=530,y=200,width=160,height=40)


        #--Category Details--#
        cat_frame=Frame(self.root,relief=RIDGE,bd=5)
        cat_frame.place(x=700,y=100,width=500,height=180)
        scolly=Scrollbar(cat_frame,orient=VERTICAL)
        scollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.CategoryTable=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scolly.set,xscrollcommand=scollx.set)
        scollx.pack(side=BOTTOM,fill=X)
        scolly.pack(side=RIGHT,fill=Y)
        scollx.config(command=self.CategoryTable.xview)
        scolly.config(command=self.CategoryTable.yview)
        

        self.CategoryTable.heading("cid",text="C ID")
        self.CategoryTable.heading("name",text="Name")
        self.CategoryTable["show"]="headings"

        self.CategoryTable.column("cid",width=90)
        self.CategoryTable.column("name",width=100)
        self.CategoryTable.pack(fill=BOTH,expand=1 )
        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data)


        #-- Images--#
        self.im1=Image.open("images/cat.jpg")
        self.im1=self.im1.resize((550,280))
        self.im1=ImageTk.PhotoImage(self.im1)

        self.lbl_im1=Label(self.root,image=self.im1,bd=2,relief=RAISED)
        self.lbl_im1.place(x=50,y=300)

        self.im2=Image.open("images/category.jpg")
        self.im2=self.im2.resize((550,280))
        self.im2=ImageTk.PhotoImage(self.im2)

        self.lbl_im2=Label(self.root,image=self.im2,bd=2,relief=RAISED)
        self.lbl_im2.place(x=650,y=300)
        self.show()

    #--Functions--#

    def add(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Category name should be required!",parent=self.root)
            elif len(self.var_name.get()) < 3 or len(self.var_name.get()) > 50:
                    messagebox.showerror("Error", "Category name should be between 3 to 50 characters!", parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Category already present, try different",parent=self.root)
                else:
                    cur.execute("Insert into category(name) values(?)",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            cur.execute("select * from category")
            rows=cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def get_data(self,ev):     
        f=self.CategoryTable.focus()
        content=(self.CategoryTable.item(f))
        row=content['values']
        #print(row)
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def delete(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Please select enter category from the list",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Error, Please try again",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

if __name__=="__main__":
    root=Tk()
    obj=CategoryClass(root)
    root.mainloop()