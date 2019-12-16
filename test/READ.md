### Overview

Turns out commuter train schedule in Jakarta is changing from time to time, averaging 2-3 months each time. You can't be certain that there's not going to be a change between your last trip and your next one.     
So that's my excuse to try some new frameworks in a hypothetical case where a fictional startup company needs to have KRL data updated for their API needs. 

Here's the general overview of what I think their data flow in this case will look like:

![](/static/pipeline.gif)

Obviously every outbound data requests will be logged, so I left that out since I decided it's irrelevant for this exercise's scope.

#### Dependencies

I'm going to use some popular third-party modules for checking & extracting the data from KRL's pages & excel files:

* requests
* bs4
* pandas
 
Data store & API endpoint serving
      
* sqlite    
* starlette & uvicorn ASGI

---

        2019/11 first draft
