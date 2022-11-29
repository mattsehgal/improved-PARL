# Improved PARL

This final project is an improvement on the algorithm of [PARL](https://www.github.com/WHUIR/PARL). Refer [here](https://www.github.com/mattsehgal/improved-PARL/blob/main/Images/modified_algo.PNG) for the algorithm modifictation and refer [here](https://www.github.com/mattsehgal/improved-PARL/blob/main/Images/parl_ep0-15.PNG) for our results comparison (both of these images are located in the Images folder).

**Statement of Work:**
<br>
I, *Matt Sehgal*, am responsible for the modified algorithm and its implementation. *[August Soderberg]*(https://www.github.com/augustsoderberg) is responsible for deriving the original PARL into a functioning version, incorporating the modified algorithm implementation into the PARL system, and performing all tests.
<br><br><br>
The README below is from the original project submission:

## COSI 150 Final Project
August Soderberg and Matt Sehgal

This is a modified implementation of the model proposed in the PARL paper (https://dl.acm.org/doi/10.1145/3269206.3271695) 
by Libing Wu, Cong Quan, Chenliang Li, and Donghong Ji. 

We have modified the data processing to generate the user auxiliary reviews using cosine similarity instead of the random
selection proposed in the paper.

HOW TO RUN:
1)  Download your Amazon 5-cores dataset and extract it to the same directory as "data_processing.py".

2)  "data_processing.py" will need to be modified to give the correct path where you would like the 7 data files to be sent
    as well as the path of the original data.

3)  In "data_processing.py" you can set the boolean value "use_cos" to be true to use our cosine similarity
    calculation in the data generation.

4)  "Parl.py" will need to be updated to look at the correct directory containing the 7 data files. 

5)  To see the implementation of standard PARL as we have tested it, you can use the "data_digital_music_random" in the
    "Parl.py" file. If you would like to compare our data processing with cosine similarity using the same model specifications,
    use the "data_digital_music_similar" directory in "Parl.py".
