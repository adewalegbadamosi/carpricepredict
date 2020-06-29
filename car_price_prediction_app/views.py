from django.shortcuts import render
from models.car_price_module import *
from pymongo import  MongoClient

#create connection to mongoDB
client = MongoClient('localhost',27017)

#create database named car_price_prediction
db = client['car_price_prediction']

# create collection named predictions
collection = db.predictions



#create an object instance of class CarPrice
car_price = CarPrice('./models/model','./models/scaler' ,'./models/buffer.csv')

def index(request):
    context = {'title':'Home'}
    
    return render(request,'index.html', context)


def predict(request):
    user_input_dict = None
    predicted_price = None
    if request.method == 'POST':
        user_input_dict = request.POST.dict()
        
        # get user inputs
        user_input = [ x for x in request.POST.dict().values() if list(request.POST.dict().values()).index(x) != 0 ]
        user_input = [ float(x) if user_input.index(x) == 1 or user_input.index(x) == 3 or 
                        user_input.index(x) == 7 else x for x in user_input  ] 
    
        # further processing of the raw user_input for modelling
    
        car_price.data_preprocessing(user_input) 
        # predicting the car price 
        predicted_price = car_price.price_predicted()

        # insert information into the collection
        #collection.insert_one({'prediction': predicted_price, 'input':user_input})

    context = { 'predicted_price': predicted_price, 'title':'Home','user_input_dict': user_input_dict }

    return render(request,'index.html', context)

def about(request):
    context = { 'title':'About' }
    return render(request,'about.html', context)

