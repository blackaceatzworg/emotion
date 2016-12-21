<h2>Supporting Scripts and Lexicon for the study "Measuring Emotion in Parliamentary Debates with Automated Textual Analysis"</h2>

This page contains scripts, data and the final lexicon used for a forthcoming study of emotional polarity in the British House of Commons.  In particular, the file (lexicon-polarity.csv) could be used as an off-the-shelf lexicon for studying sentiment in British political texts.  The lexicon was created based on the full corpus of the British Hansard for the period 1909-2013.  Details regarding the methodology appear in the text.  

If using the Please cite the study as follows (full citation and link will be updated shortly):

Rheault, Ludovic, Kaspar Beelen, Christopher Cochrane and Graeme Hirst.  2016.  "Measuring Emotion in Parliamentary Debates with Automated Textual Analysis".  PLOS ONE.

The following list describes the purpose of each script and data file.

<h2>Scripts</h2>

<b>early-hansard-parser.py</b> - Python 2.7 - A script to parse XML files of the early Hansard volumes from the UK Parliament.

<b>millbank-scraper.py</b> - Python 2.7 - A script to scrape the Millbank Systems website and retrieve Hansard volumes missing from the UK Parliament archives.

<b>modern-hansard-parser.py</b> - Python 2.7 - A script to parse XML files of the modern Hansard (post 1936), in the Political Mashup format.

<b>CoNLLSetup.java</b> - Java 8 - A custom class to use the Stanford CoreNLP library (requires CoNLLOutputter.java).

<b>remove-decorum-words.sh</b> - Bash 4.3 - A Perl-based Shell script to remove expressions required by the decorum of the House (e.g. "The Right Honourable"). 

<b>valence-shifter.R, looper.so</b> - C, R 3.2 - An R wrapper to add a valence-shifting variable to the CoNLL corpus, using C for speed.

<b>lexicon-generator.R</b> - R 3.2 - An R script to generate domain-specific lexicons based on the word vectors obtained using the Glove program.

<b>lexicon-join.py</b> - Python 2.7 - A script to perform fast SQL-type join operations on the corpus and compute polarity scores by quarter and year. 

<b>movie-classifier.py</b> - Python 2.7 - A script to assess the accuracy of machine learning models based on the movie reviews dataset. 

<b>emotion-main-models.R</b> - R 3.2 - An R script to compute graphs and empirical models.

<h2>Datasets</h2>

<b>emotion-final-y.csv</b> - Final dataset (yearly, normalized variables). 

<b>emotion-final-q.csv</b> - Final dataset (quarterly, normalized variables). 

<b>codebook.csv</b> - Description of variables in yearly and quarterly datasets. 

<b>lexicon-polarity.csv</b> - The domain-specific polarity lexicon (4200 words).
