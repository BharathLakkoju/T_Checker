# Import necessary libraries
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import joblib

# Load the dataset
df = pd.read_csv("../data.csv")
df = df.iloc[:, [0, 1]]

# Download necessary NLTK data
nltk.download("punkt")
nltk.download("stopwords")

# Function to clean text
def clean_text(text):
    tokens = word_tokenize(text.lower())  # Tokenize and convert to lower case
    tokens = [word for word in tokens if word.isalpha()]  # Remove punctuation
    tokens = [word for word in tokens if word not in stopwords.words("english")]  # Remove stop words
    return " ".join(tokens)

# Apply the cleaning function to the policy column
df["policy_clean"] = df["data"].apply(clean_text)

# Initialize the TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the cleaned policies
X = vectorizer.fit_transform(df["policy_clean"])

# Labels
y = df["class"]

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = SVC(kernel="rbf")
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
print(classification_report(y_test, y_pred, zero_division=1))

with open("model.pkl", "wb") as file:
    joblib.dump(model, 'model.pkl')
# Save the trained model

