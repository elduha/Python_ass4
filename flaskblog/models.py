from flaskblog import db


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crypto_name = db.Column(db.String(20), nullable=False)
    header = db.Column(db.Text, nullable=False)
    paragraph = db.Column(db.Text, nullable=False)

    def __init__(self, crypto_name, header, paragraph):
        self.crypto_name = crypto_name
        self.header = header
        self.paragraph = paragraph

