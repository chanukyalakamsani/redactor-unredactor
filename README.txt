The work in this repository is done for a project in Text Analysis class instructed by Dr. Grant.

This is the third text analytics PROJECT: PROJECT2

And the first edit to the README file.

====> Description of the project:

Project2 deals with unredacting and entity resolution. A large movie review dataset from IMDB is provided. The dataset contains IMDB movie reviews and ratings. The dataset is split evenly into 25 k train and 25k test and the overall set is balanced, with 25 k positives and 25k negative reviews. It also has 50k unlabeled documents. In the entire dataset no more than 30 reviews are present for any given movie. Also the train and test sets are disjoint set of movies. A negative review has a score less than 4 and a positive review has a score greater than 7.

=====> Feature Selection Extraction

The key task here is to predict the name from a redacted file. For that first the feature for a word has to be selected . The redacted items are going to be the names in the reviews. Using ne.chunk function from nltk the persons were selected from the tokenized text.  The key features which are selected are the count of words in the name eg. Marlo Futures are 2 words in one name.

Second feature is the total no of character in the name. eg Marlo Futures have 12 characters in the name

The rest of the features are the no. of character in each word of the name. For example Doctor Matthew Skinner Tyler is a name with four words. Doctor has length 6 Matthew has length 7 Skinner has 7 and Tyler has length 5. These lengths are the features. If the name only has 2 words then the rest of the features lengths for word 3 nd 4 are defualted to zero.

Features like words in front or back of the name, thier lengths and the length of the documents are all redundant features and have no influence on predicting the name of the person and hence not used.

====> Model Training

The features were stored into Xtrain dataframe and names in Ytrain dataframe. 
Naive Bayes was used to train the model since it is the simplest and fatest and most popular machine learning algorithm for text analytics.

Also k-means nearest neighbour algorithm was applied to obtain the 5 closest names predicted for the redacted name.

Only 501 text files were selected since using more than 501 caused error as mentioned in the bugs section and also took more time to train.

====> Redaction

Using ne.chunk the persons were found from the tokenized text. These name were redacted using full block character. But the unredaction part was difficult since regular expression did not support unicode character hence one of the least used character Q was used for redaction of names. These redacted files were saved in Test 2 folder. Redacted files from Test 2 folder were read and these redacted terms were easily detected because of using Q as a redacting character. The features of the redacted terms were obtained.

====> Prediction

Models were applied on the test dataset to predict the names just based on the extracted features from these test texts. The accuracy for both kmeans and Naive Bayes was zero.

====> Distance measures.

Euclidean Distance and cosine distance was also calcuated betweeen the test name to other train names and nearest 5 from the train names were chosen.
Since both distance measures are significantly different in value they were normalized and added together to get extra feature to compare and correspondingly nearest names from the train set were chosen.

====> Result Discussion

Since the test and train sets are disjoint sets of movies the probability of names being repeated in them are low unless all the actors acted in all the movies. And hence its almost impossible to predict the names accurately. Hence we get the accuracy of zero.


=> How to run the code:
The code is built in Jupyter notebook and hence the code file needs to be placed in the folder with the test and train folders which contain the text files for training and testing and simply run the code. Running the file in jupyter Notebook will be the optimum.

====> Bugs:
ne.chunk sometimes detects indivudal names in a name such as Marlo and Futures separately for Marlo Futures. While in the redacted file we are assuming that if the redacted terms are consecutive then they form only one name of the person. Hence when we try to use the unredacted file to find the names we obtain 12 names instead of 10 (as for 2 of the names are distributed into 4). Maybe a better person tag identifie could be used which would provide a single name Marlo Futures instead of 2 different names Marlo and Futures.

It is assumed that a name consists of 3 words. First name Second Name and Third name. And for some cases the Dr. or Mr. in front of the name is counted as part of the name by ne. chunk and hence 4 words are selected but for cases there maybe more words than 4 in a name detected by ne.chunk. the case might be Detective Mr. Marlo Adam Futures. Here there are 5 words and hence during creation of the dataframe error occurs since the rows would not match if there is an extra character. The selected test and train file works for the current configuration and hence more number of test files were not used in case they contained 5 word names.
Top 501 positive files from train folder for training dataset and top 3 positive files from test folder for test dataset.
 

====>Inspirations: 

https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.linalg.norm.html
https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.distance.cosine.html
https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.distance.euclidean.html
https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
https://scikit-learn.org/stable/modules/naive_bayes.html
-----------------------------