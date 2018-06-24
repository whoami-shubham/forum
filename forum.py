from flask import Flask, render_template, url_for, request, redirect,session,escape
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from forum_setup import User, Post, Comment,Base

engine = create_engine('sqlite:///forum.db', pool_pre_ping=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)


app = Flask(__name__)

@app.route('/',methods =['POST','GET'])
@app.route('/index',methods =['POST','GET'])
def Index():
    if 'email' in session:
        sess = DBSession()
        posts = sess.query(Post).all()
        return render_template('forum.html',posts=posts)
    return redirect(url_for('login'))

@app.route('/viewpost/<int:post_id>/',methods =['POST','GET'])
def Viewpost(post_id):
    if 'email' in session:
        sess = DBSession()
        post = sess.query(Post).filter_by(id=post_id).first()
        comm = sess.query(Comment).filter_by(post_id=post_id).all()
        cur_usr=escape(session['username'])
        return render_template('viewpost.html',post=post,comm=comm,cur_usr=cur_usr)
    return redirect(url_for('login'))

@app.route('/newthread',methods =['POST','GET'])
def Newthread():
    if 'email' in session:
        sess = DBSession()
        if request.method=='POST':
            t = request.form['title']
            c = request.form['content']
            u = escape(session['email'])
            n = escape(session['username'])
            if sess.query(Post).filter_by(title=t).first():
                return 'can not create thread change title and try again.'
            p = Post(title=t,content=c,user_id=u,user_name=n)
            sess.add(p)
            sess.commit()
            return redirect(url_for('Index'))
        return render_template('newthread.html')
    return redirect(url_for('login'))

            
@app.route('/login', methods=['GET', 'POST'])
def login():
    sess = DBSession()
    if request.method == 'POST':
        u=sess.query(User).filter_by(email=request.form['email']).first()
        if u:
            session['email'] = request.form['email']
            session['username'] = u.username
            return redirect(url_for('Index'))
        err1 = 1
        return render_template('register.html',err1=err1)
    return render_template('register.html')
@app.route('/register', methods=['POST','GET'])
def register():
    sess =DBSession()
    if request.method=='POST':
        e =sess.query(User).filter_by(email=request.form['email']).first()
        if e:
            err2 = 2
            return render_template('register.html',err2=err2)
        u = sess.query(User).filter_by(username=request.form['username']).first()
        if u:
            err3 = 3
            return render_template('register.html',err3=err3)
        n = User(username=request.form['username'],email=request.form['email'])
        sess.add(n)
        sess.commit()
        log = 1
        return render_template('register.html', log=log)
    return render_template('register.html')
@app.route('/addcomment/<int:post_id>/', methods = ['POST','GET'])
def Addcomment(post_id):
    if 'email' in session:
        sess=DBSession()
        c=request.form['comment']
        if c!='':
            comm = Comment(text=c,post_id=post_id,user_name=escape(session['username']))
            sess.add(comm)
            sess.commit()
            return redirect(url_for('Viewpost',post_id=post_id))
    return redirect(url_for('login'))


@app.route('/editcomment/<int:post_id>/<int:comment_id>/', methods=['POST','GET'])
def editcomment(post_id,comment_id):
    sess = DBSession()
    c = sess.query(Comment).filter_by(id = comment_id).first()
    if 'email' in session:
        if request.method=='POST':
            message = request.form['comment']
            c.text = message
            sess.add(c)
            sess.commit()
            return redirect(url_for('Viewpost',post_id=post_id))
        return render_template('editcomment.html',c=c,post_id=post_id)
    return redirect(url_for('login'))

@app.route('/deletecomment/<int:post_id>/<int:comment_id>/', methods=['POST','GET'])
def deletecomment(post_id,comment_id):
    sess = DBSession()
    c = sess.query(Comment).filter_by(id = comment_id).first()
    if 'email' in session:
        sess.delete(c)
        sess.commit()
        return redirect(url_for('Viewpost',post_id=post_id))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('Index'))
    
    
    
    
if __name__ == '__main__':
    app.secret_key='password'
    app.debug = True
    app.run(host='0.0.0.0', port=5000) 
