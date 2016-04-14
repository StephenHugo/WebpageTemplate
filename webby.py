from flask import Flask, render_template, Blueprint, redirect, send_file, flash
from flask import request as req
import requests
from StringIO import StringIO as sIO
from PIL import Image as img
from numpy import array, double, max, min, vstack, zeros, dstack, random, sum, zeros
from newt import newt

app = Flask(__name__)
app.secret_key = 'secret key'

home = Blueprint('home', __name__)
projects = Blueprint('projects', __name__)
process = Blueprint('process', __name__)
research = Blueprint('research', __name__)

@home.route('/')
def index():
   return render_template('index.html')
	
@research.route('/research')
def index():
	return render_template('researchindex.html')
	
@research.route('/research/asf')
def asf():
	return render_template('asf.html')
	
@research.route('/research/migration')
def migration():
	return render_template('migration.html')
	
@home.route('/publications')
def publications():
   return render_template('publications.html')
	
@home.route('/honors')
def honors():
   return render_template('honors.html')
	
@home.route('/about')
def about():
   return render_template('about.html')
	
@projects.route('/projects', methods=['GET', 'POST'])
def index():
	if req.method == 'POST':
		url = req.form['link']
		filtertype = req.form['button']
		if not url:
			return render_template('scientific.html')
		elif (filtertype == 'none'):
			return render_template('scientific.html')
		
		flash(url.replace(':','%3A').replace('/','%2F').replace('?','%3F').replace('=','%3D').replace('&','%26'))
		
		if (filtertype == 'hny'):
			return render_template('hny.html')	
		elif (filtertype == 'varfilt'):
			return render_template('varfilter.html')
		else:
			return redirect(url)
	else:
		return render_template('scientific.html')
	
@projects.route('/projects/standard', methods=['GET', 'POST'])
def standard():
	if req.method == 'POST':
		url = req.form['link']
		filtertype = req.form['button']
		if not url:
			return render_template('standard.html')
		elif (filtertype == 'none'):
			return render_template('standard.html')
		
		flash(url.replace(':','%3A').replace('/','%2F').replace('?','%3F').replace('=','%3D').replace('&','%26'))
		
		if (filtertype == 'highboost'):		
			return render_template('highboost.html')	
		elif (filtertype == 'srtfilt'):
			return render_template('srtfilt.html')
		else:
			return redirect(url)
	else:
		return render_template('standard.html')

@process.route('/processed')
def highboost():
	url = req.args.get('link')
	if not url:
		return render_template('standard.html')
	
	try:
		# download the image from the url
		res = requests.get(url)
		
		# open the image using PIL
		im = img.open(sIO(res.content))
		
		# convert the PIL image to a numpy array and turn it into a newt image
		pic = newt(array(im, dtype=double))
		
		# do a convolution with a 17x17 disk
		pic.highboost('d 17')
		
		# revert to PIL format
		pic = pic.pic - min(pic.pic)
		pic = 255*pic/max(pic)
		im = img.fromarray(pic.astype('uint8'))
		
		# save the new image
		buff = sIO()
		im.save(buff, 'JPEG', quality=90)
		
		buff.seek(0)
		
		return send_file(buff, mimetype='image/jpeg')
	except:
		return redirect(url)

@process.route('/hny')
def hny():
	url = req.args.get('link')
	if not url:
		return render_template('standard.html')
	
	try:
		# download the image from the url
		res = requests.get(url)
		res2 = requests.get("http://www.themarysue.com/wp-content/uploads/2012/08/c6bfb4fac68932e833f917cd45ad2ff9.jpeg")
		
		# open the image using PIL
		im = img.open(sIO(res.content))
		im2 = img.open(sIO(res2.content)).resize(im.size, img.ANTIALIAS)
		
		# convert the PIL image to a numpy array and turn it into a newt image
		a = array(im, dtype=double)
		b = array(im2, dtype=double)
		for color in range(3):
			a[:,:][:,:,color] = a[:,:][:,:,0]/3 + a[:,:][:,:,1]/3 + a[:,:][:,:,2]/3
			a[:,:][:,:,color] = 4*a[:,:][:,:,color]/7 + 3*b[:,:][:,:,color]/7
		pic = newt(a)
		
		# do a convolution with a 17x17 disk
		#pic.mix(array(im2, dtype=double))
		
		# revert to PIL format
		pic = pic.pic - min(pic.pic)
		pic = 255*pic/max(pic)
		im = img.fromarray(pic.astype('uint8'))
		
		# save the new image
		buff = sIO()
		im.save(buff, 'JPEG', quality=90)
		
		buff.seek(0)
		
		return send_file(buff, mimetype='image/jpeg')
	except:
		return redirect(url)
		
@process.route('/varfilt')
def varfilt():
	url = req.args.get('link')
	if not url:
		return render_template('standard.html')
	
	try:
		# download the image from the url
		res = requests.get(url)
		
		# open the image using PIL
		im = img.open(sIO(res.content))
		
		# convert the PIL image to a numpy array and turn it into a newt image
		pic = newt(array(im, dtype=double))
		
		# do a convolution with a 17x17 disk
		pic.varfilt('g 5')
		
		# revert to PIL format
		pic = pic.pic - min(pic.pic)
		pic = 255*pic/max(pic)
		im = img.fromarray(pic.astype('uint8'))
		
		# save the new image
		buff = sIO()
		im.save(buff, 'JPEG', quality=90)
		
		buff.seek(0)
		
		return send_file(buff, mimetype='image/jpeg')
	except:
		return redirect(url)
		
@process.route('/srtfilt')
def srtfilt():
	url = req.args.get('link')
	if not url:
		return render_template('standard.html')
	
	try:
		# download the image from the url
		res = requests.get(url)
		
		# open the image using PIL
		im = img.open(sIO(res.content))
		
		# shrink very large images
		im.thumbnail((512,512), img.ANTIALIAS)
		
		# convert the PIL image to a numpy array and turn it into a newt image
		pic = newt(array(im, dtype=complex))
		
		# do stuff
		pic.srtfilt()
		
		# revert to PIL format
		#pic = pic.pic - min(pic.pic)
		#pic = 255*pic/max(pic)
		im = img.fromarray(pic.pic.astype('uint8'))
		
		# save the new image
		buff = sIO()
		im.save(buff, 'JPEG', quality=90)
		
		buff.seek(0)
		
		return send_file(buff, mimetype='image/jpeg')
	except:
		return redirect(url)
	 
app.register_blueprint(home)
app.register_blueprint(projects)
app.register_blueprint(process)
app.register_blueprint(research)

if __name__ == '__main__':
	app.debug = True

	app.run()