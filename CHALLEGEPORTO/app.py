import requests
import json
import oracledb
from flask import Flask, jsonify, render_template, request
from flask import Flask
 
db = oracledb.connect(user='rm552539', password='130701', dsn='oracle.fiap.com.br/orcl')
 
cursor = db.cursor()

assegurados=[]
 
app = Flask(__name__)
 
@app.route('/')
def index():
    return "Bem-vindo ao Guincho Seguro!"
 
@app.route('/veiculos', methods=['GET'])
def get_veiculos():
    try:
        cursor = db.cursor()
 
        query = "SELECT * FROM T_GUISR_VEICULO"
        cursor.execute(query)
 
        result = cursor.fetchall()
 
        veiculos = []
        for row in result:
            veiculo = {
                'ID_VEICULO': row[0],
                'ID_SEGURADO': row[1],
                'ST_MODIFICACAO': row[2],
                'DS_MODIFICACAO': row[3],
                'NR_PESO': float(row[4]),
                'DT_CADASTRO': row[5].strftime('%Y-%m-%d %H:%M:%S'),
                'NM_USUARIO': row[6]
            }
            veiculos.append(veiculo)
 
        cursor.close()
 
        return jsonify({'veiculos': veiculos})
 
    except Exception as e:
        return jsonify({'error': str(e)})
 
@app.route('/veiculos/<int:id>', methods=['GET'])
def get_veiculo_by_id(id):
    try:
        cursor = db.cursor()
 
        query = "SELECT * FROM T_GUISR_VEICULO WHERE ID_VEICULO = :id"
        cursor.execute(query, id=id)
 
        result = cursor.fetchall()
 
        if not result:
            return jsonify({'message': 'Veículo não encontrado'}), 404
 
        veiculo = {
            'ID_VEICULO': result[0][0],
            'ID_SEGURADO': result[0][1],
            'ST_MODIFICACAO': result[0][2],
            'DS_MODIFICACAO': result[0][3],
            'NR_PESO': float(result[0][4]),
            'DT_CADASTRO': result[0][5].strftime('%Y-%m-%d %H:%M:%S'),
            'NM_USUARIO': result[0][6]
        }
 
        cursor.close()
 
        return jsonify({'veiculo': veiculo})
 
    except Exception as e:
        return jsonify({'error': str(e)})
   
@app.route('/veiculos/status/<string:status>', methods=['GET'])
def get_veiculos_by_status(status):
    try:
        if status.upper() not in ('A', 'I'):
            return jsonify({'message': 'Status inválido. Use "A" ou "I".'}), 400
 
        cursor = db.cursor()
 
        query = "SELECT * FROM T_GUISR_VEICULO WHERE ST_MODIFICACAO = :status"
        cursor.execute(query, status=status.upper())
 
        result = cursor.fetchall()
 
        if not result:
            return jsonify({'message': f'Nenhum veículo encontrado com status "{status}"'}), 404
 
        veiculos = []
        for row in result:
            veiculo = {
                'ID_VEICULO': row[0],
                'ID_SEGURADO': row[1],
                'ST_MODIFICACAO': row[2],
                'DS_MODIFICACAO': row[3],
                'NR_PESO': float(row[4]),
                'DT_CADASTRO': row[5].strftime('%Y-%m-%d %H:%M:%S'),
                'NM_USUARIO': row[6]
            }
            veiculos.append(veiculo)
 
        cursor.close()
 
        return jsonify({'veiculos': veiculos})
 
    except Exception as e:
        return jsonify({'error': str(e)})
 
@app.route('/veiculos', methods=['POST'])
def create_veiculo():
    try:
        data = request.json
 
        required_fields = ['ID_SEGURADO', 'ST_MODIFICACAO', 'DS_MODIFICACAO', 'NR_PESO', 'NM_USUARIO']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'O campo {field} é obrigatório'}), 400
 
        query = "INSERT INTO T_GUISR_VEICULO (ID_SEGURADO, ST_MODIFICACAO, DS_MODIFICACAO, NR_PESO, DT_CADASTRO, NM_USUARIO) VALUES (:id_segurado, :st_modificacao, :ds_modificacao, :nr_peso, SYSDATE, :nm_usuario) RETURNING ID_VEICULO INTO :new_id"
        cursor = db.cursor()
        new_id = cursor.var(oracledb.NUMBER)
        cursor.execute(query, id_segurado=data['ID_SEGURADO'], st_modificacao=data['ST_MODIFICACAO'], ds_modificacao=data['DS_MODIFICACAO'], nr_peso=data['NR_PESO'], nm_usuario=data['NM_USUARIO'], new_id=new_id)
        db.commit()
        cursor.close()
 
        return jsonify({'ID_VEICULO': new_id.getvalue()}), 201
 
    except Exception as e:
        return jsonify({'error': str(e)})
 
@app.route('/veiculos/<int:id>', methods=['PUT'])
def update_veiculo(id):
    try:
        data = request.json
 
        if 'ID_SEGURADO' not in data and 'ST_MODIFICACAO' not in data and 'DS_MODIFICACAO' not in data and 'NR_PESO' not in data and 'NM_USUARIO' not in data:
            return jsonify({'error': 'Pelo menos um campo para atualização deve ser fornecido'}), 400
 
        query = "UPDATE T_GUISR_VEICULO SET "
        for key, value in data.items():
            query += f"{key} = :{key}, "
        query = query.rstrip(', ')  
        query += f" WHERE ID_VEICULO = :id"
 
        cursor = db.cursor()
        data['id'] = id
        cursor.execute(query, data)
        db.commit()
        cursor.close()
 
        return jsonify({'message': f'Veículo com ID {id} atualizado com sucesso'}), 200
 
    except Exception as e:
        return jsonify({'error': str(e)})
 
 
@app.route('/veiculos/<int:id>', methods=['DELETE'])
def delete_veiculo(id):
    try:
        query = "DELETE FROM T_GUISR_VEICULO WHERE ID_VEICULO = :id"
        cursor = db.cursor()
        cursor.execute(query, id=id)
        db.commit()
        cursor.close()
 
        return jsonify({'message': f'Veículo com ID {id} excluído com sucesso'}), 200
 
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/funcionarios', methods=['GET'])
def get_funcionarios():
    try:
        cursor = db.cursor()

        query = "SELECT * FROM T_GUISR_FUNCIONARIO"
        cursor.execute(query)

        result = cursor.fetchall()

        funcionarios = []
        for row in result:
            funcionario = {
                'ID_FUNCIONARIO': row[0],
                'NM_FUNCIONARIO': row[1],
                'DS_CARGO': row[2],
                'DT_NASCIMENTO': row[3].strftime('%Y-%m-%d'),
                'NR_SALARIO': float(row[4]),
                'DT_CADASTRO': row[5].strftime('%Y-%m-%d %H:%M:%S'),
                'NM_USUARIO': row[6]
            }
            funcionarios.append(funcionario)

        cursor.close()

        return jsonify({'funcionarios': funcionarios})

    except Exception as e:
        return jsonify({'error': str(e)})
         
if __name__ == '__main__':
    app.run()
 
