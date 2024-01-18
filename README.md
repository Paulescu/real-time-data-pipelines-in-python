<!-- <div align="center">
    <a href='https://www.realworldml.xyz/'><img src='./media/rwml_logo.png' width='350'></a>    
</div> -->

<div align="center">
    <h1>Build and deploy a production-ready real-time feature pipeline in Python</h1>
    <h2>Kafka + Python = <a href="https://github.com/quixio/quix-streams">Quix Streams</a> 🚀</h2>
    
</div>

#### Table of contents
* [The problem](#the-problem)
* [Solution](#solution)
* [Run the whole thing in 5 minutes](#run-the-whole-thing-in-5-minutes)
* [Video lecture](#video-lecture)
* [Wanna learn more real-time ML?](#wanna-learn-more-real-time-ml)


## The problem

Imagine you want to build a trading bot for crypto currencies using ML.

Before you even get to work on your ML model, you need to design, develop and deploy a **real-time feature pipeline** that produces the features your model needs both at training time and at inference time.

This pipeline needs to

- Ingest raw data from an external service, like raw trades from the Kraken Websocket API.

- Transform these trades into features for your ML model, like trading indicators based on 1-minute OHLC candles, and

- Store these features in a Feature Store, so your ML models can fetch them both to generate training data, and to generate real-time predictions.

In a real-world setting, each of these steps is implemented as a separate service, and communication between these services happens through a message broker like Kafka.

[IMAGE]

This way you make your system scalable, by spinning up more containers as needed, and leveraging Kafka consumer groups.

And this is all great, but the question now is
> How do you implement this in practice?

Let's go through an example.

## Example

In this repo you have a full implementation of a production-ready real-time feature pipeline for crypto trading.

We will use [Quix Streams 2.0](https://github.com/quixio/quix-streams) which is a cloud native library for processing data in Kafka using pure Python.

With Quix Streams we get the best from both worlds:

- low-level scalability and resiliency from Apache Kafka, so our code is production-ready from day 1, and

- an easy-to-use Python interface, which makes this library extremely user-friendly for Data Scientist and ML engineers like you and me.


## Run the whole thing in 5 minutes

1. Create an `.env` file and fill in the necessary credentials to save 
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