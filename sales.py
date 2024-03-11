from tkinter import*
from typing import Any                     
from PIL import Image,ImageTk    
from tkinter import ttk,messagebox
import sqlite3
import os
class SalesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1250x630+270+140")
        self.root.title("InventoSync ( Inventory Management System )")
        self.root.config(bg="white")
        self.root.focus_force()

        self.bill_list=[]

        self.var_invoice=StringVar()

        #--Title--#
        lbl_title=Label(self.root,text="View Customer Bills",font=("goudy old style",30),bg="darkgoldenrod",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        lbl_invoice=Label(self.root,text="Invoice No.",font=("time new roman",25),bg="white").place(x=50,y=100)
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("time new roman",25),bg="lightyellow").place(x=240,y=105,width=250,height=40)

        btn_Search=Button(self.root,text="Search",command=self.search,font=("times new roman",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=500,y=105,width=150,height=40)
        btn_Clear=Button(self.root,text="Clear",command=self.Clear,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=660,y=105,width=150,height=40)

        #--Bill List--#
        sales_Frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_Frame.place(x=50,y=160,width=300,height=450)

        scrolly1=Scrollbar(sales_Frame,orient=VERTICAL)
        self.sales_List=Listbox(sales_Frame,font=("goudy old style",20),bg="white",yscrollcommand=scrolly1.set)
        scrolly1.pack(side=RIGHT,fill=Y)
        scrolly1.config(command=self.sales_List.yview)
        self.sales_List.pack(fill=BOTH,expand=1)
        self.sales_List.bind("<ButtonRelease-1>",self.get_data)

        #--Bill Area--#
        bill_Frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_Frame.place(x=380,y=160,width=470,height=450)

        lbl_title=Label(bill_Frame,text="Customer Bill Area",font=("goudy old style",25),bg="lightgreen").pack(side=TOP,fill=X)
 
        scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
        self.bill_area=Text(bill_Frame,bg="lightyellow",font=("goudy old style",10),yscrollcommand=scrolly2.set)
        self.bill_area.tag_configure("goudy_style", font=("goudy old style", 13))
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)


        #--Image--#
        self.bill_img=Image.open("images/cat2.jpg")
        self.bill_img=self.bill_img.resize((450,300))
        self.bill_img=ImageTk.PhotoImage(self.bill_img)

        lbl_image=Label(self.root,image=self.bill_img,bd=0)
        lbl_image.place(x=850,y=220,width=450, height=300)

        self.show()
    #------------------
    def show(self):
        del self.bill_list[:]
        self.sales_List.delete(0,END)
        #print(os.listdir('../INVENTOSYNC'))
        for i in os.listdir('bill'):
            #print(i.split('.'),i.split('.')[-1])
            if i.split('.')[-1]=="txt":
                self.sales_List.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self,ev):
        index=self.sales_List.curselection()
        file_name=self.sales_List.get(index)
        
        print(file_name)
        self.bill_area.delete('1.0',END)
        fp=open(f'bill/{file_name}','r')
        for i in fp:
            self.bill_area.insert(END,i,"goudy_style")
        fp.close()

    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice No. should be required!",parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                fp=open(f'bill/{self.var_invoice.get()}.txt','r')
                self.bill_area.delete('1.0',END)
                for i in fp:
                    self.bill_area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error","Invalid Invoice No.!",parent=self.root)
                 

    def Clear(self):
        self.show()
        self.bill_area.delete('1.0',END)

if __name__=="__main__":
    root=Tk()
    obj=SalesClass(root)
    root.mainloop()