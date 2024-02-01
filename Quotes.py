################################################################################################
#The main of this file creates the embeddings.csv                                              #
#Running this file may take a few minutes                                                      #
################################################################################################

import pandas as pd
import Embeddings

quotes_df = pd.read_json("data.json")


if __name__=="__main__":
    Embeddings.get_embeddings_for_df(df=quotes_df,save_to_file="embeddings.csv")
