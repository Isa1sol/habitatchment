from app import create_app

app = create_app()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)  # ✅ This is the key line

if __name__ == "__main__":
    app.run(debug=True)
