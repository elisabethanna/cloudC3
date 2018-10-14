from flask import Flask, jsonify
from tasks import countPronoun

app = Flask(__name__)

@app.route('/countPronouns', methods=['GET'])
def main():
    pronoun = countPronoun.delay()

    return(jsonify(pronoun.get()))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

