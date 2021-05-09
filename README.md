# Managed Cognito Users & Groups 

### Pre-Requistes
* Confiure AWS Credentials 
* python3

### Install Python3 Libraries
Install Required Libs
```
python3 -m pip install -r requirements.txt
```
### Set Cognito User POOL
> On Windows `set USER_POOL_ID=us-east-1_eQwtWJjpE`

> On Linux `export USER_POOL_ID="us-east-1_eQwtWJjpE"`


### Guide to configure usermap.properties

The Sections are the Cognito Groups to be created .
The `user=email` mapping under the Group will create the user under respective Group .

For Example 
```
[admin]
ashwin.naik = ashwinkumarnaik91@gmail.com
enrico.tam = etam@gmail.com

[devops]
aniket.aggarwal = aniket.aggarwal@gmail.com
```

In the Above config 
* `ashwin.naik`  & `enrico.tam` users will be created in admin group
* `aniket.aggarwal`  will be created in devops group

Hence Configure the `usermap.properties` per need  .

### Running Code 
```
python3 main.py
```