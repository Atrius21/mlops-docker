## Containerizing your python code to run with updated data

This example will illustrate how we can use docker to simplify the work process of updating html dashboards with just a few lines of code. While the python code that processes the data remains the same throughout the process, the only variable would be data version that is used to generate the html files. 


### Coding the main.py 


We will plotting two locations with folium using sample data. First we have to look at the dependencies required to run this python file.

1. folium
2. pandas

Since it's just a simple plot with no complicated data transformations needed, these two libraries would suffice. Below is a full sample of the main.py file. 

```python

import folium as fl
import pandas as pd

df = pd.read_csv('./datafiles/data.txt'
	, sep = '|'
	)


map_ = fl.Map(location = [df.lat.iloc[0]
						 , df.lng.iloc[0]]
	, tiles = 'cartodbpositron'
	, zoom_start = 12)

for item in df.itertuples():
	fl.Circle(location = (item.lat, item.lng)
		, color = item.color
		, weight = 3
		, radius = 100
		, popup = item.location
		, fill = True
		, fill_color = item.color
		, fill_opacity = 0.2
		).add_to(map_)



map_.save("index.html")
```


## Dockerizing the python application

Going forward all commands are run assuming you are currently within the `test-server/` directory.

```
..
└── test-server
    ├── app/
    │   └── main.py (server code)
    │   
    ├── requirements.txt (Python dependencies)
    ├── README.md (this file)
    └── Dockerfile
```


## Create the Dockerfile

The `Dockerfile` is made up of all the instructions required to build your image.


### Base Image
```Dockerfile
FROM python:3.8-slim
WORKDIR /
COPY requirements.txt ./
COPY /app ./app

RUN pip install -r requirements.txt \
	&& rm requirements.txt 


CMD ["python", "./app/main.py"]
```


The `FROM` instruction allows you to select a pre-existing image as the base for your new image. **This means that all of the software available in the base image will also be available on your own.** This is one of Docker's nicest features since it allows for reusing images when needed. 

In this case your base image is `python:3.8-slim`, let's break it down:

- `python` is its name.
- `3.8-slim` is the image's tag.

Notice that the tag let's you know that the specific version of Python being used is 3.8. Tagging is great as it allows you to create different versions of similar images. In this case you could have this same image with a different version of Python such as 3.5.


### Installing dependencies
Now that you have an environment with Python installed it is time to install all of the Python packages that your server will depend on. First you need to copy your local `requirements.txt` file into the image so it can be accessed by other processes, this can be done via the `COPY` instruction:

```Dockerfile
COPY requirements.txt .
```

Now you can use `pip` to install these Python libraries. To run any command as you would on `bash`, use the `RUN` instruction:
```Dockerfile
RUN pip install -r requirements.txt && \
	rm requirements.txt
```
Notice that two commands were chained together using the `&&` operator. After you installed the libraries specified within `requirements.txt` you don't have more use for that file so it is a good idea to delete it so the image includes only the necessary files for your server to run.

This can be done using two `RUN` instructions, however, it is a good practice to chain together commands in this manner since Docker creates a new layer every time it encounters a `RUN`, `COPY` or `ADD` instruction. This will result in a bigger image size. If you are interest in best practices for writing Dockerfiles be sure to check out this [resource](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/).



### Copying your server into the image

Now you should put your code within the image. To do this you can simply use the `COPY` instruction to copy the `app` directory within the root of the container:

```Dockerfile
COPY /app ./app
```

### Running the python file

Containers are usually meant to start and carry out a single task. This is why the `CMD` instruction was created. This is the command that will be run once a container that uses this image is started. In this case it is the command that will run the python file. Notice that the command is written in a `JSON` like format having each part of the command as a string within a list:

```Dockerfile
CMD ["python", "./app/main.py"]
```

What is meant by `JSON` like format is that Docker uses `JSON` for its configurations and the `CMD` instruction expects the commands as a list that follows `JSON` conventions.


## Build the image
Naming this image `map-gen:html-only`. 

```bash
docker build -t map-gen:html-only .
```

## Run the container

Now that the image has been successfully built it is time to run a container out of it. I'm, calling the container `my-mapgen`. You can do so by using the following command:

```bash
docker run -dit --name my-mapgen -v /Users/maxyap/Desktop/notebook-projects/machine-learning-engineering-for-production-public/course4/python-server/datafiles/:/datafiles/ map-gen:html-only
```

The objective of this container is to have docker take care of the python application while we pass in the latest data for it to produce the updated html file. We have to map a shared volume between the host and the container. This can be seen by using the `-v` command and what follows is the `source`:`host`


### Copying out the html file 
The files that are produced by the container stays inside docker. You will have to copy out the html file output to the host. It can be done with the follow commands:

```bash
docker cp my-mapgen:/index.html /Users/maxyap/Desktop/notebook-projects/machine-learning-engineering-for-production-public/course4/python-server/output/
```

### Updating the data
So lets say you have new data coming in and you would like to get the latest html files. All you have to do is copy the latest data into the datafiles folder, start the container and copy the html files out

```bash
docker start my-mapgen

docker cp my-mapgen:/index.html /Users/maxyap/Desktop/notebook-projects/machine-learning-engineering-for-production-public/course4/week2-ungraded-labs/output/
```


