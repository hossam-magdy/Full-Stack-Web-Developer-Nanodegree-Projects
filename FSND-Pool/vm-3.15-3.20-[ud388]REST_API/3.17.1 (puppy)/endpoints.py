from flask import Flask, jsonify
app = Flask(__name__) 

@app.route("/puppies")
def puppiesFunction():
  return "Yes, puppies!"
  
 
@app.route("/puppies/<int:id>")
def puppiesFunctionId(id):
  return "This method will act on the puppy with id %s" % id

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)	
