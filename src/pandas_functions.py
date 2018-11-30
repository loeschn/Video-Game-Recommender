import pandas as import pd

def clean_df(df):
    """Dropping columns to avoid games that are very similar:
    Category = 1 = DLC/Add-On
    Category = 2 = Expansion
    Category = 3 = Bundle
    Dropping any game that has a parent version:
    i.e. Overwatch Legendary Edition vs just plain Overwatch"""
    df = df.drop(df[df.category == 3].index)
    df = df.drop(df[df.category==2].index)
    df = df.drop(df[df.category==1].index)
    df = (df[df.version_parent.isnull()])

    return df
