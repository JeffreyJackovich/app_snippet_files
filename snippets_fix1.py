import psycopg2
import logging
import sys
import argparse

#set the log output file, and the log fevel
logging.basicConfig(finename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' host='localhost'")
logging.debug("Database connection established.")


def put(name, snippet):
  """ Store a snippet with an associated name."""
  logging.error("FIXME: Unimplemented - put({!r}, {!r}".format(name, snippet))
  with connection, connection.cursor() as cursor:
      try:
        command = "insert into snippets values (%s, %s)"
        cursor.execute(command, (name, snippet))
      except psycopg2.IntegrityError as e:
        connection.rollback()
        command = "update snippets set message = %s where keyword = %s"
        cursor.execute(command, (snippet, name))
  logging.debug("Snippet stored successfully")
  return name, snippet

def get(name):
  """Retrieve the snippet with the given name."""
  logging.error("FIXME: Unimplemented - get({!r})".format(name))
  with connection, connection.cursor() as cursor:
      cursor.execute("select message from snippets where keyword = %s", (name,))
      row = cursor.fetchone()
  logging.debug("Snippet successfully retrieved")
  if not row:
    return None
  else:
    return row[0]

def index():
  """Present of list of snippet names"""
  logging.error("FIXME: Unimplemented - index")
  with connection, connection.cursor() as cursor:
      cursor.execute("select keyword from snippets order by keyword")
      names = cursor.fetchall()
  return names

def search(term):
  """SEarch snippets for a specific term."""
  logging.error("FIXME: Unimplemented - search({!r})".format(term))
  with connection, connection.cursor() as cursor:
      cursor.execute("select * from snippets where message like %s", (term,))
      rows = cursor.fetchall()
  logging.debug("Snippet successfully found")
  if not rows:
    return None
  else:
    return rows

# Main
def main():
  """Main function"""
  logging.info("Constructing parser")
  parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

  subparsers = parser.add_subparsers(dest="command", help="Available commands")

  #Subparser for the put command
  logging.debug("Constructing put subparser")
  put_parser = subparsers.add_parser("put", help="Store a snippet")
  put_parser.add_argument("name", help="The name of the snippet")
  put_parser.add_argument("snippet", help="The snippet text")

  #Subparser for the get command
  logging.debug("Contructing get subparser")
  get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
  get_parser.add_argument("name", help="The name of the snippet")

  #Supbarser for the catalog command
  logging.debug("Constructing index subparser")
  catalog_parser = subparsers.add_parser("index", help="Get a list of key names")

  #Subparser for the search command
  logging.debug("Contructing search subparser")
  search_parser = subparsers.add_parser("search", help="Search snippets for specific term")
  search_parser.add_argument("term", help="The term to search for in the snippets")

  arguments = parser.parse_args(sys.argv[1:])

  # Convert parsed arguments from Namespace to dictionary
  arguments = vars(arguments)
  command = arguments.pop("command")

  if command == "put":
    name, snippet = put(**arguments)
    print ("Stored {!r} as {!r}".format(snippet, name))
  elif command == "get":
    snippet = get(**arguments)
    if snippet == None:
      print "There is no snippet with the name %s." % arguments.values()[0].upper()
    else:
      print ("Retrieved snippet: {!r}".format(snippet))
  elif command == "index":
    names = index()
    print "The following is a list of existing snippet names:"
    for name in names:
      name = name[0]
      print name
  elif command == "search":
    results = search(**arguments)
    if results == None:
      print "No snippets match the search term"
    else:
      for result in results:
        print "%s: %s" % (result[0], result[1])

if __name__ == "__main__":
    main()