# Search_movie_quotes
The dataset of quotes (data.json) from https://github.com/NikhilNamal17/popular-movie-quotes/tree/master

## Before using  Snowflake_tools.py
create the following worksheet in snowflake, and run it:

```SQL

CREATE WAREHOUSE {warehouse_name} WITH WAREHOUSE_SIZE={warehouse_size};{Database}.{SCHEMA}.EMBEDDINGS

CREATE TABLE search(embd varchar);

CREATE or REPLACE FUNCTION cosine_similarity(x VARCHAR,y VARCHAR)
    RETURNS FLOAT
    LANGUAGE PYTHON
        runtime_version=3.8
    handler = 'cosine_similarity_py'
    AS
    $$
def str_to_float_list(string : str):
    ls = string.strip("[]").split(",")
    ls = list(map(lambda itm: float(itm),ls))
    return ls

def dot_product(itm1, itm2):
    combined = zip(itm1,itm2)
    ls = [f1*f2 for f1,f2 in combined]
    return sum(ls)

def magnitude(itm):
    return sum([i**2 for i in itm])**0.5

def cosine_similarity_py(x,y):
    ls_x = str_to_float_list(x)
    ls_y = str_to_float_list(y)
    m_x  = magnitude(ls_x)
    m_y  = magnitude(ls_y)
    if m_x*m_y==0:
        return 0
    return dot_product(ls_x,ls_y)/(m_x*m_y)
    
    $$;
    
```
After creating the worksheet, run it. This should create a warehouse, an empty table called SEARCH, and the udf cosine_similarity. When finished with this step you should be able to use Snowflake_tools.py.
