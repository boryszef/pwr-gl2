from flask import render_template, request, Blueprint
from flask import redirect, url_for, flash, session
from flask_login import login_user, login_manager
from flask_menu import register_menu
import genomelink
import os
from app.login_forms import LoginForm

main = Blueprint('main', __name__)


traits = ('agreeableness', 'conscientiousness', 'extraversion', 'neuroticism',
          'openness')


@main.route("/")
@register_menu(main, '.home', 'Home', order=0)
def index():
    '''Display main view of the app'''
    return render_template('index.html')

import app.model as model
from app.__init__ import login
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login.user_loader
@main.route("/login", methods=['GET', 'POST'])
@register_menu(main, '.login','Sing in',order=4)
def login():
    # session = model.loadSession()
    form = LoginForm()
    # if user_logged_in:
    #     flash("You are already logged in")
    #     return render_template('logout.html', title='Log Out', )
    if form.validate_on_submit():
        '''check if username is in database(search to first username, 
        because I assume there is no 2 users with the same username!!!'''

        user = model.isHere(form.username.data)
        if user and form.password.data==user.password:
            flash('Logged in successfully as {}'.format(form.username.data))
            login_user(user, remember=form.remember_me.data)
            return render_template('index.html')
        else:
            flash("Wrong password or username")
            return redirect(url_for('main.login'))
    return render_template('login.html', title='Sing In ',
                           form=form)


@main.route("/logout")
def logout():
    return render_template('index.html')


@main.route("/genome")
@register_menu(main, '.genome', 'Genomic insight', order=1)
def genome():
    '''Display genomic insight based on GenomeLink API'''

    scope = ['report:{}'.format(t) for t in traits]
    authorize_url = genomelink.OAuth.authorize_url(scope=scope)

    reports = []
    if session.get('oauth_token'):
        for name in traits:
            reports.append(genomelink.Report.fetch(
                                name=name,
                                population='european',
                                token=session['oauth_token']))

    return render_template('genome.html', reports=reports,
                           authorize_url=authorize_url)


@main.route("/questionare")
@register_menu(main, '.questionare', 'Self-assessment questionare', order=2)
def questionare():
    '''Show self-assessment questionare'''
    return render_template('index.html')


@main.route("/selfassessment")
@register_menu(main, '.selfassessment', 'Self-assessment results', order=3)
def selfassessment():
    '''Show self-assessment results'''
    return render_template('index.html')


@main.route("/callback")
def callback():

    try:
        token = genomelink.OAuth.token(request_url=request.url)

    except genomelink.errors.GenomeLinkError as e:
        flash('Authorization failed.')
        if os.environ.get('DEBUG') == '1':
            flash('[DEBUG] ({}) {}'.format(e.error, e.description))
        return redirect(url_for('genome'))

    session['oauth_token'] = token
    return redirect(url_for('main.genome'))
