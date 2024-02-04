#########################################################################################################
# This file is for the flask app                                                                        #
#########################################################################################################

from flask import Flask, request, render_template
import Embeddings
import Snowflake_tools
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route("/")
def search():
    return render_template("search.html")

@app.route('/search')
def get_search():
    query = request.args.get('query')
    if len(query)<=250:
        results = Snowflake_tools.search_query(query)
    return render_template("results.html", query=query, results=results)

if __name__=="__main__":
    app.run(port = os.getenv("PORT"))
