from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import app, db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


pres = db.Table('pres',
                db.Column('user_id', db.Integer, db.ForeignKey('organisme.user_id')),
                db.Column('prestation_id', db.Integer, db.ForeignKey('prestation.prestation_id'))
                )

refs = db.Table('refs',
                db.Column('user_id', db.Integer, db.ForeignKey('organisme.user_id')),
                db.Column('reference_id', db.Integer, db.ForeignKey('reference.reference_id'))
                )
cibs = db.Table('cibles',
                db.Column('organisme_id', db.Integer, db.ForeignKey('certification.organisme_id')),
                db.Column('cible_id', db.Integer, db.ForeignKey('cible.cible_id'))
                )
evals = db.Table('evals',
                 db.Column('organisme_id', db.Integer, db.ForeignKey('ingenierie.organisme_id')),
                 db.Column('evaluateur_id', db.Integer, db.ForeignKey('evaluateur.evaluateur_id'))
                 )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Organisme(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False, unique=True)
    certification = db.relationship("Certification", uselist=False, backref="organisme")
    ingenierie = db.relationship("Ingenierie", uselist=False, backref="organisme")
    # 1
    nom = db.Column(db.String(64))
    type = db.Column(db.String(64))
    date_creation = db.Column(db.DateTime())
    # 2
    numero_declaration_activite = db.Column(db.String(64))
    # 3
    reseau = db.Column(db.String(64))
    # 4
    prestations = db.relationship('Prestation', secondary=pres,
                                  backref=db.backref('organismes', lazy='dynamic'))
    # 5
    certification_existence = db.Column(db.Boolean())
    certification_enregistree = db.relationship("CertificationEnregistree", uselist=False, backref="organisme")
    # 6
    references = db.relationship('Reference', secondary=refs,
                                 backref=db.backref('organismes', lazy='dynamic'))

    def __repr__(self):
        return '<Organisme {}>'.format(self.nom)


class Prestation(db.Model):
    prestation_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    nom = db.Column(db.String(64))

    def __repr__(self):
        return '<Prestation {}>'.format(self.nom)


class Reference(db.Model):
    reference_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    nom = db.Column(db.String(64))

    def __repr__(self):
        return '<Référence {}>'.format(self.nom)


class CertificationEnregistree(db.Model):
    organisme_id = db.Column(db.Integer, db.ForeignKey('organisme.user_id'), primary_key=True, nullable=False,
                             unique=True)
    nom = db.Column(db.String(64))
    numero_fiche = db.Column(db.String(64))
    nomenclature = db.Column(db.String(64))
    date_echeance = db.Column(db.String(64))


class Cible(db.Model):
    cible_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    nom = db.Column(db.String(64))

    def __repr__(self):
        return '<Cible {}>'.format(self.nom)


class Certification(db.Model):
    organisme_id = db.Column(db.Integer, db.ForeignKey('organisme.user_id'), primary_key=True, nullable=False,
                             unique=True)
    # 1
    nom = db.Column(db.String(64))
    # 2
    cibles = db.relationship('Cible', secondary=cibs,
                             backref=db.backref('certifications', lazy='dynamic'))
    activite_reglementee = db.Column(db.Boolean())
    # 3
    date_creation = db.Column(db.DateTime())
    # 4
    besoin_employeur = db.Column(db.String(64))
    besoin_branche_professionnelle = db.Column(db.String(64))
    besoin_reglementation = db.Column(db.String(64))
    besoin_institutions_publiques = db.Column(db.String(64))
    besoin_autre = db.Column(db.String(64))
    # 5
    etude_realisee = db.Column(db.Boolean())
    # 6
    duree = db.relationship("Duree", uselist=False, backref="certification")
    # 7
    promotions = db.Column(db.Integer)
    # 8
    stagiaires = db.Column(db.Integer)

    def __repr__(self):
        return '<Certification {}>'.format(self.organisme_id)

    def __init__(self, organisme_id):
        self.organisme_id = organisme_id


class Duree(db.Model):
    certification_id = db.Column(db.Integer, db.ForeignKey('certification.organisme_id'), primary_key=True,
                                 nullable=False,
                                 unique=True)
    description = db.Column(db.String(64))


class Evaluateur(db.Model):
    evaluateur_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    nom = db.Column(db.String(64))

    def __repr__(self):
        return '<Evaluateur {}>'.format(self.nom)


class Ingenierie(db.Model):
    organisme_id = db.Column(db.Integer, db.ForeignKey('organisme.user_id'), primary_key=True, nullable=False,
                             unique=True)
    # 1
    programme_formation = db.Column(db.Boolean)
    # 2
    refenrentiel_activites_competences = db.Column(db.Boolean)
    blocs_competences = db.Column(db.Boolean)
    nombre_blocs = db.Column(db.Integer)
    # 3
    modalites_evaluation = db.Column(db.String)
    criteres_evaluation = db.Column(db.String)
    evaluateurs = db.relationship('Evaluateur', secondary=evals,
                                  backref=db.backref('organismes', lazy='dynamic'))
    # 4
    vae = db.Column(db.Boolean)
    candidats_vae = db.Column(db.Integer)
    # 5
    ccn = db.Column(db.String)
    changement_poste = db.Column(db.Boolean)
    changement_coefficient_remuneration = db.Column(db.Boolean)
    qualification = db.Column(db.Boolean)
    # 6
    reconnaissance_certification_rs = db.Column(db.Boolean)
    reconnaissance_certification_rncp = db.Column(db.Boolean)

    def __repr__(self):
        return '<Ingénierie {}>'.format(self.organisme_id)

    def __init__(self, organisme_id):
        self.organisme_id = organisme_id


db.init_app(app)
db.create_all()
