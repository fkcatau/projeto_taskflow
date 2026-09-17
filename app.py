from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

PESSOAS_BANCO = [
    {"id": 1, "nome": "Miguel", "senha": "123", "email": "miguel@taskflow.com", "data_nascimento": "1995-05-10"},
    {"id": 2, "nome": "Amanda Silva", "senha": "456", "email": "amanda@taskflow.com", "data_nascimento": "1992-08-22"}
]

TIPOS_BANCO = [
    {"id": 1, "nome": "Desenvolvimento", "desc": "Programação e software"},
    {"id": 2, "nome": "Infraestrutura", "desc": "Manutenção de redes"},
    {"id": 3, "nome": "Design", "desc": "Modelagem visual e interfaces"}
]

RECURSOS_BANCO = [
    {"id": 1, "nome": "Computador", "descricao": "Notebook corporativo"},
    {"id": 2, "nome": "Celular", "descricao": "Smartphone da empresa"},
    {"id": 3, "nome": "Internet", "descricao": "Conexão VPN dedicada"}
]

ATIVIDADES_BANCO = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pessoas')
def gerenciar_pessoas():
    return render_template('pessoa.html', pessoas=PESSOAS_BANCO)

@app.route('/pessoas/cadastrar', methods=['GET', 'POST'])
def cadastrar_pessoa():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        email = request.form.get('email')
        data_nascimento = request.form.get('data_nascimento')

        nova_pessoa = {
            "id": len(PESSOAS_BANCO) + 1,
            "nome": nome,
            "senha": senha,
            "email": email,
            "data_nascimento": data_nascimento
        }
        PESSOAS_BANCO.append(nova_pessoa)
        return redirect(url_for('gerenciar_pessoas'))
    return render_template('cadastrar_pessoa.html')

@app.route('/pessoas/remover/<int:id_pessoa>', methods=['POST'])
def remover_pessoa(id_pessoa):
    global PESSOAS_BANCO
    PESSOAS_BANCO = [p for p in PESSOAS_BANCO if p['id'] != id_pessoa]
    return redirect(url_for('gerenciar_pessoas'))

@app.route('/atividades')
def gerenciar_atividades():
    return render_template('criar_atividade.html', atividades=ATIVIDADES_BANCO)

@app.route('/atividades/cadastrar', methods=['GET', 'POST'])
def cadastrar_atividade():
    if request.method == 'POST':
        nome = request.form.get('nome')
        hora = request.form.get('hora')
        data = request.form.get('data')
        colaborador_nome = request.form.get('colaborador_nome').strip()
        tipo_id = int(request.form.get('tipo_id'))
        recursos_selecionados = request.form.getlist('recursos')

        pessoa_existe = any(p['nome'].lower() == colaborador_nome.lower() for p in PESSOAS_BANCO)
        if not pessoa_existe and colaborador_nome:
            PESSOAS_BANCO.append({
                "id": len(PESSOAS_BANCO) + 1,
                "nome": colaborador_nome,
                "senha": "mudar_no_primeiro_acesso",
                "email": f"{colaborador_nome.lower().replace(' ', '')}@taskflow.com",
                "data_nascimento": "2000-01-01"
            })

        tipo_tarefa = next((t['nome'] for t in TIPOS_BANCO if t['id'] == tipo_id), "Geral")

        nova_tarefa = {
            "id": len(ATIVIDADES_BANCO) + 1,
            "nome": nome,
            "hora": hora,
            "data": data,
            "responsavel": colaborador_nome,
            "tipo": tipo_tarefa,
            "recurso": ", ".join(recursos_selecionados) if recursos_selecionados else "Nenhum"
        }
        ATIVIDADES_BANCO.append(nova_tarefa)
        return redirect(url_for('gerenciar_atividades'))
    return render_template('cadastrar_atividade.html', pessoas=PESSOAS_BANCO, tipos=TIPOS_BANCO, recursos_lista=RECURSOS_BANCO)

@app.route('/atividades/remover/<int:id_atividade>', methods=['POST'])
def remover_atividade(id_atividade):
    global ATIVIDADES_BANCO
    ATIVIDADES_BANCO = [a for a in ATIVIDADES_BANCO if a['id'] != id_atividade]
    return redirect(url_for('gerenciar_atividades'))

@app.route('/tipos')
def gerenciar_tipos():
    return render_template('tipo.html', tipos=TIPOS_BANCO)

@app.route('/tipos/cadastrar', methods=['GET', 'POST'])
def cadastrar_tipo():
    if request.method == 'POST':
        nome = request.form.get('nome')
        desc = request.form.get('desc')

        novo_tipo = {
            "id": len(TIPOS_BANCO) + 1,
            "nome": nome,
            "desc": desc
        }
        TIPOS_BANCO.append(novo_tipo)
        return redirect(url_for('gerenciar_tipos'))
    return render_template('cadastrar_tipo.html')

@app.route('/tipos/remover/<int:id_tipo>', methods=['POST'])
def remover_tipo(id_tipo):
    global TIPOS_BANCO
    TIPOS_BANCO = [t for t in TIPOS_BANCO if t['id'] != id_tipo]
    return redirect(url_for('gerenciar_tipos'))

@app.route('/recursos')
def gerenciar_recursos():
    return render_template('recursos.html', recursos=RECURSOS_BANCO)

@app.route('/recursos/cadastrar', methods=['GET', 'POST'])
def cadastrar_recurso():
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')

        novo_recurso = {
            "id": len(RECURSOS_BANCO) + 1,
            "nome": nome,
            "descricao": descricao
        }
        RECURSOS_BANCO.append(novo_recurso)
        return redirect(url_for('gerenciar_recursos'))
    return render_template('cadastrar_recurso.html')

@app.route('/recursos/remover/<int:id_recurso>', methods=['POST'])
def remover_recurso(id_recurso):
    global RECURSOS_BANCO
    RECURSOS_BANCO = [r for r in RECURSOS_BANCO if r['id'] != id_recurso]
    return redirect(url_for('gerenciar_recursos'))

if __name__ == '__main__':
    app.run(debug=True)
