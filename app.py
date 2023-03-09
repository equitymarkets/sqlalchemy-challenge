from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii <<<<< climate app.</br>"
        f"Choose a route:</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/</br>"
        #f"/api/v1.0/<start>/<end></br>"

    )

@app.route("/api/v1.0/precipitation")

def precip():
    return(f"precipitation")

@app.route("/api/v1.0/stations")
def stations():
    return(f"This is the stations app")

@app.route("/api/v1.0/tobs")
def temps():
    return(f"This is the temmpurature app")

@app.route("/api/v1.0/<start>")
def query_from_start():
    return(f"query app from start")

@app.route("/api/v1.0/<start>/<end>")
def query_start_to_end():
    return(f"query app from start to finish")

if __name__ == "__main__":
    app.run(debug=True)
