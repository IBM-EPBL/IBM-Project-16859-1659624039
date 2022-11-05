from flask import Flask,render_template,request
app=Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login',methods=["POST"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        email=request.form["xy"]
        number=request.form["ab"]
        return render_template("index.html",y=user,z=email,n=number)


if __name__=="__main__":
    app.run()
