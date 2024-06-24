"""Module providing a connection to mongo."""

from pprint import pprint
from pymongo import MongoClient

client = MongoClient( host="127.0.0.1", port = 27017, username='admin', password='pass' )
#client = MongoClient('mongodb://admin:pass@127.0.0.1')

dbs = client.list_database_names()

print("Databases: ")
pprint(dbs)


cols = client['sample'].list_collection_names()

print("Collections of sample: ")
print(cols)

books =  client['sample'].books
book = books.find_one()

print("A book : ")
pprint(book)

print("Numbers of books : ")
print(books.count_documents({}))

print("Numbers of books with more than 400 pages : ")
print(books.count_documents({'pageCount' : {'$gte' : 400}}))

print("Numbers of published books with more than 400 pages : ")
print(books.count_documents({'status': 'PUBLISH', 'pageCount' : {'$gte' : 400}}))


print("Numbers of books with Android on description : ")
print(books.count_documents({'$or' : [{'longDescription': {'$regex':'Android'}}, {'shortDescription': {'$regex':'Android'}}]}))

print("Categories Aggregation : ")
pprint(
    list(books.aggregate([
  {
    '$group': {
      '_id':  None,
      'Categorie1': {
        '$addToSet': {
          '$arrayElemAt': ["$categories", 0]
        }
      },
      'Categorie2': {
        '$addToSet': {
          '$arrayElemAt': ["$categories", 1]
        }
      }
    }
  }
]))
)

print("Numbers of books with Python, Java, C++, Scala on description : ")
pipeline = [
    {
        "$match": {
            "$or": [
                { "shortDescription": { "$regex": "Python", "$options": "i" } },
                { "shortDescription": { "$regex": "Java", "$options": "i" } },
                { "shortDescription": { "$regex": "C\\+\\+", "$options": "i" } },
                { "shortDescription": { "$regex": "Scala", "$options": "i" } },
                { "longDescription": { "$regex": "Python", "$options": "i" } },
                { "longDescription": { "$regex": "Java", "$options": "i" } },
                { "longDescription": { "$regex": "C\\+\\+", "$options": "i" } },
                { "longDescription": { "$regex": "Scala", "$options": "i" } }
            ]
        }
    },
    {
        "$count": "books"
    }
]

pprint(list(books.aggregate(pipeline))[0]['books'])

print("Stats : ")
pipeline = [
    { "$unwind": "$categories" },
    {
        "$group": {
            "_id": "$categories",
            "maxPages": { "$max": "$pageCount" },
            "minPages": { "$min": "$pageCount" },
            "avgPages": { "$avg": "$pageCount" },
            "totalBooks": { "$sum": 1 }
        }
    },
    {
        "$project": {
            "_id": 0,
            "category": "$_id",
            "maxPages": 1,
            "minPages": 1,
            "avgPages": 1,
            "totalBooks": 1
        }
    }
]

pprint(list(books.aggregate(pipeline)))

print("Add Year, month, day : ")
#use addFields insteadof $project
pipeline = [
       {
        "$addFields": {
            "publishedYear": { "$year": "$publishedDate" },
            "publishedMonth": { "$month": "$publishedDate" },
            "publishedDay": { "$dayOfMonth": "$publishedDate" }
        }
    },
    {
        "$match": {
            "publishedYear": { "$gt": 2009 }
        }
    },
    {
        "$limit": 20
    },

]


pprint(list(books.aggregate(pipeline)))

print("Add athorN")
pipeline = [
    {
        "$project": {
            "numAuthors": { "$size": "$authors" }
        }
    },
    {
        "$group": {
            "_id": None,
            "maxNumAuthors": { "$max": "$numAuthors" }
        }
    },
    {
        "$project": {
            "_id": 0,
            "maxNumAuthors": 1
        }
    }
]
numAuthor = list(books.aggregate(pipeline))
numAuthor = numAuthor[0]['maxNumAuthors']
newFields =  {}
for i in range(numAuthor):
    newFields['author' + str(i + 1)] = { "$arrayElemAt": ["$authors", i] }

pipeline = [
    {
        "$addFields": newFields
    },
    {
        "$sort": { "publishedDate": 1 }
    },
    {
        "$limit": 20
    }
]
pprint(list(books.aggregate(pipeline)))

print("Most plublished books by athors")

pipeline = [
    {
        "$project": {
            "firstAuthor": { "$arrayElemAt": ["$authors", 0] }
        }
    },
    {
        "$group": {
            "_id": "$firstAuthor",
            "numPublications": { "$sum": 1 }
        }
    },
    {
        "$match": {
            "_id": { "$ne": None }
        }
    },
    {
        "$sort": { "numPublications": -1 }
    },
    {
        "$limit": 10
    }
]
pprint(list(books.aggregate(pipeline)))