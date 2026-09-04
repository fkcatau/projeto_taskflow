from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Banco de dados fictício armazenado na memória do servidor
ATIVIDADES_BANCO = [
    {
        "titulo": "Atualizar Documentação da API",
        "descricao": "Atualizar os endpoints principais.",
        "prioridade": "Alta",
        "recursos": ["Computador", "Internet"]
    },
    {
        "titulo": "Treinamento da Equipe em Flask",
        "descricao": "Apresentar rotas e Jinja2 para o time.",
        "prioridade": "Média",
        "recursos": ["Computador", "Internet"]
    }
]


@app.route('/')
def index():
    # Rota de recepção: exibe a página inicial do painel do colaborador
    return render_template('index.html')


@app.route('/atividades/criar', methods=['GET', 'POST'])
def criar_atividade():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        prioridade = request.form.get('prioridade')
        recursos_selecionados = request.form.getlist('recursos')

        nova_atividade = {
            "titulo": titulo,
            "descricao": descricao,
            "prioridade": prioridade,
            "recursos": recursos_selecionados if recursos_selecionados else ["Nenhum"]
        }

        ATIVIDADES_BANCO.append(nova_atividade)
        return redirect(url_for('listar_atividades'))

    return render_template('criar_atividade.html')


@app.route('/atividades/listar')
def listar_atividades():
    return render_template('listar_atividades.html', atividades=ATIVIDADES_BANCO)


@app.route('/atividades/remover/<int:id_atividade>', methods=['POST'])
def remover_atividade(id_atividade):
    # Remove a atividade correspondente ao índice numérico enviado pelo formulário HTML
    if 0 <= id_atividade < len(ATIVIDADES_BANCO):
        ATIVIDADES_BANCO.pop(id_atividade)

    return redirect(url_for('listar_atividades'))


@app.route('/pessoa')
def pessoa():
    # Perfil atualizado e expandido com credenciais detalhadas
    usuario_mock = {
        "nome": "Miguel",
        "matricula": "TF-8941",
        "cargo": "Técnico Agrícola",
        "departamento": "Operações de Campo",
        "especializacao": "Agriculture de Precisão e Monitoramento de Safra",
        "registro_professional": "CFTA SP-08472-26",
        "unidade": "Fazenda Modelo - Setor Norte"
    }
    return render_template('pessoa.html', usuario=usuario_mock)


if __name__ == '__main__':
    # Executa o servidor local em modo de depuração para desenvolvimento
    app.run(debug=True)
