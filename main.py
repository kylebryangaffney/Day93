from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import Optional, NumberRange
from datetime import datetime
import os
from saxophone import Saxophone, fetch_saxophones

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '8BYkEfBA6O6donzWlSihBXox7C0sKR6b')
Bootstrap5(app)

class SaxSelectorForm(FlaskForm):
    available = BooleanField('Available', default=True)
    type_of_sax = SelectField('Type of Saxophone', choices=[
        ('all', 'All'),
        ('soprano', 'Soprano'),
        ('alto', 'Alto'),
        ('tenor', 'Tenor'),
        ('baritone', 'Baritone'),
        ('other', 'Other'),
    ], validators=[Optional()])
    min_price = IntegerField('Min Price $', validators=[Optional(), NumberRange(min=0)])
    max_price = IntegerField('Max Price $', validators=[Optional(), NumberRange(min=0)])
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
        min_price = form.min_price.data
        max_price = form.max_price.data
        return redirect(url_for('results', available=available, sax_type=sax_type, min_price=min_price, max_price=max_price))
    
    return render_template("index.html", form=form)

@app.route("/results")
def results():
    available = request.args.get('available') == 'True'
    sax_type = request.args.get('sax_type', '').strip().lower()
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)

    try:
        saxophones = fetch_saxophones()
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('home'))

    filtered_saxophones = [
        sax for sax in saxophones
        if (sax.availability == 'Limited Availability' if available else sax.availability == 'Sold Out') and
           (sax_type == 'all' or sax.sax_type.lower() == sax_type) and
           (min_price is None or sax.price >= min_price) and
           (max_price is None or sax.price <= max_price)
    ]

    return render_template('results.html', saxophones=filtered_saxophones)

if __name__ == '__main__':
    app.run(debug=True)
