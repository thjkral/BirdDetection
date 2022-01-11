# Detecting birds with a Raspberry Pi and Tensorflow - PROJECT IS IN PROGRESS
In this project I will buid a pipeline to detect the birds that visit the feeder on my balcony. This repository contains the code
I wrote. The project consists of different steps:

1. Detect motion and take a picture with the Raspberry Pi. The code for this step is made by Claude Pageau and can be found [here](https://github.com/pageauc/pi-timolo)
2. Deploy a CNN model to filter out pictures of birds.
3. Save the pictures to a database.
4. Deploy a second CNN  model to determine the species of bird.
5. Update the database

This project is still in progress and at stage 2 at the moment. For updates, follow this repository or [this](https://tomkral.nl/projects/birdDetection/birdDetection.html) article.
