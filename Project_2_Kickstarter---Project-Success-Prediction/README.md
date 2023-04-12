# Kickstarter_collaboration_project

Project at neuefische-Bootcamp in Hamburg in March 2020 in collaboration with [@StefanWoBa](https://github.com/StefanWoBa)


## Summary:

In this project we aimed at finding a Machine-Learning model in order to predict whether a project on kickstarter can be successful or not. By applying different kinds of Classifying models we were able to determine the best models for this approach (namely: Random Forest, Gredient Descent Boost, Ada Boost and XGBoost).
In a last step we applied the stacking method in order to find the best predictions possible.
Our aim was to find the overall best predictions, thus our target metric was the **accuracy score**.

![alt text](https://github.com/fabwerk90/Kickstarter_collaboration_project/blob/master/picture_readme.jpeg)

## Structure of the repository:

In this repository you find the whole process of our approach. To maintain a good overview, the notebooks are splitted in the following order:

Contents:
- 1. Data Mining and Cleaning
- 2. EDA: first insights
- 3. Feature Engineering
- 4. EDA: after feature engineering
- 5. Predictive Modeling


## Background information about Kickstarter:

Kickstarter, founded in 2009, is one particularly well-known and popular crowdfunding platform. It has an all-or-nothing funding model, whereby a project is only funded if it meets its goal amount; otherwise no money is given by backers to a project. A huge variety of factors contribute to the success or failure of a project — in general, and also on Kickstarter. Some of these are able to be quantified or categorized, which allows for the construction of a model to attempt to predict whether a project will succeed or not. The aim of this project is to construct such a model and also to analyse Kickstarter project data more generally, in order to help potential project creators assess whether or not Kickstarter is a good funding option for them, and what their chances of success are.


## Business Case:

### Setup:
* We are a consultancy specialized in helping entrepreneurs & investors 
* We equip our clients with the necessary entrepreneur skillset and help them to make investment decisions via our proficiency in data science
* We launched a free online-course, where we broadly discuss all topics along the founding-process and give an outlook, to what our ML-algorithms are capable of
### Key Takeaways:
* In order to be successful with your project it is beneficial to set reasonable, smaller goals.
* On average, successful projects tend to have a shorter campaign length and more time invested in setting up the project
* Projects in the category “comics”, “dance”, “games”, “music” & “publishing” are the most successful along all categories
* Our developed algorithm can correctly predicted if a project will be successful or not in 73 out of 100 cases


## Future Work:
* Tuning the hyperparamter as well as stacking did not improve our model that much, so there is a need for additional data/ more feature engineering (also extract the years)
* Have a better look at the bias/variance tradeoff -> create learning curves for the models
* Needed to drop some columns due to completely missing data -> should be enriched with external data
* To what extent are backers influenced to pledge if the project is close to be being completely funded
* Check, in which languages the individual project descriptions are written -> possible reason for failure, since english-speaking backers can be excluded by non-english descriptions
* Instead of a classification approach, try to estimate number of backers or pledged amount with linear regression or randomforestregressor

