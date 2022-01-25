from tkinter import *
from tkinter import messagebox, filedialog
import sqlite3
import os



root = Tk()
path = str(os.getcwd())+r"\bbdd.db"

#Funciones
def deshabilitar_campos():
    entry_duracion.config(state="disabled")
    entry_genero.config(state="disabled")
    entry_nombre.config(state="disabled")
    var_duracion.set("")
    var_nombre.set("")
    var_genero.set("")

def deshabilitar_botones(btn_nuevo=False):
    if btn_nuevo:
        button_nuevo.config(state="disabled")
        button_editar.config(state="disabled")
        button_eliminar.config(state="disabled")
    button_cancelar.config(state="disabled")
    button_guardar.config(state="disabled")


def habilitar_campos():
    entry_duracion.config(state="normal")
    entry_genero.config(state="normal")
    entry_nombre.config(state="normal")

def habilitar_botones(parameter):
    if parameter == 0:
        button_nuevo.config(state="normal")
        button_editar.config(state="normal")
        button_eliminar.config(state="normal")
    elif parameter ==1:
        button_cancelar.config(state="normal")
        button_guardar.config(state="normal")

def habilitar_nuevo():
    habilitar_campos()
    habilitar_botones(1)

def cancelar():
    deshabilitar_campos()
    deshabilitar_botones()

def run_query(path,query,parameters=()):
    with sqlite3.connect(path) as bd:
        cursor = bd.cursor()
        cursor.execute(query,parameters)        
        bd.commit() #guarda la consulta/accion realizada (si corresponde) en la base de datos
        resultado = cursor.fetchall()
    return resultado

def guardar_registro():
    datos = [var_nombre.get(),var_duracion.get(),var_genero.get()]
    respuesta = True
    if "" in datos:
        respuesta = messagebox.askyesno(message="Uno de los campos está vacío, ¿desea guardar los datos igualmente?")
    if respuesta:
        try:
            query = "INSERT INTO DATOS VALUES(NULL,?,?,?)"
            run_query(path,query,datos)
            actualizar_datos()
            deshabilitar_campos()
            deshabilitar_botones()
            messagebox.showinfo("Ok",f"""\
            El registro:
            
            NOMBRE = {datos[0]}
            DURACION = {datos[1]}
            GENERO = {datos[2]}
            
            se ha guardado correctamente.""")
            
        except Exception as e:
            messagebox.showerror("Error",str(e))
       

def conectar_bbdd():
    try:
        conexion=sqlite3.connect(path)    
        cursor=conexion.cursor()
        query = "SELECT * FROM DATOS"
        run_query(path,query)
        messagebox.showinfo("Conexion","Se ha conectado a la base de datos correctamente")
        
        habilitar_botones(0)
    except Exception as e:
        messagebox.showerror("Error","Se ha producido el siguiente error en la conexion a la base de datos: \n\n" + str(e).upper())
        respuesta = messagebox.askyesno(title="Conexion",message="¿Desea crear una nueva tabla?")
        if respuesta:
            try:
                query="CREATE TABLE DATOS('ID' INTEGER PRIMARY KEY AUTOINCREMENT,'NAME' VARCHAR(70),'DURACION' VARCHAR(5),'GENERO' VARCHAR(40))"
                run_query(path,query)
                messagebox.showinfo("Conexion","Base de datos creada correctamente")
                habilitar_botones(0)
            except Exception as e:
                messagebox.showerror("Error","Se ha producido el siguiente error en la creacion de la base de datos: \n\n" + str(e).upper())
    conexion.close()
    actualizar_datos()

def editar_registro():
    pass
#     if tree.selection() == "":
#         messagebox.showwarning(title="Selection",message="No se ha seleccionado ninguna fila.")
#     else:
#         habilitar_nuevo()
#         
#             
#         datos = [var_nombre.get(),var_duracion.get(),var_genero.get()]
#         respuesta = True
#         if "" in datos:
#             respuesta = messagebox.askyesno(message="Uno de los campos está vacío, ¿desea actualizar los datos igualmente?")
#         if respuesta:
#             try:
#                 query = f"UPDATE DATOS set NAME = ?, DURACION = ?, GENERO = ? WHERE NAME = {datos[0]}, DURACION = {datos[1]} AND GENERO = {datos[2]}"
#                 run_query(path,query,datos)
#                 actualizar_datos()
#                 deshabilitar_campos()
#                 
#             except Exception as e:
#                 messagebox.showerror("Error",str(e))  
    
def borrar_tabla():
    query = "DROP TABLE DATOS"
    try:
        run_query(path,query)
        messagebox.showinfo("Borrar","Se ha borrado la base de datos correctamente")
        borrar_datos()
        deshabilitar_campos()
        deshabilitar_botones(True)
    except Exception as e:
        messagebox.showerror("Error",e)

def borrar_datos():
    records = tree.get_children()
    for record in records:
        tree.delete(record)

def actualizar_datos():
    try:
        query = "SELECT * FROM DATOS ORDER BY ID DESC "
        db_rows = run_query(path,query)
        records = tree.get_children()
    
        for record in records:
            tree.delete(record)
         
        for row in db_rows:
            tree.insert("",0,text=row[0],values=[row[1],row[2],row[3]])
        
    except:
        pass
    
#MENU

menu = Menu(root)
inicio_menu = Menu(menu,tearoff=0)

inicio_menu.add_command(label="Conectar con DB",command=conectar_bbdd)
inicio_menu.add_command(label="Eliminar registro en DB",command=borrar_tabla)
inicio_menu.add_command(label="Salir",command = lambda: root.destroy())
menu.add_cascade(label="Inicio",menu=inicio_menu)

menu.add_cascade(label="Consultas")

menu.add_cascade(label="Configuracion")

menu.add_cascade(label="Ayuda")

#FRAMES
frm_entries = Frame(root,height=250,width=800)
frm_entries.grid(row=0,column=0,rowspan=4,columnspan=3,pady=0)

frm_treeview = Frame(root,height=200,width=800)
frm_treeview.grid(row=4,column=0,columnspan=4)

frm_buttons = Frame(root,height=75,width=800)
frm_buttons.grid(row=5,column=0,columnspan=3)

#LABELS
Label(root,text="Nombre: ",font=("arial",10,"bold")).grid(row=0,column=0)
Label(root,text="Duracion: ",font=("arial",10,"bold")).grid(row=1,column=0)
Label(root,text="Género: ",font=("arial",10,"bold")).grid(row=2,column=0)

#ENTRIES
var_nombre = StringVar()
var_duracion = StringVar()
var_genero = StringVar()
entry_nombre = Entry(root,width=75,textvariable=var_nombre)
entry_nombre.grid(row=0,column=1,columnspan=2,sticky=W)
entry_duracion = Entry(root,width=75,textvariable=var_duracion)
entry_duracion.grid(row=1,column=1,columnspan=2,sticky=W)
entry_genero = Entry(root,width=75,textvariable=var_genero)
entry_genero.grid(row=2,column=1,columnspan=2,sticky=W)

#BUTTONS
button_nuevo = Button(root,text="Nuevo",font=("arial",10,"bold"),fg="white",bg="green",width=20,command=habilitar_nuevo)
button_nuevo.grid(row=3,column=0)
button_guardar = Button(root,text="Guardar",font=("arial",10,"bold"),fg="white",bg="blue",width=20,command=guardar_registro)
button_guardar.grid(row=3,column=1)
button_cancelar = Button(root,text="Cancelar",font=("arial",10,"bold"),fg="white",bg="red",width=20,command=cancelar)
button_cancelar.grid(row=3,column=2)

#TREEVIEW
tree = ttk.Treeview(root,height=10,column=("NOMBRE","DURACION","GENERO"))
tree.grid(row=4,column=0,columnspan=4)
tree.heading("#0",text="ID",anchor=CENTER)
tree.heading("#1",text="NOMBRE",anchor=CENTER)
tree.heading("#2",text="DURACION",anchor=CENTER)
tree.heading("#3",text="GENERO",anchor=CENTER)



#BUTTONS
button_editar = Button(root,text="Editar",font=("arial",10,"bold"),fg="white",bg="green",width=20,command=editar_registro)
button_editar.grid(row=5,column=0,sticky=N,pady=10)
button_eliminar = Button(root,text="Eliminar",font=("arial",10,"bold"),fg="white",bg="blue",width=20)
button_eliminar.grid(row=5,column=1,sticky=N,pady=10)  

deshabilitar_campos()
deshabilitar_botones(True)

root.geometry("800x525+100+100")
root.resizable(False,False)
root.config(menu=menu)
root.mainloop()
