import sys

sys.path.append('../')

from neomodel import config, db
import bz2
from parse_ttl import TTLParser
import csv, logging, pickle as pickle, pandas as pd, re, random
from dewiki.parser import Parser

from wikidata_sparql import *
from wikitextprocessor import Wtp
import matplotlib

#matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import seaborn as sns

config.DATABASE_URL = 'neo4j://neo4j:l5IKrx07DGYdclK@151.106.35.64:7687'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler("logfile.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
import requests
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay, accuracy_score
import seaborn as sns
import requests

art = {'name': 'Art', 'collect': False, 'wikidata_ids': [], 'category_parent': [], 'category_subs': [],
       'fetch': 'wikidata',
       'category_prop': [],
       'categories': [
           {'name': 'Painting', 'type': 'Non-Human', 'subcategory_parent': ['Q968159'], 'subcategory_prop': ['P135'],
            'fetch': 'db',
            'wikidata_ids': ['Q3305213'],
            'collect': True, 'collect_subs': False, 'subcategories': [
               {'name': 'Artist', 'type': 'Human', 'subcategory_parent': [], 'wikidata_ids': ['Q1028181'],
                'collect': True,
                'fetch': 'wikidata',
                'collect_subs': False, 'subcategories': []},
           ]},
           {'name': 'Sculpting', 'type': 'Non-Human', 'subcategory_parent': ['Q968159'], 'subcategory_prop': ['P135'],
            'fetch': 'db',
            'wikidata_ids': ['Q860861'],
            'collect': True, 'collect_subs': False, 'subcategories': [
               {'name': 'Artist', 'type': 'Human', 'subcategory_parent': [], 'wikidata_ids': ['Q1281618'],
                'collect': True,
                'fetch': 'wikidata',
                'collect_subs': False, 'subcategories': []},
           ]},
           {'name': 'Music', 'type': 'Non-Human', 'subcategory_parent': ['Q968159'], 'subcategory_prop': ['P136'],
            'fetch': 'db',
            'wikidata_ids': ['Q215380', 'Q105543609'], 'collect': True, 'collect_subs': False, 'subcategories': [
               {'name': 'Instrument', 'type': 'Human', 'subcategory_parent': [], 'wikidata_ids': ['Q34379'],
                'collect': True,
                'fetch': 'wikidata',
                'collect_subs': False, 'subcategories': []},
           ]},
           {'name': 'Cinema', 'type': 'Non-Human', 'subcategory_parent': ['Q201658'], 'subcategory_prop': ['P136'],
            'fetch': 'db',
            'wikidata_ids': ['Q11424'],
            'collect': True, 'collect_subs': False, 'subcategories': [
               {'name': 'Actor', 'type': 'Human', 'subcategory_parent': [], 'wikidata_ids': ['Q10800557'],
                'collect': True,
                'fetch': 'wikidata',
                'collect_subs': False, 'subcategories': []},
           ]},
           {'name': 'Theatre', 'type': 'Non-Human', 'subcategory_parent': ['Q7777573'], 'subcategory_prop': ['P136'],
            'fetch': 'wikidata',
            'wikidata_ids': ['Q25379'],  # ,'Q7725634'
            # 'property_query': {'prop': 'P7937', 'params': ['Q25379']},
            'collect': True, 'collect_subs': False,
            'subcategories': [
                {'name': 'Actor', 'type': 'Human', 'subcategory_parent': [], 'wikidata_ids': ['Q2259451'],
                 'collect': True,
                 'fetch': 'wikidata',
                 'collect_subs': False, 'subcategories': []},
            ]},
           {'name': 'Fashion', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
            'fetch': 'wikidata',
            'wikidata_ids': ['Q29583', 'Q12684'],
            'collect': True, 'collect_subs': False, 'subcategories': [
               {'name': 'Model', 'type': 'Human', 'subcategory_parent': [], 'wikidata_ids': ['Q865851'],
                'collect': True,
                'fetch': 'wikidata',
                'collect_subs': False, 'subcategories': []},
               {'name': 'Designer', 'type': 'Human', 'subcategory_parent': [], 'wikidata_ids': ['Q3501317'],
                'collect': True,
                'fetch': 'wikidata',
                'collect_subs': False, 'subcategories': []},
           ]},
           {'name': 'Literature', 'type': 'Non-Human', 'subcategory_parent': ['Q108465955'],
            'subcategory_prop': ['P136'],
            'fetch': 'db',
            'wikidata_ids': ['Q7725634'],
            'collect': True, 'collect_subs': False, 'subcategories': [
               {'name': 'Writer', 'type': 'Human', 'subcategory_parent': [],
                'wikidata_ids': ['Q482980', 'Q36180', 'Q49757'], 'collect': True,
                'fetch': 'wikidata',
                'collect_subs': False, 'subcategories': []},
           ]},
           {'name': 'Photography', 'type': 'Non-Human', 'subcategory_parent': ['Q968159'], 'subcategory_prop': ['P136'],
            'fetch': 'wikidata',
            'wikidata_ids': ['Q125191'],
            'collect': True, 'collect_subs': False, 'subcategories': [
               {'name': 'Photographer', 'type': 'Human', 'subcategory_parent': [], 'wikidata_ids': ['Q33231'],
                'collect': True,
                'fetch': 'wikidata',
                'collect_subs': False, 'subcategories': []},
           ]},
           {'name': 'Dance', 'type': 'Non-Human', 'subcategory_parent': ['Q968159'], 'subcategory_prop': ['P136'],
            'fetch': 'db',
            'wikidata_ids': ['Q2393314'],
            'collect': True, 'collect_subs': False, 'subcategories': [
               {'name': 'Dancer', 'type': 'Human', 'subcategory_parent': [], 'wikidata_ids': ['Q5716684'],
                'collect': True,
                'fetch': 'wikidata',
                'collect_subs': False, 'subcategories': []},
           ]},
           {'name': 'Ceramics', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
            'fetch': 'wikidata',
            'wikidata_ids': ['Q11642'],
            'collect': False, 'collect_subs': False, 'subcategories': [
               {'name': 'Ceramicist', 'type': 'Human', 'subcategory_parent': [], 'wikidata_ids': ['Q7541856'],
                'collect': True,
                'fetch': 'wikidata',
                'collect_subs': False, 'subcategories': []},
           ]},
       ]}

science = {'name': 'Science', 'collect': False, 'wikidata_ids': [], 'category_parent': [], 'category_subs': [],
           'fetch': 'wikidata',
           'category_prop': [],
           'categories': [
               {'name': 'People', 'type': 'Human', 'subcategory_parent': [], 'subcategory_prop': [],
                'collect': False,
                'collect_subs': False,
                'subcategories': [], 'fetch': 'db'},
               {'name': 'Biology', 'type': 'Non-Human', 'subcategory_parent': [],
                'subcategory_prop': [],
                'fetch': 'wikidata',
                'wikidata_ids': ['Q7868'],
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Chemistry', 'type': 'Non-Human', 'subcategory_parent': ['Q11790203'], 'subcategory_prop': [],
                'wikidata_ids': ['Q11369', 'Q2329'],
                'fetch': 'wikidata',
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Physics', 'type': 'Non-Human', 'subcategory_parent': ['Q4162444'], 'subcategory_prop': [],
                'wikidata_ids': ['Q214070', 'physics'],
                'fetch': 'wikidata',
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Mathematics', 'type': 'Non-Human', 'subcategory_parent': ['Q1936384'], 'subcategory_prop': [],
                'wikidata_ids': ['Q65943'],
                'fetch': 'db',
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Medicine', 'type': 'Non-Human', 'subcategory_parent': ['Q28598684', 'Q930752'],
                'subcategory_prop': ['P279', 'P1995'],
                'fetch': 'wikidata_instance_subclass',
                'wikidata_ids': ['Q12136'], # 'Q103914748', 'Q12136', 'Q8084905'
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Earth Sciences', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
                'wikidata_ids': ['Q87058424', 'Q429795', 'Q1069'],
                'fetch': 'wikidata',
                'collect': True, 'collect_subs': True, 'collect_subs_id': 'Q87058424', 'subcategories': []},
               {'name': 'Agriculture', 'type': 'Non-Human', 'subcategory_parent': ['Q28598684'], 'subcategory_prop': [],
                'wikidata_ids': ['Q11451'],
                'fetch': 'wikidata',
                'collect': True, 'collect_subs': False,
                # 'property_query': {'prop': 'P1269', 'params': ['Q272737', 'Q11451']},
                'subcategories': []},
               {'name': 'Archeology', 'type': 'Non-Human', 'subcategory_parent': ['Q28598684'], 'subcategory_prop': [],
                'wikidata_ids': ['Q839954'],
                'fetch': 'db',
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Paleonthology', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
                'wikidata_ids': ['Q40614', 'Q7205'],
                'fetch': 'wikidata',
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Social Sciences', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
                'wikidata_ids': ['Q80083', 'Q34749'],
                'fetch': 'wikidata',
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Meteorology', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
                'wikidata_ids': ['Q25261'],
                'fetch': 'wikidata',
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Antropology', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
                'wikidata_ids': ['Q23404'],
                'fetch': 'wikidata',
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Economics', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
                'wikidata_ids': ['Q8134'],
                'fetch': 'wikidata',
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Psychology', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
                'wikidata_ids': ['Q9418'],
                'fetch': 'wikidata',
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Politics', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
                'wikidata_ids': ['Q7163'],
                'fetch': 'wikidata',
                'collect': True, 'collect_subs': False, 'subcategories': []},
           ]}

technology = {'name': 'Technology', 'collect': False, 'wikidata_ids': [], 'category_parent': [], 'category_subs': [],
              'fetch': 'wikidata',
              'category_prop': 'P31', 'categories': [
        {'name': 'People', 'type': 'Human', 'subcategory_parent': [], 'subcategory_prop': [], 'collect': False,
         'collect_subs': False,
         'subcategories': [], 'fetch': 'db'},
        {'name': 'Computer Science', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
         'fetch': 'wikidata',
         'wikidata_ids': ['Q21198'],
         'collect': True, 'collect_subs': False, 'subcategories': []},
        {'name': 'Electronics', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
         'wikidata_ids': ['Q11650'],
         'fetch': 'wikidata',
         'collect': True, 'collect_subs': False, 'subcategories': []},
        {'name': 'Mechanics', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
         'wikidata_ids': ['Q41217', 'Q101333'],
         'fetch': 'wikidata',
         'collect': True, 'collect_subs': False, 'subcategories': []},
        {'name': 'Civil Engineering', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
         'wikidata_ids': ['Q77590'],
         'fetch': 'wikidata',
         'collect': True, 'collect_subs': False, 'subcategories': []},
        {'name': 'Mechatronics', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
         'fetch': 'wikidata',
         'wikidata_ids': ['Q180165'],
         'collect': True, 'collect_subs': False, 'subcategories': []},
        {'name': 'Robotics', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
         'wikidata_ids': ['Q170978'],
         'fetch': 'wikidata',
         'collect': True, 'collect_subs': False, 'subcategories': []},
        {'name': 'Video Game', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
         'wikidata_ids': ['Q7889'],
         'fetch': 'wikidata',
         'collect': True, 'collect_subs': False, 'subcategories': []},
    ]}

astronomy = {'name': 'Astronomy', 'collect': True, 'wikidata_ids': ['Q333'], 'fetch': 'wikidata',
             'category_parent': ['Q17444909'],
             'category_subs': [],
             'category_prop': ['P31'],
             'categories': [
                 {'name': 'People', 'type': 'Human', 'subcategory_parent': [], 'subcategory_prop': [],
                  'collect': False, 'wikidata_ids': ['Q5'],
                  'collect_subs': False,
                  'subcategories': [], 'fetch': 'db'},
                 # {'name': 'Satellite', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
                 #  'fetch': 'wikidata',
                 #  'wikidata_ids': ['Q21198'],
                 #  'collect': True, 'collect_subs': False, 'subcategories': []},
                 # {'name': 'Space Station', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
                 #  'wikidata_ids': ['Q11650'],
                 #  'fetch': 'wikidata',
                 #  'collect': True, 'collect_subs': False, 'subcategories': []},
                 {'name': 'Program', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
                  'wikidata_ids': ['Q13226541'],
                  'fetch': 'wikidata',
                  'collect': True, 'collect_subs': False, 'subcategories': []},
             ]}

nature = {'name': 'Nature', 'wikidata_ids': [], 'fetch': 'wikidata', 'category_parent': [],  # 'Q7860', 'Q7150'
          'category_prop': [], 'collect': False,
          'category_subs': [],
          'categories': [
              {'name': 'Plant', 'subcategory_parent': [], 'subcategory_prop': [], 'fetch': 'wikidata',
               'wikidata_ids': ['Q756'], 'type': 'Non-Human',
               'collect': True, 'collect_subs': False, 'subcategories': []},
              {'name': 'Food', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
               'wikidata_ids': ['Q2095'],
               'fetch': 'wikidata',
               'collect': True, 'collect_subs': False, 'subcategories': []},
              {'name': 'Animal', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
               'wikidata_ids': ['Q729'],
               'fetch': 'wikidata',
               'collect': True, 'collect_subs': False, 'subcategories': []},
              {'name': 'Microorganism', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
               'wikidata_ids': ['Q39833', 'Q10876'],
               'fetch': 'wikidata',
               'collect': True, 'collect_subs': False, 'subcategories': []},
          ]}

culture = {'name': 'Culture', 'wikidata_ids': ['Q11042', 'Q309'], 'fetch': 'wikidata', 'category_parent': [],
           'category_subs': [], 'collect': True,
           'category_prop': ['P2348'],
           'categories': [
               {'name': 'Historical Figure', 'type': 'Human', 'subcategory_parent': [], 'subcategory_prop': [],
                'fetch': 'wikidata',
                'wikidata_ids': ['Q2478141'],
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Country', 'type': 'Non-Human', 'subcategory_parent': ['Q6256'], 'subcategory_prop': ['P17'],
                'wikidata_ids': ['Q2095'], 'fetch': 'wikidata',
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Classical Era', 'subcategory_parent': [], 'subcategory_prop': [], 'wikidata_ids': [],
                'fetch': 'wikidata', 'type': 'Non-Human', 'property_query': {'prop': 'P2348', 'params': ['Q486761']},
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Medieval Era', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
                'wikidata_ids': ['Q39833'],
                'fetch': 'wikidata', 'property_query': {'prop': 'P2348', 'params': ['Q12554']},
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Early Modern Era', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
                'wikidata_ids': ['Q39833'],
                'fetch': 'wikidata', 'property_query': {'prop': 'P2348', 'params': ['Q5308718']},
                'collect': True, 'collect_subs': False, 'subcategories': []},
               {'name': 'Modern Era', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
                'wikidata_ids': ['Q39833'],
                'fetch': 'wikidata', 'property_query': {'prop': 'P2348', 'params': ['Q3281534']},
                'collect': True, 'collect_subs': False, 'subcategories': []},
           ]}

religion = {'name': 'Religion', 'wikidata_ids': ['Q9174'], 'fetch': 'wikidata', 'category_parent': ['Q9174'],
            'category_prop': ['P140'], 'collect': True,
            'category_subs': [
                {'name': 'Religious Figure', 'type': 'Human', 'subcategory_parent': [], 'subcategory_prop': [],
                 'fetch': 'wikidata', 'collect': False,
                 'wikidata_ids': ['Q5']}
            ], 'categories': []}

mythology = {'name': 'Mythology', 'wikidata_ids': ['Q9134'], 'fetch': 'wikidata',
             'category_parent': ['Q9134'], 'collect': True,
             'category_prop': ['P140', 'P31', 'P2348'], 'category_subs': [
        {'name': 'Mythological Figure', 'type': 'Human', 'subcategory_parent': [], 'subcategory_prop': [],
         'fetch': 'wikidata', 'collect': False,
         'wikidata_ids': ['Q5']}
    ], 'categories': [
        {'name': 'Supernatural', 'subcategory_parent': [], 'subcategory_prop': [], 'type': 'Non-Human',
         'wikidata_ids': ['Q80837', 'Q80837', 'Q1047698', 'Q63046488', 'Q24334893', 'Q4271324'],
         'fetch': 'wikidata',
         'collect': True, 'collect_subs': False, 'subcategories': []},
    ]}

philosophy = {'name': 'Philosophy', 'collect': True,
              'wikidata_ids': ['Q7184903', 'Q5891', 'Q2915955', 'Q49447', 'Q1127759', 'Q483247', 'Q7257', 'Q151885',
                               'Q483677',
                               'Q10567262', 'Q1387659',
                               'Q781413', 'Q840396', 'Q179805', 'Q33104279'], 'fetch': 'wikidata',
              'category_parent': ['Q2915955'],
              'category_prop': [], 'category_subs': [
        {'name': 'Philosopher', 'type': 'Human', 'subcategory_parent': [], 'subcategory_prop': [], 'fetch': 'wikidata',
         'wikidata_ids': ['Q5'], 'collect': False}
    ], 'categories': [
    ]}

architecture = {'name': 'Architecture', 'wikidata_ids': ['Q12271'], 'fetch': 'wikidata', 'category_parent': ['Q32880'],
                'category_subs': [], 'collect': True,
                'category_prop': ['P149'], 'categories': [
        {'name': 'Architect', 'type': 'Human', 'subcategory_parent': [], 'wikidata_ids': ['Q5'], 'collect': False,
         'fetch': 'db', 'collect': False,
         'collect_subs': False, 'subcategories': []},
        {'name': 'Structure', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
         'fetch': 'db',
         'wikidata_ids': ['Q41176'],
         'collect': True, 'collect_subs': False, 'subcategories': []},
    ]}

media = {'name': 'Media', 'collect': True, 'wikidata_ids': ['Q11033'], 'fetch': 'wikidata', 'category_parent': [],
         'category_subs': [],
         'category_prop': [], 'categories': [
        {'name': 'TV Series & Shows', 'type': 'Non-Human', 'subcategory_parent': [],
         'wikidata_ids': ['Q5398426', 'Q15416'],
         'collect': True, 'type': 'Non-Human',
         'fetch': 'wikidata',
         'collect_subs': False, 'subcategories': []},
        {'name': 'Anime', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
         'fetch': 'wikidata', 'type': 'Non-Human',
         'wikidata_ids': ['Q1107'],
         'collect': True, 'collect_subs': False, 'subcategories': []},
        {'name': 'Cartoon', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
         'fetch': 'wikidata', 'type': 'Non-Human',
         'wikidata_ids': ['Q11425'],
         'collect': True, 'collect_subs': False, 'subcategories': []},
        {'name': 'Documentary', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
         'fetch': 'wikidata', 'type': 'Non-Human',
         'wikidata_ids': ['Q93204'],
         'collect': True, 'collect_subs': False, 'subcategories': []},
        {'name': 'News', 'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [],
         'fetch': 'wikidata', 'type': 'Non-Human',
         'wikidata_ids': ['Q1193236'],
         'collect': True, 'collect_subs': False, 'subcategories': []},
    ]}

sports = {'name': 'Sports', 'collect': True, 'wikidata_ids': ['Q13393265','Q847017'], 'fetch': 'wikidata',
          'category_parent': ['Q31629'],
          'category_subs': [], 'category_prop': ['P641'], 'categories': []}

military = {'name': 'Military', 'collect': True, 'wikidata_ids': ['Q8473'], 'fetch': 'wikidata',
            'category_parent': ['Q9134'],
            'category_subs': [],
            'category_prop': ['P140', 'P31', 'P2348'], 'categories': [
        {'name': 'Weapon', 'subcategory_parent': [], 'subcategory_prop': [],
         'wikidata_ids': ['Q15142889'], 'type': 'Non-Human',
         'fetch': 'wikidata',
         'collect': True, 'collect_subs': False, 'subcategories': []},
        {'name': 'Aviation', 'subcategory_parent': [], 'subcategory_prop': [],
         'wikidata_ids': ['Q1188543', 'Q14405627', 'Q64225484'], 'type': 'Non-Human',
         'fetch': 'wikidata_instance_subclass',
         'collect': True, 'collect_subs': False, 'subcategories': []},
        {'name': 'Naval', 'subcategory_parent': [], 'subcategory_prop': [],
         'wikidata_ids': ['Q2235308'], 'type': 'Non-Human',
         'fetch': 'wikidata',
         'collect': True, 'collect_subs': False, 'subcategories': []},
        {'name': 'Land', 'subcategory_parent': [], 'subcategory_prop': [],
         'wikidata_ids': ['Q37761255', 'Q100709275'], 'type': 'Non-Human',
         'fetch': 'wikidata_instance_subclass',
         'collect': True, 'collect_subs': False, 'subcategories': []},
    ]}

transport = {'name': 'Transportation', 'collect': True, 'wikidata_ids': ['Q96622169'], 'fetch': 'wikidata',
             'category_parent': ['Q9134'],
             'category_subs': [],
             'category_prop': ['P140', 'P31', 'P2348'], 'categories': [
        {'name': 'Aviation', 'subcategory_parent': [], 'subcategory_prop': [],
         'wikidata_ids': ['Q4120025'],
         'fetch': 'wikidata_instance_subclass', 'type': 'Non-Human',
         'collect': True, 'collect_subs': False, 'subcategories': []},
        {'name': 'Land', 'subcategory_parent': [], 'subcategory_prop': [],
         'wikidata_ids': ['Q946808', 'Q1002954'],
         'fetch': 'wikidata', 'type': 'Non-Human',
         'collect': True, 'collect_subs': False, 'subcategories': []},
        {'name': 'Railway', 'subcategory_parent': [], 'subcategory_prop': [],
         'wikidata_ids': ['Q19832486'],
         'fetch': 'wikidata', 'type': 'Non-Human',
         'collect': True, 'collect_subs': False, 'subcategories': []},
        {'name': 'Naval', 'subcategory_parent': [], 'subcategory_prop': [],
         'wikidata_ids': ['Q39804', 'Q2055880'],
         'fetch': 'wikidata', 'type': 'Non-Human',
         'collect': True, 'collect_subs': False, 'subcategories': []},
    ]}

other = {'name': 'Other', 'wikidata_ids': [], 'fetch': 'wikidata', 'category_parent': [],
         'category_subs': [], 'collect': True,
         'category_prop': [], 'categories': []}

topics = [art, science, technology, astronomy, nature, culture, religion, mythology, philosophy, architecture, media,
          sports, military, transport, other]


def constructTopics():
    logging.info("Constructing topics...")

    for topic in topics:
        if topic['name'] == 'Other':
            continue

        logging.info('Constructing topic %s...' % topic['name'])

        results, meta = db.cypher_query('MERGE(et:EntityTopic {name:$name}) return id(et)',
                                        {'name': topic['name']})

        for category in topic['categories']:
            if category['type'] == 'Human':
                continue

            logging.info('Constructing category %s...' % category['name'])

            results, meta = db.cypher_query(
                'MATCH(et:EntityTopic {name:$topicName}) '
                ' WITH et MERGE(et)-[:ENTITY_TOPIC_CATEGORY]->(ec:EntityCategory{name:$name})'
                ' return id(ec)',
                {'topicName': topic['name'], 'name': category['name']})

            category['id'] = results[0][0]

            subcategories = []
            for subcategory in category['subcategories']:
                results2, meta = db.cypher_query(
                    'MATCH(et:EntityTopic {name:$topicName}), (et)-[:ENTITY_TOPIC_CATEGORY]->(ec:EntityCategory{name:$categoryName}) '
                    ' MERGE(ec)-[:ENTITIY_CATEGORY_SUB_CATEGORY]->(esc:EntitySubCategory {name:$name})'
                    ' return id(esc)',
                    {'topicName': topic['name'], 'categoryName': category['name'], 'name': subcategory['name'
                                                                                                       '']})

                for result2 in results2:
                    subc = {'id': result2[0], 'name': subcategory['name']}
                    subcategories.append(subc)

            # category['subcategories'].extend(subcategories)

            results3 = []
            for parent in category['subcategory_parent']:
                results3.extend(parse_results(get_results(endpoint_url, query(parent))))

            nodes = [{'wikidata_id': result['wikidata_id'], 'name': result['label'], 'collect': False} for result in
                     results3]

            results2, meta = db.cypher_query(
                'MATCH(et:EntityTopic {name:$topicName}), (et)-[:ENTITY_TOPIC_CATEGORY]->(ec:EntityCategory{name:$categoryName})'
                ' UNWIND $nodes as node MERGE(ec)-[:ENTITY_CATEGORY_SUB_CATEGORY]->(esc:EntitySubCategory{name:node.name})'
                ' return id(esc)',
                {'topicName': topic['name'], 'categoryName': category['name'], 'nodes': nodes})

            category['subcategories'].extend(nodes)

        # Construct custom categories
        results = []
        for parent in topic['category_parent']:
            results.extend(parse_results(get_results(endpoint_url, query(parent))))

        results2, meta = db.cypher_query(
            'MATCH(et:EntityTopic {name:$topicName})'
            ' UNWIND $results as result MERGE(et)-[:ENTITIY_TOPIC_CATEGORY]->(ec:EntityCategory {name:result.label})'
            ' return id(ec), ec.name',
            {'topicName': topic['name'], 'results': results})

        categories = [{'wikidata_id': result['wikidata_id'], 'name': result['label'],
                       'subcategories': [], 'collect': False, 'collect_subs': False,
                       'type': 'Non-Human', 'subcategory_parent': [], 'subcategory_prop': [], 'fetch': 'wikidata'} for
                      result in results]
        topic['categories'].extend(categories)

        for category in topic['categories']:
            for subcategory in topic['category_subs']:
                results3, meta = db.cypher_query(
                    'MATCH(et:EntityTopic {name:$topicName}), (et)-[:ENTITY_TOPIC_CATEGORY]->(ec:EntityCategory{name:$categoryName})'
                    ' WITH ec MERGE(ec)-[:ENTITIY_CATEGORY_SUB_CATEGORY]->(esc:EntitySubCategory {name:$name}) '
                    ' return id(esc)',
                    {'topicName': topic['name'], 'categoryName': category['name'], 'name': subcategory['name']})

                category['subcategories'].append(subcategory)


def repl(m):
    return ' ' * len(m.group())


def get_texts_for_other():
    query = 'MATCH(e:Entity) ' + \
            'where size(e.wiki_article_markup) < 1000 return e.name, e.dbpedia_uri, e.wiki_article_markup limit 100'
    results, meta = db.cypher_query(query)

    texts = [{'name': row[0], 'dbpedia_uri': row[1],
              'text': re.sub(r'{{.*}}|\[\[.*\]\]|{{Infobox .*\n(.*\n)*}}', '_', Parser().parse_string(row[2]))}
             for row in
             results]
    return texts


def get_texts_for_topic_v2(wikidata_ids):
    template = 'MATCH(e:Entity)-[rel:`https://www.wikidata.org/wiki/Property:P31`|`https://www.wikidata.org/wiki/Property:P79`]->(parent:Entity) ' + \
               'where size(e.wiki_article_markup) > 2000 and parent.wikidata_id = "{}" return e.name, e.dbpedia_uri, e.wiki_article_markup limit 100'
    query = ' UNION ALL '.join([template.format(id) for id in wikidata_ids])
    results, meta = db.cypher_query(query)

    texts = [{'name': row[0], 'dbpedia_uri': row[1],
              'text': re.sub(r'{{.*}}|\[\[.*\]\]|{{Infobox .*\n(.*\n)*}}', '_', Parser().parse_string(row[2]))}
             for row in
             results]
    return texts


def get_texts_for_topic(wikidata_ids):
    query = 'MATCH(e:Entity)-[rel:`https://www.wikidata.org/wiki/Property:P31`|`https://www.wikidata.org/wiki/Property:P79`]->(parent:Entity) ' + \
            'where size(e.wiki_article_markup) > 2000 and parent.wikidata_id in $ids return e.name, e.dbpedia_uri, e.wiki_article_markup limit 100'
    results, meta = db.cypher_query(query, {'ids': wikidata_ids})

    texts = [{'name': row[0], 'dbpedia_uri': row[1],
              'text': re.sub(r'{{.*}}|\[\[.*\]\]|{{Infobox .*\n(.*\n)*}}', '_', Parser().parse_string(row[2]))}
             for row in
             results]
    return texts


def get_texts_for_topic_by_id(wikidata_ids):
    query = 'MATCH(e:Entity) where e.wikidata_id in $ids ' + \
            ' and size(e.wiki_article_markup) > 2000 return e.name, e.dbpedia_uri, e.wiki_article_markup limit 100'
    results, meta = db.cypher_query(query, {'ids': wikidata_ids})

    texts = [{'name': row[0], 'dbpedia_uri': row[1],
              'text': re.sub(r'{{.*}}|\[\[.*\]\]|{{Infobox .*\n(.*\n)*}}', '_', Parser().parse_string(row[2]))}
             for row in
             results]
    return texts


def get_texts_for_topic_with_property_query(wikidata_ids, prop, values):
    query = 'MATCH(e:Entity)' + (
        '-[rel:`https://www.wikidata.org/wiki/Property:P31`|`https://www.wikidata.org/wiki/Property:P79`]->(parent:Entity), '
        if wikidata_ids else ', ') + '(e)-[rel2:`https://www.wikidata.org/wiki/Property:$prop`]->(prop:Entity) ' + \
            'where prop.value in $values and ' \
            'e.wiki_article_markup is not null ' + (
                ' and  parent.wikidata_id in $ids ' if wikidata_ids else '') + ' return e.name, e.dbpedia_uri, e.wiki_article_markup limit 100'
    results, meta = db.cypher_query(query, {'ids': wikidata_ids, 'prop': prop, 'values': values})

    texts = [{'name': row[0], 'dbpedia_uri': row[1], 'text': row[2]} for row in results]
    return texts


def get_x_and_y(data):
    x, y = [], []
    for d in data:
        for dd in d['data']:
            tmp = dd['text'].replace('\n', '').replace('_', '')  # clean
            x.append(tmp) if len(tmp) > 0 else None
            y.append(dd['label']) if len(tmp) > 0 else None

    return x, y


def fetch_texts():
    logging.info('Fetching texts...')
    data = []
    for topic in topics:
        logging.info('Fetching texts for topic %s' % topic['name'])
        if topic['fetch'] == 'db' or not topic['collect']:
            pass
        elif topic['name'] != 'Other':  # wikidata
            results = []
            for wikidata_id in topic['wikidata_ids']:
                results.extend(parse_results_general(get_results(endpoint_url, query_general(wikidata_id))))

            wikidata_ids = [result['wikidata_id'] for result in results]
            texts = get_texts_for_topic_by_id(wikidata_ids)
            data.extend(
                [{'label': topic['name'], 'data': [d for d in texts]}])
            logging.info("%d texts fetched. " % len(texts))
        else:  # Other
            texts = get_texts_for_other()
            data.extend(
                [{'label': topic['name'], 'data': [d for d in texts]}])
            logging.info("%d texts fetched. " % len(texts))

        for category in topic['categories']:
            if not category['collect']:
                continue

            logging.info('Fetching texts for category %s' % category['name'])

            if 'property_query' in category:
                texts = get_texts_for_topic_with_property_query(category['wikidata_ids'],
                                                                category['property_query']['prop'],
                                                                category['property_query']['params'])
                data.extend(
                    [{'label': topic['name'] + "-" + category['name'], 'data': [d for d in texts]}])
                logging.info("%d texts fetched. " % len(texts))
            elif category['fetch'] == 'db':
                texts = get_texts_for_topic(category['wikidata_ids'])
                data.extend(
                    [{'label': topic['name'] + "-" + category['name'], 'data': [d for d in texts]}])
                logging.info("%d texts fetched. " % len(texts))
            elif category['fetch'] == 'wikidata':  # wikidata
                results = []
                for wikidata_id in category['wikidata_ids']:
                    results.extend(parse_results_general(get_results(endpoint_url, query_general(wikidata_id))))
                results = sorted(results, key=lambda x: random.random())

                wikidata_ids = [result['wikidata_id'] for result in results]
                texts = get_texts_for_topic_by_id(wikidata_ids)
                data.extend(
                    [{'label': topic['name'] + "-" + category['name'], 'data': [d for d in texts]}])
                logging.info("%d texts fetched. " % len(texts))
            else:  # wikidata_instance_subclass
                results = []
                for wikidata_id in category['wikidata_ids']:
                    results.extend(parse_results(get_results(endpoint_url, query_path(wikidata_id))))
                results = sorted(results, key=lambda x: random.random())

                wikidata_ids = [result['wikidata_id'] for result in results]
                texts = get_texts_for_topic_by_id(wikidata_ids)
                data.extend(
                    [{'label': topic['name'] + "-" + category['name'], 'data': [d for d in texts]}])
                logging.info("%d texts fetched. " % len(texts))

            for subcategory in category['subcategories']:
                if not subcategory['collect']:
                    continue

                logging.info('Fetching texts for subcategory %s' % subcategory['name'])

                if 'property_query' in subcategory:
                    texts = get_texts_for_topic_with_property_query(subcategory['wikidata_ids'],
                                                                    subcategory['property_query']['prop'],
                                                                    subcategory['property_query']['params'])
                    data.extend(
                        [{'label': topic['name'] + "-" + category['name'] + "-" + subcategory['name'],
                          'data': [d for d in texts]}])
                    logging.info("%d texts fetched. " % len(texts))
                elif subcategory['fetch'] == 'db':
                    texts = get_texts_for_topic(subcategory['wikidata_ids'])
                    data.extend(
                        [{'label': topic['name'] + "-" + category['name'] + "-" + subcategory['name'],
                          'data': [d for d in texts]}])
                    logging.info("%d texts fetched. " % len(texts))
                else:  # wikidata
                    results = []
                    for wikidata_id in subcategory['wikidata_ids']:
                        results.extend(parse_results_general(get_results(endpoint_url, query_general(wikidata_id))))
                    results = sorted(results, key=lambda x: random.random())

                    wikidata_ids = [result['wikidata_id'] for result in results]
                    texts = get_texts_for_topic_by_id(wikidata_ids)
                    data.extend(
                        [{'label': topic['name'] + "-" + category['name'] + "-" + subcategory['name'],
                          'data': [d for d in texts]}])
                    logging.info("%d texts fetched. " % len(texts))

            # if category['collect_subs']:
            #     result = get_results(endpoint_url, query_general(category['collect_subs_id']))

    return data


def read_dbpedia():
    logging.info("Reading dbpedia articles...")
    with bz2.open("/media/drived/Dev/dbpedia/long-abstracts_lang=en.ttl.bz2", 'rt') as file:
        parser = TTLParser()

        prefixes = parser.read_prefixes(file)

        rows, halt, i = [], False, 0
        while not halt:
            read_rows = parser.read_data(file, prefixes, 2)
            rows.extend(read_rows)
            i += 1

            if len(read_rows) == 0:
                halt = True

    dbpedia_uris = [row['subject'] for row in rows]
    texts = [row['object'] for row in rows]

    return dbpedia_uris, texts


def page_handler(model, title, text):
    return title, re.sub(r'{{.*}}|\[\[.*\]\]|{{Infobox .*\n(.*\n)*}}', '_', Parser().parse_string(text.strip()))


def read_wikipedia():
    wtp_thread_count = 5
    ctx = Wtp(num_threads=wtp_thread_count)
    results = ctx.process("~/Dev/wikipedia/enwiki-latest-pages-articles15.xml-p17324603p17460152.bz2",
                          page_handler)

    titles, texts = [], []
    for row in results:
        titles.append(row[0])
        texts.append(row[1])

    return titles, texts


def get_labels(data):
    labels = []
    for d in data:
        labels.append(d['label']) if d['label'] not in labels else None

    return labels


def determine_topics_v2():
    # constructTopics()
    data = fetch_texts()
    with open('data/topic_texts_data_markup_100_v3.pkl', 'wb') as outp:
        pickle.dump(data, outp, pickle.HIGHEST_PROTOCOL)

    # data = pd.read_pickle(r'data/topic_texts_data_markup_200_v2.pkl')

    x, y = get_x_and_y(data)  # starte

    logging.info("Training test model...")
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
    model = make_pipeline(TfidfVectorizer(), LinearSVC())
    model.fit(x_train, y=y_train)

    logging.info("Testing the algorithm...")
    result_labels = model.predict(x_test)

    mat = confusion_matrix(y_test, result_labels)

    sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
                xticklabels=get_labels(data), yticklabels=get_labels(data), linewidths=.5)

    print('Accuracy score: %.2f' % accuracy_score(result_labels, y_test))
    print(classification_report(y_test, result_labels))
    print(mat)

    dbpedia_uris, texts = read_dbpedia()
    # dbpedia_uris, texts = read_wikipedia()

    logging.info("Training real model...")
    model.fit(x, y=y)
    logging.info("Running the algorithm...")
    result_labels = model.predict(texts)

    logging.info("Writing results...")
    with open('determine_topics_result_old.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        header = ['Dbpedia Uri', 'Topic', 'Category', 'SubCategory']
        writer.writerow(header)

        i = 0
        for uri, label in zip(dbpedia_uris, result_labels):
            i += 1

            splitted_label = label.split('-')
            topic_label = splitted_label[0]
            category_label = splitted_label[1] if len(splitted_label) > 1 else None
            subcategory_label = splitted_label[2] if len(splitted_label) > 2 else None

            topic = [topic for topic in topics if topic['name'] == topic_label]
            topic = topic[0] if len(topic) > 0 else None
            category = [c for c in topic['categories'] if c['name'] == category_label]
            category = category[0] if len(category) > 0 else None
            subcategory = None

            # if len(topic['category_prop']) > 0:
            #     results, meta = db.cypher_query(
            #         'MATCH(e:Entity)-[rel:' + '|'.join(
            #             "`https://www.wikidata.org/wiki/Property:{}`".format(
            #                 topic['category_prop'])) + ']->(prop:Entity) '
            #                                            'where e.dbpedia_uri = $uri return prop.name',
            #         {'uri': uri})
            #
            #     if len(results) > 0:
            #         category = {'name': [' '.join(s.capitalize()) for s in results[0][0].split()]}
            #
            # if category and len(category['subcategory_prop']) > 0:
            #
            #     # Fetch genre, movement etc.
            #     results, meta = db.cypher_query(
            #         'MATCH(e:Entity)-[rel:' + '|'.join(
            #             "`https://www.wikidata.org/wiki/Property:{}`".format(
            #                 category['subcategory_prop'])) + ']->(prop:Entity) '
            #                                                  'where e.dbpedia_uri = $uri return prop.name',
            #         {'uri': uri})
            #
            #     if len(results) > 0:
            #         subcategory = {'name': [' '.join(s.capitalize()) for s in results[0][0].split()]}

            # Fetch instance of
            # results, meta = db.cypher_query(
            #     'MATCH(e:Entity)-[rel:`https://www.wikidata.org/wiki/Property:P31`]->(prop:Entity) '
            #     'where e.dbpedia_uri = $uri return prop.wikidata_id',
            #     {'uri': uri})
            #
            # instanceof = None
            # if len(results) > 0 and instanceof == 'Q5':
            #     if topic == 'Art':
            #         category = 'Artist'
            #     elif topic == 'Science' or topic == 'Technology' or topic == 'Astronomy':
            #         category = 'People'
            #     elif topic == 'History':
            #         category = 'Historical Figure'
            #     elif topic == 'Philosophy':
            #         category = 'Philosopher'
            #     elif topic == 'Architecture':
            #         category = 'Architect'
            #     elif topic == 'Religion':
            #         subcategory = 'Religious Figure'
            #     elif topic == 'Mythology':
            #         subcategory = 'Mythological Figure'

            # query = 'MATCH(e:Entity), (et:EntityTopic {name: $topic}), (ec:EntityCategory {name: $category})' \
            #         + (
            #             ',(esc:EntitySubCategory {name: $subcategory})' if subcategory else None) + ' where e.dbpedia_uri= $dbpediaUri ' \
            #             (' CREATE(esc)-[:ENTITY_SUB_CATEGORY]->(e) RETURN esc' if subcategory else ' CREATE(ec)-[:ENTITY_CATEGORY]->(e) RETURN ec')
            # db.cypher_query(query, {'dbpediaUri': uri, 'topic': topic, 'category': category, 'subcategory': subcategory})

            result_topic = topic['name'] if topic else topic_label
            result_category = category['name'] if category else category_label
            result_subcategory = subcategory['name'] if subcategory else subcategory_label
            writer.writerow([uri, result_topic, result_category, result_subcategory])

    logging.info("Finished.")


if __name__ == '__main__':
    determine_topics_v2()
