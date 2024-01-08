```python
import requests
import time


# Search for a model that you are interested in using the Hugging Face model hub: https://huggingface.co/models
# When you find a model that you are interested in using, click "Deploy" and then "Inference API"
# Click "Show API Token" and copy the API_URL and headers below
API_URL = "https://api-inference.huggingface.co/models/finiteautomata/bertweet-base-emotion-analysis"
headers = {"Authorization": "HUGGING_FACE_API_KEY"}

# Change "YOUR_NAME" and "YOUR_REVIEW" to your name and your review of the club so far,
# Your review will be emotionally analyzed by the model
my_name = "Alexander Halpern"
my_review = "I love the GDSC."


# Function to communicate with HuggingFace in order to request an emotional analysis of our review
def infer_emotions(prompt):
    # TODO implement this
    response = requests.post(API_URL, headers=headers, json=prompt)
    return response


# get the emotions of the review
answer = infer_emotions({
    "inputs": my_review,
})

# You don't need to worry about this
# It just ensures that the model is loaded before we try to use it
while answer.status_code != 200:
    answer = infer_emotions({
        "inputs": my_review,
    })
    time.sleep(4)

answer = answer.json()[0]

# Send the results to the database on our website
# helper function to format data


def format_data():
    data = {"name": my_name, "review": my_review}
    for key in answer:
        data[key['label']] = key["score"]
    return data


# Format the data
data = format_data()

# THe URL of our database
database_url = "https://oct18interestmeeting-default-rtdb.firebaseio.com/"

# push the data to a list of data under /submissions
# TODO implement this
requests.post(database_url + "/submissions.json", json=data)
```
