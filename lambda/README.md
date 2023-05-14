## LambdaSQL

In our function we wanted to limit the amount of use our Lambda had to make sure it was as secure as possible. For this we limited the REQUEST types it acceptes to just POST as we need a body to retrieve the desired data. This is achieved by checking the event and seeing if the request is a POST and if so then proceeding with the queries. If the Request does meet the required POST then we look through and grab the data given in the request body and return. 




#### Format for request body
Query Data showcases what information you want to provide for a query and function asks which query you would like to perform from our 5 premade SQL Queries. 
```
const data = {
  "query_data": {
    "table":null,
    "disease":null,
    "week":null,
    "year":null,
    "state":null
  },
  "function": {
    "number":1
  }
};
```

