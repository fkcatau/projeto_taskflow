from flask import Flask, render_template, request, redirect, url_for
from models import SessionLocal, init_db, Pessoa, Tipo, Recurso, Atividade
from datetime import datetime

app = Flask(__name__)

init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pessoas')
def gerenciar_pessoas():
    db = SessionLocal()
    pessoas = db.query(Pessoa).all()
    db.close()
    return render_template('pessoa.html', pessoas=pessoas)


@app.route('/pessoas/cadastrar', methods=['GET', 'POST'])
def cadastrar_pessoa():
    if request.method == 'POST':
        db = SessionLocal()
        data_nasc = datetime.strptime(request.form.get('data_nascimento'), '%Y-%m-%d').date()

        nova_pessoa = Pessoa(
            nome=request.form.get('nome'),
            email=request.form.get('email'),
            senha=request.form.get('senha'),
            data_nascimento=data_nasc
        )
        db.add(nova_pessoa)
        db.commit()
        db.close()
        return redirect(url_for('gerenciar_pessoas'))
    return render_template('cadastrar_pessoa.html')


@app.route('/pessoas/remover/<int:id_pessoa>', methods=['POST'])
def remover_pessoa(id_pessoa):
    db = SessionLocal()
    pessoa = db.query(Pessoa).filter(Pessoa.id == id_pessoa).first()
    if pessoa:
        db.delete(pessoa)
        db.commit()
    db.close()
    return redirect(url_for('gerenciar_pessoas'))


@app.route('/tipos')
def gerenciar_tipos():
    db = SessionLocal()
    tipos = db.query(Tipo).all()
    db.close()
    return render_template('tipo.html', tipos=tipos)


@app.route('/tipos/cadastrar', methods=['GET', 'POST'])
def cadastrar_tipo():
    if request.method == 'POST':
        db = SessionLocal()
        novo_tipo = Tipo(
            nome=request.form.get('nome'),
            desc=request.form.get('desc')
        )
        db.add(novo_tipo)
        db.commit()
        db.close()
        return redirect(url_for('gerenciar_tipos'))
    return render_template('cadastrar_tipo.html')


@app.route('/tipos/remover/<int:id_tipo>', methods=['POST'])
def remover_tipo(id_tipo):
    db = SessionLocal()
    tipo = db.query(Tipo).filter(Tipo.id == id_tipo).first()
    if tipo:
        db.delete(tipo)
        db.commit()
    db.close()
    return redirect(url_for('gerenciar_tipos'))


@app.route('/recursos')
def gerenciar_recursos():
    db = SessionLocal()
    recursos = db.query(Recurso).all()
    db.close()
    return render_template('recursos.html', recursos=recursos)


@app.route('/recursos/cadastrar', methods=['GET', 'POST'])
def cadastrar_recurso():
    if request.method == 'POST':
        db = SessionLocal()
        novo_recurso = Recurso(
            nome=request.form.get('nome'),
            descricao=request.form.get('descricao')
        )
        db.add(novo_recurso)
        db.commit()
        db.close()
        return redirect(url_for('gerenciar_recursos'))
    return render_template('cadastrar_recurso.html')


@app.route('/recursos/remover/<int:id_recurso>', methods=['POST'])
def remover_recurso(id_recurso):
    db = SessionLocal()
    recurso = db.query(Recurso).filter(Recurso.id == id_recurso).first()
    if recurso:
        db.delete(recurso)
        db.commit()
    db.close()
    return redirect(url_for('gerenciar_recursos'))


@app.route('/atividades')
def gerenciar_atividades():
    db = SessionLocal()
    atividades_db = db.query(Atividade).all()

    atividades = []
    for at in atividades_db:
        atividades.append({
            "id": at.id,
            "nome": at.nome,
            "responsavel": at.responsavel.nome,
            "tipo": at.tipo.nome,
            "data": at.data.strftime('%d/%m/%Y'),
            "hora": at.hora.strftime('%H:%M'),
            "recurso": ", ".join([r.nome for r in at.recursos]) if at.recursos else "Nenhum"
        })
    db.close()
    return render_template('criar_atividade.html', atividades=atividades)


@app.route('/atividades/cadastrar', methods=['GET', 'POST'])
def cadastrar_atividade():
    db = SessionLocal()
    if request.method == 'POST':
        colaborador_nome = request.form.get('colaborador_nome').strip()
        tipo_id = int(request.form.get('tipo_id'))
        recursos_nomes = request.form.getlist('recursos')

        pessoa = db.query(Pessoa).filter(Pessoa.nome.like(colaborador_nome)).first()
        if not pessoa and colaborador_nome:
            pessoa = Pessoa(
                nome=colaborador_nome,
                senha="mudar_no_primeiro_acesso",
                email=f"{colaborador_nome.lower().replace(' ', '')}@taskflow.com",
                data_nascimento=datetime.strptime("2000-01-01", "%Y-%m-%d").date()
            )
            db.add(pessoa)
            db.flush()

        recursos_selecionados = db.query(Recurso).filter(Recurso.nome.in_(recursos_nomes)).all()

        nova_tarefa = Atividade(
            nome=request.form.get('nome'),
            data=datetime.strptime(request.form.get('data'), '%Y-%m-%d').date(),
            hora=datetime.strptime(request.form.get('hora'), '%H:%M').time(),
            pessoa_id=pessoa.id,
            tipo_id=tipo_id,
            recursos=recursos_selecionados
        )

        db.add(nova_tarefa)
        db.commit()
        db.close()
        return redirect(url_for('gerenciar_atividades'))

    pessoas = db.query(Pessoa).all()
    tipos = db.query(Tipo).all()
    recursos_lista = db.query(Recurso).all()
    db.close()
    return render_template('cadastrar_atividade.html', pessoas=pessoas, tipos=tipos, recursos_lista=recursos_lista)


@app.route('/atividades/remover/<int:id_atividade>', methods=['POST'])
def remover_atividade(id_atividade):
    db = SessionLocal()
    atividade = db.query(Atividade).filter(Atividade.id == id_atividade).first()
    if atividade:
        db.delete(atividade)
        db.commit()
    db.close()
    return redirect(url_for('gerenciar_atividades'))


if __name__ == '__main__':
    app.run(debug=True)
