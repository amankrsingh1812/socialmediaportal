def run(request,facebook_id):
    from django.shortcuts import render
    from django.http import HttpResponse
    from django.contrib.auth.decorators import login_required
    from django.shortcuts import redirect
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    #from selenium.common.exceptions import TimeOutException, NoSuchElementException
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from bs4 import BeautifulSoup
    import requests
    import time
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import csv
    import json
    import logging
    import sys
    import urllib.parse
    import shutil
    import os
    from afinn import Afinn
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    import gensim
    import gensim.corpora as corpora
    from gensim.utils import simple_preprocess
    from gensim.models import CoherenceModel
    from gensim.models.ldamodel import LdaModel
    # Plotting tools
    import pyLDAvis
    import pyLDAvis.gensim  # don't skip this
    import matplotlib.pyplot as plt
    import re
    from nltk.corpus import wordnet
    import nltk
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize
    #from wordcloud import WordCloud
    from nltk.corpus import stopwords
    import numpy as np
    import itertools
    import xlrd
    import glob
    s1=""
    s2=""
    #***********************************************************************#
    #global declaration
    all_posts_list = []
    profile_actor_posts_list = []
    #***********************************************************************#
    #username and password to maintain a fb session
    username ='8723047187'
    password ='rs12345'
    #***********************************************************************#
    #paths
    driver_path = "/usr/bin/chromedriver"
    #id will be taken as input from website
    # facebook_id = "https://www.facebook.com/profile.php?id=100041648746887&__tn__=%2Cd-]-h-R&eid=ARBl5E-jNndxZu4Pob1DHEdPY4lyyJmBV1V6wDyb7JyGPcNNaVpsXLjGD__XajvKlGxD61FsaxIUysG9"
    #path of the json dir
    json_dir = "./"
    #***********************************************************************#
    #for getting the unique id, primary key
    #making the json dir if the dir is not created before
    friend_unique_id = ""
    s = facebook_id[25:].split('?')
    if(s[0] == "profile.php"):
        friend_unique_id =  urllib.parse.parse_qs(s[1])['id'][0]
    else:
        friend_unique_id = s[0]
    post_dir = json_dir + "user-id-" + friend_unique_id + "-posts"
    #***********************************************************************#
    #for making the json directory
    if(not os.path.isdir(post_dir)):
        os.mkdir(post_dir)
    #***********************************************************************#
    #login into facebook
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(executable_path=driver_path,chrome_options=chrome_options)
    except:
        print("Please ensure to give correct driver path and check the compatibility of the driver with the version of the Chrome.")
    driver.get("https://www.facebook.com")
    driver.find_element_by_name("email").send_keys(username)
    driver.find_element_by_name("pass").send_keys(password)
    try:
        driver.find_element_by_css_selector('button[name="login"]').click()
    except Exception as e:
        driver.find_element_by_xpath("//*[@id='loginbutton']").click()
    #***********************************************************************#


    # In[2]:


    #scraping posts and saving each posts as a json files
    post_details = ''
    def scrap_post(friend_id):
        print(friend_id)
        driver.get(friend_id)
        #for loading the page
        def LoadMore():
            view_more_comments = []
            view_more_replies = []
            try:
                time.sleep(2)
                view_more_comments = driver.find_elements_by_class_name("_4ssp")
                for element in view_more_comments:
                    time.sleep(2)
                    try:
                        element.click()
                        time.sleep(2)
                    except Exception as e:
                        print(e)
                time.sleep(2)

                view_more_replies = driver.find_elements_by_class_name("_4sso _4ssp")
                for element_1 in view_more_replies:
                    time.sleep(2)
                    try:
                        element_1.click()
                        time.sleep(2)
                    except Exception as e:
                        print(e)
                time.sleep(2)

            except Exception as e:
                print(e)

        print("\n***********************load-more-section*****************************\n")
        #Scrolling::
        flag=0
        scroll_pause_time = 5
        last_height = driver.execute_script("return document.body.scrollHeight")
        print("last height", last_height)

        while(True):
            for i in range(1,3):
                LoadMore()
            time.sleep(5)
            last_height = driver.execute_script("return document.body.scrollHeight")
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            new_height = driver.execute_script("return document.body.scrollHeight")
            time.sleep(4)
            height_diff = new_height-last_height
            print(last_height, "  ", new_height, "  ", height_diff)
            if height_diff == 0:
                flag = flag+1
            else:
                flag = 0
            if flag == 2:
                #print("flag is 2... scroll finished\n")
                break
        print("\n**********************load-more-section-end****************************\n")
        html_source_posts = driver.page_source
        print(html_source_posts)
        soup = BeautifulSoup(html_source_posts,"html.parser")
        # profile_name = soup.find('a',attrs={'class':'_2nlw _2nlv'}).text
         # list of posts:
        post_details = soup.find_all('div',attrs={'class':'_5pcb _4b0l _2q8l'})
        post_count = 0

        #creating post json
        post = {}
        post['_id'] = friend_unique_id
        post['profile_name'] = "Rahul Sharma"
        print("\n*****************************posts-section********************************\n")
        for element in post_details:
            post_count += 1
            json_path = post_dir + "/post-" + str(post_count) + '.json'
            try:
                actor = element.find('img',{'class':"_s0 _4ooo _5xib _5sq7 _44ma _rw img"}).get("aria-label")
            except Exception as e:
                actor = 'null actor'
            try:
                title = element.find('div',{'data-testid':'post_message'}).text
            except Exception as e:
                title = 'no title'
            try:
                date_time = element.find('abbr').get('title')
            except Exception as e:
                date_time = 'no date_time'
            try:
                emotions = element.find('span',{'class':'_81hb'}).text
            except Exception as e:
                emotions = 'no emotions'

            try:
                likes = element.find('span',attrs={'data-testid':'UFI2TopReactions/tooltip_LIKE'}).find('a').get('aria-label')
            except Exception as e:
                likes = 'no likes'

            try:
                loves = element.find('span',attrs={'data-testid':'UFI2TopReactions/tooltip_LOVE'}).find('a').get('aria-label')
            except Exception as e:
                loves = 'no loves'

            try:
                wowes = element.find('span',attrs={'data-testid':'UFI2TopReactions/tooltip_WOW'}).find('a').get('aria-label')
            except Exception as e:
                wowes = 'no wowes'

            try:
                hahas = element.find('span',attrs={'data-testid':'UFI2TopReactions/tooltip_HAHA'}).find('a').get('aria-label')
            except Exception as e:
                hahas = 'no hahas'

            try:
                sads = element.find('span',attrs={'data-testid':'UFI2TopReactions/tooltip_SORRY'}).find('a').get('aria-label')
            except Exception as e:
                sads = 'no sads'

            try:
                angries = element.find('span',attrs={'data-testid':'UFI2TopReactions/tooltip_ANGER'}).find('a').get('aria-label')
            except Exception as e:
                angries = 'no angries'

            try:
                shares = element.find('a',attrs={'rel':'dialog'}).text
            except Exception as e:
                shares = "no shares"

            try:
                no_of_comments = element.find('a',attrs={'class':'_3hg- _42ft'}).text
            except Exception as e:
                no_of_comments = "no comments"

            comments_details = element.find_all('div',attrs={'class':'_680y'})

            print("Post Details:" + " "+ str(post_count)+" "+ actor,title,date_time,emotions,likes,loves,wowes,hahas,sads,angries,shares,no_of_comments)
            #json
            post['serial_no'] = post_count
            post['post_actor'] = actor
            post['post_actor_unique_id'] = 'unique id of the post actor'
            post['post_title'] = title
            post['post_details'] = {}
            post['post_details']['p_total_no_of_comments'] = no_of_comments
            post['post_details']['p_total_no_of_shares'] = shares
            post['post_details']['p_total_no_of_emotions'] = emotions
            post['post_details']['p_total_no_of_likes'] = likes
            post['post_details']['p_total_no_of_hahas'] = hahas
            post['post_details']['p_total_no_of_angries'] = angries
            post['post_details']['p_total_no_of_sads'] = sads
            post['post_details']['p_total_no_of_wowes'] = wowes

            #for comments
            comment_section_full = element.find_all("ul", attrs = {"class": "_7791"})
            if(len(comment_section_full) == 0):
                print("No comments \n")
                post['post_details']['if_comments'] = False
                with open(json_path,'w') as jsonwriteFile:
                    json.dump(post,jsonwriteFile,indent=4)
                continue
            else:
                post['post_details']['if_comments'] = True

            first_li = comment_section_full[0].find_next()
            rest_li = first_li.find_next_siblings('li')
            rest_li.insert(0, first_li)
            all_li = rest_li.copy()

            post['comments'] = {}

            c_count = 1
            for comment_reply_li in all_li:
                comment_block = comment_reply_li.find("div", attrs = {"aria-label": "Comment"})
                replies = comment_reply_li.find_all("div", attrs = {"aria-label": "Comment reply"})

                try:
                    c_actor = comment_block.find('a',attrs={'class':'_6qw4'}).text
                except Exception as e:
                    c_actor = 'no comment actor'
                try:
                    c_actor_id = comment_block.find('a',attrs={'class':'_6qw4'}).get('href')
                except Exception as e:
                    c_actor_id = 'no comment actor id'

                try:
                    c_comment =  comment_block.find('span',attrs={'class':'_3l3x'}).text
                except Exception as e:
                    c_comment = 'no comment'
                try:
                    c_emotions = comment_block.find('span',attrs={'class':'_1lld'}).text
                except Exception as e:
                    c_emotions = 'no comment emotions'

                print("Comment is : ", c_comment)
                print("Comment details: ", "c_ actor:", c_actor, ", c_ actor_id:", c_actor_id, ", c_emotions: ", c_emotions)

                #updating json
                comment_count = 'comment ' + str(c_count)
                post['comments'][comment_count] = {}
                post['comments'][comment_count]['c_serial_no'] = c_count
                post['comments'][comment_count]['c_title'] = c_comment
                post['comments'][comment_count]['c_actor_name'] = c_actor
                post['comments'][comment_count]['c_actor_id'] = c_actor_id
                post['comments'][comment_count]['c_total_no_of_emotions'] = c_emotions

                if(len(replies) == 0):
                    post['comments'][comment_count]['if_replies'] = False
                    with open(json_path,'w') as jsonwriteFile:
                        json.dump(post,jsonwriteFile,indent=4)
                    continue
                else:
                    post['comments'][comment_count]['if_replies'] = True
                    post['comments'][comment_count]['replies'] = {}

                #replies
                r_count = 1
                for reply in replies:
                    try:
                        r_actor = reply.find('a',attrs={'class':'_6qw4'}).text
                    except Exception as e:
                        r_actor = 'no reply actor'
                    try:
                        r_actor_id = reply.find('a',attrs={'class':'_6qw4'}).get('href')
                    except Exception as e:
                        r_actor_id = 'no reply actor id'

                    try:
                        r_reply =  reply.find('span',attrs={'class':'_3l3x'}).text
                    except Exception as e:
                        r_reply = 'no reply'
                    try:
                        r_emotions = reply.find('span',attrs={'class':'_1lld'}).text
                    except Exception as e:
                        r_emotions = 'no reply emotions'
                    print("Reply is : ", r_reply)
                    print("Reply details: ", "r_ actor:", r_actor, ", r_ actor_id:", r_actor_id, ", r_emotions: ", r_emotions)

                    #updating json
                    reply_count = 'reply ' + str(r_count)
                    post['comments'][comment_count]['replies'][reply_count] = {}
                    post['comments'][comment_count]['replies'][reply_count]['r_serial_no'] = r_count
                    post['comments'][comment_count]['replies'][reply_count]['r_title'] = r_reply
                    post['comments'][comment_count]['replies'][reply_count]['r_actor_name'] = r_actor
                    post['comments'][comment_count]['replies'][reply_count]['r_actor_id'] =  r_actor_id
                    post['comments'][comment_count]['replies'][reply_count]['r_total_no_of_emotions'] = r_emotions

                    r_count = r_count + 1

                c_count = c_count + 1

            with open(json_path,'w') as jsonwriteFile:
                json.dump(post,jsonwriteFile,indent=4)

        print("\n***************************post-end*******************************\n")


    # In[3]:


    #*************************************************#
    #affins and vader score
    #traversing the root directory and reading json files of each posts
    def sentiment_scores():
        s1=""
        s2=""
        for file in os.listdir(post_dir):
            full_filename = "%s/%s" % (post_dir, file)
            with open(full_filename,'r') as fi:
                json_dict = json.load(fi)
                #print(json_dict['post_title'])
                all_posts_list.append(json_dict['post_title'])
                if(json_dict['profile_name'] == json_dict['post_actor']):
                    #print("post is given by the profile actor")
                    profile_actor_posts_list.append(json_dict['post_title'])
                if(json_dict['post_details']['if_comments'] == True):
                    for comment_no, comment_details  in json_dict['comments'].items():
                        #print("comment is : ", comment_details['c_title'])
                        all_posts_list.append(comment_details['c_title'])
                        if(comment_details['c_actor_name'] == json_dict['profile_name']):
                            profile_actor_posts_list.append(comment_details['c_title'])
                        if(comment_details['if_replies'] == True):
                            for reply_no, reply_details in comment_details['replies'].items():
                                #print("reply is : ", reply_details['r_title'])
                                all_posts_list.append(reply_details['r_title'])
                                if(reply_details['r_actor_name'] == json_dict['profile_name']):
                                    profile_actor_posts_list.append(reply_details['r_title'])


        print("\n******************sentiment-scores-in-complete-eco-system*******************\n")
        #print(all_posts_list)
        #analysis of posts overall
        message_str = " ".join(str(x) for x in all_posts_list)
        afinn = Afinn(language='en')
        analyzer = SentimentIntensityAnalyzer()
        print("overall affin score is ", str(afinn.score(message_str)) + "\n")
        s1+="overall Analysis 1 score is "+ str(afinn.score(message_str)) + "\n"
        print("overall vader score is ", str(analyzer.polarity_scores(message_str)) + "\n")
        s1+="overall Analysis 2 score is "+str(analyzer.polarity_scores(message_str)) + "\n"
        for post in all_posts_list:
            if(not post == "no title"):
                print("post is :", post, "\n")
                s1+="post is :"+ post+ "\n"
                #AFINN's score
                print("affin score is --  ", afinn.score(post))
                s1+="Analysis 1 is --  "+ str(afinn.score(post))
                #vader
                print("vader score is --  ", analyzer.polarity_scores(post),"\n")
                s1+="Analysis 2 is --  "+str(analyzer.polarity_scores(post))+"\n"
        print("\n****************sentiment-scores-in-complete-eco-system-end*******************\n")


        print("\n*********************sentiment-scores-of-profile-actor***********************\n")
        #print(profile_actor_posts_list)
        p_actor_message_str = " ".join(str(x) for x in profile_actor_posts_list)
        afinn = Afinn(language='en')
        analyzer = SentimentIntensityAnalyzer()
        print("overall affin score is ", str(afinn.score(p_actor_message_str)) + "\n")
        s2+="overall Analysis 1 score is "+ str(afinn.score(message_str)) + "\n"
        print("overall vader score is ", str(analyzer.polarity_scores(p_actor_message_str)) + "\n")
        s2+="overall Analysis 2 score is "+str(analyzer.polarity_scores(message_str)) + "\n"
        for post in profile_actor_posts_list:
            if(not post == "no title"):
                print("post is :", post, "\n")
                #AFINN's score
                s2+="post is :"+ post+ "\n"
                print("affin score is --  ", afinn.score(post))
                s2+="Analysis 1 is --  "+ str(afinn.score(post))
                #vader
                print("vader score is --  ", analyzer.polarity_scores(post),"\n")
                s2+="Analysis 2 is --  "+str(analyzer.polarity_scores(post))+"\n"
        print("\n*******************sentiment-scores-of-profile-actor-end***********************\n")
        return (s1,s2)
    #*************************************************#


    # In[4]:


    #helping methods
    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'no title', 'title'])
    final_list_of_keywords = []
    def unique(List):
        x = np.array(List)
        x = np.unique(x)
        return x

    #helping methods to extract keywords:
    def get_wordnet_pos(word):
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)

    def remove_stop_words(texts):
        data_words_nostop = []
        for doc in texts:
            for word in simple_preprocess(str(doc)):
                if word not in stop_words:
                    data_words_nostop.append(word)
        return data_words_nostop

    #method to extract keywords:
    data = []


    def keywords_with_posts(List_of_titles):
        data = []
        for element in List_of_titles:
            element = str(element).lower()
            data.append(element)

        # Remove new line characters
        data = [re.sub('\s+', ' ', sent) for sent in data]
        # Remove distracting single quotes
        data = [re.sub("\'", "", sent) for sent in data]
        #print(List_of_titles)
        # tokenize and lemmatize:
        lemmatized_list = []
        lemmatizer = WordNetLemmatizer()
        for sentence in data:
            element = nltk.word_tokenize(sentence)
            for word in element:
                 word = lemmatizer.lemmatize(word,pos = 'n')
                 word = gensim.utils.simple_preprocess(word, deacc=True)
                 lemmatized_list.append(word)
        #print(lemmatized_list)
        # Build the bigram and trigram models:
        bigram = gensim.models.Phrases(lemmatized_list, min_count=5, threshold=100) # higher threshold fewer phrases.
        trigram = gensim.models.Phrases(bigram[lemmatized_list], threshold=100)

        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram_mod = gensim.models.phrases.Phraser(trigram)

        # functions for stopwords, bigrams, trigrams and lemmatization:
        data_words_nostop = []
        data_words_lemmatized = []
        data_words_bigrams = []

        # call the functions in order:
        data_words_nostop = remove_stop_words(lemmatized_list)

        # Create Dictionary:
        id2word_dic = corpora.Dictionary([data_words_nostop])

        # Create Corpus:
        texts = [data_words_nostop]

        # Term Document Frequency
        corpus = [id2word_dic.doc2bow(text) for text in texts]

        # Build LDA model:
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,id2word=id2word_dic, num_topics=25, random_state=100, update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True)

        doc_lda = lda_model[corpus]

        #keywords:
        Unique_List = []
        for index, topic in lda_model.show_topics(formatted=False, num_words= 30):
            final_list_of_keywords.append([w[0] for w in topic])

        for sublist in final_list_of_keywords:
            for element in sublist:
                Unique_List.append(element)

        Unique_List = unique(final_list_of_keywords)
        #print(final_list_of_keywords)
        Unique_List = str(Unique_List)
        #print(Unique_List)

        is_noun = lambda pos: pos[:2] == 'NN'
        tokenized = nltk.word_tokenize(Unique_List)

        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
        #print("Noun Keywords...........")
        #print(nouns)

        #keywords with posts:
        keywords_with_posts = {}
        for keyword in nouns:
            posts_list = []
            #removal of extra comma
            key = keyword.replace("'", "")
            key = key.lower()
            #removal of bad keys
            if(keyword == "]"):
                continue
            for post in List_of_titles:
                #print(post.find(keyword))
                #print(post)
                post = post.lower()
                post = post.lower()
                if(not post.find(key) == -1):
                    #print(keyword, "is found in ", post)
                    posts_list.append(post)
            keywords_with_posts[key] = posts_list
        #print(keywords_with_posts)

        return keywords_with_posts


    # In[5]:


    def keywords_frequency(keywords_with_posts):
        keywords_frequency = {}
        for keyword, posts in keywords_with_posts.items():
            keywords_frequency[keyword] = len(posts)
        return keywords_frequency


    # In[24]:


    #comparing keywords of lda with csv file keywords
    #currently not in use
    def trait_score_compare_keyword_with_lda_csv(keywords_with_posts):
        #print("inside keyword method")
        afinn = Afinn(language='en')
        analyzer = SentimentIntensityAnalyzer()
        loc = "portal/keywords.xlsx"  # path of data set
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        no_of_rows = sheet.nrows  # number of rows in the data set
        traits_with_posts = {}

        for i in range(no_of_rows-1):
            #print("trait is ", sheet.cell_value(i+1, 0),"\n")
            given_keywords_list = sheet.cell_value(i+1, 1).split(",")
            posts_with_trait = []
            #print("keywords are..............\n")
            for given_keyword in given_keywords_list:
                #print(given_keyword)
                g_keyword = given_keyword.replace(" ", "")
                if g_keyword in keywords_with_posts.keys():
                    #print(given_keyword, " is matched in fb keywords")
                    posts_with_trait.append(keywords_with_posts[g_keyword])
            traits_with_posts[sheet.cell_value(i+1, 0)] = posts_with_trait

        #print(traits_with_posts)
        print("\n*********************scores of traits*******************************\n")
        traits_with_score = {}
        for trait, traits_posts in traits_with_posts.items():
            #print("trait is ", trait, "\n")
            #print(traits_posts)
            traits_posts_list = list(itertools.chain(*traits_posts))
            trait_vader_score = 0
            if(not len(traits_posts_list) == 0):
                #print("vader score is ", analyzer.polarity_scores(traits_posts_list[0]), "\n")
                trait_vader_score = analyzer.polarity_scores(traits_posts_list[0])
            affin_trait_score = 0
            for traits_post in traits_posts_list:
                #print(traits_post)
                #affins
                #print("affin score is ", afinn.score(traits_post))
                affin_trait_score = affin_trait_score + afinn.score(traits_post)

            traits_with_score[trait] = {}
            traits_with_score[trait]['affin_score'] = affin_trait_score
            traits_with_score[trait]['vader_score'] = trait_vader_score
            #print("\n")
        print(traits_with_score)


    # In[31]:


    def trait_score_from_csv_keyword(posts_list):
        afinn = Afinn(language='en')
        analyzer = SentimentIntensityAnalyzer()

        loc = "portal/keywords.xlsx"  # path of data set
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        no_of_rows = sheet.nrows  # number of rows in the data set

        traits_with_posts = {}
        for i in range(no_of_rows-1):
            #print("trait is ", sheet.cell_value(i+1, 0))
            given_keywords_list = sheet.cell_value(i+1, 1).split(",")
            trait_posts_list = []
            for given_keyword in given_keywords_list:
                #print(given_keyword)
                given_keyword = given_keyword.lower()
                for post in posts_list:
                    #print(post)
                    #to do, post clean
                    post = post.lower()
                    post = post.replace(".", "")
                    if(not post.find(given_keyword) == -1):
                        #print(given_keyword, " is found in ", post)
                        trait_posts_list.append(post)
            traits_with_posts[sheet.cell_value(i+1, 0)] = trait_posts_list
            #print("\n")

        #print(traits_with_posts)
        #print("\n*********************scores of traits*******************************\n")
        traits_with_score = {}
        for trait, traits_posts_list in traits_with_posts.items():
            #print("trait is ", trait, "\n")
            trait_vader_score = 0
            if(not len(traits_posts_list) == 0):
                #print("vader score is ", analyzer.polarity_scores(traits_posts_list[0]), "\n")
                trait_vader_score = analyzer.polarity_scores(traits_posts_list[0])
            affin_trait_score = 0
            for traits_post in traits_posts_list:
                #print(traits_post)
                #affins
                #print("affin score is ", afinn.score(traits_post))
                affin_trait_score = affin_trait_score + afinn.score(traits_post)

            traits_with_score[trait] = {}
            traits_with_score[trait]['affin_score'] = affin_trait_score
            traits_with_score[trait]['vader_score'] = trait_vader_score
            #print("\n")
        #print(traits_with_score)
        return traits_with_score


    # In[33]:


    #*************************************************#
    #method calls
    # print(os.curdir)
    # wb = xlrd.open_workbook("portal/keywords.xlsx")
    scrap_post(facebook_id)
    s1,s2=sentiment_scores()
    keywords_with_posts_overall = keywords_with_posts(all_posts_list)
    keywords_with_posts_profile_actor = keywords_with_posts(profile_actor_posts_list)
    keywords_frequency_overall = keywords_frequency(keywords_with_posts_overall)
    keywords_frequency_profile_actor = keywords_frequency(keywords_with_posts_profile_actor)
    #trait_score_overall = trait_score_compare_keyword_with_lda_csv(keywords_with_posts_overall)
    #trait_score_profile_actor = trait_score_compare_keyword_with_lda_csv(keywords_with_posts_profile_actor)
    trait_score_overall = trait_score_from_csv_keyword(all_posts_list)
    trait_score_profile_actor = trait_score_from_csv_keyword(profile_actor_posts_list)



    print("\n*************************lda keywrods with posts for all**************************\n")
    print(keywords_with_posts_overall)
    print("\n*************************lda keywrods with posts for profile actor**************************\n")
    print(keywords_with_posts_profile_actor)
    print("\n*************************lda keywrods frequency for all**************************\n")
    print(keywords_frequency_overall)
    print("\n*************************lda keywrods frequency for profile actor**************************\n")
    print(keywords_frequency_profile_actor)
    print("\n*************************CSV traits score for all**************************\n")
    print(trait_score_overall)
    print("\n*************************CSV traits score for profile actor**************************\n")
    print(trait_score_profile_actor)
    print("\n********************************************************************************\n")
    #*************************************************#

    driver.close()
    g={}
    for key in trait_score_profile_actor:
        g[key]={'1':trait_score_profile_actor[key],'2':trait_score_overall[key]}
    return render(request,'result.html',{'kfpa':keywords_frequency_profile_actor,'kfo':keywords_frequency_overall,'g':g,'s1':s1,'s2':s2})
    # In[ ]:





    # In[ ]:





    # In[ ]:




