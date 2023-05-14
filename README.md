# AWS Cloud Environment Setup and Configuration

## Database Configuration

In AWS we used AWS RDS as our database of choice, with a MySQL server. To set this section ofthe project up we used the AWS console to make sure we were not provisioning more resources then we needed or had errors in the set up process.

#### Setup Information :

![Setup](images\DatabaseSetup.png)
_Default setup with a t3.micro, which keeps our deployment under the free tier_

#### Connectivity & Security :

![Security Rules](images\ConnectivitySecure.png)
_Default settings were used for security, note port 3306 and Endpoint_

#### Inbound/Outbound :

![INbound/Outbound](images\InboundOutbound.png)
_Make sure inbound and outbound are set to 0.0.0.0/0, this sets all endpounts to public for retreival_

## AWS Lambda Configuration

To create an API for our database we need to use AWS lambda as a way to query our data. Our language of choice was Python as it is supported by AWS and we all have familiarity working within it.

All files used in this portion of the project are located in the lambda folder. You will notice a lot of package files contained in this folder, as when adding a function to AWS you need to have all packages locally added before you zip the file. In this case we had to include mysql as a package for our lambda to access our data. Once the code zip file is added to our lambda function we are ready to attahc an API gateway to the database to allow our web app to grab information from the database.

![AWSLambda](images\MySQLAPI.png)
_Note the lambda is connected to the api gateway which calls it to run_

![Time To Live](images\TTLAPI.png)
_Since our lambda queries up to 90 thousands datapoints we needed to set the ttl to 50 seconds to make sure that it never timed our early_

More information on how this works within [./lambda/](./lambda/README.md)

## API Gateway Configuration

As stated earlier the API gateway is need to set up the copnnection to run our lambda queries from the web applications. In this section we set up an API gateway to attach to the lambda. It should be noted we used a Lambda Proxy for this gateway as other models need CORS configuration at all stages of the Gateway but for a Lambda function it is handled in the return statement of the as so :

```python
return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST"
            },
            "body": ""
        }
```

Our API can now be envoked at this this url, but only a POST request will retrieve the needed data.

URL : https://gfn1a5n8m7.execute-api.us-east-2.amazonaws.com/example

![ApiGateway](images\APIgate.png)

_Defualt Configuration was done besides the lambda proxy_

## AWS Amplify Configuration

This section needed the least amount of configuration or setup. As we are using github as our home for our UI and Web Application all pipelining is automated by AWS. All that was need was connectiong the database and runnning the build. AWS amplifiy also sets up that on every push the build is remade and the files are uploaded.

![ampl](images\ampl.png)
_All configuration was defaulted and set to node 14.0 as the runtime_
