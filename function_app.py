import azure.functions as func
import logging

app = func.FunctionApp()

@app.function_name(name="resume_httptrigger")
@app.route(route="hello", auth_level=func.AuthLevel.ANONYMOUS)
@app.cosmos_db_input(arg_name="inputDocument", database_name="visitsdb", container_name="visitscountainer", 
                     connection="CosmosDbConnectionSetting", sql_query="SELECT * FROM c WHERE c.id = 'visits'")
@app.cosmos_db_output(arg_name="outputDocument", database_name="visitsdb", container_name="visitscountainer", connection="CosmosDbConnectionSetting")
def count_visits(req: func.HttpRequest, inputDocument: func.DocumentList, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
     
     logging.info('Processing a new visit.')
     # the inputDocument means all the documents satisfying the query in the database.
     # therefore, in my case there is only one, which means that inputDocument is a list of 1 item.
     if not inputDocument:
         logging.error("No document found in the DB with the ID 'visits'.")
         return func.HttpResponse(
             "No visit record found. Please check the db and try again.", 
             status_code=404,
             headers={
                "Access-Control-Allow-Origin": "*",  # Allow all origins
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
             )
     # now we have got the document we need.
     document = inputDocument[0]
     current_count = document.get('count', 0)
     updated_count = current_count + 1

     # update the document with the new count
     document['count'] = updated_count
     outputDocument.set(func.Document.from_dict(document))

     # return the updated count as the response
     # Azure Function's HTTP response only takes string or json as the body
     return func.HttpResponse(
         body=str(updated_count),
         status_code=200,
         mimetype="text/plain",
         headers={
            "Access-Control-Allow-Origin": "*",  # Allow all origins
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
     )