# PDF Analysis: Extracting words and their word frequencies from PDF files
# 
# Scope/ Purpose: Preparation of data for performing topic analysis on annual
# reports of German car manufacturers - e.g. Volkswagen, Porsche and Audi
# Please note that words are only being extracted, stemming is not applied.
# To improve this, use nltk.stem.snowball.SnowballStemmer('german'), for example.

# Import all Python modules required for PDF analysis 
import PyPDF2
import nltk
from nltk.corpus import stopwords
  
# Create a pdf file object from a pdf file stored locally
# In the example at hand, Volkswagen's annual report 2018 is being used
pdfFilename = 'gesamt_vw_gb18.pdf'
pdfFileObj = open(pdfFilename, 'rb') 
  
# Create a pdf reader object using PyPDF2 library and
# read NLTK's default German stopwords into a variable
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
defaultStopwords = set(nltk.corpus.stopwords.words('german'))
#stemmer = nltk.stem.snowball.SnowballStemmer('german')
  
# Print the total number of pages the pdf file contains
totalNumberOfPages = pdfReader.numPages
print("Total number of pages: ", totalNumberOfPages) 

# If required, define a page (x) to start with, e.g. for skipping cover
# page, table of contents, etc. as well as a page (excludePage) to exclude
x = 7                           # Number of page to start with
excludePage = 37                # If needed, exclude a page from processing
textFromDocument = []           # Variable will contain text

# While number of page is lower than the total number of pages
# extract words from each page and store them in local variable
while x < totalNumberOfPages:

    if x != excludePage:
        # For dev it might be useful to print the number of the current page
        #print("Current Page: ", x) 

        # Create an object for the current page and extract the page's text
        pageObject = pdfReader.getPage(x) 
        pageText = pageObject.extractText()

        # Clean the text extracted - e.g. from newlines
        pageText = pageText.replace("\n", "")
        pageText = pageText.replace("\t", "")

        # User NLTK's tokenizer and extract all words/ tokens from page
        words = nltk.word_tokenize(pageText)

        # Remove single-character tokens (i.e. mostly punctuation)
        # and remove all numbers afterwards
        words = [word for word in words if len(word) > 1]
        words = [word for word in words if not word.isnumeric()]

        # Turn all words into lower case since NLTK's stopwords are
        # lower case, too. Afterwards, remove stopwords from words
        words = [word.lower() for word in words]
        #words = [stemmer.stem(word) for word in words]
        words = [word for word in words if word not in defaultStopwords]

        # Add all words extracted to textFromDocument
        textFromDocument = textFromDocument + words

    # Increase page counter
    x = x + 1 

# Calculate frequency distribution of the words extracted
frequencyDist = nltk.FreqDist(textFromDocument)

# Print most frequent words and their frequencies
numberOfWordsToPrint = 50
for textFromDocument, frequency in frequencyDist.most_common(numberOfWordsToPrint):
    print(u'{}={}'.format(textFromDocument, frequency))

# Plot frequencies of words
numberOfWordsToPlot = 25
frequencyDist.plot(numberOfWordsToPlot, cumulative=False)

# Close the pdf file object 
pdfFileObj.close() 