# Photo Studio

This repository aims to provide a web based photo generation and editing tool. 

# Quirks

Using xformers v0.0.18 prevents upscaling unless the initial resolution is <192x192.

Installing xformers==0.0.17 allows upscaling with an initial resolution of 256x256