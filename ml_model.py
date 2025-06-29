from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
from strategy import calculate_indicators

def train_model(df):
    df = calculate_indicators(df).dropna()
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    X = df[['RSI', '20DMA', '50DMA', 'Volume']]
    y = df['Target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    return model, acc 