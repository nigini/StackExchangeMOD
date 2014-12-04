StackExchangeMOD
================

MOD = Modification

This project aims to provide an environment where researchers can build experiments using online StackExchange data and API.

Dependencies
===
(For SCRIPTS)
  1- Py-StackExchange
  2- pymongo (and Mongo)
(For BACKEND API)
  3- django
  4- djangorestframework

Experiments
===

The basic steps we plan to use:
  1- greb needed data via an offline script, digest it, and store it in a MongoDB
  2- design your experiment user interfaces using the stored data and beautiful viz
  3- let participants play (and save relevant data to your experiment)
  4- when possible, give them nice feedback
  5- go process the data and write some paper ;)
