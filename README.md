<!-- <div align="center">
    <a href='https://www.realworldml.xyz/'><img src='./media/rwml_logo.png' width='350'></a>    
</div> -->

<div align="center">
    <h1>Develop, deploy and monitor a production-ready real-time data pipeline in Python</h1>
    <h2><a href="">Quix</a> + MLOps = 🚀</h2>
    
</div>

#### Table of contents
* [The problem](#the-problem)
* [Solution](#solution)
* [Run the whole thing in 5 minutes](#run-the-whole-thing-in-5-minutes)
* [Video lecture](#video-lecture)
* [Wanna learn more real-time ML?](#wanna-learn-more-real-time-ml)


## The problem

[TODO]

## Solution

[TODO]


## Run the whole thing in 5 minutes

1. Create an `.env` file and fill in the necessary credentials.
    ```
    $ cp .env.example .env
    ```

2. Run the pipeline locally
    ```
    $ make start
    ```

3. Stop the pipeline locally
    ```
    $ make stop
    ```

## Video lecture

[TODO]


## Wanna learn more real-time ML?

Join more than 10k subscribers to the Real-World ML Newsletter. Every Saturday morning.

[👉🏽 Click to subscribe](https://www.realworldml.xyz/subscribe)


## Next steps

- [x] Make it run on quix platform
    - [x] ProducerWrapper that works locally
    - [x] Deploy trade_producer to quix platform

- [ ] Run trade to ohlc
    - [x] Locally
    - [x] Quix platform
    - [ ] Add window operator to compute OHLC data

- [x] Save OHLC data to Feature Group
    - [x] Create feature group
    - [x] Save to online Feature Group
    - [ ] Run on Quix platform

- [ ] Streamlit dashboard.
    - [ ] FeatureView to read data from Hopsworks
    - [ ] Deploy Streamlit as container locally





