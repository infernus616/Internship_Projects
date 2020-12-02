from Automated_version_3 import myClass
import pandas as pd
import numpy as np
import datetime
import time
import gspread
from pymongo import MongoClient
import itertools
from multiprocessing.dummy import Pool as ThreadPool 
import multiprocessing
from itertools import repeat
from bson import ObjectId


def get_city_info():
    all_city = sh.worksheet("ALL_City")
    temp = all_city.get()
    city_info = {}
    for x in range(len(temp)):
        if temp[x][0]==city:
            city_info = temp[x]
    return city_info

def get_city_languages_from_sheet(city):
    city_sheet_name = city+"_Language"
    city_sheet_from_googlesheets = sh.worksheet(city_sheet_name)
    temp_1 = city_sheet_from_googlesheets.get()
    df1 = pd.DataFrame(temp_1,columns=temp_1[0])
    df1 = df1.drop(labels=0).reset_index()
    df1.drop(['index'],axis=1,inplace=True)
    return df1

def converting_string_to_list(string_of_languages):
    return string_of_languages.strip('][').split(',')

def get_city_info():
    all_city = sh.worksheet("ALL_City")
    temp = all_city.get()
    city_info = {}
    for x in range(len(temp)):
        if temp[x][0]==city:
            city_info = temp[x]
    return city_info

def get_city_languages_from_sheet(city):
    city_sheet_name = city+"_Language"
    city_sheet_from_googlesheets = sh.worksheet(city_sheet_name)
    temp_1 = city_sheet_from_googlesheets.get()
    df1 = pd.DataFrame(temp_1,columns=temp_1[0])
    df1 = df1.drop(labels=0).reset_index()
    df1.drop(['index'],axis=1,inplace=True)
    return df1
def storing_in_mongodb(language,browser_language,autocomplete):
    global object_id_given_or_not
    global object_id
    hour = str(datetime.datetime.now().strftime("%I")) + str(datetime.datetime.now().strftime("%p"))
    date = str(datetime.datetime.now()).split(' ')[0]
    combination_name = "Autocomplete."+ str(language)+"_"+str(browser_language)
    rec={
            "City": city,
            "Month": datetime.datetime.now().strftime("%b"),
            "Date": str(datetime.datetime.now()).split(' ')[0],
            "State":values_list[3],
            "Hour": str(datetime.datetime.now().strftime("%I")) + str(datetime.datetime.now().strftime("%p")),
            str(combination_name): autocomplete
    }
    if object_id_given_or_not == False:
        object_id = collection_name.update_one({"City":city,"Date":date,"Hour":hour},{"$set":rec},upsert=True).upserted_id
        object_id_given_or_not = True
    else:
        collection_name.update_one({'_id':object_id},
                           {"$set":rec},upsert=True)


def write(i,obj,combination,lat,log,data_frame):
    time.sleep(i)
    print(i, "---", obj,"---",combination)
    obj.set_location(lat,log,"https://www.google.com/")
    obj.change_language_settings(combination[1])
    name = str(combination[0]) + "_binary"
    language_array = np.array(data_frame[data_frame[name]=='Yes'][combination[0]])
    result = obj.retrieving_alphabets(language_array)
    storing_in_mongodb(combination[0],combination[1],result)
    obj.driver.close()
    obj.driver.quit()
#     print(result)

if __name__ == '__main__':    
    city='Delhi'
    object_id = ''
    object_id_given_or_not = False
    client = MongoClient("localhost", 27017)
    database_name = client.Madhav
    collection_name = database_name.India2
    gc = gspread.service_account(filename=r"D:\coding\internship\rising-area-287717-2aa397dd3fc7.json")
    sh = gc.open("India_master")
    values_list = get_city_info()
    language_dataframe = get_city_languages_from_sheet(city)
    latitude,longitude = float(values_list[4]),float(values_list[5])
    languages = converting_string_to_list(values_list[1])
    languages_abbreviation = converting_string_to_list(values_list[2])
    combinations = list(itertools.product(languages, languages_abbreviation))
    list_of_numbers = list(range(0, len(combinations)))
    list_of_objects = []
    for j in range(len(combinations)):
        list_of_objects.append(myClass())
    pool = ThreadPool(len(combinations))
    pool.starmap(write, zip(list_of_numbers,list_of_objects,combinations,
                      repeat(latitude,len(combinations)),repeat(longitude,len(combinations)),repeat(language_dataframe,len(combinations)))) 
    pool.close() 
    pool.join()
    client.close()