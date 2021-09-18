from flask import Flask, render_template, request, session, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_mail import Mail
import json
import os
import random
from datetime import date

with open('config.json') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.secret_key = "super-secret-key"
app.config['cv_path'] = params['cv_path']
app.config['dp_path'] = params['dp_path']
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT="465",
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['email'],
    MAIL_PASSWORD=params['password']
)
mail = Mail(app)

db = SQLAlchemy(app)


def get_password(n):
    s = "qwertyupkjhgfdsazxcvbnmQWERTYUPLKJHGFDSAZXCVBNM23456789"
    str = ''
    for i in range(0, n):
        a = random.randint(0, len(s))
        str += s[a]
    return str


def initials(s):
    str = s.split()
    ns = ""

    # traverse in the list
    for i in range(len(str) - 1):
        s = str[i]

        # adds the capital first character
        ns += (s[0].upper() + '. ')

    ns += str[-1].title()

    return ns


class Feedback(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    email_id = db.Column(db.String(50), unique=False, nullable=False)
    contact_no = db.Column(db.String(15), unique=False, nullable=False)
    feedback = db.Column(db.String(500), unique=False, nullable=False)
    dof = db.Column(db.String(50), unique=False, nullable=True, default=datetime.now())
    status = db.Column(db.String(1), unique=False, nullable=False, default='N')


class Enquiry(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    email_id = db.Column(db.String(50), unique=False, nullable=False)
    gender = db.Column(db.CHAR(1), unique=False, nullable=False)
    contact_no = db.Column(db.String(15), unique=False, nullable=False)
    enquiry = db.Column(db.String(500), unique=False, nullable=False)
    city = db.Column(db.String(50), unique=False, nullable=False)
    doe = db.Column(db.String(50), unique=False, nullable=True, default=datetime.now())
    status = db.Column(db.String(1), unique=False, nullable=False, default='N')


class Career(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    email_id = db.Column(db.String(50), unique=False, nullable=False)
    contact_no = db.Column(db.String(15), unique=False, nullable=False)
    gender = db.Column(db.CHAR(1), unique=False, nullable=False)
    address = db.Column(db.String(500), unique=False, nullable=False)
    doc = db.Column(db.String(15), unique=False, nullable=True, default=datetime.now())
    cv_file = db.Column(db.String(50), unique=False, nullable=True)
    status = db.Column(db.CHAR(1), unique=False, nullable=False, default='N')


class Application(db.Model):
    mid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    father_name = db.Column(db.String(40), unique=False, nullable=False)
    email_id = db.Column(db.String(50), unique=False, nullable=False)
    contact_no = db.Column(db.String(15), unique=False, nullable=False)
    gender = db.Column(db.CHAR(1), unique=False, nullable=False)
    address = db.Column(db.String(500), unique=False, nullable=False)
    dob = db.Column(db.String(50), unique=False, nullable=True)
    course_code = db.Column(db.String(20), unique=False, nullable=False)
    bank_name = db.Column(db.String(100), unique=False, nullable=False)
    ddno = db.Column(db.String(8), unique=False, nullable=True)
    doj = db.Column(db.String(15), unique=False, nullable=True, default=datetime.now())


class Member(db.Model):
    mid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    father_name = db.Column(db.String(40), unique=False, nullable=False)
    email_id = db.Column(db.String(50), unique=False, nullable=False)
    contact_no = db.Column(db.String(15), unique=False, nullable=False)
    gender = db.Column(db.CHAR(1), unique=False, nullable=False)
    address = db.Column(db.String(500), unique=False, nullable=False)
    dob = db.Column(db.String(50), unique=False, nullable=True)
    course_code = db.Column(db.String(20), unique=False, nullable=False)
    status = db.Column(db.String(10), unique=False, nullable=False, default='Active')
    image = db.Column(db.String(20), unique=False, nullable=False)


class MemCourseDetail(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    mid = db.Column(db.Integer, nullable=False)
    course_code = db.Column(db.CHAR(20), unique=False, nullable=False)
    modules = db.Column(db.CHAR(200), unique=False, nullable=False)
    duration = db.Column(db.CHAR(15), unique=False, nullable=False)
    course_fees = db.Column(db.CHAR(8), unique=False, nullable=False)
    doa = db.Column(db.String(15), unique=False, nullable=True, default=datetime.today().strftime("%Y/%m/%d"))
    bank_name = db.Column(db.CHAR(100), unique=False, nullable=False)
    ddno = db.Column(db.CHAR(8), unique=False, nullable=True)


class Courses(db.Model):
    course_code = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    course_name = db.Column(db.String(100), unique=True, nullable=False)
    duration = db.Column(db.String(10), unique=False, nullable=False)
    fees = db.Column(db.String(7), unique=False, nullable=False)
    module = db.Column(db.CHAR(200), unique=False, nullable=False)
    career = db.Column(db.String(500), unique=False, nullable=False)


class Login(db.Model):
    mid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    profile = db.Column(db.String(10), unique=False, nullable=False)


class Question(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=False, nullable=False)
    question = db.Column(db.String(500), unique=False, nullable=False)
    option1 = db.Column(db.String(100), unique=False, nullable=False)
    option2 = db.Column(db.String(100), unique=False, nullable=False)
    option3 = db.Column(db.String(100), unique=False, nullable=False)
    option4 = db.Column(db.String(100), unique=False, nullable=False)
    answer = db.Column(db.String(1), unique=False, nullable=False)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mid = db.Column(db.Integer, nullable=False)
    correct_answer = db.Column(db.CHAR(2), unique=False, nullable=False)
    wrong_answer = db.Column(db.CHAR(2), unique=False, nullable=False)
    unanswered = db.Column(db.CHAR(2), unique=False, nullable=False)
    total_marks = db.Column(db.CHAR(2), unique=False, nullable=False)
    percentage = db.Column(db.CHAR(6), unique=False, nullable=False)
    grade = db.Column(db.CHAR(1), unique=False, nullable=False)
    result = db.Column(db.CHAR(4), unique=False, nullable=False)
    cid = db.Column(db.CHAR(20), unique=False, nullable=False)
    doe = db.Column(db.String(15), unique=False, nullable=True, default=datetime.today().strftime("%Y/%m/%d"))


@app.route('/')
def index():
    li = ['1']
    pid = '0'
    course = Courses.query.all()
    return render_template('index.html', li=li, course=course, pid=pid)


@app.route('/about')
def about():
    li = ['2']
    return render_template('aboutus.html', li=li)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    msg = ''
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        cno = request.form.get('cno')
        fb = request.form.get('fb')
        sql = Feedback(name=name, email_id=email, contact_no=cno, feedback=fb)
        db.session.add(sql)
        db.session.commit()
        mail.send_message('Message from ' + "eLearning",
                          sender=params['email'],
                          recipients=[email],
                          body="Hello " + name + "\nYour details are received. We contact you soon ")
        msg = 'Your Details saved Successfully'
    li = ['3', msg]
    return render_template('contactus.html', li=li)
    # return render_template('contactus.html')


@app.route('/enquiry', methods=['GET', 'POST'])
def enquiry():
    msg = ""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        cno = request.form.get('cno')
        enq = request.form.get('enq')
        gen = request.form.get('gen')
        city = request.form.get('city')

        entry = Enquiry(name=name, email_id=email, gender=gen, contact_no=cno, enquiry=enq, city=city)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('Message from ' + "eLearning",
                          sender=params['email'],
                          recipients=[email],
                          body="Hello " + name + "\nYour details are received. We contact you soon ")
        msg = 'Your Details saved Successfully'
    li = ['4', msg]
    return render_template('enquiry.html', li=li)


@app.route('/career', methods=['GET', 'POST'])
def career():
    name = ""
    email = ""
    cno = ""
    gen = ""
    add = ""
    msg = ""
    if request.method == 'POST':
        msg = 'Your Career Details saves Successfully'
        name = request.form.get('name')
        email = request.form.get('email')
        cno = request.form.get('cno')
        add = request.form.get('add')
        gen = request.form.get('gen')
        uploaded_file = request.files['cv']
        filename = secure_filename(uploaded_file.filename)
        ext = os.path.splitext(filename)[1]
        # cv_file = file.filename
        # ext = cv_file[cv_file.rfind(".")+1:]
        if ext == ".pdf" or ext == ".doc" or ext == ".docx":
            # search by email
            data = Career.query.filter_by(email_id=email).first()

            # all in the search box will return all the tuples
            if not data:

                data = Career.query.order_by(Career.sno.desc()).first()
                if not data:
                    fname = secure_filename("1" + ext)
                    sno = 1
                else:
                    fname = secure_filename(str(int(data.sno) + 1) + ext)
                    sno = int(data.sno) + 1
                entry = Career(sno=sno, name=name, email_id=email, contact_no=cno, gender=gen, address=add,
                               cv_file=fname)
                db.session.add(entry)
                db.session.commit()

                uploaded_file.save(os.path.join(app.config['cv_path'], fname))
                mail.send_message('Message from ' + "eLearning",
                                  sender=params['email'],
                                  recipients=[email],
                                  body="Hello " + name + "\nYour details are received. We contact you soon ")
                name = ""
                email = ""
                cno = ""
                gen = ""
                add = ""
                msg = "Career Detail Successfully Saved"
            else:
                msg = 'Email-Id already exist'


        else:
            msg = "Please upload a valid CV File"

    li = ['6', name, email, cno, gen, add, msg]
    return render_template('career.html', li=li)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    uid = ''
    name = ''
    fname = ''
    email = ''
    cno = ''
    add = ''
    ddno = ''
    bname = ''
    dob = ''
    gen = ''
    ccode = 'Select Course Code'
    pid = '0'
    if request.method == 'POST' and 'RegSubmit' in request.form:

        name = request.form.get('name')
        fname = request.form.get('fname')
        email = request.form.get('email')
        cno = request.form.get('contact')
        gen = request.form.get('gen')
        add = request.form.get('address')
        dob = request.form.get('dob')
        ccode = request.form.get('ccode')
        bname = request.form.get('bname')
        ddno = request.form.get('ddno')

        find = Member.query.filter_by(email_id=email).first()
        flag = 1
        if find:
            flag = 0
            msg = "Email already registered"
            pid = '7'
        else:
            entry = Application(name=name, father_name=fname, email_id=email, contact_no=cno, gender=gen,
                                address=add, dob=dob, course_code=ccode, bank_name=bname, ddno=ddno)
            db.session.add(entry)
            db.session.commit()
            mail.send_message('Message from ' + 'eLearning',
                              sender=params['email'],
                              recipients=[email],
                              body="Hello " + name + "\nYour details are received. We contact you soon ")
            msg = "Details saved Successfully, Contact you soon"

    elif request.method == 'POST' and 'btnLogin' in request.form:
        pid = '8'
        uid = request.form.get('userid')
        password = request.form.get('password')
        data = Login.query.filter_by(user_id=uid).first()
        if data:
            rs = Member.query.filter_by(email_id=uid).first()
            if rs.status == 'Inactive':
                msg = "Your Id is deactivated. Contact Admin"
            elif rs.status == 'Process':
                msg = "Your Application is Under Process. Contact Admin"
            else:
                if data.password == password:
                    profile = data.profile
                    session["uid"] = uid
                    if profile == 'A':
                        session["profile"] = "Admin"
                    else:
                        session["profile"] = "Student"
                    session['mid'] = data.mid
                    session['img'] = rs.image

                    session['uname'] = rs.name.title()
                    session['sn'] = initials(rs.name.title())
                    session['cno'] = rs.contact_no
                    session['course_code'] = rs.course_code
                    if rs.gender == 'M':
                        session['gen'] = 'Male'
                    else:
                        session['gen'] = 'Female'
                    pid = '0'
                    if profile == "A":
                        return redirect("/admin_index/0")
                    else:
                        return redirect("/member_index/0")
                else:
                    msg = "Invalid Password try again"

        else:
            msg = "Invalid User Id try again"
    course = Courses.query.all()
    li = [pid, name, fname, email, cno, gen, add, dob, ccode, bname, ddno, msg, uid]
    return render_template('index.html', params=params, li=li, course=course, pid=pid)


############## Start of Admin #################


@app.route('/admin_index/<string:cmd>', methods=["GET", "POST"])
def admin_index(cmd):
    if 'uid' in session:
        uid = session['uid']
        msg = ''
        if request.method == 'POST':
            name = request.form.get('name')
            fname = request.form.get('fname')
            cno = request.form.get('cno')
            gen = request.form.get('gen')
            add = request.form.get('add')
            dob = request.form.get('dob')
            uploaded_file = request.files['img']

            filename = secure_filename(uploaded_file.filename)
            ext = os.path.splitext(filename)[1]
            flag = 1
            if ext != '':
                if ext == ".jpg" or ext == ".png" or ext == ".gif" or ext == 'jpeg':
                    flag = 1
                else:
                    flag = 0
                    msg = 'Please upload a valid profile image'
            if flag == 1:
                data = Member.query.filter_by(email_id=uid).first()
                filename = secure_filename(str(int(data.mid)) + ext)

                data.name = name
                data.father_name = fname
                data.contact_no = cno
                data.gender = gen
                data.address = add
                data.dob = dob
                data.image = filename
                uploaded_file.save(os.path.join(app.config['dp_path'], filename))
                db.session.commit()
                return redirect('/admin_index/0')

        data = Member.query.filter_by(email_id=uid).first()

        li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
              session['course_code'], cmd, msg]
        return render_template('user/admin/profile.html', li=li, params=params, data=data)
    else:
        li = ['1']
        pid = '0'
        course = Courses.query.all()
        return render_template('index.html', li=li, course=course, pid=pid, params=params)


@app.route('/admin_course/<string:code>,<string:cmd>', methods=["GET", "POST"])
def admin_course(code, cmd):
    if 'uid' in session:
        msg = ""
        cc = ""
        cn = ""
        cd = "Select Duration"
        cf = ""
        cm = ""
        car = ""

        if request.method == 'POST':
            cc = request.form.get('ccode').upper()
            cn = request.form.get('cname').upper()
            cd = request.form.get('duration')
            cf = request.form.get('cfee')
            cm = request.form.get('modules').upper()
            car = request.form.get('car').upper()
            if cmd == '1':
                find = Courses.query.filter_by(course_code=cc).first()
                if find:
                    msg = "Course Code already exist"
                else:
                    find = Courses.query.filter_by(course_name=cn).first()
                    if find:
                        msg = "Course Name already exist"
                    else:
                        data = Courses(course_code=cc, course_name=cn, duration=cd, fees=cf, module=cm,
                                       career=car)
                        db.session.add(data)
                        db.session.commit()
                        cc = ""
                        cn = ""
                        cd = "Select Duration"
                        cf = ""
                        cm = ""
                        car = ""
                        msg = "Course Added Successfully"
            elif cmd == '2':
                flag = 1
                if session['cc'] != cc:
                    find = Courses.query.filter_by(course_code=cc).first()
                    if find:
                        flag = 0
                        msg = "Course Code already exist"
                elif session['cn'] != cn:
                    find = Courses.query.filter_by(course_name=cn).first()
                    if find:
                        flag = 0
                        msg = "Course Name already exist"
                if flag == 1:
                    data = Courses.query.filter_by(course_code=code).first()
                    data.course_code = cc
                    data.course_name = cn
                    data.duration = cd
                    data.fees = cf
                    data.module = cm
                    data.career = car
                    db.session.commit()
                    session.pop("cc")
                    session.pop("cn")
                    cmd = '0'
            elif cmd == '3':
                data = Courses.query.filter_by(course_code=code).first()
                db.session.delete(data)
                db.session.commit()
                session.pop("cc")
                session.pop("cn")
                cmd = '0'
        elif cmd == '2' or cmd == '3' or cmd == '4':
            course = Courses.query.filter_by(course_code=code).first()
            cc = course.course_code
            cn = course.course_name
            cd = course.duration
            cf = course.fees
            cm = course.module
            car = course.career
            session['cc'] = cc
            session['cn'] = cn
        li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
              session['course_code'], msg, code, cmd, cc, cn, cd, cf, cm, car]
        course = Courses.query.all()
        return render_template('user/admin/course.html', li=li, params=params, course=course)
    else:
        li = ['1']
        pid = '0'
        course = Courses.query.all()
        return render_template('index.html', li=li, course=course, pid=pid, params=params)


@app.route('/admin_application/<string:sno>', methods=["GET", "POST"])
def admin_application(sno):
    msg = ''
    name = ''
    father_name = ''
    email_id = ''
    contact_no = ''
    gender = ''
    address = ''
    dob = ''
    course_code = ''
    bank_name = ''
    ddno = ''
    if 'uid' in session:
        if request.method == 'POST' and 'Verify' in request.form:
            print(sno)
            data = Application.query.filter_by(mid=sno).first()
            print(data.email_id)
            mem = Member.query.filter_by(email_id=data.email_id).first()
            if not mem:
                login = Login.query.order_by(Login.mid.desc()).first()
                if not data:
                    sn = 1
                else:
                    sn = int(login.mid) + 1
                upass = get_password(6)

                if data.gender == 'M':
                    img = 'male.jpg'
                else:
                    img = 'female.jpg'
                entry = Login(mid=sn, user_id=data.email_id, password=upass, profile='S')
                db.session.add(entry)
                db.session.commit()
                entry = Member(mid=sn, name=data.name, father_name=data.father_name, email_id=data.email_id,
                               contact_no=data.contact_no, gender=data.gender, address=data.address, dob=data.dob,
                               course_code=data.course_code, image=img)
                db.session.add(entry)
                db.session.commit()
                mail.send_message('Message from ' + 'eLearning',
                                  sender=params['email'],
                                  recipients=[data.email_id],
                                  body="Hello " + data.name + "\nYour User Id is : " + data.email_id +
                                       "\nYour Password is : " + upass)
            else:
                sn = mem.mid
                mem.course_code += "," + data.course_code
                db.session.commit()
                mail.send_message('Message from ' + 'eLearning',
                                  sender=params['email'],
                                  recipients=[data.email_id],
                                  body="Hello " + data.name + "\nYou successfully enrolled in " +
                                       data.course_code + " Course")
            course = Courses.query.filter_by(course_code=data.course_code).first()
            entry = MemCourseDetail(mid=sn, course_code=data.course_code, modules=course.module,
                                    duration=course.duration, course_fees=course.fees, bank_name=data.bank_name,
                                    ddno=data.ddno)
            db.session.add(entry)
            db.session.commit()
            db.session.delete(data)
            db.session.commit()

            sno = '0'
        elif request.method == 'POST' and 'Delete' in request.form:
            rs = Application.query.filter_by(mid=sno).first()
            db.session.delete(rs)
            db.session.commit()
            sno = '0'
        else:

            if sno != '0':
                data = Application.query.filter_by(mid=sno).first()
                name = data.name
                father_name = data.father_name
                email_id = data.email_id
                contact_no = data.contact_no
                if data.gender == 'M':
                    gender = 'Male'
                else:
                    gender = 'Female'
                address = data.address
                dob = data.dob
                course_code = data.course_code
                bank_name = data.bank_name
                ddno = data.ddno
        # data = Application.query.filter((UserDetails.status == 'Active') & (UserDetails.role != 'ADMIN')).all()
        data = Application.query.all()

        li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
              session['course_code'], sno, name, father_name, contact_no, email_id, gender, address, dob, course_code,
              bank_name, ddno]
        return render_template('user/admin/application.html', params=params, li=li, data=data)
    else:
        li = ['1']
        pid = '0'
        course = Courses.query.all()
        return render_template('index.html', li=li, course=course, pid=pid, params=params)


@app.route('/admin_member/<string:sno>,<string:cmd>', methods=["GET", "POST"])
def admin_member(sno, cmd):
    msg = ''
    name = ''
    father_name = ''
    email_id = ''
    contact_no = ''
    gender = ''
    address = ''
    dob = ''
    course_code = ''
    bank_name = ''
    course_fee = ''
    modules = ''
    duration = ''
    ddno = ''
    if 'uid' in session:
        if request.method == 'POST' and 'Active' in request.form:

            data = Member.query.filter_by(mid=sno).first()
            data.status = 'Active'
            db.session.commit()
            mail.send_message('Message from ' + 'eLearning',
                              sender=params['email'],
                              recipients=[data.email_id],
                              body="Hello " + data.name + "\nYour User Id " + data.email_id +
                                   " deactivated. Please contact Admin ")
            sno = '0'
        elif request.method == 'POST' and 'Inactive' in request.form:
            data = Member.query.filter_by(mid=sno).first()
            data.status = 'Inactive'
            db.session.commit()
            mail.send_message('Message from ' + 'eLearning',
                              sender=params['email'],
                              recipients=[data.email_id],
                              body="Hello " + data.name + "\nYour User Id " + data.email_id + " activated.")
            sno = '0'
        elif request.method == 'POST' and 'Delete' in request.form:
            data = Member.query.filter_by(mid=sno).first()
            db.session.delete(data)
            db.session.commit()
            data = Login.query.filter_by(mid=sno).first()
            db.session.delete(data)
            db.session.commit()
            sno = '0'
            return redirect("/admin_member/0," + cmd)

        if sno == '0':
            if cmd == '1':
                data = Member.query.filter_by(status='Active').all()
            elif cmd == '2':
                data = Member.query.filter_by(status='Inactive').all()

        else:
            data = Member.query.filter_by(mid=sno).first()
            name = data.name
            father_name = data.father_name
            email_id = data.email_id
            contact_no = data.contact_no
            if data.gender == 'M':
                gender = 'Male'
            else:
                gender = 'Female'
            address = data.address
            dob = data.dob
            course_code = data.course_code
            bank_name = data.bank_name
            ddno = data.ddno

        # data = Application.query.filter((UserDetails.status == 'Active') & (UserDetails.role != 'ADMIN')).all()
        # data = Application.query.all()

        li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
              session['course_code'], sno, name, father_name, contact_no, email_id, gender, address, dob, course_code,
              bank_name, ddno, cmd]
        return render_template('user/admin/members.html', params=params, li=li, data=data)
    else:
        li = ['1']
        pid = '0'
        course = Courses.query.all()
        return render_template('index.html', li=li, course=course, pid=pid, params=params)


@app.route('/admin_show/<string:sno>,<string:cmd>', methods=["GET", "POST"])
def admin_show(sno, cmd):
    msg = ''
    name = ''
    email_id = ''
    contact_no = ''
    message = ''
    gender = ''
    dom = ''
    file = ''
    city = ''
    title = ''
    gen = ''
    if 'uid' in session:
        if request.method == 'POST' and (cmd == '5' or cmd == '6' or cmd == '7'):
            name = request.form.get('name')
            email_id = request.form.get('email')
            message = request.form.get('message')
            print(message)
            mail.send_message('Message from ' + 'eLearning',
                              sender=params['email'],
                              recipients=[email_id],
                              body="Hello " + name + "\n" + message)
            if cmd == '5':
                data = Feedback.query.filter_by(sno=sno).first()
                cmd = '1'
            elif cmd == '6':
                data = Enquiry.query.filter_by(sno=sno).first()
                cmd = '2'
            elif cmd == '7':
                data = Career.query.filter_by(sno=sno).first()
                cmd = '3'
            data.status = 'Y'
            db.session.commit()
            return redirect('/admin_show/0,' + cmd)

        elif request.method == 'POST' and 'Delete' in request.form:
            if cmd == '1':
                data = Feedback.query.filter_by(sno=sno).first()
            elif cmd == '2':
                data = Enquiry.query.filter_by(sno=sno).first()
            elif cmd == '3':
                data = Enquiry.query.filter_by(sno=sno).first()
            db.session.delete(data)
            db.session.commit()

            return redirect('/admin_show/0,' + cmd)

        elif request.method == 'POST' and 'Reply' in request.form:
            name = request.form.get('name')
            email_id = request.form.get('email')
            if cmd == '1':
                title = 'Feedback'
                cmd = '5'
            elif cmd == '2':
                title = 'Enquiry'
                cmd = '6'
            else:
                title = 'Career'
                cmd = '7'

            li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
                  session['course_code'], sno, name, message, contact_no, email_id, gender, dom, city, file, cmd, title]
            return render_template('user/admin/show_fec.html', params=params, li=li)
        elif sno != '0':
            if cmd == '1':
                data = Feedback.query.filter_by(sno=sno).first()
                message = data.feedback
                dom = data.dof
                title = 'Feedback'
            elif cmd == '2':
                data = Enquiry.query.filter_by(sno=sno).first()
                message = data.enquiry
                dom = data.doe
                city = data.city
                gen = data.gender
                title = 'Query'
            elif cmd == '3':
                data = Career.query.filter_by(sno=sno).first()
                message = data.address
                dom = data.doc
                file = data.cv_file
                gen = data.gender
                title = 'Address'
            name = data.name
            email_id = data.email_id
            contact_no = data.contact_no
            if gen == 'M':
                gender = 'Male'
            else:
                gender = 'Female'
        else:
            if cmd == '1':
                data = Feedback.query.all()
            elif cmd == '2':
                data = Enquiry.query.all()
            else:
                data = Career.query.all()

        # data = Application.query.filter((UserDetails.status == 'Active') & (UserDetails.role != 'ADMIN')).all()
        # data = Application.query.all()

        li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
              session['course_code'], sno, name, message, contact_no, email_id, gender, dom, city, file, cmd, title]
        return render_template('user/admin/show_fec.html', params=params, li=li, data=data)
    else:
        li = ['1']
        pid = '0'
        course = Courses.query.all()
        return render_template('index.html', li=li, course=course, pid=pid, params=params)


@app.route('/admin_change_password', methods=["GET", "POST"])
def admin_change_password():
    opass = ''
    npass = ''
    msg = ''
    if 'uid' in session:
        if request.method == 'POST':
            opass = request.form.get('opass')
            npass = request.form.get('npass')
            uid = request.session["uid"]
            data = Login.query.filter_by(userid=uid).first()
            if data.password == opass:
                data.password = npass
                db.session.commit()
                msg = "Password Changed Successfully"
                mail.send_message('Message from ' + 'Medicopedia',
                                  sender=params['email'],
                                  recipients=[uid],
                                  body="Your new password is : " + npass)
            else:
                msg = "Invalid Old Password try again"
        li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
              session['course_code'], msg]
        return render_template('user/admin/change_password.html', params=params, li=li)
    else:
        li = ['', '', '1']
        return render_template('index.html', params=params, li=li)


@app.route('/question/<string:ccode>', methods=["GET", "POST"])
def question(ccode):
    if 'uid' in session:
        session['ccode'] = ccode

        return redirect('/admin_question/0,0')
    else:
        li = ['1']
        pid = '0'
        course = Courses.query.all()
        return render_template('index.html', li=li, course=course, pid=pid, params=params)


@app.route('/admin_question/<string:sno>,<string:cmd>', methods=["GET", "POST"])
def admin_question(sno, cmd):
    if 'uid' in session:
        msg = ""
        cc = ""
        ques = ""
        op1 = ""
        op2 = ""
        op3 = ""
        op4 = ""
        ans = ""
        ccode = ''
        cmd = int(cmd)
        if 'ccode' in session:
            ccode = session['ccode']
        if request.method == 'POST':
            cc = session['ccode']
            ques = request.form.get('ques')
            op1 = request.form.get('op1')
            op2 = request.form.get('op2')
            op3 = request.form.get('op3')
            op4 = request.form.get('op4')
            ans = request.form.get('ans')
            if cmd == 1:
                data = Question(course_code=cc, question=ques, option1=op1, option2=op2, option3=op3, option4=op4,
                                answer=ans)
                db.session.add(data)
                db.session.commit()
                cc = ""
                ques = ""
                op1 = ""
                op2 = ""
                op3 = ""
                op4 = ""
                ans = ""
                msg = "Question Added Successfully"
            elif cmd == 2:
                data = Question.query.filter_by(sno=sno).first()
                data.course_code = cc
                data.question = ques
                data.option1 = op1
                data.option2 = op2
                data.option3 = op3
                data.option4 = op4
                data.answer = ans
                db.session.commit()
                sno = '0'
                cmd = 0
            elif cmd == 3:
                data = Question.query.filter_by(sno=sno).first()
                db.session.delete(data)
                db.session.commit()
                sno = '0'
                cmd = 0
        elif cmd >= 2:
            data = Question.query.filter_by(sno=sno).first()
            cc = data.course_code
            ques = data.question
            op1 = data.option1
            op2 = data.option2
            op3 = data.option3
            op4 = data.option4
            ans = data.answer
        print(ccode, cmd, sno)
        cmd = int(cmd)
        li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
              session['course_code'], msg, cc, ques, op1, op2, op3, op4, ans, sno, cmd]

        data = Question.query.filter_by(course_code=ccode).all()
        return render_template('user/admin/question.html', li=li, params=params, data=data)
    else:
        li = ['1']
        pid = '0'
        course = Courses.query.all()
        return render_template('index.html', li=li, course=course, pid=pid, params=params)


@app.route('/admin_logout')
def admin_logout():
    if 'uid' in session:
        session.pop("uid")
        return redirect("/")
    else:
        li = ['1']
        pid = '0'
        course = Courses.query.all()
        return render_template('index.html', li=li, course=course, pid=pid, params=params)


############## End of Admin #################


############## Start of Member #################


@app.route('/member_index/<string:cmd>', methods=["GET", "POST"])
def member_index(cmd):
    if 'ccc' in session:
        session.pop('ccc')
    if 'uid' in session:
        uid = session['uid']
        msg = ''
        if request.method == 'POST':
            name = request.form.get('name')
            fname = request.form.get('fname')
            cno = request.form.get('cno')
            gen = request.form.get('gen')
            add = request.form.get('add')
            dob = request.form.get('dob')
            uploaded_file = request.files['img']

            filename = secure_filename(uploaded_file.filename)
            ext = os.path.splitext(filename)[1]
            flag = 1
            if ext != '':
                if ext == ".jpg" or ext == ".png" or ext == ".gif" or ext == 'jpeg':
                    flag = 1
                else:
                    flag = 0
                    msg = 'Please upload a valid profile image'
            if flag == 1:
                data = Member.query.filter_by(email_id=uid).first()
                filename = secure_filename(str(int(data.mid)) + ext)

                data.name = name
                data.father_name = fname
                data.contact_no = cno
                data.gender = gen
                data.address = add
                data.dob = dob
                data.image = filename
                uploaded_file.save(os.path.join(app.config['dp_path'], filename))
                db.session.commit()
                session['img'] = filename
                return redirect('/member_index/0')

        data = Member.query.filter_by(email_id=uid).first()
        mid = session['mid']
        course = MemCourseDetail.query.filter_by(mid=mid).all()

        li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
              session['course_code'], cmd, msg]
        return render_template('user/member/profile.html', li=li, params=params, data=data, courses=course)
    else:
        li = ['1']
        pid = '0'
        course = Courses.query.all()
        return render_template('index.html', li=li, course=course, pid=pid, params=params)


@app.route('/member_course/<string:code>', methods=["GET", "POST"])
def member_course(code):
    if 'ccc' in session:
        session.pop('ccc')
    if 'uid' in session:
        msg = ""
        cc = ""
        cn = ""
        cd = "Select Duration"
        cf = ""
        cm = ""
        car = ""

        if code != '0':
            course = Courses.query.filter_by(course_code=code).first()
            cc = course.course_code
            cn = course.course_name
            cd = course.duration
            cf = course.fees
            cm = course.module
            car = course.career
            session['cc'] = cc
            session['cn'] = cn
        li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
              session['course_code'], msg, code, cc, cn, cd, cf, cm, car]
        # result = TableName.query.filter(TableName.id.in_([1, 2, 3]))
        mem_cc = session['course_code'].split(',')
        print(mem_cc)
        course = Courses.query.filter(Courses.course_code.in_(mem_cc)).all()
        return render_template('user/member/course.html', li=li, params=params, course=course)
    else:
        li = ['1']
        pid = '0'
        course = Courses.query.all()
        return render_template('index.html', li=li, course=course, pid=pid, params=params)


@app.route('/member_application/<string:sno>', methods=["GET", "POST"])
def member_application(sno):
    msg = ''
    course_code = 'Select Course Code'
    bank_name = ''
    ddno = ''
    if 'ccc' in session:
        session.pop('ccc')
    if 'uid' in session:
        sn = session['mid']
        mem = Member.query.filter_by(mid=sn).first()
        if request.method == 'POST' and 'Save' in request.form:
            ccode = request.form.get('ccode')
            bname = request.form.get('bname')
            ddno = request.form.get('ddno')

            entry = Application(name=mem.name, father_name=mem.father_name, email_id=mem.email_id,
                                contact_no=mem.contact_no, gender=mem.gender,
                                address=mem.address, dob=mem.dob, course_code=ccode, bank_name=bname, ddno=ddno)
            db.session.add(entry)
            db.session.commit()
            mail.send_message('Message from ' + 'eLearning',
                              sender=params['email'],
                              recipients=[mem.email_id],
                              body="Hello " + mem.name + "\nYour details are received. We contact you soon ")
            sno = '0'

        elif request.method == 'POST' and 'Delete' in request.form:
            rs = Application.query.filter_by(mid=sno).first()
            db.session.delete(rs)
            db.session.commit()
            sno = '0'
        elif int(sno) > 0:
            data = Application.query.filter_by(mid=sno).first()
            course_code = data.course_code
            bank_name = data.bank_name
            ddno = data.ddno
        # data = Application.query.filter((UserDetails.status == 'Active') & (UserDetails.role != 'ADMIN')).all()
        data = Application.query.filter_by(email_id=mem.email_id).all()
        # courses = Courses.query.filter_by(course_code  mem.course_code).all()
        # courses = Courses.query.filter((Courses.course_code != mem.course_code)).all()
        mem_cc = session['course_code'].split(',')
        course = Courses.query.filter(Courses.course_code.not_in(mem_cc)).all()
        li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
              session['course_code'], sno, course_code, bank_name, ddno]
        return render_template('user/member/application.html', params=params, li=li, data=data, courses=course)
    else:
        li = ['1']
        pid = '0'
        course = Courses.query.all()
        return render_template('index.html', li=li, course=course, pid=pid, params=params)


@app.route('/member_study/<string:code>', methods=["GET", "POST"])
def member_study(code):
    if 'uid' in session:
        session['ccc'] = code
        li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
              session['course_code'], code]
        return render_template('user/member/studymaterial.html', params=params, li=li)
    else:
        li = ['1']
        pid = '0'
        course = Courses.query.all()
        return render_template('index.html', li=li, course=course, pid=pid, params=params)


@app.route('/member_study_c/<string:pno>', methods=["GET", "POST"])
def member_study_c(pno):
    if 'uid' in session:
        session['ccc'] = 'C'
        if pno == '0':
            page = 'index.html'
        elif pno == '1':
            page = 'c_overview.html'
        elif pno == '2':
            page = 'c_environment_setup.html'
        elif pno == '3':
            page = 'c_program_structure.html'
        elif pno == '4':
            page = 'c_basic_syntax.html'
        elif pno == '5':
            page = 'c_data_types.html'
        elif pno == '6':
            page = 'c_variables.html'
        elif pno == '7':
            page = 'c_constants.html'
        elif pno == '8':
            page = 'c_storage_classes.html'
        elif pno == '9':
            page = 'c_operators.html'
        elif pno == '10':
            page = 'c_decision_making.html'
        elif pno == '11':
            page = 'c_loops.html'
        elif pno == '12':
            page = 'c_functions.html'
        elif pno == '13':
            page = 'c_scope_rules.html'
        elif pno == '14':
            page = 'c_arrays.html'
        elif pno == '15':
            page = 'c_pointers.html'
        elif pno == '16':
            page = 'c_strings.html'
        elif pno == '17':
            page = 'c_structures.html'
        elif pno == '18':
            page = 'c_unions.html'
        li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
              session['course_code']]
        return render_template('user/member/course/c/'+page, params=params, li=li)
    else:
        li = ['1']
        pid = '0'
        course = Courses.query.all()
        return render_template('index.html', li=li, course=course, pid=pid, params=params)


@app.route('/member_study_java/<string:pno>', methods=["GET", "POST"])
def member_study_java(pno):
    if 'uid' in session:
        session['ccc'] = 'Java'
        li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
              session['course_code']]
        return render_template('user/member/course/java/index.html', params=params, li=li, pid=pno)
    else:
        li = ['1']
        pid = '0'
        course = Courses.query.all()
        return render_template('index.html', li=li, course=course, pid=pid, params=params)


@app.route('/member_test', methods=["GET", "POST"])
def member_test():
    if 'uid' in session:
        if request.method == 'POST':
            print(request.form.keys())
            ql = list(request.form.keys())
            questions = Question.query.filter(Question.sno.in_(ql)).all()
            ca = 0
            wa = 0
            ua = 0
            for q in questions:
                if q.answer == request.form.get(str(q.sno)):
                    ca += 1
                elif request.form.get(str(q.sno)) == 'nil':
                    ua += 1
                else:
                    wa += 1
            ua = 10 - (ca + wa)
            print(ca, wa, ua)
            tot = ca - (wa * .25)
            per = tot * 10
            result = "PASS"
            if per >= 90:
                gr = "A"
            elif per >= 85:
                gr = "B"
            elif per >= 60:
                gr = "C"
            elif per >= 50:
                gr = "D"
            else:
                result = "FAIL"
                gr = "Nil";
            res = Result(mid=session['mid'],correct_answer=ca, wrong_answer=wa, unanswered=ua,total_marks=tot,
                         percentage=per, grade=gr, result=result, cid=session['ccc'])
            db.session.add(res)
            db.session.commit()
            li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
                  session['course_code'], ca, wa, ua, tot, per, gr, result, session['ccc'], date.today(), '1']
            session.pop('ccc')
            return render_template('user/member/result.html', params=params, li=li)
        questions = Question.query.filter_by(course_code=session['ccc']).all()
        questions = random.sample(questions, k=10)
        li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
              session['course_code']]
        return render_template('user/member/test.html', params=params, li=li, questions=questions)
    else:
        li = ['1']
        pid = '0'
        course = Courses.query.all()
        return render_template('index.html', li=li, course=course, pid=pid, params=params)


@app.route('/member_result/<string:rid>', methods=["GET", "POST"])
def member_result(rid):
    ca = ''
    wa = ''
    ua = ''
    tot = ''
    per = ''
    result = ''
    doe = ''
    gr = ''
    cid = ''
    if 'uid' in session:
        if rid == '0':
            if 'ccc' in session:
                sql = Result.query.filter((Result.mid == session['mid']) & (Result.cid == session['ccc'])).all()
                session.pop('ccc')
            else:
                sql = Result.query.filter_by(mid=session['mid']).all()
            print(len(sql))
        else:
            sql = Result.query.filter_by(id=rid).first()
            cid = sql.cid
            ca = sql.correct_answer
            wa = sql.wrong_answer
            ua = sql.unanswered
            result = sql.result
            gr = sql.grade
            per = sql.percentage
            doe = sql.doe
            tot = sql.total_marks

    li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
         session['course_code'], ca, wa, ua, tot, per, gr, result, cid, doe, rid]
    return render_template('user/member/result.html', params=params, li=li, data=sql)


@app.route('/member_print/<string:rid>', methods=["GET", "POST"])
def member_print(rid):
    ca = ''
    wa = ''
    ua = ''
    tot = ''
    per = ''
    result = ''
    doe = ''
    gr = ''
    cid = ''
    if 'uid' in session:
        sql = Result.query.filter_by(id=rid).first()
        cid = sql.cid
        ca = sql.correct_answer
        wa = sql.wrong_answer
        ua = sql.unanswered
        result = sql.result
        gr = sql.grade
        per = sql.percentage
        doe = sql.doe
        tot = sql.total_marks

        li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
              session['course_code'], ca, wa, ua, tot, per, gr, result, cid, doe, rid]
        page = render_template('user/member/print_temp.html', params=params, li=li)
        pdfkit.from_file('user/member/print_temp.html', "abc.pdf")
        # pdf = pdfkit.from_string(page, False)
        # response = make_response(pdf)
        # response.headers['content-Type'] = 'application/pdf'
        # response.headers['content-Disposition'] = 'atteched; filenme='+str(session['mid'])+'-'+cid+'.pdf'
        #
        # return response
    # return render_template('user/member/print.html', params=params, li=li)


@app.route('/member_change_password', methods=["GET", "POST"])
def member_change_password():
    opass = ''
    npass = ''
    msg = ''
    if 'uid' in session:
        if request.method == 'POST':
            opass = request.form.get('opass')
            npass = request.form.get('npass')
            uid = request.session["uid"]
            data = Login.query.filter_by(userid=uid).first()
            if data.password == opass:
                data.password = npass
                db.session.commit()
                msg = "Password Changed Successfully"
                mail.send_message('Message from ' + 'Medicopedia',
                                  sender=params['email'],
                                  recipients=[uid],
                                  body="Your new password is : " + npass)
            else:
                msg = "Invalid Old Password try again"
        li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
              session['course_code'], msg]
        return render_template('user/member/change_password.html', params=params, li=li)
    else:
        li = ['', '', '1']
        return render_template('index.html', params=params, li=li)


@app.route('/member_logout')
def member_logout():
    if 'uid' in session:
        session.pop("uid")
        return redirect("/")
    else:
        li = ['1']
        pid = '0'
        course = Courses.query.all()
        return render_template('index.html', li=li, course=course, pid=pid, params=params)

@app.route('/member_video/<string:code>', methods=['GET', 'POST'])
def member_video(code):
    session['code']=code

    li = [session["uid"], session['mid'], session['uname'], session['sn'], session['profile'], session['img'],
          session['course_code']]
    if code=='Java':
        return render_template('user/member/course/java/video.html',li=li)
    elif code=='C':
        return render_template('user/member/course/c/video.html',li=li)



if __name__ == '__main__':
    app.run(debug=True)


