import csv
import nltk
import contractions
import pycontractions
import re


def main():
    # Load Hate Speech Dictionary
    with open('Dictionary2.csv') as hate_file:
        hreader = csv.reader(hate_file, delimiter=',')
        lcount = 0

        hate_list = []

        for hrow in hreader:
            hate_list.append(hrow[0])


    # Load Tweets
    with open('ElectionTweets.csv', encoding='UTF-8') as tweet_file:
        treader = csv.reader(tweet_file, delimiter=',')
        tcount = 0

        tweet_list = []

        for trow in treader:
            tweet_list.append(trow)

    # For each Tweet, for each words

    for i,tweetrow in enumerate(tweet_list):
        rowtext = tweetrow[1]

        # Contraction Expansions: expand contracted words to their normal forms -----------------------
        rowtextcontraction = contractions.fix(rowtext)

        # rowTextpContraction = pycontractions.Contractions(rowText)


        # Text Cleaning --------------------------------------------------------------------------------
        rowcleanedtext = text_cleaning(rowtextcontraction)

        # Write cleaned text to file
        tweet_list[i].append(rowcleanedtext)
        # Write to csv file
        with open('cleaned_text.csv', 'w', encoding='UTF-8', newline='') as output_file:
            writer = csv.writer(output_file, dialect='excel')
            writer.writerows(tweet_list)

        # Labelling


# For each Tweet, if the tweet contains any of the words in the Hate Speech Dictionary, label the tweet as hatespeech
#Tweet row should be row 2 so that we are using cleanded text

    for j, tweetrow in enumerate(tweet_list):
        rowTxt = tweetrow[2]
        # Tokenize words here
        # words = rowText.split()
        words = rowTxt.split()
        doublewords = list(map(' '.join, zip(words[:-1], words[1:])))
        words.extend(doublewords)

        # bool_result = any(substring in rowText for substring in hate_list)
        # bool_result = any(substring in words for substring in hate_list)
        # bool_result = any(y in x for x in hate_list for y in words)

        bool_result = False

        for wo in words:

            if bool_result == True:
                break

            # Porter Stemmer
            porter = nltk.PorterStemmer()

            p_wo = porter.stem(wo)

            # Lancaster Stemmer
            # lancaster = nltk.LancasterStemmer()

            # l_wo = lancaster.stem(wo)

            # Lemmatizer WordNet
            wnl = nltk.WordNetLemmatizer()

            # wnl_hateword = wnl.lemmatize(hateword)

            for hateword in hate_list:
                # should not be case sensitive
                hateword = hateword.lower()
                wo = wo.lower()

                if hateword == wo:
                    bool_result = True
                    break
                elif hateword == p_wo:
                    bool_result = True
                    break
                # elif hateword == l_wo:
                #    bool_result = True
                #    break
                # elif wnl_hateword == wo:
                #    bool_result = True
                #    break

        if bool_result:
            val = '1'
            tweet_list[j].append(val)
            # once a line is detected as hatespeech, no need to check other words in that line
            continue
        else:
            val = '0'
            tweet_list[j].append(val)



    # Write to csv file
    with open('cleaned_text_labelled.csv', 'w', encoding='UTF-8', newline='') as output_file:
        writer = csv.writer(output_file, dialect='excel')
        writer.writerows(tweet_list)

    # Handle text imbalance dataset

    # final preprocessing for algorithm training

    # text vectorization


def contraction_expansion(sentence):
    return contractions.fix(sentence)


def text_cleaning(sentence):

    #remove @user mention link of a tweet
    result1 = re.sub("(?<![\w.-])@[A-Za-z][\w-]+", "", sentence)

    # remove # hashtags r'\B#\w*[a-zA-Z]+\w*'         r"#(\w+)"   "(?<![\w.-])#[A-Za-z][\w-]+"
    result2 = re.sub(r"#(\w+)", "", result1)

    # Remove URLs
    result3 = re.sub(r'http\S+', '', result2)

    # Convert 419 to criminal
    result4 = re.sub('419', ' criminal ', result3)

    # Remove anything that  is not an alphabet, remove numbers
    result5 = re.sub('[^A-Za-z ]+', ' ', result4)

    # Remove anything that  is not an alphabet or number
    #result4 = re.sub('[^A-Za-z0-9 ]+', ' ', result3)

    # Remove single characters
    result6 = re.sub(r"\b[a-zA-Z]\b", "", result5)


    # Replace multiple spaces with single space
    result7 = re.sub('\s+', ' ', result6)

    return result7



main()