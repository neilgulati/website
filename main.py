from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
import smtplib
import os

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]


sender_email = os.environ["EMAIL_ADDRESS"]
gmail_password = os.environ["EMAIL_PASSWORD"]


class ContactForm(FlaskForm):
    name = StringField("Name*", validators=[DataRequired()], render_kw={"placeholder": "Your Name"})
    email = StringField("Email*", validators=[DataRequired(), Email()], render_kw={"placeholder": "Your Email"})
    message = TextAreaField("Message", render_kw={"placeholder": "Your Message"})
    submit_btn = SubmitField("Send Message")


@app.route("/")
def home():
    contact_form = ContactForm()
    return render_template("index.html", form=contact_form)

@app.route("/work")
def work():
    return render_template("work.html")


@app.route("/contact", methods=["POST","GET"])
def contact():
    contact_form = ContactForm()
    user_name = contact_form.name.data
    user_email = contact_form.email.data
    user_msg = contact_form.message.data
    # if request.method == "POST": #to check if the user submit the form (whether it is a get or post request)
    if contact_form.validate_on_submit():
        try:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=sender_email, password=gmail_password)
                connection.sendmail(to_addrs=sender_email, from_addr=sender_email,
                                    msg=f"Subject: Query\n\nName: {user_name}\nEmail: {user_email}\nMessage: {user_msg}")
            return jsonify({"success": True, "message": "Message sent successfully."})
        except Exception:
            return jsonify({"success": False, "errors": {"server": ["Failed to send email."]}})

    if contact_form.errors:
        return jsonify({"success": False, "errors": contact_form.errors})
    return render_template("contact.html", form=contact_form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
