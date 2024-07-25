from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('contas.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS contas')
    c.execute('''
        CREATE TABLE contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mes TEXT NOT NULL,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            data_vencimento TEXT NOT NULL,
            parcelas INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def format_date(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return date.strftime('%d/%m/%Y')
    except ValueError:
        return date_str

@app.route('/', methods=['GET', 'POST'])
def index():
    mes_selecionado = request.args.get('mes', 'Janeiro')
    conn = sqlite3.connect('contas.db')
    c = conn.cursor()
    c.execute('SELECT * FROM contas WHERE mes = ?', (mes_selecionado,))
    contas = c.fetchall()
    conn.close()

    # Formatar as datas
    contas = [(id, mes, descricao, valor, format_date(data_vencimento), parcelas) for (id, mes, descricao, valor, data_vencimento, parcelas) in contas]

    return render_template('index.html', contas=contas, mes_selecionado=mes_selecionado)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    try:
        mes = request.form['mes']
        descricao = request.form['descricao']
        valor = float(request.form['valor'])
        data_vencimento = request.form['data_vencimento']
        parcelas = int(request.form['parcelas'])

        conn = sqlite3.connect('contas.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO contas (mes, descricao, valor, data_vencimento, parcelas)
            VALUES (?, ?, ?, ?, ?)
        ''', (mes, descricao, valor, data_vencimento, parcelas))
        conn.commit()
        conn.close()

        return redirect('/?mes=' + mes)
    except KeyError as e:
        # Se algum campo estiver faltando, retornará um erro
        return f"Erro: Campo faltando - {e}", 400
    except ValueError as e:
        # Se houver um problema com a conversão dos valores, retornará um erro
        return f"Erro: Valor inválido - {e}", 400

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        try:
            descricao = request.form['descricao']
            valor = float(request.form['valor'])
            data_vencimento = request.form['data_vencimento']
            parcelas = int(request.form['parcelas'])

            conn = sqlite3.connect('contas.db')
            c = conn.cursor()
            c.execute('''
                UPDATE contas
                SET descricao = ?, valor = ?, data_vencimento = ?, parcelas = ?
                WHERE id = ?
            ''', (descricao, valor, data_vencimento, parcelas, id))
            conn.commit()
            conn.close()

            mes = request.form['mes']
            return redirect('/?mes=' + mes)
        except KeyError as e:
            return f"Erro: Campo faltando - {e}", 400
        except ValueError as e:
            return f"Erro: Valor inválido - {e}", 400

    # GET request
    conn = sqlite3.connect('contas.db')
    c = conn.cursor()
    c.execute('SELECT * FROM contas WHERE id = ?', (id,))
    conta = c.fetchone()
    conn.close()

    return render_template('editar.html', conta=conta)

@app.route('/excluir/<int:id>')
def excluir(id):
    conn = sqlite3.connect('contas.db')
    c = conn.cursor()
    c.execute('DELETE FROM contas WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    mes = request.args.get('mes', 'Janeiro')
    return redirect('/?mes=' + mes)

if __name__ == '__main__':
    app.run(debug=True)
