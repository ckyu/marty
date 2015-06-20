# Marty

A Markov chain text generator using Python. Databases are stored in MongoDB. Default database used is called "marty".

## Usage

To parse the text
```
python markov.py <text_to_parse> <depth> <collection_name>
```

To generate a random sentence:
```
python gen.py <collection_name>
```

No infinite loop checking yet.
