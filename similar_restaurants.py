#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from scipy.spatial import distance
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings("error")


restaurants = pd.read_csv('restaurants.csv', encoding='iso_8859-9')

restaurant_codes = restaurants['Restaurant_Code']

del restaurants['Restaurant_Code']


class MostSimilarK:
    def __init__(self, k):
        self.k = k
        self.n_equations = 0
        self.most_similar_k_indexes = []
        self.most_similar_k_similarities = []
        
    def add(self, row_idx, new_similarity):
        
        if not self.most_similar_k_similarities:
            self.most_similar_k_similarities = []
            self.most_similar_k_indexes = []
            
            self.most_similar_k_similarities.append(new_similarity)
            self.most_similar_k_indexes.append(row_idx)
            return
        
        for index, similarity in enumerate(self.most_similar_k_similarities):
            if new_similarity >= similarity:
                if new_similarity == similarity:
                    # Prevents cutting out any equality
                    self.n_equations += 1
                
                self.most_similar_k_similarities.insert(index, new_similarity)
                self.most_similar_k_indexes.insert(index, row_idx)
                
                # Limit number of similars
                n_most_similars = self.k + self.n_equations
                self.most_similar_k_indexes = self.most_similar_k_indexes[:n_most_similars]
                self.most_similar_k_similarities = self.most_similar_k_similarities[:n_most_similars]
                return
            
        self.most_similar_k_similarities.append(new_similarity)
        self.most_similar_k_indexes.append(row_idx)
        
        # Limit number of similars
        n_most_similars = self.k + self.n_equations
        self.most_similar_k_indexes = self.most_similar_k_indexes[:n_most_similars]
        self.most_similar_k_similarities = self.most_similar_k_similarities[:n_most_similars]
        return
                

def list_to_numerical(input_list):
    if not input_list:
        return input_list
    
    for index, value in enumerate(input_list):
        try:
            input_list[index] = int(value)
        except ValueError:
            input_list[index] = value
            
    return input_list


def similar_records(all_records, k, input_columns, similarity_metric='cosine', unknown_identifier=None):
    mostSimilars = MostSimilarK(k)
    
    for row_idx, row in all_records.iterrows():
        
        choosen_input_values = []
        choosen_record_values = []
        
        # Convert non-numerical values into numerical ones
        record_values = list_to_numerical(list(row.values.flatten()))
        
        for column_idx, input_value in enumerate(input_columns):
            record_value = record_values[column_idx]
            if input_value != unknown_identifier and record_value != unknown_identifier:
                
                choosen_input_values.append(input_value)
                choosen_record_values.append(record_value)
            
        if similarity_metric == 'cosine':
            similarity = 1 - distance.cosine(choosen_input_values, choosen_record_values)
        elif similarity_metric == 'pearson':
            try:
                similarity = pearsonr(choosen_input_values, choosen_record_values)[0]
            except Warning:
                similarity = 0
        else:
            raise Exception('Function: similar_records - Invalid similarity_metric argument.')
            
        #print(input_columns, list_to_numerical(list(record_values)), similarity, sep='\t')
        mostSimilars.add(row_idx, similarity)
    
    most_similars_data = pd.DataFrame()
    most_similars_data['index'] = mostSimilars.most_similar_k_indexes
    most_similars_data['similarity'] = mostSimilars.most_similar_k_similarities
    
    return most_similars_data

# Gives most similar restaurants with given number, criteria and similarity metric 
def similar_restaurants(n_restaurants, input_columns, similarity_metric='cosine'):
    
    similars = similar_records(all_records=restaurants, k=n_restaurants, input_columns=input_columns, similarity_metric=similarity_metric, unknown_identifier='?')

    output = []
    output.append('Code,   {} Similarity'.format(similarity_metric.capitalize()))

    for index, similarity in zip(similars['index'], similars['similarity']):
        output.append('{}  {}'.format(str(index).rjust(4), str(similarity).ljust(20)))

    return output