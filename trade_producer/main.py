import quixstreams as qx
import os

# Quix injects credentials automatically to the client.
# Alternatively, you can always pass an SDK token manually as an argument.
client = qx.QuixStreamingClient()

# Use Input / Output topics to stream data in or out of your service
consumer_topic = client.get_topic_consumer(os.environ["input"])
producer_topic = client.get_topic_producer(os.environ["output"])

# for more samples, please see samples or docs
