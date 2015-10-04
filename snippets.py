import logging
import argparse
import sys
import psycopg2

#logging.debug("Connecting to PostgreSQL")
#connection = psycopg2.connect("dbname='snippets'")
#logging.debug("Database connection established.")

#Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """
    Store a snippet with an associated name.
    Returns the name and the snippet
    """
    #logging.info("Storing snippet {!r}: {!r})".format(name, snippet))
    #cursor =  connection.cursor()
    ##command = "insert into snippets values (%s, %s)"
    #cursor.execute(command, (name, snippet))
    #connection.commit()
    #logging.debug("Snippet stored successfully.")
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet
    
def get(name):
    """Retrieve the snippet with a given name.
    If there is no such snippet... Initial Snippet??
    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""

# Use positional rather than optional arguments
#python snippets.py put list "A sequence of things -  created using []"
put_v = "put"
list_v = "list"
seq_v = "A sequence of things -  created using []"

def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve of text")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    arguments = parser.parse_args(sys.argv[1:])
    
    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("name")
    get_parser.add_argument("snippet")
    
    
    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
        
    
if __name__ == "__main__":
    main()