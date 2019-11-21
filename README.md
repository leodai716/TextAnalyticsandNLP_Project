# TextAnalyticsandNLP_Project
Application of Text Analytics and NLP in Brexit-Sentiment-Driven Financial Indicators

## Motivation 
The United Kingdom’s departure from the European Union has been delayed multiple times due to failure of political parties in reaching compromises of Brexit deal. Parliamentary approval of the bill is critical to the Brexit process. As the outcome of Brexit divorce deal has major implications to the global financial market as well as investment strategies, we particularly interested in collecting public opinions that would be reflected in the investment decision of the public.  
In this project, we will be capturing the public's sentiment through analyzing news articles of British media with Natural Language Processing Techniques. We aim to find correlations between public sentiment and market movemen.

## Steps  
1. Data collection   
2. Data preprocessing  
3. Running Machine Learning Model   
4. Applying Model to classify previous events  
5. Back test results with financial data to find correlation 

## Notes to Developer
Most, if not all, codes can be run directly with the appropriate set up outlined below:  
1. Please change the content of _LocalVariable.example.py file and rename that as _LocalVariable.py
2. Please download the lattest Data file from https://bit.ly/2XzFPMO and put data into a folder in  Data/ 

#### Parallel Computing Scripts   
Scripts involving multiprocessing, and parallel computation with GPU are labeled *_multiprocessing.py.  
Without sufficient computer resources, such code may temporarily and significantly reduce computer performance on other tasks. It is advised to use the standard scripts.   
In general, developers/ endusers are not advised to modify anything in multiprocessing scripts.  
