from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Create the Flask application
app = Flask(__name__)

# Configure SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)


# Home route
@app.route("/")
def home():
    return {
        "message": "Expense Tracker API is running!"
    }

# Expenses route
@app.route("/expenses", methods=["POST"])
def create_expense():
    data = request.get_json()

    expense = Expense(
        title=data["title"],
        amount=data["amount"],
        category=data["category"]
    )

    db.session.add(expense)
    db.session.commit()

    return jsonify({
        "message": "Expense created successfully!"
    }), 201
#Get expense
@app.route("/expenses", methods=["GET"])
def get_expenses():
    expenses = Expense.query.all()

    result = []

    for expense in expenses:
        result.append({
            "id": expense.id,
            "title": expense.title,
            "amount": expense.amount,
            "category": expense.category
        })

    return jsonify(result)

@app.route("/expenses/<int:id>", methods=["GET"])
def get_expense(id):
    expense = Expense.query.get_or_404(id)

    return jsonify({
        "id": expense.id,
        "title": expense.title,
        "amount": expense.amount,
        "category": expense.category
    })

@app.route("/expenses/<int:id>", methods=["PUT"])
def update_expense(id):
    expense = Expense.query.get_or_404(id)

    data = request.get_json()

    expense.title = data["title"]
    expense.amount = data["amount"]
    expense.category = data["category"]

    db.session.commit()

    return jsonify({
        "message": "Expense updated successfully!"
    })
@app.route("/expenses/<int:id>", methods=["DELETE"])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)

    db.session.delete(expense)
    db.session.commit()

    return jsonify({
        "message": "Expense deleted successfully!"
    })


# Create the database
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)