# %%
''' Based on https://www.kaggle.com/code/prateekmaj21/fuzzywuzzy-python-library/notebook
'''


# %%
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
# %%
#string comparison

#exactly same text
fuzz.ratio('London is a big city.', 'London is a big city.')
# %%
#string comparison

#not same text
fuzz.ratio('London is a big city.', 'London is a very big city.')
# %%
#now let us do conversion of cases

a1 = "Python Program"
a2 = "PYTHON PROGRAM"
Ratio = fuzz.ratio(a1.lower(),a2.lower())
print(Ratio)
# %%
'''without lower'''
Ratio = fuzz.ratio(a1.lower(),a2)
print(Ratio)
# %%
#fuzzywuzzy functions to work with substring matching

b1 = "The Samsung Group is a South Korean multinational conglomerate headquartered in Samsung Town, Seoul."
b2 = "Samsung Group is a South Korean company based in Seoul"

Ratio = fuzz.ratio(b1.lower(),b2.lower())
Partial_Ratio = fuzz.partial_ratio(b1.lower(),b2.lower())

print("Ratio:",Ratio)
print("Partial Ratio:",Partial_Ratio)
# %%
c1 = "Samsung Galaxy SmartPhone"
c2 =  "SmartPhone Samsung Galaxy"
Ratio = fuzz.ratio(c1.lower(),c2.lower())
Partial_Ratio = fuzz.partial_ratio(c1.lower(),c2.lower())
Token_Sort_Ratio = fuzz.token_sort_ratio(c1.lower(),c2.lower())
print("Ratio:",Ratio)
print("Partial Ratio:",Partial_Ratio)
print("Token Sort Ratio:",Token_Sort_Ratio)
# %%
d1 = "Windows is built by Microsoft Corporation"
d2 = "Microsoft Windows"


Ratio = fuzz.ratio(d1.lower(),d2.lower())
Partial_Ratio = fuzz.partial_ratio(d1.lower(),d2.lower())
Token_Sort_Ratio = fuzz.token_sort_ratio(d1.lower(),d2.lower())
Token_Set_Ratio = fuzz.token_set_ratio(d1.lower(),d2.lower())
print("Ratio:",Ratio)
print("Partial Ratio:",Partial_Ratio)
print("Token Sort Ratio:",Token_Sort_Ratio)
print("Token Set Ratio:",Token_Set_Ratio)
# %%
d1 = "Windows is built by Microsoft Corporation"
d2 = "Microsoft Windows 10"


Ratio = fuzz.ratio(d1.lower(),d2.lower())
Partial_Ratio = fuzz.partial_ratio(d1.lower(),d2.lower())
Token_Sort_Ratio = fuzz.token_sort_ratio(d1.lower(),d2.lower())
Token_Set_Ratio = fuzz.token_set_ratio(d1.lower(),d2.lower())
print("Ratio:",Ratio)
print("Partial Ratio:",Partial_Ratio)
print("Token Sort Ratio:",Token_Sort_Ratio)
print("Token Set Ratio:",Token_Set_Ratio)

# %%
#fuzz.WRatio()

print("Slightly change of cases:",fuzz.WRatio('Ferrari LaFerrari', 'FerrarI LAFerrari'))
# %%
#fuzz.WRatio()

print("Slightly change of cases and a space removed:",fuzz.WRatio('Ferrari LaFerrari', 'FerrarILAFerrari'))
# %%
#uses of fuzzy wuzzy
#summary similarity

input_text="Text Analytics involves the use of unstructured text data, processing them into usable structured data. Text Analytics is an interesting application of Natural Language Processing. Text Analytics has various processes including cleaning of text, removing stopwords, word frequency calculation, and much more. Text Analytics has gained much importance these days. As millions of people engage in online platforms and communicate with each other, a large amount of text data is generated. Text data can be blogs, social media posts, tweets, product reviews, surveys, forum discussions, and much more. Such huge amounts of data create huge text data for organizations to use. Most of the text data available are unstructured and scattered. Text analytics is used to gather and process this vast amount of information to gain insights. Text Analytics serves as the foundation of many advanced NLP tasks like Classification, Categorization, Sentiment Analysis, and much more. Text Analytics is used to understand patterns and trends in text data. Keywords, topics, and important features of Text are found using Text Analytics. There are many more interesting aspects of Text Analytics, now let us proceed with our resume dataset. The dataset contains text from various resume types and can be used to understand what people mainly use in resumes. Resume Text Analytics is often used by recruiters to understand the profile of applicants and filter applications. Recruiting for jobs has become a difficult task these days, with a large number of applicants for jobs. Human Resources executives often use various Text Processing and File reading tools to understand the resumes sent. Here, we work with a sample resume dataset, which contains resume text and resume category. We shall read the data, clean it and try to gain some insights from the data."
# %%
output_text="Modern Text Analytics involves the use of unstructured text data, processing them into usable structured data. Text Analytics is an interesting application of Natural Language Processing. Text Analytics has various processes including cleaning of text, removing stopwords, word frequency calculation, and much more. Text Analytics is used to understand patterns and trends in text data. Keywords, topics, and important features of Text are found using Text Analytics. There are many more interesting aspects of Text Analytics, now let us proceed with our resume dataset. The dataset contains text from various resume types and can be used to understand what people mainly use in resumes."
# %%
Ratio = fuzz.ratio(input_text.lower(),output_text.lower())
Partial_Ratio = fuzz.partial_ratio(input_text.lower(),output_text.lower())
Token_Sort_Ratio = fuzz.token_sort_ratio(input_text.lower(),output_text.lower())
Token_Set_Ratio = fuzz.token_set_ratio(input_text.lower(),output_text.lower())

print("Ratio:",Ratio)
print("Partial Ratio:",Partial_Ratio)
print("Token Sort Ratio:",Token_Sort_Ratio)
print("Token Set Ratio:",Token_Set_Ratio)
# %%
#choosing the possible string match

#using process library

query = 'Stack Overflow'

choices = ['Stock Overhead', 'Stack Overflowing', 'S. Overflow',"Stoack Overflow"] 

print("List of ratios: ")

print(process.extract(query, choices))

print("Best choice: ",process.extractOne(query, choices))
# %%
#handling some random punctuations
g1='Microsoft Windows is good, but takes up lof of ram!!!'
g2='Microsoft Windows is good but takes up lof of ram?'
print(fuzz.WRatio(g1,g2 ))
# %%
