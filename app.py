from flask import Flask, flash, render_template
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'secret!'

#login
@app.route('/login')
def login():
 return render_template('login.html')

#socketio login
@socketio.on('login')
def socketio_login(login_senha):
    senha = login_senha['senha']
    login = login_senha['login']
    try:
        with open(f'{login}.txt', 'r') as arquivo:
            senha_teste = arquivo.read()
    except:
        socketio.emit('erro', 'erro')
    else:
        if senha == senha_teste:
            socketio.emit('cookie_', 'cookie')
            socketio.emit('login_aprovado', 'login aprovado')
        else:
            socketio.emit('erro', 'erro')

#cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

#socketio Cadastro
@socketio.on('cadastro')
def socketio_cadastro(login_senha):
    senha = login_senha['_senha_']
    login = login_senha['_login_']
    try:
        with open(f'{login}.txt', 'r') as arquivo:
            teste = arquivo.read()
    except:
        with open(f'{login}.txt', 'w') as arquivo:
            arquivo.write(senha)
        socketio.emit('login_aprovado_', 'login aprovado')
        socketio.emit('cookie_', 'cookie')
    else:
        socketio.emit('cadastro_erro', 'erro')

#banco
@app.route('/banco')
def banco():
    return render_template('banco.html')

#redirecionar 
@app.route('/')
def redirecionar():
    return """
    <script>
        let url = document.location
        window.location.href = url+'login';
    </script>
    """

@socketio.on('conectado')
def conectado(msssg):
    print(msssg)

if __name__ == "__main__":    
    socketio.run(app, debug=True)