import psycopg2
from .config import config

conn = psycopg2.connect("dbname={} user={} host={} port={} password={}".format(
    config["database"]["db"], config["database"]["user"],
    config["database"]["host"], config["database"]["port"],
    config["database"]["password"]))
