COSI 150 Final Project
August Soderberg, Matt Sehgal

This is a modified implementation of the model proposed in the PARL paper (https://dl.acm.org/doi/10.1145/3269206.3271695) 
by Libing Wu , Cong Quan , Chenliang Li, and Donghong Ji. 

We have modified the data processing to generate the user auxiliary reviews using cosine similarity instead of the random
selection proposed in the paper.

HOW TO RUN:
First download your Amazon 5-cores dataset and extract it to the same directory as "data_processing.py".
"data_processing.py" will need to be modified to give the correct path where you would like the 7 data files to be sent
as well as the path of the original data.
Additionally in "data_processing.py" you can set the boolean value "use_cos" to be true to use our cosine similarity
calculation in the data generation.
Then "Parl.py" will need to be updated to look at the correct directory containing the 7 data files. 
To see the implementation of standard PARL as we have tested it, you can use the "data_digital_music_random" in the
"Parl.py" file. If you would like to compare our data processing with cosine similarity using the same model specifications,
use the "data_digital_music_similar" directory in "Parl.py".