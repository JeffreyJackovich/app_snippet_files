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

  arguments = parser.parse_args(sys.argv[1:])

  # Convert parsed arguments from Namespace to dictionary
  arguments = vars(arguments)
  command = arguments.pop("command")

  if command == "put":
    name, snippet = put(**arguments)
    print ("Stored {!r} as {!r}".format(snippet, name))
 

if __name__ == "__main__":
    main()