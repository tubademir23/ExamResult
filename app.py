from flask import Flask, render_template, request
import os
import pandas as pd

app = Flask(__name__)
headings=('İsim', 'TC Kimlik No', 'Puan', 'Sıralama')
columns=['ADI_SOYADI','TC', 'PUAN','SIRALAMA']
def get_data():
    DATA_PATH=os.path.abspath('sonuc')
    files = os.listdir(DATA_PATH)  
    df = pd.DataFrame()
    for file in files:
        df_ = pd.read_excel(os.path.join(DATA_PATH, file), index_col=None)
        df = df.append(df_, ignore_index=True)
    df['TC'] = df['TC'].apply(str)
    return df

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tc = request.form.get("tc")
        data=get_data()
        sonuc= data[data['TC']==tc]
        if(sonuc.empty):
            return render_template('index.html', mesaj='Başarılı Olamadınız')
        
        subset = sonuc[columns].values[0]
       
        return render_template('index.html',headings=headings, data=(subset))
    elif request.method == 'GET':
        print("get")
        return render_template('index.html')

if __name__ == '__main__': 

    app.run(debug=True)
