import sqlite3
from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import time
import os
import tempfile

class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1920x1080+0+0")
        self.root.title("InventoSync ( Inventory Management System )")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0

        #---Title---#
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text=" InventoSync ",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="darkgoldenrod",fg="white").place(x=0,y=0,relwidth=1,height=70)

        #--Btn Logout--#
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="peachpuff",cursor="hand2").place(x=1350,y=10,height=50,width=150)

        #--Clock--#
        self.lbl_clock=Label(self.root,text="Welcome To InventoSync\t\t Date: DD-MM-YYYY\t\t Time: HH-MM-SS ",font=("times new roman",17),bg="gainsboro")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=40)

        #--Product Frame--#
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE)
        ProductFrame1.place(x=6,y=115,width=485,height=650)
        pTitle=Label(ProductFrame1,text="All Product",font=("goudy old style",25,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

        #--Product Search Frame--#
        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE)
        ProductFrame2.place(x=3,y=48,width=472,height=110)

        lbl_search=Label(ProductFrame2,text="Search Product | By Name ",font=("times new roman",20,"bold"),fg="green",bg="white").place(x=2,y=5)

        lbl_search=Label(ProductFrame2,text="Product Name",font=("times new roman",20,"bold"),bg="white").place(x=2,y=50)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=180,y=55,width=162,height=30)
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=350,y=65,width=110,height=30)
        btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=350,y=20,width=110,height=30)

        #--Product Detail Frame--#
        ProductFrame3=Frame(ProductFrame1,relief=RIDGE,bd=5)
        ProductFrame3.place(x=3,y=162,width=468,height=475)
        scolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scolly.set,xscrollcommand=scollx.set)
        scollx.pack(side=BOTTOM,fill=X)
        scolly.pack(side=RIGHT,fill=Y)
        scollx.config(command=self.product_Table.xview)
        scolly.config(command=self.product_Table.yview)
        
        self.product_Table.heading("pid",text="Pid")
        self.product_Table.heading("name",text="Name")
        self.product_Table.heading("price",text="Price")
        self.product_Table.heading("qty",text="QTY")
        self.product_Table.heading("status",text="Status")
        self.product_Table["show"]="headings"
        self.product_Table.column("pid",width=40)
        self.product_Table.column("name",width=80)
        self.product_Table.column("price",width=80)
        self.product_Table.column("qty",width=40)
        self.product_Table.column("status",width=80)
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)

        lbl_note=Label(ProductFrame3,text="Note: 'Enter 0 Qty to remove product from the Cart",font=("goudy old style",16),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)

        #--Customer Frame--#
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        CustomerFrame1=Frame(self.root,bd=4,relief=RIDGE)
        CustomerFrame1.place(x=495,y=115,width=520,height=90)

        cTitle=Label(CustomerFrame1,text="Customer Details",font=("goudy old style",20),bg="lightgray").pack(side=TOP,fill=X)
        lbl_name=Label(CustomerFrame1,text="Name",font=("times new roman",20),bg="white").place(x=4,y=40)
        txt_name=Entry(CustomerFrame1,textvariable=self.var_cname,font=("times new roman",15),bg="lightyellow").place(x=75,y=45,width=175,height=30)
 
        lbl_contact=Label(CustomerFrame1,text="Contact No.",font=("times new roman",20),bg="white").place(x=250,y=40)
        txt_contact=Entry(CustomerFrame1,textvariable=self.var_contact,font=("times new roman",15),bg="lightyellow").place(x=385,y=45,width=124,height=30)
 
        #--Calculator Cart Frame--#
        cal_CartFrame=Frame(self.root,bd=4,relief=RIDGE)
        cal_CartFrame.place(x=495,y=210,width=520,height=430)

        #--Calculator Frame--#
        self.var_cal_input=StringVar()
        cal_Frame=Frame(cal_CartFrame,bd=9,relief=RIDGE)
        cal_Frame.place(x=5,y=5,width=295,height=410)

        txt_cal_input=Entry(cal_Frame,textvariable=self.var_cal_input,font=("arial",15,"bold"),width=22,bd=15,relief=GROOVE,state='readonly',justify=RIGHT) #Groove Input field in type any output show
        txt_cal_input.grid(row=0,columnspan=4)
        
        btn_7=Button(cal_Frame,text='7',font=('arial',16,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=18,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(cal_Frame,text='8',font=('arial',16,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=18,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(cal_Frame,text='9',font=('arial',16,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=18,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(cal_Frame,text='+',font=('arial',16,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=18,cursor="hand2").grid(row=1,column=3)
        
        btn_4=Button(cal_Frame,text='4',font=('arial',16,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=18,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(cal_Frame,text='5',font=('arial',16,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=18,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(cal_Frame,text='6',font=('arial',16,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=18,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(cal_Frame,text='-',font=('arial',16,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=18,cursor="hand2").grid(row=2,column=3)
        
        btn_1=Button(cal_Frame,text='1',font=('arial',16,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=18,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(cal_Frame,text='2',font=('arial',16,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=18,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(cal_Frame,text='3',font=('arial',16,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=18,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(cal_Frame,text='*',font=('arial',16,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=18,cursor="hand2").grid(row=3,column=3)
        
        btn_0=Button(cal_Frame,text='0',font=('arial',16,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=19,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(cal_Frame,text='C',font=('arial',16,'bold'),command=self.Clear_cal,bd=5,width=4,pady=19,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(cal_Frame,text='=',font=('arial',16,'bold'),command=self.Perform_cal,bd=5,width=4,pady=19,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(cal_Frame,text='/',font=('arial',16,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=19,cursor="hand2").grid(row=4,column=3)
        

        #--Cart Frame--#
        CartFrame=Frame(cal_CartFrame,relief=RIDGE,bd=5)
        CartFrame.place(x=305,y=5,width=208,height=410)
        self.cartTitle=Label(CartFrame,text="Cart     Total Product: [0]",font=("goudy old style",13),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)
        
        scolly=Scrollbar(CartFrame,orient=VERTICAL)
        scollx=Scrollbar(CartFrame,orient=HORIZONTAL)

        self.CartTable=ttk.Treeview(CartFrame,columns=("pid","name","price","qty"),yscrollcommand=scolly.set,xscrollcommand=scollx.set)
        scollx.pack(side=BOTTOM,fill=X)
        scolly.pack(side=RIGHT,fill=Y)
        scollx.config(command=self.CartTable.xview)
        scolly.config(command=self.CartTable.yview)
        
        
        self.CartTable.heading("pid",text="Pid")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="QTY")
        self.CartTable["show"]="headings"
        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=90)
        self.CartTable.column("price",width=50)
        self.CartTable.column("qty",width=40)
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)


        #--Add Cart Widgtes Frame--#
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        
        Add_CartWidgtesFrame=Frame(self.root,bd=4,relief=RIDGE)
        Add_CartWidgtesFrame.place(x=495,y=645,width=520,height=120)

        lbl_p_name=Label(Add_CartWidgtesFrame,text="Product Name",font=("times new roman",18),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgtesFrame,textvariable=self.var_pname,font=("times new roman",18),bg="lightyellow",state='readonly').place(x=5,y=40,width=190,height=30)

        lbl_p_price=Label(Add_CartWidgtesFrame,text="Price Per Qty",font=("times new roman",18),bg="white").place(x=220,y=5)
        txt_p_price=Entry(Add_CartWidgtesFrame,textvariable=self.var_price,font=("times new roman",18),bg="lightyellow",state='readonly').place(x=220,y=40,width=150,height=30)

        lbl_p_qty=Label(Add_CartWidgtesFrame,text="Quantity",font=("times new roman",18),bg="white").place(x=380,y=5)
        txt_p_qty=Entry(Add_CartWidgtesFrame,textvariable=self.var_qty,font=("times new roman",18),bg="lightyellow").place(x=385,y=40,width=120,height=30)

        self.lbl_inStock=Label(Add_CartWidgtesFrame,text="In Stock",font=("times new roman",18),bg="white")
        self.lbl_inStock.place(x=5,y=75)

        btn_Clear_Cart=Button(Add_CartWidgtesFrame,text="Clear",command=self.clearCart,font=("times new roman",18,"bold"),bg="lightgray",cursor="hand2").place(x=170,y=75,width=120,height=30)
        btn_Add_Cart=Button(Add_CartWidgtesFrame,text="Add | Update Cart",command=self.addUpdate_cart,font=("times new roman",18,"bold"),bg="orange",cursor="hand2").place(x=300,y=75,width=210,height=30)
        
        #--Billing Area--#
        BillFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        BillFrame.place(x=1020,y=115,width=500,height=500)

        bTitle=Label(BillFrame,text="Customer Bill Area",font=("goudy old style",25,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(BillFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(BillFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scolly.config(command=self.txt_bill_area.yview)

        #--Billing Buttons--#
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billMenuFrame.place(x=1020,y=620,width=500,height=143)

        self.lbl_amt=Label(billMenuFrame,text="Bill Amount\n[0]",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amt.place(x=2,y=5,width=160,height=70)

        self.lbl_disc=Label(billMenuFrame,text="Discount \n[5%]",font=("goudy old style",15,"bold"),bg="gray",fg="white")
        self.lbl_disc.place(x=170,y=5,width=160,height=70)

        self.lbl_netPay=Label(billMenuFrame,text="Net Pay\n[0]",font=("goudy old style",15,"bold"),bg="#009688",fg="white")
        self.lbl_netPay.place(x=338,y=5,width=160,height=70)

        btn_print=Button(billMenuFrame,text="Print",command=self.print_bill,font=("goudy old style",15,"bold"),cursor="hand2",bg="#3f51b5",fg="white")
        btn_print.place(x=2,y=80,width=160,height=50)

        btn_clearAll=Button(billMenuFrame,text="Clear All",command=self.ClearAll,font=("goudy old style",15,"bold"),cursor="hand2",bg="gray",fg="white")
        btn_clearAll.place(x=170,y=80,width=160,height=50)

        btn_generate=Button(billMenuFrame,text="Generate/Save Bill",command=self.generateBill,font=("goudy old style",15,"bold"),cursor="hand2",bg="#009688",fg="white")
        btn_generate.place(x=338,y=80,width=160,height=50)

        self.show()
        self.updateDateTime()

        #--All Functions--#
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def Clear_cal(self):
        self.var_cal_input.set('')

    def Perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))



    def show(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def search(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def get_data(self,ev):     
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def get_data_cart(self,ev):     
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])

    def addUpdate_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error','Please select the product from the list',parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror('Error','Quantity isRequired',parent=self.root)
        elif not self.var_qty.get().isdigit() or int(self.var_qty.get()) <= 0:
            messagebox.showerror('Error', 'Please enter a valid positive quantity', parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('Error','Invalid Quantity',parent=self.root)
        else:
            #price_cal=float(price_cal)
            #price_cal=int(self.var_qty.get())*float(self.var_price.get())
            price_cal=self.var_price.get()
            cartData=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            #--Update Cart--#
            Present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    Present='yes'
                    break
                index_+=1
            if Present=='yes':
                op=messagebox.askyesno('Confirm',"Product already present\nDo you want to Update | Remove from the Cart List",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal     #Price 
                        self.cart_list[index_][3]=self.var_qty.get()  #Qty
            else:
                self.cart_list.append(cartData)
            self.show_cart()
            self.billUpdate()


    def billUpdate(self):
        self.billAmt=0
        self.netPay=0
        self.discount=0
        for row in self.cart_list:
            self.billAmt=self.billAmt+(float(row[2])*int(row[3]))
        self.discount=(self.billAmt*5)/100
        self.netPay=self.billAmt-self.discount
        self.lbl_amt.config(text=f'Bill Amount(Rs.)\n{str(self.billAmt)}')
        self.lbl_netPay.config(text=f'Net Pay(Rs.)\n{str(self.netPay)}')
        self.cartTitle.config(text=f"Cart     Total Product: [{str(len(self.cart_list ))}]")


    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def generateBill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please Add Product to Cart",parent=self.root)
        else:
            #--Bill Top--#
            self.billTop()
            #--Bill Middle--#
            self.billMiddle()
            #--Bill Bottom--#
            self.billBottom()
            
            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill has been generated/Save in Backend!",parent=self.root)
            self.chk_print=1

    def billTop(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        billTopTemp=f'''
\t\t  Basti Boys-InventoSync
\t Phone No.:- 12345***** \t \tMumbai-400022
{str("="*47)}
    Customer Name :- {self.var_cname.get()}
    Phone No. :- {self.var_contact.get()}
    Bill No. :- {str(self.invoice)}\t\t\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
 {str("="*47)}
    Product Name \t\t\t\tQTY\t\tPrice
 {str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',billTopTemp)

        self.txt_bill_area.tag_configure("goudy_style", font=("goudy old style", 14))
        self.txt_bill_area.tag_add("goudy_style", "1.0", "end")


    def billBottom(self):
        billBottomTemp=f'''
{str("="*47)}
    Bill Amount\t\t\t\tRs.{self.billAmt}
    Discount\t\t\t\tRs.{self.discount}
    Net Pay\t\t\t\tRs.{self.netPay}
 {str("="*47)}\n
        '''
        self.txt_bill_area.insert(END,billBottomTemp)

    
    def billMiddle(self):
        con=sqlite3.connect(database=r'INVENTOSYNC.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    Status='Inactive'
                if int(row[3])!=int(row[4]):
                    Status='Active'
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n    "+name+"\t\t\t\t"+row[3]+"\t\tRs."+price )
                #--Update quantity in product Table--#
                cur.execute('Update product set qty=?,status=? where pid=?',(
                    qty,
                    Status,
                    pid
                ))
                con.commit() 
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    
    def clearCart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')

    
    def ClearAll(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart     Total Product: [0]")
        self.var_search.set('')
        #self.chk_print=0
        self.clearCart()
        self.show()
        self.show_cart()

    def updateDateTime(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome To InventoSync\t\t Date: {str(date_)}\t\t Time: {str(time_)} ")
        self.lbl_clock.after(200,self.updateDateTime)


    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
            newFile=tempfile.mktemp('.txt')
            open(newFile,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(newFile,'print')
        else:
            messagebox.showerror('Print',"Please generate bill, to print the receipt",parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")
            


if __name__=="__main__":
    root=Tk()
    obj=BillClass(root)
    root.mainloop()