from flask import Flask,render_template,request,flash
from gpt2.src.summary import interact_model
from gpt2.src.qa import question_model
from gpt2.src.genText import genText

app = Flask(__name__)
app.secret_key="12345asbsadfasdf"
app.TEMPLATES_AUTO_RELOAD=True

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

def generate_summary(user_text):
    summary = interact_model(input_for_model=user_text,top_k=40,length=200,temperature=.85)
    return summary

@app.route('/',methods=['GET','POST'])
def index():
    return render_template("index.html")


@app.route('/summary-gen',methods=['GET','POST'])
def summary_gen():
    if request.method == 'POST':
        user_text=request.form['user_text']
        print(user_text)
        summary=generate_summary(user_text=user_text)
        flash(summary,category='success')
        # print(summary)
        return render_template("summary_gen.html")
    return render_template("summary_gen.html")



@app.route("/question-and-answer-gen",methods=['GET','POST'])
def qa_gen():
    if request.method=='POST':
        user_question=request.form['user_text']
        answer=question_model(input_for_model=user_question)
        flash(answer,category='success')
        return render_template('qa.html')
    return render_template('qa.html')

    

@app.route("/gen-text",methods=['GET','POST'])
def text_gen():
    if request.method=='POST':
        user_info=request.form['user_text']
        generation = genText(user_text=user_info,top_k=40,length=200,temperature=.85)
        flash(generation,category='success')
        return render_template('qa.html')
    return render_template('qa.html')