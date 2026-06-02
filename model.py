import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# SAMPLE REALISTIC DATASET (KAGGLE STYLE)
data = {
    "social": [1,2,3,4,5,6,7,8,9,10],
    "talkative": [1,2,2,3,4,5,6,7,8,9],
    "alone_time": [10,9,8,7,6,5,4,3,2,1],
    "stress": [8,7,6,6,5,5,4,3,2,1],
    "personality": [0,0,0,1,1,1,2,2,2,2]  
}

df = pd.DataFrame(data)

X = df.drop("personality", axis=1)
y = df["personality"]

model = RandomForestClassifier()
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))

print("Personality Model trained successfully ✔")