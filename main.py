"""This is program"""
import pandas as pd
import os
import tkinter as tk
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox
from datetime import date, datetime, timedelta
from matplotlib.figure import Figure
from tkinter import ttk
from tkinter import font
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)



month = 1
year = int(str(date.today()).split("-")[0])
root = tk.Tk()
root.geometry('700x500')
root.title('Save Safe')
root.minsize(900, 700)
# root.resizable(False,False)
photo = tk.PhotoImage(file='./extention/Logo.png')
root.iconphoto(False, photo)


def main():
    """This is main function about window"""
    try:
        dataframe = pd.read_csv("data.csv")  # get data
    except:
        df = pd.DataFrame(columns=["ID", "TimeStamp","Money","MainType","Type","Description"])
        df.to_csv('data.csv',index=False)
    finally:
        dataframe = pd.read_csv("data.csv")

    income = money_calculating()[0]
    outcome = money_calculating()[1]
    
    income_box = tk.Label(root, text="Revenue\n"+str(round(income, 2)),
                          borderwidth=1, relief="solid", font='Helvetica 18 bold', fg="#FFFFFF")
    outcome_box = tk.Label(root, text="Expense\n"+str(round(outcome,2)),
                           borderwidth=1, relief="solid", font='Helvetica 18 bold', fg="#FFFFFF")
    remain_box = tk.Label(root, text="Remain\n"+str(round(income-outcome, 2)),
                          borderwidth=1, relief="solid", font='Helvetica 18 bold', fg="#FFFFFF")

    income_box.config(bg="#279D59")
    outcome_box.config(bg="#D82F35")
    remain_box.config(bg="#77A6ED")

    # Nav bar that show red green
    income_box.place(relx=0, rely=0, relwidth=(1/3), relheight=0.1)
    outcome_box.place(relx=(1/3), rely=0, relwidth=(1/3), relheight=0.1)
    remain_box.place(relx=(2/3), rely=0, relwidth=(1/3), relheight=0.1)

    now_date = str(date.today()).split("-")
    
    def plotting(m, y):
        global canvas, plot1, toolbar

        fig = Figure(figsize=(5, 5),
                     dpi=70)
        # list of squares
        df = pd.DataFrame(dataframe)
        df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])

        nowmonth = m
        nowyear = y
        

        listmonth = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                     'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        label_nowmonth = [listmonth[(nowmonth-1) % 12], listmonth[(nowmonth) % 12], listmonth[(nowmonth+1) % 12],
                          listmonth[(nowmonth+2) % 12], listmonth[(nowmonth+3) % 12]]

        def fit_m_posi(month, year):
            x = df[df['TimeStamp'].dt.year == year]
            x = x[x['TimeStamp'].dt.month == month+1]
            return x["Money"][x["Money"] >= 0].sum()

        def fit_m_negat(month, year):
            x = df[df['TimeStamp'].dt.year == year]
            x = x[x['TimeStamp'].dt.month == month+1]
            return abs(x["Money"][x["Money"] < 0].sum())
        data = [
            [fit_m_posi((nowmonth-1) % 12, nowyear), fit_m_posi((nowmonth) % 12, nowyear),
             fit_m_posi((nowmonth+1) %
                        12, nowyear), fit_m_posi((nowmonth+2) % 12, nowyear),
             fit_m_posi((nowmonth+3) % 12, nowyear)],


            [fit_m_negat((nowmonth-1) % 12, nowyear), fit_m_negat((nowmonth) % 12, nowyear),
             fit_m_negat((nowmonth+1) %
                         12, nowyear), fit_m_negat((nowmonth+2) % 12, nowyear),
             fit_m_negat((nowmonth+3) % 12, nowyear)]]
        # adding the subplot
        plot1 = fig.add_subplot(111)
        plot1.bar(label_nowmonth, data[0], width=0.2,
                  align='center', label='Revenue', color="green")
        plot1.bar(label_nowmonth, data[1], width=0.2,
                  align='edge', label='Expense', color="red")
        plot1.set_facecolor("#F0F3FC")
        fig.set_facecolor('#F0F3FC')
        
        plot1.set_title(nowyear)

        plot1.legend()
        canvas = FigureCanvasTkAgg(fig
                                   )
        canvas.draw()

        # placing the canvas on the Tkinter window
        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().place(relx=2/3, rely=0.1, relwidth=1/3, relheight=0.45)
        toolbar = NavigationToolbar2Tk( canvas, root)
        toolbar.place(relx=2/3, rely=0.55, relwidth=1/3, relheight=0.08)
    global sequence, plot_changeBtn, toolbar
    sequence = 0
    plotting(month, year)
    def change_graph():
        """change ploting of the graph"""
        global sequence, plot_changeBtn, toolbar
        plot1.clear()
        canvas.get_tk_widget().destroy()
        plot_changeBtn.destroy()
        toolbar.destroy()
        
        sequence += 1
        sequence = sequence%3
        if sequence == 0:
            plotting(month, year)
        elif sequence == 1:
            ploting_Revenue()
        elif sequence == 2:
            ploting_Expense()
        plot_changeBtn = tk.Button(root, text='Change', command=change_graph,bg='#1F3A63', fg="#FFFFFF")
        plot_changeBtn.place(relx=9.3/10, rely=0.12, relwidth=0.053, relheight=0.03)

    def ploting_Revenue():
        data = filt_er()
        data = data[data['MainType']=='Revenue']
        datadict = {
            "Salary":(data['Money'][data['Type']=='Salary']).sum(),
            "Business":(data['Money'][data['Type']=='Business']).sum(),
            "Refund":(data['Money'][data['Type']=='Refund']).sum(),
            "Borrow":(data['Money'][data['Type']=='Borrow']).sum(),
            "Other":(data['Money'][data['Type']=='Other']).sum()
        }
        print(datadict)
        fig = Figure(figsize=(4, 5),
                     dpi=60)
        
        plot1 = fig.add_subplot(111)
        plot1.barh(["Salary", "Business", "Refund","Borrow", "Other"], [datadict["Salary"],datadict["Business"],datadict["Refund"],datadict["Borrow"],datadict["Other"]], 
                  align='center', label='Revenue', color="green")
        plot1.legend()
        plot1.set_facecolor("#F0F3FC")
        fig.set_facecolor('#F0F3FC')
        plot1.set_title("Revenue")
        
        canvas = FigureCanvasTkAgg(fig,
                                   )
        canvas.draw()
        canvas.get_tk_widget().place(relx=2/3, rely=0.1, relwidth=1/3, relheight=0.45)
        toolbar = NavigationToolbar2Tk( canvas, root )
        toolbar.place(relx=2/3, rely=0.55, relwidth=1/3, relheight=0.08)
        

        print("ploting Revenue")
        print(data)
    def ploting_Expense():
        
        data = filt_er()
        data = data[data['MainType']=='Expense']
        datadict = {
            "Food & Drink":abs((data['Money'][data['Type']=='Food & Drink']).sum()),
            "Transport":abs((data['Money'][data['Type']=='Transport']).sum()),
            "Accommodation":abs((data['Money'][data['Type']=='Accommodation']).sum()),
            "Mobile":abs((data['Money'][data['Type']=='Mobile']).sum()),
            "Shopping":abs(data['Money'][data['Type']=='Shopping']).sum(),
            "Other":abs((data['Money'][data['Type']=='Other'])).sum()
        }
        fig = Figure(figsize=(5, 5),
                     dpi=60)
        
        plot1 = fig.add_subplot(111)
        plot1.barh(["Food&Drink","Transport", "Accommodation", "Mobile", "Shopping", "Other"],
                    [datadict["Food & Drink"],datadict["Transport"],datadict["Accommodation"],datadict["Mobile"],datadict["Shopping"],datadict["Other"]], 
                  align='center', label='Expense', color="red")
        plot1.legend()
        
        plot1.set_facecolor("#F0F3FC")
        fig.set_facecolor('#F0F3FC')
        plot1.set_title("Expense")
        
        canvas = FigureCanvasTkAgg(fig,
                                   )
        canvas.draw()
        canvas.get_tk_widget().place(relx=2/3, rely=0.1, relwidth=1/3, relheight=0.45)
        toolbar = NavigationToolbar2Tk( canvas, root )
        toolbar.place(relx=2/3, rely=0.55, relwidth=1/3, relheight=0.08)

        print("ploting Expense")
        print(data)
    plot_changeBtn = tk.Button(root, text='Change', command=change_graph,bg='#1F3A63', fg="#FFFFFF")
    plot_changeBtn.place(relx=9.3/10, rely=0.12, relwidth=0.053, relheight=0.03)
    def change_month_n():
        global month, sequence, toolbar
        sequence = 0
        month += 1
        
        if month > 12:
            month = 1

        plot1.clear()
        canvas.get_tk_widget().destroy()
        toolbar.destroy()
        plotting(month, year)
        
        plot_changeBtn = tk.Button(root, text='Change', command=change_graph,bg='#1F3A63', fg="#FFFFFF")
        plot_changeBtn.place(relx=9.3/10, rely=0.12, relwidth=0.053, relheight=0.03)
        

    def change_month_p():
        global month, sequence, toolbar
        sequence = 0
        month -= 1
        if month < -10:
            month = 1

        plot1.clear()
        canvas.get_tk_widget().destroy()
        toolbar.destroy()
        plotting(month, year)
        
        
        plot_changeBtn = tk.Button(root, text='Change', command=change_graph,bg='#1F3A63', fg="#FFFFFF")
        plot_changeBtn.place(relx=9.3/10, rely=0.12, relwidth=0.053, relheight=0.03)

    def change_year_n():
        global year, sequence, toolbar
        sequence = 0
        year += 1
        plot1.clear()
        canvas.get_tk_widget().destroy()
        toolbar.destroy()
        plotting(month, year)
        plot_changeBtn = tk.Button(root, text='Change', command=change_graph,bg='#1F3A63', fg="#FFFFFF")
        plot_changeBtn.place(relx=9.3/10, rely=0.12, relwidth=0.053, relheight=0.03)

    def change_year_p():
        global year, sequence, toolbar
        sequence = 0
        year -= 1
        plot1.clear()
        canvas.get_tk_widget().destroy()
        toolbar.destroy()
        plotting(month, year)
        plot_changeBtn = tk.Button(root, text='Change', command=change_graph,bg='#1F3A63', fg="#FFFFFF")
        plot_changeBtn.place(relx=9.3/10, rely=0.12, relwidth=0.053, relheight=0.03)

    next_m = tk.Button(root, text=">", command=change_month_n,
                       borderwidth=1, relief="solid", font=("Helvetica", 19),bg='#1F3A63', fg="#FFFFFF")

    next_m.place(relx=2.8/3, rely=0.64, relwidth=0.04, relheight=0.03)
    month_label = tk.Label(root, text="month")
    month_label.place(relx=2.65/3, rely=0.64, relwidth=0.042, relheight=0.03)
    pre_m = tk.Button(root, text="<", command=change_month_p,
                      borderwidth=1, relief="solid", font=("Helvetica", 19),bg='#1F3A63', fg="#FFFFFF")
    pre_m.place(relx=2.5/3, rely=0.64, relwidth=0.04, relheight=0.03)

    next_y = tk.Button(root, text=">", command=change_year_n,
                       borderwidth=1, relief="solid", font=("Helvetica", 19),bg='#1F3A63', fg="#FFFFFF")
    next_y.place(relx=2.35/3, rely=0.64, relwidth=0.04, relheight=0.03)
    year_label = tk.Label(root, text="year")
    year_label.place(relx=2.2/3, rely=0.64, relwidth=0.04, relheight=0.03)
    pre_y = tk.Button(root, text="<", command=change_year_p,
                      borderwidth=1, relief="solid", font=("Helvetica", 19),bg='#1F3A63', fg="#FFFFFF")
    pre_y.place(relx=2.05/3, rely=0.64, relwidth=0.04, relheight=0.03)

    # Adding Calendar

    cal = Calendar(root,
                   year=int(now_date[0]), month=int(now_date[1]),
                   day=int(now_date[2]), date_pattern="y-mm-dd", font="Helvetica 14 bold",firstweekday="sunday",
                   othermonthbackground='white',othermonthwebackground='white', bordercolor="black", headersbackground="white",
                   background="black",selectbackground='grey',borderwidth = 2,
                    normalforeground='black', weekendforeground='black', weekendbackground="white")
    
    cal.place(relx=0/2, rely=0.1, relwidth=2/3, relheight=0.5)

    # Button get date from Calendar
    current_date = datetime.now()

    # Calculate the first day of the current month
    first_day = current_date.replace(day=1)

    # Calculate the last day of the current month by adding one month and subtracting one day
    next_month = current_date.replace(day=28) + timedelta(days=4)  # Adding 4 days to avoid issues at the end of some months
    last_day = next_month - timedelta(days=next_month.day)

    # Format the dates as "yyyy-mm-dd"
    first_date_formatted = first_day.strftime('%Y-%m-%d')
    last_date_formatted = last_day.strftime('%Y-%m-%d')
    start_stop = [str(first_date_formatted), str(last_date_formatted)]

    def start_date():
        """Label showing start date"""
        global plot_changeBtn
        plot_changeBtn.destroy()
        container.destroy()
        start_stop[0] = cal.get_date()
        startdate.config(text=f"{'   '*20}{str(cal.get_date())}{'   '*20}")
        if sequence == 0:
            plotting(month, year)
        elif sequence == 1:
            ploting_Revenue()
        elif sequence == 2:
            ploting_Expense()
        plot_changeBtn = tk.Button(root, text='Change', command=change_graph,bg='#1F3A63', fg="#FFFFFF")
        plot_changeBtn.place(relx=9.3/10, rely=0.12, relwidth=0.053, relheight=0.03)
        
        create_list()

    def stop_date():
        """Label showing stop date"""
        global plot_changeBtn
        plot_changeBtn.destroy()
        container.destroy()
        start_stop[1] = cal.get_date()
        stopdate.config(text=f"{'   '*20}{str(cal.get_date())}{'   '*20}")
        if sequence == 0:
            plotting(month, year)
        elif sequence == 1:
            ploting_Revenue()
        elif sequence == 2:
            ploting_Expense()
        plot_changeBtn = tk.Button(root, text='Change', command=change_graph,bg='#1F3A63', fg="#FFFFFF")
        plot_changeBtn.place(relx=9.3/10, rely=0.12, relwidth=0.053, relheight=0.03)
        
        create_list()

    def filt_er():
        """function filtering data when click start and stop date and calculate..."""
        
        new_dataframe = dataframe
        if start_stop[0] > start_stop[1]:
            messagebox.showerror(
                "Error", "End date must not lower than Start date")
            reset_main()
        else:
            new_dataframe = dataframe[dataframe["TimeStamp"] >= start_stop[0]]
            new_dataframe = new_dataframe[dataframe["TimeStamp"]<= start_stop[1]]
            
            new_income = new_dataframe["Money"][new_dataframe["Money"] >= 0].sum(
            )
            new_outcome = new_dataframe["Money"][new_dataframe["Money"] < 0].sum(
            )
            new_remain = new_income - abs(new_outcome)
            income_box.config(text="Revenue\n"+str(round(new_income,2)))
            outcome_box.config(text="Expense\n"+str(round(abs(new_outcome),2)))
            remain_box.config(text="Remain\n"+str(round(new_remain, 2)))
        return new_dataframe

    # create and place start button
    
    # Label showing start date
    startdate_label = tk.Label(root, text="Start Date", font=("Helvetica", 14))
    startdate_label.place(relx=6.5/9, rely=0.7, relwidth=2/10, relheight=0.032)
    
    startdate = tk.Label(root, text=f"{'   '*20}{str(first_date_formatted)}{'   '*20}", font=font.Font(underline=True))
    startdate.place(relx=6.5/9, rely=0.74, relwidth=2/10, relheight=0.05)
    start_btn = tk.Button(root, text="Get",
                          command=start_date, borderwidth=1, relief="solid", font=("Helvetica", 13),bg='#1F3A63', fg="#FFFFFF")
    start_btn.place(relx=8/9, rely=0.7, relwidth=0.5/10, relheight=0.032)

    stop_btn = tk.Button(root, text="Get",
                         command=stop_date, borderwidth=1, relief="solid", font=("Helvetica", 13),bg='#1F3A63', fg="#FFFFFF")
    stop_btn.place(relx=8/9, rely=0.8, relwidth=0.5/10, relheight=0.032)

    stopdate_label = tk.Label(root, text="Stop Date", font=("Helvetica", 14))
    stopdate_label.place(relx=7/9, rely=0.8, relwidth=1/10, relheight=0.032)
    # Label showing stop date
    stopdate = tk.Label(root, text=f"{'   '*20}{str(last_date_formatted)}{'   '*20}", font=font.Font(underline=True))
    stopdate.place(relx=6.5/9, rely=0.84, relwidth=2/10, relheight=0.05)
    def create_list():
        global container
        container = ttk.Frame(root)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
      
        data = filt_er()
        data['TimeStamp'] = pd.to_datetime(data['TimeStamp'])
        df_sorted = data.sort_values(by='TimeStamp')
        df_sorted = df_sorted.reset_index(drop=True)
        print(df_sorted)
        index=0
    
        for index, row in df_sorted.iterrows():
            
            description = row['Description']
            if len(str(description)) > 27:
                description = description[:26]+'...'
            if row['MainType'] == "Expense":
                tk.Label(scrollable_frame, text=f" {description:35}", anchor='w', font="Helvetica 14").grid(row = index, column = 0, pady = 2, padx=10,sticky='W')
                tk.Label(scrollable_frame, text=f"-{str(abs(float(row['Money'])))} THB", anchor='e', font="Helvetica 14").grid(row = index, column = 1, pady = 2, padx=5,sticky='E')

            else:
                tk.Label(scrollable_frame, text=f" {description:35}", anchor='w', font="Helvetica 14").grid(row = index, column = 0, pady = 2, padx=10, sticky='W')
                tk.Label(scrollable_frame, text=f"+{str(abs(float(row['Money'])))} THB", anchor='e', font="Helvetica 14").grid(row = index, column = 1, pady = 2, padx=5,sticky='E')
        tk.Label(scrollable_frame, text="_"*38, anchor='w', font="Helvetica 14").grid(row = index+2, column = 0, pady = 2, sticky='W')
        tk.Label(scrollable_frame, text="_"*14, anchor='e', font="Helvetica 14").grid(row = index+2, column = 1, pady = 2,sticky='E')
        container.place(relheight=0.35,relwidth=2/3,rely=0.65)
    
        canvas.pack(fill='both', side='left', expand=True, padx=(0, 5))
        scrollbar.pack(side='right', fill='y')
        
        


    label_history = tk.Label(root, text=" Statements", font="Helvetica 18 bold",anchor='w')
    label_history.place(rely=0.6, relwidth=2/3, relheight=0.05)
    create_list()

    def reset_main():
        global month
        """This function destroy all main widgets and run function main() again"""
        for widget in root.winfo_children():
            widget.destroy()
        
        
        month = 1
        main()
    

    # Button for adding data to excel
    def add_data():
        """This function create page of adding data"""
        # Destroying widgets from first page
        for widget in root.winfo_children():
            widget.destroy()

        head = tk.Label(root, text="ประเภทของการเก็บข้อมูล", font="Helvetica 13 bold")
        head.place(relx=1/3, rely=0.1, relwidth=1/3, relheight=0.05)
      
        options = ["Revenue", "Expense"]
        
        option_type = {
            "Revenue" :["Salary", "Business", "Refund","Borrow", "Other"], #Food & Drinks
            "Expense" : ["Food & Drink","Transport", "Accommodation", "Mobile", "Shopping", "Other"]
        }
        type_label = tk.Label(root, text=f"หมวดหมู่รายรับ", font="Helvetica 13 bold")
        type_label.place(relx=1/3, rely=0.4, relwidth=1/3, relheight=0.05)
        type_box = ttk.Combobox(root, width=37, state='readonly')
        type_box['justify'] = 'left'
        type_box['values'] = option_type["Revenue"]
        type_box.set(option_type["Revenue"][0])
        type_box.place(relx=1/3, rely=0.45, relwidth=1/3, relheight=0.05)
        # Create Dropdown menu
        def print_selected_value(value):
            
            type_box.set(option_type[value][0])
            type_box['values'] = option_type[value]
            if value == 'Revenue':
                type_label.config(text="หมวดหมู่รายรับ")
            elif value == 'Expense':
                type_label.config(text="หมวดหมู่รายจ่าย")
        
        radio = tk.StringVar(root, value="Revenue")
        
        rev_radio  = tk.Radiobutton(root, text= options[0], variable=radio, value="Revenue", command=lambda: print_selected_value(radio.get()), font="Helvetica 13 bold")
        rev_radio.place(relx=1/3, rely=0.15, relwidth=1/3, relheight=0.05)
        ex_radio  = tk.Radiobutton(root, text= options[1], variable=radio, value="Expense",command=lambda: print_selected_value(radio.get()), font="Helvetica 13 bold")
        ex_radio.place(relx=1/3, rely=0.2, relwidth=1/3, relheight=0.05)
        
        
        date_label = tk.Label(root, text="เลือกวันที่", font="Helvetica 13 bold")
        date_label.place(relx=1/3, rely=0.27, relwidth=1/3, relheight=0.05)
        cal_en = DateEntry(root, selectmode='day', year=int(str(date.today()).split(
            "-")[0]), month=int(str(date.today()).split("-")[1]), day=int(str(date.today()).split("-")[2]))
        cal_en.place(relx=1/3, rely=0.33, relwidth=1/3, relheight=0.05)

        money_prompt = tk.Label(root, text="ใส่จำนวนเงิน", font="Helvetica 13 bold")
        money_prompt.place(relx=1/3, rely=0.53, relwidth=1/3, relheight=0.05)
        enter_money = tk.Entry()
        enter_money.place(relx=1/3, rely=0.58, relwidth=1/3, relheight=0.05)

        des_label = tk.Label(root, text="เพิ่มเติม", font="Helvetica 13 bold")
        des_label.place(relx=1/3, rely=0.66, relwidth=1/3, relheight=0.05)
        enter_des = tk.Entry()
        enter_des.place(relx=1/3, rely=0.72, relwidth=1/3, relheight=0.05)

        def to_excel():
            if len(enter_money.get()) >6:
                messagebox.showerror(
                    "Error", "Money must not more than 6 digits")
                return
            
            try:
                assert float(enter_money.get()) > 0
                
            except:
                messagebox.showerror(
                    "Error", "Money must be numeric and more than zero")
            else:
                try:
                    assert type_box.get() != "Choose something"
                except:
                    messagebox.showerror(
                    "Error", "You forgot to choose type")
                else:
                    lst_type = radio.get()
                    money = enter_money.get()
                    des = enter_des.get()
                    if des == '':
                        des = 'Null'
                    if lst_type == "Expense":
                        money = 0-float(money)

                    dataframe.loc[len(dataframe.index)] = [len(dataframe.index)+1,str(cal_en.get_date()), str(money),lst_type, type_box.get(), des]
                    dataframe.to_csv("data.csv", index=False)
                    
                    messagebox.showinfo("Successful", "Your data is collected\nDate: "+str(
                        cal_en.get_date())+"\nMoney: "+str(enter_money.get()))
                    goback_tomain()
        def reset_data():
            try:
                os.remove('data.csv')
            finally:
                messagebox.showinfo('Data Deleted',"All data is deleted.")
        def show_warning():
            result = messagebox.askyesno("Warning", "All data will be reset. Are you sure you want to proceed?")
            
            if result:
                reset_data()
            else:
                
                print("Cancelled.")
        reset_data_btn = tk.Button(root, text="Reset",
                                command=show_warning, borderwidth=1, relief="solid",bg='#1F3A63', fg="#FFFFFF")
        reset_data_btn.place(relx=3.5/5, rely=0.92, relwidth=0.7/10, relheight=0.05)
        
        toexcel_btn = tk.Button(root, text="Save",
                                command=to_excel, borderwidth=1, relief="solid",bg='#1F3A63', fg="#FFFFFF")
        toexcel_btn.place(relx=4/5, rely=0.92, relwidth=0.7/10, relheight=0.05)

        def goback_tomain():
            """Function destroy add data page and go back to main page"""
            for widget in root.winfo_children():
                widget.destroy()
            main()
        goback_btn = tk.Button(
            root, text="Back", command=goback_tomain, borderwidth=1, relief="solid",bg='#1F3A63', fg="#FFFFFF")
        goback_btn.place(relx=4.5/5, rely=0.92,
                         relwidth=0.7/10, relheight=0.05)
        
    reset_btn = tk.Button(root, text="RESET",
                          command=reset_main, borderwidth=1, relief="solid",bg='#1F3A63', fg="#FFFFFF", font="Helvetica 13 bold")
    reset_btn.place(relx=3.55/5, rely=0.9, relwidth=0.9/10, relheight=0.06)

    add = tk.Button(root, text="Add", command=add_data,
                    borderwidth=1, relief="solid",bg='#1F3A63', fg="#FFFFFF", font="Helvetica 13 bold")
    add.place(relx=4.25/5, rely=0.9, relwidth=0.9/10, relheight=0.06)


def data_preparation(data):
    try:
        data
    except:
        return 0
    else:
        return data


def money_calculating():
    
    dataframe = pd.read_csv("data.csv").sort_values(
        by=['TimeStamp']).reset_index()  # get data
    income = abs(data_preparation(
        dataframe["Money"][dataframe["Money"] >= 0].sum()))
    outcome = abs(data_preparation(
        dataframe["Money"][dataframe["Money"] < 0].sum()))
    
    return [income, outcome]


main()
root.mainloop()
