from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
#import payfast

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taxi.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    card_number = db.Column(db.String(20), nullable=False)
    journeys_left = db.Column(db.Integer, default=0)

db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/load_journey', methods=['GET', 'POST'])
def load_journey():
    if request.method == 'POST':
        card_number = request.form['card_number']
        journeys = request.form['journeys']
        user = User.query.filter_by(card_number=card_number).first()
        if user:
            user.journeys_left += int(journeys)
            db.session.commit()
            return 'Journeys loaded successfully'
        else:
            return 'Invalid card number'
    return render_template('load_journey.html')

# Set up PayFast API key
#payfast.setup('fl6pyied0azwu', '16416161')
@app.route('/pay_cash', methods=['GET', 'POST'])
def pay_cash():
    if request.method == 'POST':
        amount = request.form['amount']
        currency = request.form['currency']
        
        # Create a payment request with PayFast
        payment_request = payfast.PaymentRequest(
            amount=amount,
            item_name='Taxi payment',
            return_url='http://localhost:5000/payment_complete',
            cancel_url='http://localhost:5000/pay_cash'
        )
        
        # Generate the payment form HTML
        payment_form = payment_request.generate_form()
        
        # Render the payment form
        return payment_form
    
    return render_template('pay_cash.html')

@app.route('/payment_complete', methods=['GET'])
def payment_complete():
    return 'Payment complete. Thank you for using PayFast!'

if __name__ == '__main__':
    app.run(debug=True)
