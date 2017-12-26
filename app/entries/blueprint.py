import os
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required
from werkzeug import secure_filename
from models import Entry, Tag
from helpers import object_list, entry_list, get_entry_or_404
from entries.forms import EntryForm, ImageForm
from app import app, db

entries = Blueprint('entries', __name__, template_folder='templates')

@entries.route('/')
def index():
	entries = Entry.query.order_by(Entry.created_timestamp.desc())
	return entry_list('entries/index.html', entries)

@entries.route('/tags/')
def tag_index():
	tags = Tag.query.order_by(Tag.name)
	return object_list('entries/tag_index.html', tags)

@entries.route('/tags/<slug>/')
def tag_detail(slug):
	tag = Tag.query.filter(Tag.slug == slug).first_or_404()
	entries = tag.entries.order_by(Entry.created_timestamp.desc())
	return entry_list('entries/tag_detail.html', entries, tag=tag)

@entries.route('/<slug>/')
def detail(slug):
	# entry = Entry.query.filter(Entry.slug == slug).first_or_404()
	entry = get_entry_or_404(slug)
	return render_template('entries/detail.html', entry=entry)

@entries.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
	if request.method == 'POST':
		form = EntryForm(request.form)
		if form.validate():
			entry = form.save_entry(Entry())
			db.session.add(entry)
			db.session.commit()
			flash("Entry {0} created successfully.".format(entry.title), 'success')
			return redirect(url_for('entries.detail', slug=entry.slug))
	else:
		form = EntryForm()
	return render_template('entries/create.html', form=form)

@entries.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
	# entry = Entry.query.filter(Entry.slug == slug).first_or_404()
	entry = get_entry_or_404(slug)
	if request.method == 'POST':
		form = EntryForm(request.form, obj=entry)
		if form.validate():
			entry = form.save_entry(entry)
			db.session.add(entry)
			db.session.commit()
			flash("Entry {0} has been saved.".format(entry.title), 'success')
			return redirect(url_for('entries.detail', slug=entry.slug))
	else:
		form = EntryForm(obj=entry)
	return render_template('entries/edit.html', entry=entry, form=form)

@entries.route('/<slug>/delete/', methods=['GET', 'POST'])
@login_required
def delete(slug):
	# entry = Entry.query.filter(Entry.slug == slug).first_or_404()
	entry = get_entry_or_404(slug)
	if request.method == 'POST':
		entry.status = Entry.STATUS_DELETED
		db.session.add(entry)
		db.session.commit()
		flash("Entry {0} has been deleted.".format(entry.title), 'success')
		return redirect(url_for('entries.index'))
	return render_template('entries/delete.html', entry=entry)

@entries.route('/image-upload/', methods=['GET', 'POST'])
@login_required
def image_upload():
	if request.method == 'POST':
		form = ImageForm(request.form)
		if form.validate():
			image_file = request.files['file']
			filename = os.path.join(app.config['IMAGES_DIR'], secure_filename(image_file.filename))
			image_file.save(filename)
			flash("Saved {0}".format(os.path.basename(filename), 'success'))
			return redirect(url_for('entries.index'))
	else:
		form = ImageForm()
	return render_template('entries/image_upload.html', form=form)