# serverlesswebsite
Worked on setting a serverless website for class work for cloud computing. I follow sample provided by AWS https://aws.amazon.com/getting-started/hands-on/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/

Issue: documentation talked adding Token Source=Authorization when added cognito as Authorizers. One should validate if browser is sending token in Authorization or authorization header and change accordingly.
An other was that document does not talk about adding mapping template in API gateway integration requestion to lambda. we need to create a template to match input of lambda function

I added lambda function in python alog with nodejs code that was provide in doc.
