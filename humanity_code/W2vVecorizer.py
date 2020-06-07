import numpy as np

## TO DO 
#  Попробовать обучить линейную модель на w2v
#  Надо попробовать в наш класс добавить PADD, UNKN 
#  Надо поробовать впихнуть tf-idf 
#  Сварить ещё одни w2v, но на основе другой модели https://rusvectores.org/ru/models/


class W2vVecorizer:
    
    def __init__(self, word2index, embedding):
        self.word2index = word2index
        self.embedding = embedding
        self.vocabulary = set()
        
        self.nice_cnt = 0
        self.all_cnt = 0 
    
    def fit(self, X):
        for text in X:
            tokens = text.split(" ")
            for tok in tokens:
                self.vocabulary.add(tok)
    
    # без PADDING
    def transform(self, X):
        X_vect = np.zeros((len(X), self.embedding.shape[1]))

        for i, text in enumerate(X):
            vect = np.zeros(self.embedding.shape[1]) # копим вектор 
            cnt = 0
            
            tokens = text.split(" ")
            for tok in tokens:
                self.all_cnt += 1
                if (tok in self.vocabulary) and (tok in self.word2index):
                    vect += self.embedding[self.word2index[tok]]
                    cnt += 1
                    self.nice_cnt += 1
            X_vect[i] = vect/cnt
        return X_vect
    
    def fit_transform(self, X):
        self.fit()
        return self.transform()
  



