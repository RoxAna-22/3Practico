from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'

# Seminarios disponibles
seminarios_disponibles = ['Inteligencia Artificial', 'Machine Learning', 'Simulación con Arena', 'Robótica Educativa']

@app.route("/")
def index():
    if 'registros' not in session:
        session['registros'] = []
    registros = session.get('registros', [])
    return render_template('index.html', registros = registros)


#Para el contador  de id
def generar_id():
    if 'registros' in session and len(session['registros']) > 0:
        return max(item['id'] for item in session['registros']) +1
    else:
        return 1



@app.route("/nuevo", methods =['GET','POST'])
def nuevo():
    if request.method == 'POST':
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        turno = request.form['turno']
        seminarios_seleccionados = request.form.getlist('seminarios')


        nuevo_registro = {
            'id':generar_id(), 
            'fecha':fecha, 
            'nombre':nombre, 
            'apellido':apellido,
            'turno':turno,
            'seminarios':seminarios_seleccionados
        }
        if 'registros' not in session:
            session['registros'] =[]

        session['registros'].append(nuevo_registro)
        session.modified = True
        return redirect(url_for('index'))
    return render_template('nuevo.html', seminarios = seminarios_disponibles)




#EDITAR
@app.route('/editar/<int:id>', methods =['GET', 'POST'])
def editar(id):
    lista_registros = session.get('registros', [])
    registro = next((c for c in lista_registros  if c['id'] == id), None)

    if not registro:
        return redirect(url_for('index'))

    if request.method == 'POST':
        registro['fecha'] = request.form['fecha']
        registro['nombre'] = request.form['nombre']
        registro['apellido'] = request.form['apellido']
        registro['turno'] = request.form['turno']
        registro['seminarios'] = request.form.getlist('seminarios')
        session.modified = True
        return redirect(url_for('index'))
    return render_template('editar.html', registro = registro, seminarios=seminarios_disponibles)



#ELIMINAR
@app.route('/eliminar/<int:id>', methods =['POST'])
def eliminar(id):

    lista_registros = session.get('registros', []) #en caso de que no haya una lista vacia 
    registro = next((c for c in lista_registros  if c['id'] == id), None) #iteramos esta lista,  si id == id
    if registro:
        session['registros'].remove(registro)
        session.modified = True
    return redirect(url_for('index'))
    

if __name__ == "__main__":
    app.run(debug = True)
