import psycopg2
import logging
import sys
import argparse
#import ptb
#ptb.enable()

#Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets'")
logging.debug("Database connection established.")


def put(name, snippet):
    """
    Store a snippet with an associated name.
    Returns the name and the snippet
    """
    #logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    logging.info("Storing snippet {!r}: {!r})".format(name, snippet))
    cursor = connection.cursor()
    try:
        command = "insert into snippets values (%s, %s)"
        cursor.execute(command, (name, snippet))
    except psycopg2.IntegrityError as e:
        connection.rollback()
        command = "udpate snippets set message=%s where keyword=%s"
        cursor.execute(command, (snippet, name))
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet
    
def get(name):
    """Retrieve the snippet with a given name.
    If there is no such snippet... ??Initial Snippet and potential error conditions ??
    Returns the snippet.
    """
    logging.info("Selecting with keyword {!r})".format(name))
    cursor = connection.cursor()
    command = "select keyword, message from snippets where keyword=(%s)"
    cursor.execute(command, (name, ))
    row_count = 0
    for row in cursor:
        row_count += 1
        print "row: %s   %s\n" % (row_count, row)
    #return row[0]
    connection.commit()
    logging.debug("Snippet obtained successfully.")
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    #return ""



def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve of text")
    #parser.add_argument("list", help="echo the string you use here")
    #arguments = parser.parse_args(sys.argv[1:])
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    #arguments = parser.parse_args(sys.argv[1:])
    
    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="get a snippet")
    get_parser.add_argument("name", help="The keyword to get the snippet")
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