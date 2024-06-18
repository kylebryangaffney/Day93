from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField
from wtforms.validators import Optional
from datetime import datetime
import os
from saxophone import Saxophone, fetch_saxophones

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '8BYkEfBA6O6donzWlSihBXox7C0sKR6b')
Bootstrap5(app)

class SaxSelectorForm(FlaskForm):
    available = BooleanField('Available', default=True)
    type_of_sax = StringField('Type of Saxophone', validators=[Optional()])
    submit = SubmitField('Submit')

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

@app.route("/", methods=['GET', 'POST'])
def home():
    form = SaxSelectorForm()
    if form.validate_on_submit():
        available = form.available.data
        sax_type = form.type_of_sax.data
        return redirect(url_for('results', available=available, sax_type=sax_type))
    
    return render_template("index.html", form=form)

@app.route("/results")
def results():
    available = request.args.get('available') == 'True'
    sax_type = request.args.get('sax_type', '').strip().lower()

    try:
        saxophones = fetch_saxophones()
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('home'))

    if sax_type:
        filtered_saxophones = [
            sax for sax in saxophones
            if (sax.availability == 'Limited Availability' if available else sax.availability == 'Sold Out') and
               (sax.sax_type.lower() == sax_type)
        ]
    else:
        filtered_saxophones = [
            sax for sax in saxophones
            if (sax.availability == 'Limited Availability' if available else sax.availability == 'Sold Out')
        ]

    return render_template('results.html', saxophones=filtered_saxophones)

if __name__ == '__main__':
    app.run(debug=True)
