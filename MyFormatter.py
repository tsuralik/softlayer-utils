import json

space = ' '

starting_blank_lines = 5 * "\n"
frwd_str = 70 * "/"
dash_str = 70 * "-"
back_str = 70 * "\\"

def print_program_start():
    print starting_blank_lines
    print "Program starting..."
    print back_str
    print dash_str

def print_program_end():
    print dash_str
    print frwd_str
    print "Program completed"

def print_json_listings_w_header(objects, header, text, dashCount=20):
    print_listing_delimeter(header+' start')
    for object in objects: 
        print_listing_delimeter(text+' start', 19)
        print json.dumps(object, indent=4)
        print_listing_delimeter(text+' end')
    print_listing_delimeter(header+' end')

def print_json_listings(object, text, dashCount=20):
    print_listing_delimeter(text+' start', 19)
    print json.dumps(object, indent=4)
    print_listing_delimeter(text+' end')

def print_listing_delimeter(text, dashCount=20):
    print "{0}{1}{2}{3}{4}".format('-'*dashCount, space, text, space, '-'*dashCount)

