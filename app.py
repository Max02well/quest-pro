from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def homepage():
  return render_template('home.html')


@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact')
def contact():
  return render_template('contact.html')
    
@app.route('/explore')
def explore():
  return render_template('explore.html')

@app.route('/blog')
def blog():
  return render_template('blog.html')

@app.route('/privacy')
def privacy():
  return render_template('privacy.html')
@app.route('/terms')
def terms():
  return render_template('terms.html')
  

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
