from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, SelectMultipleField, widgets, IntegerField, \
    TextAreaField
from wtforms.validators import DataRequired, NumberRange, Optional, Required
from wtforms.fields.html5 import DateField

TYPES_ORGANISME = [
    'Un formateur indépendant',
    'Un organisme de formation (OF)',
    'Un organisme certificateur (OC)'
]
TYPES_RESEAU = [
    'En tant que tête de réseau',
    'En tant que partenaire',
    'Autre'
]
TYPES_PRESTATION = [
    ('Formation initiale', 'Formation initiale'),
    ('Formation continue', 'Formation continue'),
    ('Formation en alternance', 'Formation en alternance'),
    ('Formation en apprentissage', 'Formation en apprentissage')
]
TYPES_REFERENCE = [
    ('Data-Dock', 'Data-Dock'),
    ('Qualiopi', 'Qualiopi'),
]
TYPES_CIBLE = [
    ('Métier', 'Métier'),
    ('Activité professionnelle', 'Activité professionnelle'),
    ("Spécialité d'un métier", "Spécialité d'un métier"),
    ('Compétence', 'Compétence')
]
TYPES_DUREE = [
    ('Moins de 21 heures', 'Moins de 21 heures'),
    ('Moins de 70 heures', 'Moins de 70 heures'),
    ('Entre 70 et 150 heures', 'Entre 70 et 150 heures'),
    ('Plus de 150 heures', 'Plus de 150 heures')
]
TYPES_EVALUATEUR = [
    ("Jury d'évaluation", "Jury d'évaluation"),
    ("Evaluateur interne à l'organisme", "Evaluateur interne à l'organisme"),
    ("Evaluateur externe à l'organisme (professionnels)", "Evaluateur externe à l'organisme (professionnels)"),
    ("Autres (à renseigner)", "Autres (à renseigner)")
]


# UTILITAIRE


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ul', prefix_label=False)
    option_widget = widgets.CheckboxInput()


class RequiredIf(DataRequired):
    """Validator which makes a field required if another field is set and has a truthy value.

    Sources:
        - https://wtforms.simplecodes.com/docs/1.0.1/validators.html
        - https://stackoverflow.com/questions/8463209/how-to-make-a-field-conditionally-optional-in-wtforms
        - https://gist.github.com/devxoul/7638142#file-wtf_required_if-py
    """
    field_flags = ('requiredif',)

    def __init__(self, message=None, **kwargs):
        super(RequiredIf).__init__()
        self.message = message
        self.conditions = kwargs

    # field is requiring that name field in the form is data value in the form
    def __call__(self, form, field):
        for name, data in self.conditions.items():
            other_field = form[name]
            if other_field is None:
                raise Exception('no field named "%s" in form' % name)
            if other_field.data == data and not field.data:
                DataRequired.__call__(self, form, field)
            Optional()(form, field)


# ORGANISME


class OrganismForm1(FlaskForm):
    nom = StringField(validators=[DataRequired()], render_kw={"placeholder": "Nom de votre organisme", "autofocus": ""})
    type = SelectField('Type d\'organisme', choices=TYPES_ORGANISME, validators=[DataRequired()])
    date_creation = DateField('Date création', validators=[DataRequired()])
    submit = SubmitField('Suivant')


class OrganismForm2(FlaskForm):
    numero_declaration_activite = StringField(validators=[DataRequired()],
                                              render_kw={"placeholder": "Numéro de déclaration d'activité",
                                                         "autofocus": ""})
    submit = SubmitField('Suivant')


class OrganismForm3(FlaskForm):
    reseau = SelectField('Réseau', choices=TYPES_RESEAU, validators=[DataRequired()])
    submit = SubmitField('Suivant')


class OrganismForm4(FlaskForm):
    prestations = MultiCheckboxField(choices=TYPES_PRESTATION)
    submit = SubmitField('Suivant')


class OrganismForm5(FlaskForm):
    certification_enregistree = BooleanField('Certification enregistrée', default=False)
    certification_nom = StringField(validators=[RequiredIf(certification_enregistree=True)],
                                    render_kw={"placeholder": "Nom de la certification enregistrée"})
    certification_numero_fiche = StringField(validators=[RequiredIf(certification_enregistree=True)],
                                             render_kw={"placeholder": "Numéro de fiche"})
    certification_nomenclature = StringField(validators=[RequiredIf(certification_enregistree=True)],
                                             render_kw={"placeholder": "Nomenclature du niveau de qualification"})
    certification_date_echeance = DateField(validators=[RequiredIf(certification_enregistree=True)],
                                            render_kw={"placeholder": "Date d'échéance de la certification"})
    submit = SubmitField('Suivant')


class OrganismForm6(FlaskForm):
    references = MultiCheckboxField('Référence(s)', choices=TYPES_REFERENCE)
    submit = SubmitField('Suivant')


# CERTIFICATION


class CertificationForm1(FlaskForm):
    nom = StringField(validators=[DataRequired()],
                      render_kw={"placeholder": "Nom de votre certification", "autofocus": ""})
    submit = SubmitField('Suivant')


class CertificationForm2(FlaskForm):
    cibles = MultiCheckboxField('Cible(s)', choices=TYPES_CIBLE)
    submit = SubmitField('Suivant')


class CertificationForm3(FlaskForm):
    date_creation = DateField('Date création', validators=[DataRequired()])
    submit = SubmitField('Suivant')


class CertificationForm4(FlaskForm):
    besoin_employeur_existence = BooleanField()
    besoin_employeur = TextAreaField()
    besoin_branche_professionnelle_existence = BooleanField()
    besoin_branche_professionnelle = TextAreaField()
    besoin_reglementation_existence = BooleanField()
    besoin_reglementation = TextAreaField()
    besoin_institutions_publiques_existence = BooleanField()
    besoin_institutions_publiques = TextAreaField()
    besoin_autre_existence = BooleanField()
    besoin_autre = TextAreaField()
    submit = SubmitField('Suivant')


class CertificationForm5(FlaskForm):
    etude_realisee = BooleanField("Votre activité est-elle liée à une activité réglementée", default=False)
    submit = SubmitField('Suivant')


class CertificationForm6(FlaskForm):
    duree = SelectField('Durée de la formation', choices=TYPES_DUREE, validators=[DataRequired()])
    submit = SubmitField('Suivant')


class CertificationForm7(FlaskForm):
    promotions = IntegerField(default=0, render_kw={"type": "number", "autofocus": ""})
    submit = SubmitField('Suivant')


class CertificationForm8(FlaskForm):
    stagiaires = IntegerField(default=0, render_kw={"type": "number", "autofocus": ""})
    submit = SubmitField('Suivant')


# INGENIERIE DE CERTIFICATION


class IngenierieForm1(FlaskForm):
    programme_formation = BooleanField()
    submit = SubmitField('Suivant')


class IngenierieForm2(FlaskForm):
    refenrentiel_activites_competences = BooleanField()
    blocs_competences = BooleanField()
    nombre_blocs = IntegerField()
    submit = SubmitField('Suivant')


class IngenierieForm3(FlaskForm):
    modalites_evaluation = StringField()
    criteres_evaluation = StringField()
    evaluateurs = MultiCheckboxField('Evaluateur(s)', choices=TYPES_EVALUATEUR)
    submit = SubmitField('Suivant')


class IngenierieForm4(FlaskForm):
    vae = BooleanField()
    candidats_vae = IntegerField()
    submit = SubmitField('Suivant')


class IngenierieForm5(FlaskForm):
    ccn = StringField()
    changement_poste = BooleanField()
    changement_coefficient_remuneration = BooleanField()
    qualification = BooleanField()
    submit = SubmitField('Suivant')


class IngenierieForm6(FlaskForm):
    reconnaissance_certification_rs = BooleanField()
    reconnaissance_certification_rncp = BooleanField()
    submit = SubmitField('Suivant')
