import cv2
import urllib.request
import os
import secrets
from PIL import Image
from werkzeug.utils import secure_filename
from flask import render_template, url_for, flash, redirect, request, abort, Flask
from graphics import app, db, bcrypt
from graphics.dct_watermark1 import *
from graphics.forms import RegistrationForm, LoginForm, UpdateAccountForm
from graphics.models import User
from flask_login import login_user, current_user, logout_user, login_required


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
@app.route("/homepage")
def homepage(): 
	return render_template('homepage.html')


@app.route("/register", methods =['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('homepage'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit() 
		flash('Your account has been Created! ou can now log in', 'success') 
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods =['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('homepage'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('account'))
		else:
			flash('Login Unsuccessful, Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('homepage'))


def save_picture(form_picture): #To save profile pictures
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path,'static/profile_pics', picture_fn) #path for profile pictures
	
	output_size = (125, 125) #image resizing
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn

@app.route("/account", methods =['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated!', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/portfolio", methods =['GET', 'POST'])
@login_required
def portfolio():
	form = UpdateAccountForm()
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('portfolio.html', title='Portfolio', image_file=image_file, form=form)

			# ROUTES FOR IMAGE READER SYSTEM #


@app.route('/getImg', methods=['POST'])
def upload_image():    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        file.filename = "original.jpg"
        # filename = secure_filename(file.filename)
        path = os.path.join(app.root_path,'static/uploads', file.filename)
        file.save(path)

        return render_template('portfolio.html', show_predictions_modal=True, filename=file.filename, )
        # return redirect(url_for ('static', filename='uploads/' + file.filename, show_predictions_modal=True), code=301)
        
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/embed')
def embed_DCT():
    
    cover = cv2.imread('C:/Users/Hermenia Bucana/Desktop/Graphics/graphics/static/uploads/original.jpg')
    # # read wm
    wm = cv2.imread('C:/Users/Hermenia Bucana/Desktop/Graphics/graphics/static/dataset/logo.jpg')
    model = DCT_Watermark()
    emb_img = model.embed(cover, wm)
    cv2.imwrite('C:/Users/Hermenia Bucana/Desktop/Graphics/graphics/static/results/watermarked.png', emb_img)

    return redirect (url_for('portfolio'))

def doneEmbedding():
    
    return render_template('portfolio.html')#directory after embedding/portfolio

@app.route('/display/<filename>')
def display_image(filename):

    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/exit')
def exit_IRS():

     return render_template('portfolio.html') #cancel embedding


