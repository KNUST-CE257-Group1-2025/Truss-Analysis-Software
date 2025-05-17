# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 21:55:44 2025

@author: hp
"""

#importation of relevant modules
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np  
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#definition of classes and attributes of the truss
class joint():
    def __init__(self,name,x,y):
        self.name= name
        self.x= x
        self.y= y

class member():
    def __init__(self,name,joint1,joint2):
        self.name= name
        self.joint1= joint1
        self.joint2= joint2
    
    def length(self):
        x1=self.joint1.x
        y1=self.joint1.y
        x2=self.joint2.x
        y2=self.joint2.y
        distance=np.sqrt(((x2-x1)**2)+((y2-y1)**2))
        return distance
    
    def vertical_component(self):
        y1=self.joint1.y
        y2=self.joint2.y
        v_component=y2-y1
        return v_component
    
    def horizontal_component(self):
        x1=self.joint1.x
        x2=self.joint2.x      
        h_component=x2-x1
        return h_component
    
    def hypotenuse(self):#edited the variables of the hypotenuse function
        y1=self.joint1.y
        y2=self.joint2.y
        v_component=y2-y1
        x1=self.joint1.x
        x2=self.joint2.x      
        h_component=x2-x1
        hypotenuse=np.sqrt((v_component**2)+(h_component**2))
        return hypotenuse
        
class hinge():
    def __init__(self,joint):
        self.joint=joint
        
class horizontalRoller():
    def __init__(self,joint):
        self.joint=joint
        
class verticalRoller():
    def __init__(self,joint):
        self.joint=joint

class force():
    def __init__(self,joint,magnitude,angle):
        self.joint=joint
        self.magnitude=magnitude
        self.angle=angle
        
    def horizontal_component(self):
        magnitude=self.magnitude
        angle=np.radians(self.angle)#edited
        h_component=magnitude*np.cos(angle)
        return h_component
    
    def vertical_component(self):
        magnitude=self.magnitude
        angle=np.radians(self.angle)#edited
        v_component=magnitude*np.sin(angle)
        return v_component

#display of creators info and app info when program starts
def information():
    info=tk.Toplevel(win)
    info.title("")
    info.geometry("+200+150")#offsets the pop up window
    info.attributes('-topmost', True)#displays the pop up window above the main window
    info.resizable(False,False)
    info.iconbitmap("roof.ico")
    heading="🧾 About This Application"
    paragraph="Truss Analysis Software is a graphical, user-friendly application designed to assist engineering\nstudents and professionals in performing static analysis of planar statically determinate trusses.\n\nWith this tool, users can define joints, members, supports, and loads, and then compute internal forces\n\
and reactions while visualizing the truss structure.\n\nThis application was developed by Yoofi Smith and Nana Kwame Agyeman, second-year Civil Engineering\nstudents of Kwame Nkrumah University of Science and Technology (KNUST), as part of their coursework in CE 257."
    contact_info="For inquiries, feedback, or collaboration opportunities, the authors can be contacted via:\n\
Email: yoofismith@gmail.com, nanakwamekyeretwieagyeman@gmail.com\n\
Department of Civil Engineering, KNUST, Kumasi, Ghana.\n\n\
We hope this tool proves useful in your academic or professional journey.\nGood luck in your research and structural explorations!"
    heading_label=ttk.Label(info,text=heading,justify="center")  
    heading_label.grid(column=0,row=0,padx=5,pady=5,columnspan=3)
    info_label=ttk.Label(info,text=paragraph,justify="center")
    info_label.grid(column=0,row=1,padx=5,pady=5,columnspan=3)
    wish_label=ttk.Label(info,text=contact_info,justify="center")
    wish_label.grid(column=0,row=2,padx=5,pady=5,columnspan=3)
    
#creation of window
win=tk.Tk()
win.title("Truss analysis")
win.resizable(False,False)
win.iconbitmap("roof.ico")

#display of information function
information()

#lists to store joint attributes
node_entries = []  
nodes=[]

#creates the input entries of the nodes   
def create_node_entries(event=None):    
    node_entries.clear()
    nodes.clear()
    
    children = input_frame.winfo_children()
    for widget in children[7:]:  
        widget.destroy()
    
    node_num=eval(node_num_entry.get())
    
    if node_num < 1:
        return
       
    for i in range(node_num):
        node_name=ttk.Label(input_frame,text=i+1)
        node_name.grid(row=i+4,column=0,padx=5,pady=5)
        node_x_cord=ttk.Entry(input_frame,width=15,justify="center")
        node_x_cord.grid(row=i+4,column=1,padx=5,pady=5)
        node_y_cord=ttk.Entry(input_frame,width=15,justify="center")
        node_y_cord.grid(row=i+4,column=2,padx=5,pady=5)
    
        node_entries.append((node_x_cord, node_y_cord))
        
    add_node = ttk.Button(input_frame, text="Add nodes", width=15,command=create_node_instances)
    add_node.grid(row=node_num+4,column=0,padx=5,pady=5,sticky="")
    clear_node=ttk.Button(input_frame,text="Clear nodes",width=15,command=clear_node_instances)
    clear_node.grid(row=node_num+4,column=2,padx=5,pady=5,sticky="")
     
#creates the instances of the joints 
def create_node_instances():
    nodes.clear()
    for i, (x_entry, y_entry) in enumerate(node_entries):
            if x_entry.get()=="" or y_entry.get()=="":
                messagebox.showerror("Input Error","Missing coordinate for node {}. Please fill all fields.".format(i+1)) 
                return
            
            else:
                x = eval(x_entry.get())
                y = eval(y_entry.get())
                new_node=joint(str(i+1),x,y)
                nodes.append(new_node)
    
    messagebox.showinfo("Success","Nodes added successfully")

    return nodes


#clears or removes all instances of previously entered joints
def clear_node_instances():
    node_num=eval(node_num_entry.get())
    
    nodes.clear()
    node_entries.clear()
        
    if node_num < 1:
        return
       
    for i in range(node_num):
        node_name=ttk.Label(input_frame,text=i+1)
        node_name.grid(row=i+4,column=0,padx=5,pady=5)
        node_x_cord=ttk.Entry(input_frame,width=15,justify="center")
        node_x_cord.grid(row=i+4,column=1,padx=5,pady=5)
        node_y_cord=ttk.Entry(input_frame,width=15,justify="center")
        node_y_cord.grid(row=i+4,column=2,padx=5,pady=5)
    
        node_entries.append((node_x_cord, node_y_cord))
         
    messagebox.showinfo("Cleared", "All node entries have been cleared")

    
#creating a frame for the node attribute inputs
def add_nodes_window():
    global node_num_entry
    for widget in input_frame.winfo_children():
        widget.destroy()
        
    title=ttk.Label(input_frame,text="Truss nodes")
    title.grid(column=0,row=0,padx=5,pady=5,columnspan=3)
    explanation=ttk.Label(input_frame,text="Enter the number of truss nodes (N)\n\
and their x and y coordinates in the\nfields provided below.\n\nPress the Enter key after entering N.")
    explanation.grid(column=0,row=1,padx=5,pady=5,columnspan=3)
    node_num=ttk.Label(input_frame,text="N (1 < N < 27): ")
    node_num.grid(column=0,row=2,padx=5,pady=5,columnspan=1)
    node_num_entry=ttk.Entry(input_frame,width=10,justify="center")
    node_num_entry.grid(column=1,row=2,padx=5,pady=5,columnspan=2)
    
    node_name=ttk.Label(input_frame,text="Node #")
    node_name.grid(column=0,row=3,padx=5,pady=5,sticky="")
    node_x_cord=ttk.Label(input_frame,text="x")
    node_x_cord.grid(column=1,row=3,sticky="",padx=5,pady=5)
    node_y_cord=ttk.Label(input_frame,text="y")
    node_y_cord.grid(column=2,row=3,sticky="",padx=5,pady=5)
    
    node_num_entry.bind("<Return>",create_node_entries)

#lists to store member attributes
member_entries = []  
members= []

#creates the input entries of the members   
def create_member_entries(event=None):    
    member_entries.clear()
    members.clear()
    
    children = input_frame.winfo_children()
    for widget in children[7:]:  
        widget.destroy()
    
    member_num=eval(member_num_entry.get())
    
    if member_num < 1:
        return
    
    for i in range(member_num):
        member_name=ttk.Label(input_frame,text=i+1)
        member_name.grid(row=i+4,column=0,padx=5,pady=5)
        beginning_joint=ttk.Entry(input_frame,width=15,justify="center")
        beginning_joint.grid(row=i+4,column=1,padx=5,pady=5)
        ending_joint=ttk.Entry(input_frame,width=15,justify="center")
        ending_joint.grid(row=i+4,column=2,padx=5,pady=5)
    
        member_entries.append((beginning_joint,ending_joint))
    
    add_member = ttk.Button(input_frame, text="Add members", width=15,command=create_member_instances)
    add_member.grid(row=member_num+5,column=0,padx=5,pady=5,sticky="")
    clear_member=ttk.Button(input_frame,text="Clear members",width=15,command=clear_member_instances)
    clear_member.grid(row=member_num+5,column=2,padx=5,pady=5,sticky="")
    
#creates the instances of the members 
def create_member_instances():
    members.clear()
    for i, (b_joint,e_joint) in enumerate(member_entries):
            if b_joint.get()=="" or e_joint.get()=="":
                messagebox.showerror("Input Error","Missing node for member {}. Please fill all fields.".format(i+1)) 
                return
            
            else:
                beginning_joint = nodes[eval(b_joint.get())-1]
                ending_joint = nodes[eval(e_joint.get())-1]
                new_member=member(str(i+1),beginning_joint,ending_joint)
                members.append(new_member)
    
    messagebox.showinfo("Success","Members added successfully")

    return members


#clears or removes all instances of previously entered members
def clear_member_instances():
    member_num=eval(member_num_entry.get())
    
    members.clear()
    member_entries.clear()
    
    if member_num < 1:
        return
    
    for i in range(member_num):
        member_name=ttk.Label(input_frame,text=i+1)
        member_name.grid(row=i+4,column=0,padx=5,pady=5)
        beginning_joint=ttk.Entry(input_frame,width=15,justify="center")
        beginning_joint.grid(row=i+4,column=1,padx=5,pady=5)
        ending_joint=ttk.Entry(input_frame,width=15,justify="center")
        ending_joint.grid(row=i+4,column=2,padx=5,pady=5)
        
        member_entries.append((beginning_joint,ending_joint))
    
    messagebox.showinfo("Cleared","All member entries have been cleared")

    
#creating a frame for the member attribute inputs
def add_members_window():
    global member_num_entry    
    for widget in input_frame.winfo_children():
        widget.destroy()
        
    title=ttk.Label(input_frame,text="Truss members")
    title.grid(column=0,row=0,padx=5,pady=5,columnspan=3)
    explanation=ttk.Label(input_frame,text="Enter the number of truss members (M)\n\
and position of each member in terms of its\nend nodes in the fields provided below.\
\n\nPress the Enter key after entering M.")
    explanation.grid(column=0,row=1,padx=5,pady=5,columnspan=3)
    member_num=ttk.Label(input_frame,text="M (0 < M < 47): ")
    member_num.grid(column=0,row=2,padx=5,pady=5,columnspan=1)
    member_num_entry=ttk.Entry(input_frame,width=10,justify="center")
    member_num_entry.grid(column=1,row=2,padx=5,pady=5,columnspan=2)
    
    member_name=ttk.Label(input_frame,text="Member #")
    member_name.grid(column=0,row=3,padx=5,pady=5,sticky="")
    beginning_joint=ttk.Label(input_frame,text="Node 1")
    beginning_joint.grid(column=1,row=3,sticky="",padx=5,pady=5)
    ending_joint=ttk.Label(input_frame,text="Node 2")
    ending_joint.grid(column=2,row=3,sticky="",padx=5,pady=5)
    
    member_num_entry.bind("<Return>",create_member_entries)
    
#lists to store support attributes
support_entries = []  
supports= []
support_reactions=[]

#creates the input entries of the supports   
def create_support_entries(event=None):    
    support_entries.clear()
    supports.clear()
    support_reactions.clear()
    
    children = input_frame.winfo_children()
    for widget in children[7:]:  
        widget.destroy()
    
    support_num=eval(support_num_entry.get())
    
    if support_num < 1:
        return
    
    for i in range(support_num):
        node_number=ttk.Entry(input_frame,width=10,justify="center")
        node_number.grid(row=i+4,column=0,padx=5,pady=5)
        
        #dropdown for support types
        support_types=["pin","horizontal roller","vertical roller"]
        support_type=ttk.Combobox(input_frame,values=support_types,state="readonly",width=15)#gives dropdown menu of items
        support_type.grid(row=i+4,column=1,padx=5,pady=5)
        support_type.current(0) #default to "pin"
    
        support_entries.append((node_number,support_type))
    
    add_support = ttk.Button(input_frame, text="Add supports", width=15,command=create_support_instances)
    add_support.grid(row=support_num+5,column=0,padx=5,pady=5,sticky="")
    clear_support=ttk.Button(input_frame,text="Clear supports",width=15,command=clear_support_instances)
    clear_support.grid(row=support_num+5,column=1,padx=5,pady=5,sticky="")

#creates the instances of the supports 
def create_support_instances():
    supports.clear()
    support_reactions.clear()
    for i, (node_num,support_type) in enumerate(support_entries):
            if node_num.get()=="":
                messagebox.showerror("Input Error","Missing node # for support {}. Please fill all fields.".format(i+1)) 
                return
            
            elif support_type.get()=="pin":
                node= nodes[eval(node_num.get())-1]
                x_reaction=0
                y_reaction=0
                support_reactions.append(x_reaction)
                support_reactions.append(y_reaction)
                new_support=hinge(node)
                supports.append(new_support)
            
            elif support_type.get()=="horizontal roller":
                node= nodes[eval(node_num.get())-1]
                y_reaction=0
                support_reactions.append(y_reaction)
                new_support=horizontalRoller(node)
                supports.append(new_support)
                
            elif support_type.get()=="vertical roller":
                node= nodes[eval(node_num.get())-1]
                x_reaction=0
                support_reactions.append(x_reaction)
                new_support=verticalRoller(node)
                supports.append(new_support)
                
    messagebox.showinfo("Success","Supports added successfully")

    return supports

#clears or removes all instances of previously entered supports
def clear_support_instances():
    support_num=eval(support_num_entry.get())
    
    supports.clear()
    support_entries.clear()
    support_reactions.clear()
    
    if support_num < 1:
        return
    
    for i in range(support_num):
        node_number=ttk.Entry(input_frame,width=10,justify="center")
        node_number.grid(row=i+4,column=0,padx=5,pady=5)
        
        #dropdown for support types
        support_types=["pin","horizontal roller","vertical roller"]
        support_type=ttk.Combobox(input_frame,values=support_types,state="readonly",width=15)
        support_type.grid(row=i+4,column=1,padx=5,pady=5)
        support_type.current(0) #default to "pin"
    
        support_entries.append((node_number,support_type))
    
    messagebox.showinfo("Cleared","All support entries have been cleared")

#creating a frame for the support attributes
def add_supports_window():
    global support_num_entry
    for widget in input_frame.winfo_children():
        widget.destroy()
        
    title=ttk.Label(input_frame,text="Truss supports")
    title.grid(column=0,row=0,padx=5,pady=5,columnspan=3)
    explanation=ttk.Label(input_frame,text="Three types of supports can be defined:\n\
pin, horizontal roller, and vertical roller.\nUse the fields provided below to specify\n\
the number of supports (S), and their\nlocations and types.\n\nPress the Enter key after entering S.")
    explanation.grid(column=0,row=1,padx=5,pady=5,columnspan=2)
    support_num=ttk.Label(input_frame,text="S (1 < N < 27): ")
    support_num.grid(column=0,row=2,padx=5,pady=5)
    support_num_entry=ttk.Entry(input_frame,width=10,justify="center")
    support_num_entry.grid(column=1,row=2,padx=5,pady=5)
    
    node_num=ttk.Label(input_frame,text="Node #")
    node_num.grid(column=0,row=3,padx=5,pady=5,sticky="")
    
    support_type=ttk.Label(input_frame,text="Type")
    support_type.grid(column=1,row=3,sticky="",padx=5,pady=5)
    
    support_num_entry.bind("<Return>",create_support_entries)
    
#lists to store load attributes
load_entries = []  
loads= []

#creates the input entries of the loads   
def create_load_entries(event=None):    
    load_entries.clear()
    loads.clear()
    
    children = input_frame.winfo_children()
    for widget in children[8:]:  
        widget.destroy()
    
    load_num=eval(load_num_entry.get())
    
    if load_num < 1:
        return
    
    for i in range(load_num):
        node_num=ttk.Entry(input_frame,width=15,justify="center")
        node_num.grid(row=i+4,column=0,padx=5,pady=5)
        magnitude=ttk.Entry(input_frame,width=15,justify="center")
        magnitude.grid(row=i+4,column=1,padx=5,pady=5)
        angle=ttk.Entry(input_frame,width=15,justify="center")
        angle.grid(row=i+4,column=2,padx=5,pady=5)
    
        load_entries.append((node_num,magnitude,angle))
    
    add_load = ttk.Button(input_frame, text="Add loads", width=15,command=create_load_instances)
    add_load.grid(row=load_num+5,column=0,padx=5,pady=5,sticky="")
    clear_load=ttk.Button(input_frame,text="Clear loads",width=15,command=clear_load_instances)
    clear_load.grid(row=load_num+5,column=2,padx=5,pady=5,sticky="")

#creates the instances of the loads 
def create_load_instances():
    loads.clear()
    for i, (node_num,magnitude,angle) in enumerate(load_entries):
            if node_num.get()=="" or magnitude.get()=="" or angle.get()=="":
                messagebox.showerror("Input Error","Missing component for load {}. Please fill all fields.".format(i+1)) 
                return
            
            else:
                node = nodes[eval(node_num.get())-1]
                magnitude=eval(magnitude.get())
                angle=eval(angle.get())
                new_load=force(node,magnitude,angle)
                loads.append(new_load)
    
    messagebox.showinfo("Success","Loads added successfully")

    return loads

#clears or removes all instances of previously entered loads
def clear_load_instances():
    load_num=eval(load_num_entry.get())
    
    loads.clear()
    load_entries.clear()
    
    if load_num < 1:
        return
    
    for i in range(load_num):
        node_num=ttk.Entry(input_frame,width=15,justify="center")
        node_num.grid(row=i+4,column=0,padx=5,pady=5)
        magnitude=ttk.Entry(input_frame,width=15,justify="center")
        magnitude.grid(row=i+4,column=1,padx=5,pady=5)
        angle=ttk.Entry(input_frame,width=15,justify="center")
        angle.grid(row=i+4,column=2,padx=5,pady=5)
    
        load_entries.append((node_num,magnitude,angle))
    
    messagebox.showinfo("Cleared","All load entries have been cleared")

#tip for inputting load attributes
def load_hints():
    load_hint=tk.Toplevel(win)
    load_hint.title("")
    load_hint.geometry("350x350")
    load_hint.resizable(False,False)
    load_hint.attributes('-topmost', True)
    load_hint.iconbitmap("roof.ico")
    canvas=tk.Canvas(load_hint,width=350,height=350)
    canvas.grid(column=0,row=0,sticky="nsew")
    
    #drawing the load formats
    canvas.create_line(30,50,30,100,arrow=tk.LAST, width=2, fill="red")
    canvas.create_text(30,110,text="-P")
    canvas.create_line(80,100,80,50,arrow=tk.LAST, width=2, fill="red")
    canvas.create_text(80,40,text="+P")
    canvas.create_line(30,150,80,150,arrow=tk.LAST, width=2, fill="red")
    canvas.create_text(90,150,text="+P")
    canvas.create_line(80,190,30,190,arrow=tk.LAST, width=2, fill="red")
    canvas.create_text(20,190,text="-P")
    
    #drawing the angle representation
    canvas.create_oval(150,30,310,190,width=1.8)
    canvas.create_line(140,110,320,110,width=1.4, fill="black")
    canvas.create_line(230,20,230,200, width=1.4, fill="black")
    canvas.create_text(330,110,text="0°")
    canvas.create_text(230,10,text="90°")
    canvas.create_text(125,110,text="180°")
    canvas.create_text(230,210,text="270°")
    
    #example
    canvas.create_text(175,260,text="Example")
    canvas.create_line(225,290,125,290,arrow=tk.LAST, width=2, fill="red")
    canvas.create_text(100,290,text="5kN")
    canvas.create_text(175,320,text="Magnitude= -5 and Angle= 0°")
    
    
#creating a frame for the load attribute inputs
def add_loads_window():
    global load_num_entry
    for widget in input_frame.winfo_children():
        widget.destroy()
        
    title=ttk.Label(input_frame,text="Truss loads")
    title.grid(column=0,row=0,padx=5,pady=5,columnspan=3)
    explanation=ttk.Label(input_frame,text="Enter the number of nodal loads (L), and\n\
the position, magnitude, and direction of\neach load in the fields provided below.\
\n\nPress the Enter key after entering L.")
    explanation.grid(column=0,row=1,padx=5,pady=5,columnspan=3)
    load_num=ttk.Label(input_frame,text="L (L < 27): ")
    load_num.grid(column=0,row=2,padx=5,pady=5)
    load_num_entry=ttk.Entry(input_frame,width=10,justify="center")
    load_num_entry.grid(column=1,row=2,padx=5,pady=5)
    load_hint=ttk.Button(input_frame,text="Hint",command=load_hints)
    load_hint.grid(column=2,row=2,padx=5,pady=5)
    
    node_num=ttk.Label(input_frame,text="Node #")
    node_num.grid(column=0,row=3,padx=5,pady=5,sticky="")
    magnitude=ttk.Label(input_frame,text="Magnitude")
    magnitude.grid(column=1,row=3,sticky="",padx=5,pady=5)
    angle=ttk.Label(input_frame,text="Angle (°)")
    angle.grid(column=2,row=3,sticky="",padx=5,pady=5)
    
    load_num_entry.bind("<Return>",create_load_entries)

unknown_values=[]
#finding the unknowns of the truss
def truss_solver():
    if len(loads)==0 or len(supports)==0 or len(nodes)==0 or len(members)==0:
        messagebox.showerror("Cannot solve","Missing some data. Please fill all fields.") 
        return
    
    else:
        #creating the index of the excel file
        row_index=[]

        for i in range(len(nodes)):
            j=nodes[i]
            row_index.append("Σ{}x".format(j.name))
            row_index.append("Σ{}y".format(j.name))

        #creating the default row data
        Truss_rows=[]

        for i in range(2*len(nodes)):
            Truss_rows.append(0)

        #Creating the Excel file
        Truss_Solver=pd.DataFrame(index=row_index)

        #Creation of the columns of the Excel file
        for i in range(len(support_reactions)):
            for j in supports:
                if isinstance(j,hinge):
                    Truss_Solver["{}x".format(j.joint.name)]=Truss_rows
                    Truss_Solver["{}y".format(j.joint.name)]=Truss_rows
          
                elif isinstance(j,horizontalRoller):
                    Truss_Solver["{}y".format(j.joint.name)]=Truss_rows
                
                elif isinstance(j,verticalRoller):
                    Truss_Solver["{}x".format(j.joint.name)]=Truss_rows

        for i in range(len(members)):
            for j in members:
                    Truss_Solver["F{}".format(j.name)]=Truss_rows

        Truss_Solver[" "]=np.nan

        for i in range(len(loads)):#edited
            j=loads[i]
            Truss_Solver["P{}({})".format(j.joint.name,i+1)]=Truss_rows

        #converting the rows under the various columns to eval
        column_names=Truss_Solver.columns.tolist()

        for i in range(len(column_names)):#this prevents warnings of data type
            Truss_Solver[column_names[i]]=Truss_Solver[column_names[i]].astype(float)

        #removed creation of excel file due to dataframe already created            

        #adding the coefficients of the support reactions to the excel file
        for i in range(len(support_reactions)):
            for j in supports:
                if isinstance(j,hinge):
                    Truss_Solver.loc["Σ{}x".format(j.joint.name),"{}x".format(j.joint.name)]=1
                    Truss_Solver.loc["Σ{}y".format(j.joint.name),"{}y".format(j.joint.name)]=1
                
                elif isinstance(j,horizontalRoller):
                    Truss_Solver.loc["Σ{}y".format(j.joint.name),"{}y".format(j.joint.name)]=1
                    
                elif isinstance(j,verticalRoller):
                    Truss_Solver.loc["Σ{}x".format(j.joint.name),"{}x".format(j.joint.name)]=1

        #adding the coefficients of the forces to the excel file
        for i in range(len(loads)):
            j=loads[i]
            Truss_Solver.loc["Σ{}x".format(j.joint.name),"P{}({})".format(j.joint.name,i+1)]=-(j.horizontal_component())
            Truss_Solver.loc["Σ{}y".format(j.joint.name),"P{}({})".format(j.joint.name,i+1)]=-(j.vertical_component())


        #adding the coefficients of the members to the excel file
        for i in range(len(members)):
            for j in members:
                if j.vertical_component()!=0 and j.horizontal_component()!=0:
                    Truss_Solver.loc["Σ{}x".format(j.joint1.name),"F{}".format(j.name)]=(j.horizontal_component()/j.hypotenuse())
                    Truss_Solver.loc["Σ{}y".format(j.joint1.name),"F{}".format(j.name)]=(j.vertical_component()/j.hypotenuse())
                    Truss_Solver.loc["Σ{}x".format(j.joint2.name),"F{}".format(j.name)]=-(j.horizontal_component()/j.hypotenuse())
                    Truss_Solver.loc["Σ{}y".format(j.joint2.name),"F{}".format(j.name)]=-(j.vertical_component()/j.hypotenuse())
                
                elif j.horizontal_component()==0.0:
                    Truss_Solver.loc["Σ{}y".format(j.joint1.name),"F{}".format(j.name)]=1
                    Truss_Solver.loc["Σ{}y".format(j.joint2.name),"F{}".format(j.name)]=-1
                
                elif j.vertical_component()==0.0:
                    Truss_Solver.loc["Σ{}x".format(j.joint1.name),"F{}".format(j.name)]=1
                    Truss_Solver.loc["Σ{}x".format(j.joint2.name),"F{}".format(j.name)]=-1

        #creating the coefficient matrix A
        A_column=len(members)+len(support_reactions)

        Matrix_A=Truss_Solver.iloc[0:len(row_index),0:A_column]

        Matrix_A=np.array(Matrix_A)

        #the inverse of the coefficient matrix A
        try:
            Inverse_A=np.linalg.inv(Matrix_A)

        except np.linalg.LinAlgError: #if the matrix is not a square matrix
            messagebox.showerror("Error", "System is not solvable. Check your truss configuration.")
            return
        
        #Preventing small float pointing errors
        Inverse_A=np.round(Inverse_A,decimals=10)

        #obtaining the matrices of the forces and summing them
        B_matrices=0
        for i in range(len(loads)):
            Matrix_B=Truss_Solver.iloc[0:len(row_index),A_column+1+i]
            B_matrices=B_matrices+np.array(Matrix_B)

        #Preventing small float pointing errors
        B_matrices=np.round(B_matrices,decimals=10)

        #Evaluation of the values of the unknowns
        Unknown_values=np.matmul(Inverse_A,B_matrices)
    
        for i in Unknown_values:
            unknown_values.append(i)      
        
        #creation of table with unknown values
        data=[]
        
        column_names=Truss_Solver.columns.tolist()
        
        for widget in solution_frame.winfo_children():
            widget.destroy()
            
        title=ttk.Label(solution_frame,text="Member Forces and Support Reactions")
        title.grid(column=0,row=0,padx=5,pady=5,columnspan=3)
        explanation=ttk.Label(solution_frame,text="Truss member forces and support reactions are given in the table below")
        explanation.grid(column=0,row=1,padx=5,pady=5,columnspan=3)
        
        #removes the table's border
        style = ttk.Style()
        style.configure("Custom.Treeview", highlightthickness=0, bd=0)
        
        #creates the column headings of the table
        columns=("Unknowns","Force (kN)","Type")
        unknown_values_tree=ttk.Treeview(solution_frame,columns=columns,show="headings",style="Custom.Treeview")
        
        unknown_values_tree.column("Unknowns", width=80, anchor="center")#adjusts the columns size and alignment
        unknown_values_tree.column("Force (kN)", width=80, anchor="center")
        unknown_values_tree.column("Type", width=100, anchor="center")
        
        #loop to create the rows of the table
        for j in range(len(support_reactions)):
            name=column_names[j]
            force=round(unknown_values[j],2)
            
            data.append((name,force,"reaction"))
        
        m=j    
        for l in members: 
            force=round(unknown_values[m+1],2)
            if force<0:
                data.append(("F{}-{}".format(l.joint1.name,l.joint2.name),force,"compression"))
                
            elif force>0:
                data.append(("F{}-{}".format(l.joint1.name,l.joint2.name),force,"tension"))
            
            else:
                data.append(("F{}-{}".format(l.joint1.name,l.joint2.name),force,"zero"))
            
            m+=1
    
        #loop to create the headers
        for col in columns:
            unknown_values_tree.heading(col, text=col)

        #loop to fill the rows of the table
        for row in data:
            unknown_values_tree.insert("",tk.END,values=row)
        
        unknown_values_tree.config(height=len(data)) #prevents scrolling of treeview and displays every row
        unknown_values_tree.grid(column=0,row=2,padx=5,pady=5,sticky="we",columnspan=3)
        
        #plotting the truss model
        fig, ax = plt.subplots(figsize=(6,4),dpi=75)
        ax.set_aspect('equal')#ensures 1 unit on both axes is equal
        ax.axis("off")
        ax.grid(False)#removes gridboxes
        
        #drawing joints
        for n in nodes:
            x=n.x
            y=n.y
            name=n.name
            circle=plt.Circle((x,y),0.1, 
                              fc="green",ec="black",zorder=2)#zorder is the order in which it is plotted
            ax.add_patch(circle)
            ax.text(x,y-0.5,name,ha='center',va='center',fontsize=12,fontweight="bold")#labels node number
        
        #drawing members
        for m in members:
            x0=m.joint1.x
            y0=m.joint1.y
            x1=m.joint2.x
            y1=m.joint2.y
            ax.plot([x0, x1],[y0, y1],'k-',lw=2)#lw=lineweight
        
        #drawing loads    
        for l in loads:
            x=l.joint.x
            y=l.joint.y
            m=l.magnitude
            fx=l.horizontal_component()
            fy=l.vertical_component()
            if round(fy,)==0:#empty argument means no decimal place
                ax.arrow(x, y, 0.5, 0, head_width=0.125, head_length=0.125, fc='red', ec='red', linewidth=2) 
                ax.text(x+0.7, y, "{} kN".format(m), fontsize=12, color='red')

            elif round(fx,)==0:
                ax.arrow(x, y, 0, 0.5, head_width=0.125, head_length=0.125, fc='red', ec='red', linewidth=2) 
                ax.text(x, y+0.7, "{} kN".format(m), fontsize=12, color='red')
           
            else:
                ax.arrow(x, y, 0.5, 0.5, head_width=0.125, head_length=0.125, fc='red', ec='red', linewidth=2) 
                ax.text(x+0.7, y+0.7, "{} kN".format(m), fontsize=12, color='red')
            
        #drawing reactions
        i=0
        for j in supports:
            x=j.joint.x
            y=j.joint.y
        
            if isinstance(j,hinge):
                rx=unknown_values[i]
                ry=unknown_values[i+1]
                
                ax.arrow(x,y, 0.5, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue')  # horizontal
                ax.text(x + 0.6, y, "{0:0.2f} kN".format(rx), fontsize=12, color='blue')
        
                ax.arrow(x, y, 0, 0.5, head_width=0.1, head_length=0.1, fc='blue', ec='blue')  # vertical
                ax.text(x, y + 0.7, "{0:0.2f} kN".format(ry), fontsize=12, color='blue')
                
                i+= 2
        
            elif isinstance(j, horizontalRoller):
                ry=unknown_values[i]
                ax.arrow(x, y, 0, 0.5, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
                ax.text(x, y + 0.7, "{0:0.2f} kN".format(ry), fontsize=12, color='blue')
                i+= 1
        
            elif isinstance(j, verticalRoller):
                rx=unknown_values[i]
                ax.arrow(x, y, 0.5, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
                ax.text(x + 0.6, y, "{0:0.2f} kN".format(rx), fontsize=12, color='blue')
                i+= 1


        #placing the plot in the GUI
        canvas=FigureCanvasTkAgg(fig,master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(column=0,row=0,padx=5,pady=5,sticky="n")
            
#command to clear already obtained solution values and plots
def clear_solution():
    for widget in solution_frame.winfo_children():
        widget.destroy()
        
    for widget in plot_frame.winfo_children():
        widget.destroy()
        
    unknown_values.clear()
    
#creation of button frame
button_frame=ttk.LabelFrame(win,text="Truss components")
button_frame.grid(column=0,row=0,padx=5,pady=5,sticky="n")

#creating canvas for input frame
input_canvas=tk.Canvas(win,highlightthickness=0)
input_canvas.grid(column=1,row=0,padx=5,pady=5,sticky="nsew")

#creating scrollbar for input frame
input_scrollbar=ttk.Scrollbar(win,orient="vertical",command=input_canvas.yview)
input_scrollbar.grid(column=2,row=0,sticky="ns")

#combining scrollbar with canvas
input_canvas.configure(yscrollcommand=input_scrollbar.set)
input_canvas.bind("<Configure>",lambda e:input_canvas.configure(scrollregion=input_canvas.bbox("all")))

#function to update input canvas scroll region
def update_scroll_region(event=None):
    input_canvas.configure(scrollregion=input_canvas.bbox("all"))

#creation of input frame
input_frame=ttk.LabelFrame(input_canvas,text="Input parameters")
input_canvas.create_window((0,0),window=input_frame,anchor="nw")
input_frame.bind("<Configure>",update_scroll_region) #updates scroll region

#creation of solution frame
solution_frame=ttk.LabelFrame(win,text="Solution")
solution_frame.grid(column=3,row=0,padx=5,pady=5,sticky="n")

#creation of plot frame
plot_frame=ttk.LabelFrame(win,text="Truss Free Body Diagram")
plot_frame.grid(column=3,row=1,padx=5,pady=5,sticky="n")

#creation of buttons in button frame
node=ttk.Button(button_frame,text="Nodes",width=15,command=add_nodes_window)
node.grid(column=0,row=0,padx=5,pady=5,sticky="")

member_button=ttk.Button(button_frame,text="Members",width=15,command=add_members_window)
member_button.grid(column=0,row=1,padx=5,pady=5,sticky="")

support=ttk.Button(button_frame,text="Supports",width=15,command=add_supports_window)
support.grid(column=0,row=2,padx=5,pady=5,sticky="")

load=ttk.Button(button_frame,text="Loads",width=15,command=add_loads_window)
load.grid(column=0,row=3,padx=5,pady=5,sticky="")

solve=ttk.Button(button_frame,text="Solve and plot",width=15,command=truss_solver)
solve.grid(column=0,row=4,padx=5,pady=5,sticky="")

clear_solution=ttk.Button(button_frame,text="Clear solution",width=15,command=clear_solution)
clear_solution.grid(column=0,row=5,padx=5,pady=5,sticky="")

#allows the GUI to run as a loop
win.mainloop()
 
