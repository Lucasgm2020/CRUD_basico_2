from tkinter import *
import sqlite3
import os
from tkinter import messagebox

path = str(os.getcwd()) + r"\bbdd.db" 
root = Tk()
caso_guardar = "nuevo"

#2) Funciones de habilitación de botones

def deshabilitar(caso=""):
    if caso == "todo":
        button_editar.config(state="disabled")
        button_nuevo.config(state="disabled")
        button_eliminar.config(state="disabled")
    button_guardar.config(state="disabled")
    button_cancelar.config(state="disabled")
    entry_nombre.config(state="disabled")
    entry_duración.config(state="disabled")
    entry_genero.config(state="disabled")   
    var_nombre.set("")
    var_duracion.set("")
    var_genero.set("")
    
    
def habilitar_botones(caso):
    if caso == "BBDD":
        button_editar.config(state="normal")
        button_nuevo.config(state="normal")
        button_eliminar.config(state="normal")
    elif caso == "nuevo" or "editar":
        button_cancelar.config(state="normal")
        button_guardar.config(state="normal")
        entry_nombre.config(state="normal")
        entry_duración.config(state="normal")
        entry_genero.config(state="normal")  

def run_query(query,parameters=()):
    with sqlite3.connect(path) as bd:
        cursor = bd.cursor()
        cursor.execute(query,parameters)
        bd.commit()#guarda la consulta/accion realizada (si corresponde) en la base de datos
        results = cursor.fetchall() #retorna lo seleccionado si corresponde.
    return results

def conectar_BBDD():
    try:
        query = "SELECT * FROM DATOS"
        run_query(query)
        mensaje(titulo="Conexion",msj="Se ha conectado con la base de datos correctamente")
        mostrar_registros()
        habilitar_botones("BBDD")
    except Exception as error:
        mensaje(titulo="Error",error=str(error))
        result = messagebox.askyesno("Crear BBDD","¿Desea crear una nueva tabla en la BBDD?")
        if result:
            try:
                query = "CREATE TABLE DATOS ('ID' INTEGER PRIMARY KEY AUTOINCREMENT,'NOMBRE' TEXT VARCHAR(50),'DURACIÓN' REAL,'GÉNERO' TEXT VARCHAR(50))"
                run_query(query)
                mensaje(titulo="Conexion",msj="Se ha creado correctamente la base de datos.")
                mostrar_registros()
                habilitar_botones("BBDD")
            except Exception as error:   
                mensaje(titulo="Error",error=str(error))


def mostrar_registros():
    query = "SELECT * FROM DATOS ORDER BY ID DESC"
    resultados = run_query(query)
    
    borrar_registros()
    
    for resultado in resultados:
        tree.insert("",0,text=resultado[0],values=[resultado[1],resultado[2],resultado[3]])
        

def borrar_registros():
    registros = tree.get_children()

    for registro in registros:
        tree.delete(registro)   

def nuevo_registro():
    habilitar_botones("nuevo")
    global caso_guardar
    caso_guardar = "nuevo"
    
def guardar_registro(caso=caso_guardar):
    try:
        if caso_guardar == "nuevo":
            query = "INSERT INTO DATOS VALUES (NULL,?,?,?)"
            values = [var_nombre.get(),var_duracion.get(),var_genero.get()]
            run_query(query,values)
            borrar_registros()
            mostrar_registros()          
            mensaje(titulo="Ok",msj="Se ha agregado el registro correctamente.")
            
        elif caso_guardar == "editar":
            values = [var_nombre.get(),var_duracion.get(),var_genero.get()]
            query = f"UPDATE DATOS set NOMBRE=?,DURACIÓN=?,GÉNERO=? WHERE NOMBRE='{str(var_nombre.get())}'" 
            run_query(query,values)
            borrar_registros()
            mostrar_registros()
            mensaje(titulo="Ok",msj="Se ha editado correctamente el registro.")
            
    except Exception as error: 
        mensaje(titulo="Error",error="Error")
    deshabilitar()
    
def cancelar():
    deshabilitar()

def editar():
    try:

        data = selectedItem() 
        nombre,duracion,genero = data[0],data[1],data[2]
        values = [nombre,duracion,genero]
        var_nombre.set(nombre)
        var_duracion.set(duracion)
        var_genero.set(genero)
        global caso_guardar
        caso_guardar = "editar"
        habilitar_botones("editar")
    except Exception as error:
        print(str(error))
        if str(error)=="string index out of range":
            error = "No se ha seleccionado un registro."
        mensaje(titulo="Error",error=str(error))
        deshabilitar()
        
def selectedItem():
    try:
        curItem = tree.focus()
        return(tree.item(curItem)["values"])
    except Exception as error:
        mensaje(titulo="Error",error=str(error))
        
def mensaje(titulo,error="",msj="Se ha producido el siguiente error: \n\n"):
    if len(str(error))==0:
        messagebox.showinfo(titulo,msj)
    else:
        messagebox.showerror(titulo,msj + error.upper())
        
def eliminar_registro():
    try:
        data = selectedItem()
        query = f"DELETE FROM DATOS WHERE NOMBRE='{data[0]}'"
        run_query(query)
        mensaje(titulo="Ok",msj=f"El siguiente registro se ha borrado correctamente:\n\nNombre={data[0]}\nDuración={data[1]}\nGenero={data[2]}")
        deshabilitar()
        borrar_registros()
        mostrar_registros()
    except Exception as error:
        if str(error)=="string index out of range":
            error = "No se ha seleccionado un registro."
        mensaje(titulo="Error",error=str(error))    
        deshabilitar()
 
def borrar_BBDD():
    query = "DROP TABLE DATOS"
    try:
        run_query(query)
        mensaje(titulo="Borrar",msj="Se ha borrado correctamente la BBDD")
        borrar_registros()
        deshabilitar("todo")
    except Exception as error:
        mensaje(titulo="Error",error=str(error))
        
#1) Apariencia de la aplicación

#Frames

Frame(root,width=800,height=250).grid(row=0,column=0,rowspan=4,columnspan=3)
Frame(root,width=800,height=200).grid(row=4,column=0,rowspan=1,columnspan=4)
Frame(root,width=800,height=75).grid(row=5,column=0,rowspan=1,columnspan=3)

#Labels
Label(root,text="Nombre",font=("arial",10,"bold"),fg="black").grid(row=0,column=0)
Label(root,text="Duración",font=("arial",10,"bold"),fg="black").grid(row=1,column=0)
Label(root,text="Genero",font=("arial",10,"bold"),fg="black").grid(row=2,column=0)

#Botones
button_nuevo = Button(root,text="Nuevo",font=("arial",10,"bold"),fg="white",bg="green",width=20,command=nuevo_registro)
button_nuevo.grid(row=3,column=0)
button_guardar = Button(root,text="Guardar",font=("arial",10,"bold"),fg="white",bg="blue",width=20,command=guardar_registro)
button_guardar.grid(row=3,column=1)
button_cancelar = Button(root,text="Cancelar",font=("arial",10,"bold"),fg="white",bg="red",width=20,command=cancelar)
button_cancelar.grid(row=3,column=2)

#Entries
var_nombre = StringVar()
var_duracion = StringVar()
var_genero = StringVar()
entry_nombre = Entry(root,textvariable=var_nombre,width=75)
entry_nombre.grid(row=0,column=1,columnspan=2)
entry_duración = Entry(root,textvariable=var_duracion,width=75)
entry_duración.grid(row=1,column=1,columnspan=2)
entry_genero = Entry(root,textvariable=var_genero,width=75)
entry_genero.grid(row=2,column=1,columnspan=2)


#Menu
menu = Menu(root)

inicio_menu = Menu(menu,tearoff=0)
inicio_menu.add_command(label="Conectar con BBDD",command=conectar_BBDD)
inicio_menu.add_command(label="Eliminar BBDD",command=borrar_BBDD)
inicio_menu.add_command(label="Salir",command=root.destroy)
menu.add_cascade(label="Inicio",menu=inicio_menu)
menu.add_cascade(label="Consultas",menu=inicio_menu)
menu.add_cascade(label="Configuracion",menu=inicio_menu)
menu.add_cascade(label="Ayuda",menu=inicio_menu)

#Treeview
tree = ttk.Treeview(root,height=10,column=("NOMBRE","DURACIÓN","GENERO"))
tree.grid(row=4,column=0,columnspan=4)
tree.heading("#0",text="ID")
tree.heading("#1",text="NOMBRE")
tree.heading("#2",text="DURACIÓN")
tree.heading("#3",text="GÉNERO")

#Botones de abajo

button_editar = Button(root,text="Editar",font=("arial",10,"bold"),fg="white",bg="green",width=20,command=editar)
button_editar.grid(row=5,column=0,pady=10,sticky=N)
button_eliminar = Button(root,text="Eliminar",font=("arial",10,"bold"),fg="white",bg="red",width=20,command=eliminar_registro)
button_eliminar.grid(row=5,column=1,pady=10,sticky=N)

#---------Estado inicial---------#
deshabilitar("todo")


"""
Tamaño de la aplicación:

Width (total) = 800
Height (total) = 525
Distancia del (0,0), desde arriba a la izquierda = 100 + 100

"""

root.resizable(0,0)
root.config(menu=menu)
root.geometry("800x525+100+100")
root.mainloop()
