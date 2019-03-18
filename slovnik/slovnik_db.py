import pymysql.cursors
from distutils import text_file

# Connect to the database
con = pymysql.connect(host='localhost',
                             user='root', #insert login
                             password='dbproject', # insert password
                             db='slovnik',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cur = con.cursor()

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

# Main page
@app.route('/main')
def main_page():
    return render_template('main.html')

#Data by language
@app.route('/results')
def by_language():
    n = ''
    if request.args:
        query = request.args['search_form']
        lemmas = query.split(' ')
        if request.args['logic']=='and':
            for i in range(0, len(lemmas)-1):           
                n += lemmas[i] + ' %" and lemmas like "% '
        else:
            for i in range(0, len(lemmas)-1):           
                n += lemmas[i] + ' %" or lemmas like "% '
        n += lemmas[len(lemmas)-1]
        cur.execute('select lexemes.lex, definitions.def \
        from definitions \
        join lexemes on lexemes.lex_id=definitions.lex_id \
        where definitions.lemmas like "% ' + n + ' %"')
        res = cur.fetchall()
        if res==():
            res=0
        
    return render_template('results.html', res=res, n=n, lemmas=lemmas)


if __name__ == '__main__':
    app.run(debug=True)

con.close()
