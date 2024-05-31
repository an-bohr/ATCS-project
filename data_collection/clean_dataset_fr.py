'''
This code is used to aggregate samples that are identical for multiple search engines, 
to clean up the duplicate predictions from the same search engines, and filter out predictions
that do not have an adjective.
'''
import argparse
import pandas as pd
import spacy

try:
    nlp = spacy.load("fr_core_news_lg")
except OSError:
    spacy.cli.download("fr_core_news_lg")
    nlp = spacy.load("fr_core_news_lg")

def filter_duplicates(dataframe, savefile):
    df = pd.read_csv(dataframe,  encoding='utf-8', sep='\t')
    df.loc[~df.index.duplicated(), :]
    index_names = df[ (df['target_category'] == 'country') & (df['input'].str.contains('sont'))].index
    df.drop(index_names, inplace = True)
    index_names = df[ (df['target_category'] != 'country') & (df['input'].str.contains('est'))].index
    df.drop(index_names, inplace = True)
    df.dropna(inplace=True)
    df = df.loc[~df.index.duplicated(), :]
    sd = df.duplicated(subset=['input', 'target_category', 'target_group', 'completion'], keep=False)
    indices = [i for i, x in enumerate(sd.tolist()) if x == True]
    for i in indices:
        df.loc[i,'search_engine'] = 'multiple'
    df = df.drop_duplicates()
    df.to_csv(savefile, index=False,  encoding='utf-8', sep='\t')
    
def filter_multiple_word_answers(dataframe, savefile):
    df = pd.read_csv(dataframe, encoding='utf-8', sep='\t')
    # remove rows where 'completion' contains more than one word
    df = df[df['completion'].apply(lambda x: len(x.split()) == 1)]
    df.to_csv(savefile, index=False, encoding='utf-8', sep='\t')
    
def filter_adjectives(dataframe, savefile):
    nlp = spacy.load('fr_core_news_lg')
    df = pd.read_csv(dataframe, encoding='utf-8', sep='\t')
    
    def is_adjective(word):
        doc = nlp(word.strip())  # remove any spaces
        return any(token.pos_ == 'ADJ' for token in doc)
    
    df = df[df['completion'].apply(is_adjective)]
    df.to_csv(savefile, index=False, encoding='utf-8', sep='\t')
        
def main():
    '''
    Remove duplicates, multiple word answers and only keep adjectives from a csv file.
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument("--file_path", default="stereo_dataset/merged_data_fr+bing.csv", type=str, help="Path to retrieve dataset")
    parser.add_argument("--save_no_duplicates", default="stereo_dataset/cleaned_data_fr+bing.csv", type=str, help="Path to save dataset with no duplicates")
    parser.add_argument("--save_single_word_path", default="stereo_dataset/single_word_data_fr+bing.csv", type=str, help="Path to save dataset with single word answers")
    parser.add_argument("--save_adjective_path", default="stereo_dataset/adjective_data_fr+bing.csv", type=str, help="Path to save dataset with only adjectives")

    args = parser.parse_args()

    filter_duplicates(args.file_path, args.save_no_duplicates)
    filter_multiple_word_answers(args.save_no_duplicates, args.save_single_word_path)
    filter_adjectives(args.save_single_word_path, args.save_adjective_path)


if __name__ == '__main__':
    main()