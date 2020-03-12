from flask import Flask, render_template

app = Flask(__name__)

@app.route('/callback')
def complete():
    return "Complete!"

if __name__ == '__main__':
    app.run(debug=True)