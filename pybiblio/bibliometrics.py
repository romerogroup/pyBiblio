import sys
import pandas as pd
import numpy as np
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pkg_resources
import nltk
nltk.download('stopwords')
nltk.download('punkt')


class Bibliometrics:
    '''
    This class provides a bibliometric implementation for Web of Science datasets.
    
    Members:
        - titleClean: Clean title names (remove punctuation, stopwords and numbers).
        
        - fundingClean: Clean funding agencies (remove grant number and punctuation) and group the ones with similar names.
        
        - cit_by: Computes number of citations as function of the chosen parameter.
        
        - cit_num: Computes number of citations per number of occurences in the chosen parameter.
        
        - pub_by: Computes number of publications as function of the chosen parameter.
        
        - pub_num: Computes number of publications per number of occurences in the chosen parameter.
    '''
    
    def __init__(self):
        #Sets up the dataframe used in funding agencies processing
        stream = pkg_resources.resource_stream(__package__, 'FU.csv')
        self.agencies = pd.read_csv(stream)
        self.agencies.columns = ["pre", "post"]
    
    
    def titleClean(self, TI, sep = ";"):
        ''' 
        Clean all titles in the list TI.
        
        Function called by cit_num, cit_by, pub_num and pub_by if the parameter is TI.
        
        Converts all titles to lowercase, remove punctuation, symbols and numbers, removes stopwords defined in the NLTK package and strip whitespaces.
        
        Returns a string of leftover words separated by a semicolon. 
        
        '''
        
        #if only one title or if function used on its own
        if (not isinstance(TI, pd.Series)) and (isinstance(TI, str)):
            TI = [TI]
        
        #get stop words 
        stoplist = set(stopwords.words('english'))
        #convert to lowercase
        TI = [y.lower() for y in TI] 
    
        #remove punctuation, hyperlinks, @ and &
        TI = [re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", elem) for elem in TI] 
        #remove digits
        TI = [re.sub(r"\d+", "", elem) for elem in TI]
    
        #separate words and remove the ones we don't want
        ls = []
        for x in TI:
            s = word_tokenize(x)
            filtered_sentence = [w for w in s if not w in stoplist] 
            #remove whitespace before and after a word
            filtered_sentence = [w.strip() for w in filtered_sentence]
            ls.append(sep.join(np.unique(filtered_sentence)))
            
        return ls
        
    
    def fundingClean(self, FU, sep = ";"):
        ''' 
        Clean all funding agencies in the list FU.
        
        Function called by cit_num, cit_by, pub_num and pub_by if the parameter is FU.
        
        For each element of the list, remove grant number, punctuation and symbols, strip whitespaces.
        
        Agencies are compared with known data to group similar names.
        
        Returns a list of strings in the same format as FU to keep the order.
        
        '''
        
        #if function used on its own
        if (not isinstance(FU, pd.Series)) and (isinstance(FU, str)):
            FU = [FU]
        
        post = []
        for x in FU:
            #for all observations
            #split agencies
            s = np.unique(x.split(sep))
            row = []
            for agency in s:
                #for each agency
                #remove grant numbers
                regex = re.compile("\[(.*?)\]")
                agency = re.sub(regex, "", agency)         
                #remove symbols and punctuation
                agency = re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", agency) 
                #trim whitespaces
                agency = agency.strip()
                agency = agency.upper()
                if any(pd.Series(self.agencies['pre']).isin([agency])):
                    row.append(self.agencies[self.agencies['pre']==agency].iat[0,1])
                else:
                    if len(agency)>1:
                        row.append(str(agency))
            post.append(sep.join(row))
        
        return post
    
    
    def cit_by(self, df, by, n=0, subset = [], dpc=[], sep = ";", sort=True, norm=False):
        
        '''
        Computes number of citations as function of the chosen parameter 'by'.
        
        Returns a pandas dataframe with 2 columns: value and frequency.
        
        Example: number of citations by year, number of citations per author.
        
        Parameters:
            - df is a pandas dataframe.
            - by is a string of the column name chosen.
            - n is an integer to select the n rows with largest values.
            - subset is a list of items to consider in the chosen column.
            - dpc is a list of column names to consider to remove duplicates.
            - sep is the separator (e.g. for China;USA in countries)
            - sort is a binary variable. If true, the dataframe returned is sorted by decreasing frequency value
            - norm is a binary variable. If true, frequency values are normalized by the total number of citations.
            
        '''
        
        if not by in df.columns:
            sys.exit('Column not found.')
        
        if not 'TC' in df.columns:
            sys.exit('Column TC for citations not found.')
            
        #if dpc parameter is not empty, remove duplicates
        if dpc:
            temp = df.copy()
            for x in dpc:
                if x in temp.columns:
                    temp.drop_duplicates(subset=x, keep='first', inplace=True)
                else:
                    sys.exit('Column in dpc parameter not found.')
            df = temp.reset_index(drop=True)
        
        #remove null values
        df = df.dropna(subset=[by])
        df = df.dropna(subset=['TC'])
        df = df.reset_index(drop=True)
        #isolate 
        TC = pd.Series(df['TC'])
        
        if by=='TI':
            #get clean titles
            SUB = self.titleClean(df[by], sep)
        elif by=='FU':
            #get clean funding agencies
            SUB = self.fundingClean(df[by], sep)
        else:
            SUB = pd.Series(df[by])
        
        if subset:
            #only get occurences with particular subset
            keep = []
            cit = []
            col = SUB
            if isinstance(SUB[0], str):  
                subset = [s.lower() for s in subset]
                count = 0
                for elem in col:
                    if all(w in elem.lower() for w in subset):
                        keep.append(elem)
                        cit.append(TC[count])
                    count+=1    
            else:
                count = 0
                for elem in col:
                    if elem in subset:
                        keep.append(elem)
                        cit.append(TC[count])
                    count+=1
            SUB = pd.Series(keep)
            TC = cit
    
        if isinstance(SUB[0], str):
            #if the elements are string type
            total_unwrap = []
            for x in SUB:
                ls = np.unique(x.split(sep))
                total_unwrap.append([word.strip() for word in ls])
    
            #list of unique number of authors
            uniq = np.unique([item for sublist in total_unwrap for item in sublist])
            
            #create a list with added number of citations
            total_cit = [0]*len(uniq)
            for i in range(len(total_unwrap)):
                for j in total_unwrap[i]:
                    idx = np.where(uniq == j)[0][0]
                    total_cit[idx] = total_cit[idx] + TC[i]
                
            #create final database
            result = pd.DataFrame(list(zip(uniq, total_cit)), columns=[by, 'freq'])
        
        else:
            x = pd.DataFrame(zip(SUB, np.array(TC)), columns = ['SUB', 'TC'])
            #group by the selected column
            final = x.groupby('SUB').sum()
            #create final database
            result = pd.DataFrame(final)
            result.reset_index(inplace = True)
            result.columns = [by, 'freq']
    
        #normalization
        if norm == True:
            #compute sum of citations
            sumT = sum(result['freq'])
            F = result['freq'] / sumT
            result['freq'] = F   
            
        if n != 0:
            result = result.nlargest(n,'freq').reset_index(drop=True)
        
        if sort == False:
            result = result.sort_values(by = by)
            result = result.reset_index(drop=True)
    
        return result
    
              
    def cit_num(self, df, by, n=0, subset = [], dpc = [], sep = ";", sort=True, norm=False):
        
        '''
        Computes number of citations as function of the number of occurences for chosen parameter 'by'.
        
        Returns a pandas dataframe with 2 columns: value and frequency.
        
        Example: number of citations per number of authors in a paper.
        
        Parameters:
            - df is a pandas dataframe.
            - by is a string of the column name chosen.
            - n is an integer to select the n rows with largest values.
            - subset is a list of items to consider in the chosen column.
            - dpc is a list of column names to consider to remove duplicates.
            - sep is the separator (e.g. for China;USA in countries)
            - sort is a binary variable. If true, the dataframe returned is sorted by decreasing frequency value
            - norm is a binary variable. If true, frequency values are normalized by the total number of citations.
            
        '''
    
        if not by in df.columns:
            sys.exit('Column not found.')
        
        if not 'TC' in df.columns:
            sys.exit('Column names do not match WoS tags.')
        
        #if dpc parameter is not empty, remove duplicates
        if dpc:
            temp = df.copy()
            for x in dpc:
                if x in temp.columns:
                    temp.drop_duplicates(subset=x, keep='first', inplace=True)
                else:
                    sys.exit('Column in dpc parameter not found.')
            df = temp.reset_index(drop=True)
        
        #remove null values
        df = df.dropna(subset=[by])
        df = df.dropna(subset=['TC'])
        df = df.reset_index(drop=True)
        #isolate 
        TC = pd.Series(df['TC'])
        
        if by=='TI':
            #get clean titles
            SUB = self.titleClean(df[by], sep)
        elif by=='FU':
            #get clean funding agencies
            SUB = self.fundingClean(df[by], sep)
        else:
            SUB = pd.Series(df[by])
        
        if subset:
            #only get occurences with particular subset
            keep = []
            cit = []
            col = SUB
            subset = [s.lower() for s in subset]
            count = 0
            for elem in col:
                if all(w in elem.lower() for w in subset):
                    keep.append(elem)
                    cit.append(TC[count])
                count+=1    
            SUB = pd.Series(keep)
            TC = cit
    
        #compute number of occurences
        numSUB = []
        if isinstance(SUB[0], str):
            for x in SUB:
                x = np.unique(x.split(sep))
                s = [w.strip() for w in x]
                numSUB.append(len(s))
        else: 
            sys.exit('Cannot compute number of occurences for this type of object. Please make sure this column type is string.')
    
        #list of unique number of occurences
        uniq = np.unique(numSUB)
        
        #create a list with added number of citations
        total_cit = [0]*len(uniq)
        for k in range(len(TC)):
            #find the index of number of occurences
            index = np.where(uniq == numSUB[k])[0][0]
            #add number of citations to matching number of occurences
            total_cit[index] = total_cit[index]+TC[k]
    
        #create final database
        result = pd.DataFrame(list(zip(uniq, total_cit)), columns=['num'+by, 'freq'])
    
        #normalization
        if norm == True:
            #compute sum of citations
            sumT = sum(result['freq'])
            F = result['freq'] / sumT
            result['freq'] = F   
         
        if n != 0:
            result = result.nlargest(n,'freq').reset_index(drop=True)
        
        if sort == False:
            result = result.sort_values(by = 'num'+by).reset_index(drop=True)
    
        return result
    
    
    def pub_by(self, df, by, n=0, subset = [], dpc = [], sep = ";", sort=True, norm=False):
    
        '''
        Computes number of publications for chosen parameter 'by'.
        
        Returns a pandas dataframe with 2 columns: value and frequency.
        
        Example: number of publications per year.
        
        Parameters:
            - df is a pandas dataframe.
            - by is a string of the column name chosen.
            - n is an integer to select the n rows with largest values.
            - subset is a list of items to consider in the chosen column.
            - dpc is a list of column names to consider to remove duplicates.
            - sep is the separator (e.g. for China;USA in countries)
            - sort is a binary variable. If true, the dataframe returned is sorted by decreasing frequency value
            - norm is a binary variable. If true, frequency values are normalized by the total number of citations.
            
        '''
        
        if not by in df.columns:
            sys.exit('Column not found.')
        
        #if dpc parameter is not empty, remove duplicates
        if dpc:
            temp = df.copy()
            for x in dpc:
                if x in temp.columns:
                    temp.drop_duplicates(subset=x, keep='first', inplace=True)
                else:
                    sys.exit('Column in dpc parameter not found.')
            df = temp.reset_index(drop=True)
        
        #remove null values
        df = df.dropna(subset=[by])
        df = df.reset_index(drop=True)
        
        if by=='TI':
            #get clean titles
            SUB = self.titleClean(df[by], sep)
        elif by=='FU':
            #get clean funding agencies
            SUB = self.fundingClean(df[by], sep)
        else:
            SUB = pd.Series(df[by])
        
        if subset:
            #only get occurences with particular subset
            keep = []
            col = SUB
            for elem in col:
                if all(w in elem for w in subset):
                    keep.append(elem)
            SUB = pd.Series(keep)
    
        #unwrap
        total_unwrap = []
        if isinstance(SUB[0], str):
            for x in SUB:
                for y in np.unique(x.split(sep)):
                    total_unwrap.append(y.strip())
        else:
            total_unwrap = SUB
    
        #create frequency table
        table = pd.Series(total_unwrap).value_counts()
        result = pd.DataFrame(list(zip(table.index, table)), columns=[by, 'freq'])
    
        if n != 0:
            result = result.nlargest(n,'freq').reset_index(drop=True)
        
        if sort == False:
            result = result.sort_values(by = by).reset_index(drop=True)
    
        #normalization
        if norm == True:
            #compute sum of publications
            sumT = sum(result['freq'])
            F = result['freq'] / sumT
            result['freq'] = F   
    
        return result
    
    
    def pub_num(self, df, by, n=0, subset = [], dpc = [], sep = ";",  sort=True, norm=False):
        
        '''
        Computes number of publications as function of the number of occurences for chosen parameter 'by'.
        
        Returns a pandas dataframe with 2 columns: value and frequency.
        
        Example: number of publications per number of authors in a paper.
        
        Parameters:
            - df is a pandas dataframe.
            - by is a string of the column name chosen.
            - n is an integer to select the n rows with largest values.
            - subset is a list of items to consider in the chosen column.
            - dpc is a list of column names to consider to remove duplicates.
            - sep is the separator (e.g. for China;USA in countries)
            - sort is a binary variable. If true, the dataframe returned is sorted by decreasing frequency value
            - norm is a binary variable. If true, frequency values are normalized by the total number of citations.
            
        '''
    
        if not by in df.columns:
            sys.exit('Column not found.')
        
        #if dpc parameter is not empty, remove duplicates
        if dpc:
            temp = df.copy()
            for x in dpc:
                if x in temp.columns:
                    temp.drop_duplicates(subset=x, keep='first', inplace=True)
                else:
                    sys.exit('Column in dpc parameter not found.')
            df = temp.reset_index(drop=True)
        
        #remove null values
        df = df.dropna(subset=[by])
        df = df.reset_index(drop=True)
        
        if by=='TI':
            #get clean titles
            SUB = self.titleClean(df[by], sep)
        elif by=='FU':
            #get clean funding agencies
            SUB = self.fundingClean(df[by], sep)
        else:
            SUB = pd.Series(df[by])
        
        if subset:
            #only get occurences with particular subset
            keep = []
            col = SUB
            for elem in col:
                if all(w in elem for w in subset):
                    keep.append(elem)
            SUB = pd.Series(keep)
        
        #compute number of authors
        numSUB = []
        if isinstance(SUB[0], str):
            for x in SUB:
                x = np.unique(x.split(sep))
                s = [w.strip() for w in x]
                numSUB.append(len(s))
        else: 
            sys.exit('Cannot compute number of occurences for this type of object. Please make sure this column type is string.')
    
        #create frequency table
        table = pd.Series(numSUB).value_counts()
        result = pd.DataFrame(list(zip(table.index, table)), columns=['num'+by, 'freq'])
    
        if n != 0:
            result = result.nlargest(n,'freq').reset_index(drop=True)
        
        if sort == False:
            result = result.sort_values(by = 'num'+by).reset_index(drop=True)
    
        #normalization
        if norm == True:
            #compute sum of publications
            sumT = sum(result['freq'])
            F = result['freq'] / sumT
            result['freq'] = F   
    
        return result
