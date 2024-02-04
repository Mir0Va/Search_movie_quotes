#########################################################################################################
# This file is for the flask app                                                                        #
#########################################################################################################

from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import Embeddings
import Snowflake_tools

def to_df(emb_ls):
    '''
    Creates a df from list of embeddings to serve to the data pipline.

    Arguments:
    emb_ls   :    List of embeddings.

    Returns:      pd.DataFrame
    '''
    return pd.DataFrame(data=[[emb_ls]], columns=["EMBD"])

app = Flask(__name__)

@app.route("/")
def search():
    return render_template("search.html")

@app.route('/search')
def get_search():
    query = request.args.get('query')
    if len(query)<=250:
        search_item = to_df(Embeddings.get_embeddings(query))
        results     = Snowflake_tools.do_embedding_search(search_df=search_item)
    return render_template("results.html", query=query, results=results)

if __name__=="__main__":
    app.run()
