###########################################################################
#This file is meant to contain functions that deal with embeddings        #
###########################################################################
import requests
import os
from dotenv import load_dotenv
import json
from openai import OpenAI
import pandas as pd

load_dotenv()

client     = OpenAI(
    api_key= os.environ["OPENAI_KEY"],
)

def get_embeddings(string : str, model = "text-embedding-3-small", save_to_file = None):
    '''
    This function tries to send a post request to OpenAI to make embeddings of a given string.

    Arguments:
    string      :        the string send to OpenAI
    model       :        (Optional) choose the model
    save_to_file:        (Optional) save the full statement from OpenAI to given file

    returns     :        the embeddings as a list
    '''   
    embeddings = client.embeddings.create(input = [string], model=model)
    if save_to_file:
        with open(save_to_file, mode="w+") as fl:
            fl.write(f'{embeddings}')
    return embeddings.data[0].embedding

def get_embeddings_for_df(df : pd.DataFrame, model="text-embedding-3-small", save=False):
    df["embeddings"] = df["text"].apply(lambda line: get_embeddings(line, model=model))
    if save:
        df.to_csv("Embeddings.csv")

if __name__ == "__main__":
    test = "Hello world!"
    file = "Dump.txt"
    #print(openai_key )
    