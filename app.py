from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)

# Load the data
with open("HS model.pkl", "rb") as f:
    data = pickle.load(f)


def recommend_assets(elevation, threat, region):
    rec = []
    if threat == "High":
        if elevation > 4000:
            rec += ["HAL Prachand", "HAL Dhruv (High Altitude)", "Su-30MKI"]
        elif elevation > 2000:
            rec += ["HAL Rudra", "Mi-17 V5", "Tejas Mk1A"]
        else:
            rec += ["Apache AH-64E", "Tejas Mk1A", "Jaguar"]
    elif threat == "Medium":
        if elevation > 4000:
            rec += ["HAL Dhruv (High Altitude)"]
        elif elevation > 2000:
            rec += ["HAL Rudra"]
        else:
            rec += ["ALH Dhruv"]

    if "Andaman" in region or "INS" in region:
        rec += ["MH-60R Seahawk", "MiG-29K", "Tejas Naval"]
    return list(set(rec))


@app.route("/")
def index():
    return render_template("index.html", locations=list(data.keys()))


@app.route("/recommend", methods=["POST"])
def recommend():
    location = request.json.get("location")
    if location in data:
        elevation, threat, region = data[location]
        assets = recommend_assets(elevation, threat, region)
        return jsonify({
            "location": location,
            "threat": threat,
            "recommendations": assets
        })
    return jsonify({"error": "Invalid location"}), 400


if __name__ == "__main__":
    app.run(debug=True)