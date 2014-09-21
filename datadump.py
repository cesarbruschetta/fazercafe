from google.appengine.ext import db
import logging
import cgi
import time
import os
from google.appengine.api import datastore
from google.appengine.api import datastore_admin
from google.appengine.api import datastore_errors

SCHEMA_CACHE_TIMEOUT = 60

class DataType(object):
  """A DataType represents a data type in the datastore.

  Each DataType subtype defines four methods:

     format: returns a formatted string for a datastore value
     input_field: returns a string HTML <input> element for this DataType
     name: the friendly string name of this DataType
     parse: parses the formatted string representation of this DataType
     python_type: the canonical Python type for this datastore type

  We use DataType instances to display formatted values in our result lists,
  and we uses input_field/format/parse to generate forms and parse the results
  from those forms to allow editing of entities.
  """
  @staticmethod
  def get(value):
    return _DATA_TYPES[value.__class__]

  @staticmethod
  def get_by_name(name):
    return _NAMED_DATA_TYPES[name]

  def format(self, value):
    return str(value)

  def short_format(self, value):
    return self.format(value)

  def input_field(self, name, value, sample_values):
    if value is not None:
      string_value = self.format(value)
    else:
      string_value = ''
    return '<input class="%s" name="%s" type="text" size="%d" value="%s"/>' % (cgi.escape(self.name()), cgi.escape(name), self.input_field_size(),
            cgi.escape(string_value))

  def input_field_size(self):
    return 30

def get_kinds():
    cache = {}
    server_software = os.environ['SERVER_SOFTWARE']
    in_production = not server_software.startswith('Development')
    if in_production and ('kinds' in cache):
      if cache['kinds_timestamp'] + SCHEMA_CACHE_TIMEOUT > time.time():
        print "false"
      else:
        del cache['kinds']
    schema = datastore_admin.GetSchema()
    kinds = []
    for entity_proto in schema:
      kinds.append(entity_proto.key().path().element_list()[-1].type())
    kinds.sort()
    if in_production:
      cache['kinds'] = kinds
      cache['kinds_timestamp'] = time.time()
    return kinds

def get(requestHandler):
    request = requestHandler.request
    kind = request.get("kind")
    if not kind:
      print "false"
    query = datastore.Query(kind)
    order = None
    order_type = None
    if order and order_type:
      order_type = DataType.get_by_name(order_type).python_type()
      if order.startswith('-'):
        direction = datastore.Query.DESCENDING
        order = order[1:]
      else:
        direction = datastore.Query.ASCENDING
      try:
        query.Order((order, order_type, direction))
      except datastore_errors.BadArgumentError:
        pass
    
    start = 0
    num = 1
    total = query.Count()
    logging.info(total)
    
    entities = query.Get(start + total)[start:]
    logging.info("****************")
    for entity in entities:
        counter = 0
        requestHandler.response.out.write("insert into " + kind.lower() + " (" )
        for key, value in entity.items():
            logging.info(type(db.PostalAddress()))
            if type(value) != type(db.Key()) and value:
                #keep out heading comma
                if counter > 0: 
                    requestHandler.response.out.write(", ")
                
                requestHandler.response.out.write(key)
                counter = counter + 1
        requestHandler.response.out.write(") values (" )
        counter = 0
        for key, value in entity.items():
            if type(value) != type(db.Key()) and value:
                
                #keep out heading comma
                if counter > 0: 
                    requestHandler.response.out.write(", ")
                    
                if type(value) == type(u'') or type(value) == type(""):
                    requestHandler.response.out.write("'")
                    requestHandler.response.out.write(value.replace("'","\\'"))
                    requestHandler.response.out.write("'")
                else:
                    requestHandler.response.out.write(value)

                counter = counter + 1
        requestHandler.response.out.write(");" )
        requestHandler.response.out.write("<br><br>")
    #template_values = {
    #                   "entities" : entities, 
    #}
    #requestHandler.display('data_dump.html', template_values, __file__)
        

def post(requestHandler):
    pass
