import json


with open('states.txt', 'r') as f:
  data = f.read().split('\n')
  data = data[-4:-1]
 
  for state in data:
       state = state.dumps(state) 
       with open('states.json', 'a') as f:
         f.write(({ state , indent = 2))
      
