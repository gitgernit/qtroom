# qtroom
qtroom is a Qt-based, server-side & client-side asynchronous 
app written on python that lets you chat with anyone around 
the world in a chatroom.

### Client installation
1. Clone the repo:  
 `git clone https://github.com/gitgernit/qtroom`
2. Create a virtual environment:  
`python -m venv venv`
3. Install the requirements:  
`pip install -r requirements/client.txt`
4. Create .env and configure SERVER_HOST and SERVER_PORT:  
`cp .env.template .env`
5. Run the app!  
`python main.py`

### Server installation
! A redis server is required !
1. Clone the repo:  
   `git clone https://github.com/gitgernit/qtroom`
2. Create a virtual environment:  
   `python -m venv venv`
3. Install the requirements:  
   `pip install -r requirements/server.txt`
4. Create .env and configure all the variables:  
   `cp .env.template .env`
5. (Optional): use docker to build and run the image
 from Dockerfile
6. Run the server! Entry file is located at server/main.py

### Contribution
Pull requests & issues are warmly welcome! This repository 
is mainly an educational project & a reference for all the 
others who wonder how to build an asynchronous Qt TCP app.
