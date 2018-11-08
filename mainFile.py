from flask import Flask,render_template,request,flash,redirect,url_for,session
from Databases import User,Patient
from flask_bcrypt import generate_password_hash,check_password_hash

app = Flask(__name__)
app.secret_key = "bnvsdnvsfvdvkvnjvdvdkbvdsc"

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    user = Patient.get(Patient.id==id)
    if request.method == "POST":
        names = request.form["names"]
        age = request.form["age"]
        weight = request.form["weight"]
        user.names = names
        user.age = age
        user.weight = weight
        user.save()
        flash("User Updated Successfully")
        return redirect(url_for('show'))
    return render_template("update.html",user = user)


@app.route('/delete/<int:id>')
def delete(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    owner_id = session['id']
    Patient.delete().where(Patient.id == id).execute()
    flash("Details Deleted Successfully")
    return redirect(url_for('show'))


@app.route('/show')
def show():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    users = Patient.select()
    return render_template('show.html',users = users)


@app.route('/',methods=['GET','POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == "POST":
        names = request.form["names"]
        age = request.form["age"]
        weight = request.form["weight"]
        id = session['id']
        Patient.create(owner = id,names = names, age = age, weight = weight)
        flash("User Saved Successfully")
        flash("User "+names)
    return render_template("patientRecord.html")


@app.route('/reg',methods=['GET','POST'])
def register():
    if request.method == "POST":
        sname = request.form["sName"]
        fname = request.form["fName"]
        lname = request.form["lName"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["pwd"]
        password = generate_password_hash(password)
        User.create(sname = sname,fname=fname,lname = lname, email = email,phone = phone, password = password)
        flash("Account Created Successfully")
    return render_template("signUp.html")


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = User.get(User.email==email)
            hashed_password = user.password
            if check_password_hash(hashed_password,password):
                flash("Logged in Successfully")
                session['logged_in']=True
                session['names']=user.names
                session['id']=user.id
                return redirect(url_for('show'))
        except User.DoesNotExist:
            flash("Wrong Username or Password")
    return render_template("Homepage.html")


if __name__ == '__main__':
    app.run()