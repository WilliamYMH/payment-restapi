import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# settings db
DB_URI = os.environ.get('DATABASE_URL')
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.DECIMAL(15, 2))
    credit_card = db.Column(db.String(16))
    username = db.Column(db.String(50))
    correo = db.Column(db.String(40))
    tienda = db.Column(db.String(15))


@app.route('/payment-service', methods=['POST'])
def payment():

    try:
        monto = request.form.get('monto')
        credit_card = request.form.get('credit_card')
        username = request.form.get('username')
        correo = request.form.get('correo')
        tienda = request.form.get('tienda')

        payment = Payment(monto=monto, username=username,
                          correo=correo, tienda=tienda, credit_card=credit_card)
        db.session.add(payment)
        db.session.commit()

        payment_dict = {
            'status': 'ok',
            'id_payment': payment.id,
            'username': payment.username,
            'correo': payment.correo,
            'tienda': payment.tienda
        }
        return jsonify(payment_dict)
    except:
        payment_dict = {
            'status': 'no response',
            'message': 'Los datos son invalidos'
        }
        return jsonify(payment_dict)

if __name__=='__main__':        
    #Run the applications
    app.run()