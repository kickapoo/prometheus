from . import flatpages
from flask import render_template


@flatpages.route('/terms-of-use')
def terms_of_use():
    return render_template('flatpages/terms-of-use.html')

@flatpages.route('/privacy-policy')
def privacy_policy():
    return render_template('flatpages/privacy-policy.html')
