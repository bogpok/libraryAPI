# libraryAPI

## Usage
run server
```bash
uvicorn main:app --reload
```


```bash
# Depricated
curl -X POST -H "Content-Type: application/json" 'http://localhost:8000/items?item=apple'

curl -X POST -H "Content-Type: application/json" -d '{"text":"apple"}' 'http://localhost:8000/items'

curl -X GET http://localhost:8000/items/1
```

Interactive Documentation
http://127.0.0.1:8000/docs


## Objectives

- Connect mongo
- Make all possible http methods
- Draw all possible diagrams


