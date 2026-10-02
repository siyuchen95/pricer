# Pricing Model

## Goal
We want to create a simple pricing model for cryptocurrency on major exchanges. The model is used for mid-frequency trading purposes. We are aiming for accuracy and stability.

## Models
- stage 0: start with linear regression models. Read market data feed from verified sources.
- stage 1: random forests or SG-boost. introduce some boosting and resampling techniques to shake off outliers.
- stage 2: cross-ticker and cross-exchange data. needs project "mdfeed" to develop further.

some tips to follow when seen fit:
- use EMA-weighted price to even out volatility.
- design a few technical factors, instead of always using raw market data. however, keep the technical factors simple and explainable. 

## Valuation
- we evaluate on two metrics: directional correctness and absolute value correctness. design meaningful measurements for the two metrics and get ready to export statistical statements on our pricing models (maybe several models).

## Endpoints
- verified data sources: project in ~/code/mdfeed should provide structured json market data coming from Binance (at the moment) for the ticker BTCUSDC (at the moment). Understand the pipeline there and use data from that project (or fetched by that project. as of now it is stored in a file system, but we will have moved that into a proper database in the future).
- a pipeline to read and project price predictions. can be stopped at anytime. offers possibility to backfill if data is available. 
- a simple web application that displays the historical datafeed and our current price prediction. with time, update the data points and offer simple statistics on our prediction accuracy. 
- store predictions locally. 

## Code Design
- simple, limited comments. modularised models. quick to adapt if we find more details on pricing: there could be different aspects, from market trading behavior to exchange-specific adjustments. 
- bottom line: keep very strick separation of training and testing data. make sure that we are never future-peeking.
- use a "scientist" agent to design and think about the whole model-building process: what is missing, what is working well, how does it compare to a statistical physics model (? i am a human physicist), which part seems week, and is my model explanable and elegant? is the code quality good? is the code flexible enough to incoporate new strategies? 
- use a "project manager" agent to make sure that the pricer model is in alignment with our goal: it should be reasonably accurate but also give it an acceptable range of misalignment so that the pricer is not overfitted. the project manager also reviews from a user's perspective: is the web application clear to grab information? are we hiding critical information? are we convincing on areas that we are confident with? did we disclose enough risk so that the users don't feel like they are been cheated on? is the usage of the data feed correct? how do we compare to other pricer models? why do we standout? is the code development on a good pace? 
- use a "product manager" to answer quickly questions about the pricer without diving too much into details.
- the "scientist" and the "project manager" agent should be best friends who trust each other with professional critical thinking. they can dispatch jobs to other specialised agents and update notes and memories.