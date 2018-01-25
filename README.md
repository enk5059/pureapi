# Penn State PURE Elsevier

Extract useful data and relationships from the backend API for https://pennstate.pure.elsevier.com/

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

```
pandas==0.21.1
requests==2.18.4
```

You'll also need your PURE Backend API Key handy.  We format it in the pure_config.json file using the format below.

```
{
    "apikey": "INSERT YOUR API KEY HERE"
}
```

### Installing

Once you have your dependencies installed and your API Key inserted you can run pure_api.py

Pure_API.py executes two functions.
1) Get count totals for each API endpoint. The output will be count_totals.json
2) Create a static download of all files within the backend database in JSON format organized for each endpoint.
   The last time I ran a static download, the total folder size was 3.59Gb.

## Authors

* **Robbie Fraleigh** - *Initial work* - [GitHub](https://github.com/rfraleigh)

