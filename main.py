
from flask import Flask, render_template, request, session, redirect, url_for
import json
import time
from vhdlweb_build import * 

app = Flask(__name__)
app.secret_key = b'ap9283hjpfa3jP(*#J(*$' # Used for session encryption

def readfile(filename):
  """ Read a file's contents into a string. """
  f = open(filename)
  s = f.read()
  f.close()
  return s

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    # If it's a POST, then validate the info and log the user in
    session['username'] = request.form['username']
    return redirect(url_for('index'))

  # If it's a GET, show the login page
  return render_template('login.html')

@app.route('/logout')
def logout():
  # Just delete the username cookie and send them back to the home page
  session.pop('username')
  return redirect(url_for('index'))

@app.route('/sandbox')
def sandbox():
  return "The sandbox is still under construction."

@app.route('/assignments')
def showAssignments():
  if 'username' in session:
    assignments = json.load(open('data/assignments.json'))
    # TODO: annotate this with the ones that are complete
  else:
    assignments = []

  return render_template('assignments.html', assignments = assignments)

@app.route('/compile/<problemId>', methods=['POST'])
def compilerequest(problemId):
  if request.method == 'POST':
    requestblob = request.json

    if 'username' in session:
      username = session['username']
    else:
      username = "anonymous"
 
    # Get a working directory for this submission
    wdir = findpath(username, problemId)

    # Write a metadata file into the directory
    # Username/problem are captured by the directory name
    metadata = {'button':requestblob['button'],
                'changetext':requestblob['changetext'],
                'pagetime':requestblob['pagetime'],
                'time':time.ctime()}
    metafile = open(wdir + '/metadata.json', 'w')
    json.dump(metadata, metafile)
    metafile.close()

    # Write the code file into the directory
    codefile = open(wdir + '/submission.vhd', 'w')
    codefile.write(requestblob['code'])# code.decode('utf-8')
    codefile.close()

    # Copy build files and execute the build
    output = compile(wdir, problemId)

    # TODO: If the test passed, then mark this problem as complete
    return json.dumps(output)

@app.route('/problem/<problemId>')
def showProblem(problemId):
  prompt = readfile("data/problems/{}/prompt".format(problemId))

  # TODO: If the user has already tried this problem, give them their last attempt
  # Otherwise, use the starter code
  # TODO: need a starter-code reset button, and/or a history log
  startercode = readfile("data/problems/{}/startercode".format(problemId))

  return render_template('problem.html', problemId=problemId, prompt=prompt, startercode=startercode)

