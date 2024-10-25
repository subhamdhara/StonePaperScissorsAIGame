from flask import Flask, render_template, request, redirect, url_for
###WSGI Application
app = Flask(__name__)

# Store submissions locally in a file (text or CSV) or in memory

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    remarks = request.form['remarks']
    
    # Store the data in the list or write it to a file
    # submissions.append({'name': name, 'remarks': remarks})
    
    # You can also store in a file by uncommenting the next two lines
    with open('remarks/submissions.txt', 'a') as f:
        f.write(f"{name}, {remarks}\n")
    print(name, remarks)
    
    return redirect(url_for('index'))

@app.route('/view')
def view():
    submissions = []
    file1 = open("remarks/submissions.txt","r")
    r = file1.readlines()
    for i in r:
        name, remarks = i.split(",")
        submissions.append({'name': name, 'remarks': remarks})
    file1.close()
    return render_template('view.html', submissions=submissions)

if __name__ == '__main__':
    app.run()