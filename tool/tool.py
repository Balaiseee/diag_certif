from flask import Blueprint, render_template, redirect, url_for, send_from_directory
from flask_login import login_required, current_user
from tool.forms import *
from models import *
from app import db

tool_bp = Blueprint('tool_bp', __name__, template_folder='templates/tool')


# UTILITAIRE


def instanciate_organism():
    user_id = current_user.get_id()
    if not Organisme.query.filter_by(user_id=user_id).first():
        organism = Organisme(user_id=user_id)
        db.session.add(organism)
        db.session.commit()


def instanciate(field, name):
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()
    if not getattr(organism, field):
        element = globals()[name](organisme_id=user_id)
        db.session.add(element)
        db.session.commit()


def check_fields_not_none_subclass(main_field, fields):
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()
    for field in fields:
        if getattr(getattr(organism, main_field), field):
            return True
    return False


def check_fields_not_none(fields):
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()
    for field in fields:
        if getattr(organism, field):
            return True
    return False


def create_route_simple_form(fields, template, next, form):
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()
    if not check_fields_not_none(fields):
        if form.validate_on_submit():
            for field in fields:
                if not getattr(organism, field):
                    setattr(organism, field, getattr(form, field).data)
            db.session.commit()
            return redirect(url_for(next))
        return render_template(template, form=form)
    return redirect(url_for(next))


def create_route_simple_form_subclass(main_field, fields, template, next, form):
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()
    if not check_fields_not_none_subclass(main_field, fields):
        if form.validate_on_submit():
            for field in fields:
                if not getattr(getattr(organism, main_field), field):
                    setattr(getattr(organism, main_field), field, getattr(form, field).data)
            db.session.commit()
            return redirect(url_for(next))
        return render_template(template, form=form)
    return redirect(url_for(next))


# ORGANISME


@tool_bp.route('/org_1', methods=['GET', 'POST'])
@login_required
def org_1():
    instanciate_organism()
    return create_route_simple_form(['nom', 'type', 'date_creation'],
                                    'Org_1.html',
                                    'tool_bp.org_2',
                                    OrganismForm1(), )


@tool_bp.route('/org_2', methods=['GET', 'POST'])
@login_required
def org_2():
    return create_route_simple_form(['numero_declaration_activite'],
                                    'Org_2.html',
                                    'tool_bp.org_3',
                                    OrganismForm2(), )


@tool_bp.route('/org_3', methods=['GET', 'POST'])
@login_required
def org_3():
    return create_route_simple_form(['reseau'],
                                    'Org_3.html',
                                    'tool_bp.org_4',
                                    OrganismForm3(), )


@tool_bp.route('/org_4', methods=['GET', 'POST'])
@login_required
def org_4():
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()
    form = OrganismForm4()
    if not organism.prestations:
        if form.validate_on_submit():
            for prestation in form.prestations.data:
                organism.prestations.append(Prestation(nom=prestation))
            db.session.commit()
            return redirect(url_for('tool_bp.org_5'))
        return render_template('Org_4.html', form=OrganismForm4())
    return redirect(url_for('tool_bp.org_5'))


@tool_bp.route('/org_5', methods=['GET', 'POST'])
@login_required
def org_5():
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()
    form = OrganismForm5()
    if not organism.certification_existence:
        if form.validate_on_submit():
            if not form.certification_enregistree.data:
                organism.certification_existence = False
                db.session.commit()
                return redirect(url_for('tool_bp.org_6'))
            else:
                organism.certification_existence = True
                certification = CertificationEnregistree(organisme_id=user_id,
                                                         nom=form.certification_nom.data,
                                                         numero_fiche=form.certification_numero_fiche.data,
                                                         nomenclature=form.certification_nomenclature.data,
                                                         date_echeance=form.certification_date_echeance.data
                                                         )
                db.session.add(certification)
                db.session.commit()
                return redirect(url_for('tool_bp.org_6'))
        return render_template('Org_5.html', form=OrganismForm5())
    return redirect(url_for('tool_bp.org_6'))


@tool_bp.route('/org_6', methods=['GET', 'POST'])
@login_required
def org_6():
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()
    form = OrganismForm6()
    if not organism.references:
        if form.validate_on_submit():
            for reference in form.references.data:
                ref = Reference(nom=reference)
                organism.references.append(ref)
            db.session.commit()
            return redirect(url_for('tool_bp.cert_1'))
        return render_template('Org_6.html', form=OrganismForm6())
    return redirect(url_for('tool_bp.cert_1'))


# CERTIFICATION


@tool_bp.route('/cert_1', methods=['GET', 'POST'])
@login_required
def cert_1():
    instanciate('certification', 'Certification')
    return create_route_simple_form_subclass('certification', ['nom'],
                                             'Cert_1.html',
                                             'tool_bp.cert_2',
                                             CertificationForm1())


@tool_bp.route('/cert_2', methods=['GET', 'POST'])
@login_required
def cert_2():
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()
    form = CertificationForm2()
    if not organism.certification.cibles:
        if form.validate_on_submit():
            for cible in form.cibles.data:
                cible = Cible(nom=cible)
                organism.certification.cibles.append(cible)
            db.session.commit()
            return redirect(url_for('tool_bp.cert_3'))
        return render_template('Cert_2.html', form=CertificationForm2())
    return redirect(url_for('tool_bp.cert_3'))


@tool_bp.route('/cert_3', methods=['GET', 'POST'])
@login_required
def cert_3():
    return create_route_simple_form_subclass('certification', ['date_creation'],
                                             'Cert_3.html',
                                             'tool_bp.cert_4',
                                             CertificationForm3())


@tool_bp.route('/cert_4', methods=['GET', 'POST'])
@login_required
def cert_4():
    return create_route_simple_form_subclass('certification', ['besoin_employeur',
                                                               'besoin_branche_professionnelle',
                                                               'besoin_reglementation',
                                                               'besoin_institutions_publiques',
                                                               'besoin_autre'],
                                             'Cert_4.html',
                                             'tool_bp.cert_5',
                                             CertificationForm4())


@tool_bp.route('/cert_5', methods=['GET', 'POST'])
@login_required
def cert_5():
    return create_route_simple_form_subclass('certification', ['etude_realisee'],
                                             'Cert_5.html',
                                             'tool_bp.cert_6',
                                             CertificationForm5(), )


@tool_bp.route('/cert_6', methods=['GET', 'POST'])
@login_required
def cert_6():
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()
    form = CertificationForm6()
    if not organism.certification.duree:
        if form.validate_on_submit():
            duree = Duree(description=form.duree.data)
            organism.certification.duree = duree
            db.session.commit()
            return redirect(url_for('tool_bp.cert_7'))
        return render_template('Cert_6.html', form=CertificationForm6())
    return redirect(url_for('tool_bp.cert_7'))


@tool_bp.route('/cert_7', methods=['GET', 'POST'])
@login_required
def cert_7(): return create_route_simple_form_subclass('certification', ['promotions'],
                                                       'Cert_7.html',
                                                       'tool_bp.cert_8',
                                                       CertificationForm7(), )


@tool_bp.route('/cert_8', methods=['GET', 'POST'])
@login_required
def cert_8():
    return create_route_simple_form_subclass('certification', ['stagiaires'],
                                             'Cert_8.html',
                                             'tool_bp.ing_1',
                                             CertificationForm8())


# INGENIERIE DE CERTIFICATION

@tool_bp.route('/ing_1', methods=['GET', 'POST'])
@login_required
def ing_1():
    instanciate('ingenierie', 'Ingenierie')
    return create_route_simple_form_subclass('ingenierie', ['programme_formation'],
                                             'Inge_1.html',
                                             'tool_bp.ing_2',
                                             IngenierieForm1())


@tool_bp.route('/ing_2', methods=['GET', 'POST'])
@login_required
def ing_2():
    return create_route_simple_form_subclass('ingenierie', ['refenrentiel_activites_competences',
                                                            'blocs_competences',
                                                            'nombre_blocs'],
                                             'Inge_2.html',
                                             'tool_bp.ing_3',
                                             IngenierieForm2())


@tool_bp.route('/ing_3', methods=['GET', 'POST'])
@login_required
def ing_3():
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()
    form = IngenierieForm3()
    if not organism.ingenierie.criteres_evaluation:
        if form.validate_on_submit():
            organism.ingenierie.modalites_evaluation = form.modalites_evaluation.data
            organism.ingenierie.criteres_evaluation = form.criteres_evaluation.data
            for evaluateur in form.evaluateurs.data:
                organism.ingenierie.evaluateurs.append(Evaluateur(nom=evaluateur))
            db.session.commit()
            return redirect(url_for('tool_bp.ing_4'))
        return render_template('Inge_3.html', form=IngenierieForm3())
    return redirect(url_for('tool_bp.ing_4'))


@tool_bp.route('/ing_4', methods=['GET', 'POST'])
@login_required
def ing_4():
    return create_route_simple_form_subclass('ingenierie', ['vae',
                                                            'candidats_vae'],
                                             'Inge_4.html',
                                             'tool_bp.ing_5',
                                             IngenierieForm4())


@tool_bp.route('/ing_5', methods=['GET', 'POST'])
@login_required
def ing_5():
    return create_route_simple_form_subclass('ingenierie', ['ccn',
                                                            'changement_poste',
                                                            'changement_coefficient_remuneration',
                                                            'qualification'],
                                             'Inge_5.html',
                                             'tool_bp.ing_6',
                                             IngenierieForm5())


@tool_bp.route('/ing_6', methods=['GET', 'POST'])
@login_required
def ing_6():
    return create_route_simple_form_subclass('ingenierie', ['reconnaissance_certification_rs',
                                                            'reconnaissance_certification_rncp'],
                                             'Inge_6.html',
                                             'home_bp.outro',
                                             IngenierieForm6())


# DASHBOARD


@tool_bp.route('/resultat')
@login_required
def resultat():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'pdf/resultat.pdf')


@tool_bp.route('/home')
@login_required
def home():
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()
    return render_template('home.html', organisme=organism)


def references_contains():
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()
    for ref in organism.references:
        if ref.nom == 'Data-Dock':
            return True
    return False


def cibles_contains():
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()
    for cible in organism.certification.cibles:
        if cible.nom == 'Métier':
            return True
    return False


def rs():
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()
    eligibilite_rs = False
    if (
            len(organism.prestations) != 0 and
            references_contains() and
            len(organism.certification.cibles) != 0 and
            (
                    organism.certification.besoin_autre or
                    organism.certification.besoin_employeur or
                    organism.certification.besoin_reglementation or
                    organism.certification.besoin_branche_professionnelle or
                    organism.certification.besoin_institutions_publiques
            ) and
            not organism.certification.duree.description == 'Moins de 21 heures' and
            organism.ingenierie.refenrentiel_activites_competences
    ):
        eligibilite_rs = True
    return eligibilite_rs


def rncp():
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()
    eligibilite_rncp = False
    if (
            len(organism.prestations) != 0 and
            references_contains() and
            cibles_contains() and
            (
                    organism.certification.besoin_autre or
                    organism.certification.besoin_employeur or
                    organism.certification.besoin_reglementation or
                    organism.certification.besoin_branche_professionnelle or
                    organism.certification.besoin_institutions_publiques
            ) and
            organism.certification.duree.description == 'Plus de 150 heures' and
            organism.certification.promotions >= 2 and
            organism.ingenierie.refenrentiel_activites_competences and
            organism.ingenierie.vae and
            (
                    organism.ingenierie.changement_coefficient_remuneration or
                    organism.ingenierie.changement_poste or
                    organism.ingenierie.qualification
            )
    ):
        eligibilite_rncp = True
    return eligibilite_rncp


@tool_bp.route('/verdict')
@login_required
def verdict():
    user_id = current_user.get_id()
    organism = Organisme.query.filter_by(user_id=user_id).first()

    return render_template('verdict.html', organisme=organism, rs=rs(), rncp=rncp())
