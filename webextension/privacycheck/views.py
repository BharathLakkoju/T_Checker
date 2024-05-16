from django.shortcuts import render
import os
import pickle
from django.conf import settings
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Get absolute path to the pickle file
pickle_file_path = os.path.join(settings.BASE_DIR, "privacycheck", "model.pkl")
# Load the model from the pickle file
with open(pickle_file_path, "rb") as file:
    loaded_model, vectorizer = pickle.load(file)


# Create your views here.
@csrf_exempt
def index(request):
    # Define the predict_policy function using the loaded clean_text and vectorizer
    if request.method == "POST":
        data = json.loads(request.body)

        def clean_text(text):
            tokens = word_tokenize(text.lower())  # Tokenize and convert to lower case
            tokens = [word for word in tokens if word.isalpha()]  # Remove punctuation
            tokens = [
                word for word in tokens if word not in stopwords.words("english")
            ]  # Remove stop words
            return " ".join(tokens)

        def predict_policy(policy):
            policy_clean = clean_text(policy)
            policy_vec = vectorizer.transform([policy_clean])
            return loaded_model.predict(policy_vec)

        def getTermsLink(links):
            for link in links:
                if link.get("href") != None:
                    l = link.get("href")
                    if (
                        "terms" in l
                        or "terms-and-conditions" in l
                        or "conditions" in l
                        or "policies" in l
                    ):
                        if l.startswith("/"):
                            l = URL + l
                            return l
                        else:
                            return l

        def getPoliciesLink(links):
            for link in links:
                l = link.get("href")
                if "policies" in l or "privacy" in l or "privacy-policy" in l:
                    if l.startswith("/"):
                        l = URL + l
                        return l
                    else:
                        return l

        # def get_text_content(soup):
        #     body = soup.find('body')
        #     text_content = body.get_text('. ', strip=True)
        #     return text_content
        def get_text_content(soup):
            text_content = soup.get_text()
            return text_content

        try:
            URL = data.get("url")
            response = requests.get(URL)
            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.find_all("a")
            links.reverse()

            if links != []:
                terms_link = getTermsLink(links)
                privacy_link = getPoliciesLink(links)
                t_page = requests.get(terms_link)
                t_soup = BeautifulSoup(t_page.content, "html.parser")
                p_page = requests.get(privacy_link)
                p_soup = BeautifulSoup(p_page.content, "html.parser")
                overall_content = (
                    get_text_content(t_soup).strip()
                    + ". "
                    + get_text_content(p_soup).strip()
                )
                overall_content_split = overall_content.split(".")
                overall_content_split = set(overall_content_split)
                pos_data = []
                neg_data = []
                for i in overall_content_split:
                    if len(i) >= 20 and len(i) <= 100:
                        prediction = predict_policy(i)
                        if prediction == "positive" or prediction == "neutral":
                            pos_data.append(i)
                        else:
                            neg_data.append(i)
                pos_data.sort(reverse=True, key=len)
                neg_data.sort(reverse=True, key=len)
                pos_percent = (len(pos_data) / (len(pos_data) + len(neg_data))) * 100
                neg_percent = (len(neg_data) / (len(pos_data) + len(neg_data))) * 100
                pos_data = pos_data[:5]
                neg_data = neg_data[:5]
                return JsonResponse(
                    {
                        "pos_data": pos_data,
                        "neg_data": neg_data,
                        "pos_percent": pos_percent,
                        "neg_percent": neg_percent,
                    }
                )
        except:
            text_content = (
                "Few websites stop unauthorized scraping for security reasons."
            )
            return JsonResponse({"error": text_content})
    else:
        return JsonResponse({"error": text_content})
