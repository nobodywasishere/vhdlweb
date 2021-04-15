from flask import Flask, render_template, request, session, redirect, url_for, flash
from flaskext.markdown import Markdown
from logging import FileHandler, Formatter
import json
import time
import re
import os
from random import choices
from string import ascii_letters
from vhdlweb_build import *

app = Flask(__name__)
app.config.from_envvar('VHDLWEB_CONFIG')

# Set up Flask to log errors to a file (in addition to the console by default)
filelog_handler = FileHandler('vhdlweb_errors.log')
filelog_handler.setFormatter(Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
app.logger.addHandler(filelog_handler)

# Set up the Markdown extension
md = Markdown(app, extensions=['fenced_code'])

def readfile(filename):
  """ Read a file's contents into a string. """
  f = open(filename)
  s = f.read()
  f.close()
  return s

def get_user(session):
  """ Returns the identifier for this user.  If the user is not logged in,
      returns a temporary identifier. """
  if 'username' in session:
    return session['username']
  elif 'tempId' in session:
    return session['tempId']
  else:
    tempId = "".join(choices(ascii_letters, k=25))
    session['tempId'] = tempId
    return tempId

@app.route('/')
def index():
    prompt = "Put ur block diagram here"

    # Build a list of the submissions
    basepath = app.config['WORKDIR'] + '/' + get_user(session) + '/'
    submissions = []
    subdir = '0000' # Start at zero and count up

    startercode = ""

    return render_template('problem.html', prompt=prompt, submissions=submissions, startercode=startercode)
  # return render_template('index.html')

@app.route('/compile/', methods=['POST'])
def compilerequest():
  if request.method == 'POST':
    requestblob = request.json

    username = get_user(session)

    timestamp = time.ctime()

    # Get a working directory for this submission
    wdir = findpath(app.config['WORKDIR'], username)

    # Write the code file into the directory
    codefile = open(wdir + '/submission.vhd', 'w')
    codefile.write(requestblob['code'])# code.decode('utf-8')
    codefile.close()

    # Copy build files and execute the build
    output = runtest(wdir)

    # Write a metadata file into the directory
    # Username/problem are captured by the directory name
    metadata = {'button':requestblob['button'],
                'pagetime':requestblob['pagetime'],
                'pastes':requestblob['pastes'],
                'time':timestamp,
                'status':output['status'] }
    metafile = open(wdir + '/metadata.json', 'w')
    json.dump(metadata, metafile)
    metafile.close()

    # Send the result plus a little more metadata back
    submissionId = wdir.strip('/').rsplit('/', 1)[-1]
    if (output['status'] != "buildfail"):
        output.update({'netlist':'/netlist/' + submissionId})
    return json.dumps(output)

@app.route('/netlist/<subId>')
def generateNetlist(subId):
  # and the submission exists
  wdir = app.config['WORKDIR'] + '/' + get_user(session) + '/' + subId + '/'
  sub_metapath = wdir + 'metadata.json'
  if not os.path.isfile(sub_metapath):
    return "Submission {} not found".format(subId), 404

  # and the submission built successfully
  metadata = json.load(open(sub_metapath))
  if metadata['status'] == 'buildfail':
    return "Netlist not available because synthesis failed", 404

  # then try to generate the netlist!
  try:
    output = run_netlist(wdir)
    print(output)
    headers = {'Content-Type':'image/svg+xml'}
    return (readfile(wdir + "netlist.svg"), headers)
  except Exception as e:
    current_app.logger.error("netlist generation error with wdir=" + wdir + " :\n" + output + '\n\n' + str(e))
    return "Error generating netlist: " + str(e), 500

# https://stackoverflow.com/a/29516120
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
