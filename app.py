#Import biblioteca
from flask import Flask, render_template, request

#Criar objeto flask "apelido - app"
app = Flask(__name__)


base_fake = []


#Rotas
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pessoa')
def pessoa():
    return render_template('pessoa.html')


@app.route('/criar/atividade', methods=['GET', 'POST'])
def criar_atividade():
    if request.method == 'POST':
        nome_atividade = request.form.get('nome_atividade')
        data_atividade = request.form.get('data_atividade')
        recurso_atividade = request.form.getlist('recurso_atividade')
        categoria_atividade = request.form.get('form_categoria_atividade')
        desc_atividade = request.form.get('form_descricao_atividade')

        dados = {
            'nome_atividade': nome_atividade,
            'data_atividade': data_atividade,
            'recurso_atividade': recurso_atividade,
            'categoria_atividade': categoria_atividade,
            'desc_atividade': desc_atividade
        }
        print(f'dados cadastrado: {dados}')
        base_fake.append(dados)
        print(f'base_fake: {base_fake}')
        return render_template('criar_atividade.html',dados_atividade=base_fake)

    return render_template('criar_atividade.html')


@app.route('/listar/atividades')
def listar_atividades():
    return render_template('listar_atividades.html')


#iniciar aplicação web

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

#Nada deve ser colocado abaixo
