from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import session
import csv
import json
import subprocess

app = Flask(__name__)
app.secret_key = "1234567"

@app.route('/')
def root():

   with open('category.txt') as f:
        # init dataset
        categories = f.read().split('\n')
        #print(categories[-4:-1])
   with open('states.txt') as f:
       states = f.read().split('\n')
       #print(states[-4:-1])     

   

   return render_template('home.html', categories = categories[-4:-1], states = states[-4:-1] )
  
  
@app.route('/home', methods = ['POST', 'GET'])  
def home():
    if request.method == "POST": 
      category = request.form.get('category')
      state = request.form.get('states')
     
      if (category == '') and  (state == ''):
        print('\nfailed for both field\n')
        return 'failed'
        
      elif  (category == '') or  (state == ''):
           print('\nfailed for single field\n')
           return 'filed'
        
      else:
          categories = ''
           
          with open('category.json', 'r') as f:
             for line in f.read():
                 categories +=line
          categories = json.loads(categories)
             
          categories['category'] = category 
          print(categories)
          with open('category.json', 'w') as f:
              f.write(json.dumps(categories, indent=4))
              
          states2 = ''
           
          with open('states.json', 'r') as f:
             for line in f.read():
                 states2 +=line
          states2 = json.loads(states2)
             
          states2['state'] = state    
          print('\n',states2)
          with open('states.json', 'w') as f:
              f.write(json.dumps(states2, indent=4))   
              
              
          process =  subprocess.Popen('python3 yelp.py ', shell = True)
          process.wait()
          return 'ok'
      return 'seccess'

  
if __name__ ==  '__main__':  
    app.run(debug = True, threaded = True)  
