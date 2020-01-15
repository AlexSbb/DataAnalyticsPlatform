

def ImportData():
    import numpy as np
    import pandas as pd

    mydata = pd.read_csv("u.csv") 
    #print(mydata.head())

    #print(np.random.randn(6, 2)*10)


    df1 = pd.DataFrame(np.random.randn(6, 2)*10, columns=list('xy'))
    #print(df1)
    df2 = pd.DataFrame(mydata.to_numpy(), columns=list('xy'))
    #print(df2)
    return df2
