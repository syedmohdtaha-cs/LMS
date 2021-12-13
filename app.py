from flask import Flask,flash, render_template,request,redirect, url_for ,make_response
import sqlite3

login=False
app = Flask(__name__)

@app.route('/home2')
def indexq():
    if not request.cookies.get("user"):
        return redirect("/")

    if login==True:
        with sqlite3.connect("library1.db") as con:  
            con.row_factory=sqlite3.Row
            cur = con.cursor()  
            cur.execute("SELECT * FROM Admin")
            rv=cur.fetchall()

            return render_template('index.html',rv=rv,name=request.cookies.get("user"))
    else:
        return "<h1>Error</h1>"

@app.route('/', methods=['GET', 'POST'])
def index():
    global login
    if request.method == "POST":
        name = request.form["Username"]  
        pswd = request.form["password"]             
        with sqlite3.connect("library1.db") as con:  
            cur = con.cursor()  
            if name=="admin" and pswd=="admin":
                
                login=True
                return redirect(url_for('admin')) 
            else:
                cur.execute("SELECT * from Students where name=? AND pswd=? ",(name,pswd))
                if cur.fetchall(): 
                    login=True
                    resp = make_response(redirect(url_for('indexq')))
                    resp.set_cookie("user",name)
                    return resp
                else:
                    error = "Invalid Credentials"
                    return render_template('login.html',error=error) 
            con.commit() 
            con.close()
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/registerd', methods=['GET', 'POST'])
def registerd():
    msg = "msg" 
    if request.method == "POST": 
        name = request.form["name"]  
        pswd = request.form["password"]  
        with sqlite3.connect("library1.db") as con:  
            cur = con.cursor()  
            cur.execute("INSERT into Students(name, pswd) values (?,?)",(name,pswd))  
            con.commit()  
        return redirect('/')  
          
@app.route('/admin')
def admin():   
    return render_template('admin.html') 
   



@app.route('/submit', methods=['POST'])
def submitbook():

    name=request.form['exampleInputName']
    author=request.form['exampleInputAuthor']
    category=request.form['exampleInputCategory']
    url=request.form['exampleInputURL']
    count=request.form['exampleInputCount']
    with sqlite3.connect("library1.db") as con:  
        cur = con.cursor()  
        cur.execute("SELECT book_name,Count FROM Admin where book_name=?",(name,))
        rr = cur.fetchall()
        if len(rr):
            cur.execute("UPDATE Admin SET Count=? where book_name=?",(int(count)+int(rr[0][1]),name,))
        else:
            cur.execute("INSERT into Admin(book_name,Author_name,Category,url,Count) values (?,?,?,?,?)",(name, author, category,url,int(count)))  
        con.commit()
    return redirect('/home2')



@app.route('/category', methods=['POST'])  
def categ():

    category=request.form['exampley']
    with sqlite3.connect("library1.db") as con:  
        con.row_factory=sqlite3.Row
        cur = con.cursor()  
        cur.execute("SELECT * from Admin where Category = ? ",(category,))  
        rv=cur.fetchall()
        return render_template('index.html',rv=rv)



@app.route('/issue',methods=["POST"])
def issue():

    book = []
    student = []
    name = request.cookies.get("user")
    id = request.form['id']



    with sqlite3.connect("library1.db") as con:
        cur = con.cursor()
        cur.execute("Select * from Admin where book_id=?",(id,))
        r = cur.fetchall()
        book = r[0]

    with sqlite3.connect("library1.db") as con:
        cur = con.cursor()
        cur.execute("Select * from Students where name=?",(name,))
        r = cur.fetchall()
        student = r[0][0]

    with sqlite3.connect("library1.db") as con:  
        cur = con.cursor()  
        if int(book[5])>0:
            cur.execute("INSERT into Record(book_id,book_name,Student_id,Student_name) values (?,?,?,?)",(id,book[1],student,request.cookies.get('user'),))  
            cur.execute("UPDATE Admin SET Count=? where book_name=?",(int(book[5])-1,book[1])) 
            cur.execute("SELECT * FROM Admin")
            rv=cur.fetchall()
            con.commit() 
            return render_template('issued.html')

    return redirect('/home2')
            

if __name__=="__main__":
    app.run(debug=True)

