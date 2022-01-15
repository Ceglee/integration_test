#Integration test project

## Introduction
Currently, data processed by auction service are not as extensive as they could be. With help of additional external
APIs there is a chance to extend them with more valuable information. Thanks to that, it could make whole auction process
more accurate and simply better. 

At the moment only user's first and last name are passed in a single filed. 

### Goals
Main reason standing behind the project is to extend user details with following data:
* first name as a separate field
* last name as a separate field
* nationality
* gender
* age 

## Implementation
New API has to be created. It will reside in a standalone, dedicated http server, where whole solution will be 
written in python language.

Once created, auction service will utilize it in order to enhance user details during the auction process.

### API design
Because there is not many requirements, everything can be done in scope of a single HTTP endpoint.

#### POST /user-details
Used to collect enriched user details based on its name.

##### Request headers
|Name|Value|
|----|-----|
|Accept|application/json|
|Content-Type|application/json|

##### Request body
```json
{
  "user_name": string // not null
}
```
##### 200 Response
Sent when everything went well and service was able to enrich user details. Following body will be attached to the 
response:
```json
{
 "first_name": string, // not null
 "last_name": string, // not null
 "nationality": string, // nullable
 "age": number, // nullable
 "gender": "male"/"female" //nullable
}
```
#### 204 Response
Sent when service is not be able to collect information about all **not null** fields.

#### 422 Response
Sent when user name provided by the client is empty or null.

### Implementation details
Client will initiate process by calling **/user-details** endpoint. Following sequence diagram shows request processing flow:
![user_details_flow](./uml/user_details_flow.png)

Everything starts with a simple validation of the request body. If all goes right, then further processing will
be done by ```UserDetailsService```. It will be responsible for creating ```UserDetails``` object which will be mapped 
afterwards to a json and attached to the response as its body.

Algorithm of extracting user first name and second name will be discussed in separate paragraph.

Each request sent to the external APIs will executed in asynchronous manner. Because there is strict limit
put on the time of the whole process, main execution thread will wait at most 10 milliseconds to finish all of pending requests. 
If any of them won't be able to meet this time constraint, then http response won't be applied to the final ```UserDetails``` object.
**But still these results will be stored in cache for further upcoming requests.**

Implementation of the internal clients used in communication with the external APIs has been moved to separate
diagram. Example shown below relates to ```NationalizeClient```, but the similar flow applies to the other two.

![client_implementation](./uml/client_implementation.png)

As shown on the diagram, cache can be also populated with null values. It is a valid situation, where it means that application 
should not take any more attempts to retrieve details from external API.
This approach applies to either to empty results or 4xx type error response, which usually mean there is something 
with the client's request, which should not be resent.

### Name extraction
Application expects to receive **user_name** value in following format: *"first_name last_name"*.
If that won't happen, application will still try to resolve these value in accordance with diagram below:

![user_name_processing](./uml/user_name_processing.png)

Worth to mention here is that this logic will run after validation process, so it is assumed that **user_name** is neither 
null nor empty.

## Further improvements

### Cache shared among nodes
Implementation shown above uses only internal cache. As a next step, it could share it among multiple nodes. Thanks
to that it will fill up quicker for most common keys, and it won't consume each process's memory.

### Https protocol support
In order to support secured connection, test integration server will have to authenticate itself to the caller
(auction service in this case) with a certificate signed by CA accepted by the client. Assuming, that the only client
will be auction service, this can be achieved by adding that certificate to the trust store used by the client while
establishing secured connection.

Drawback of this approach is that it will impact response time, due to messages encryption and ssl handshake.

This feature is only required when communication between the client, and the service happens outside the internal 
network where they operate or when some third party users might have unprivileged access to it.

### Authentication & Authorization
If the only client would be auction service and assuming that https will be enabled, then the best option would be 
to use *ssl mutual authentication* in order to identify clients. This will of course impact also performance, because
application first need to get client's certificate, and check whether it accepts it. Of course this will also require
create private/public key pair for auction service.
