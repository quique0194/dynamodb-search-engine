#!/usr/bin/env python
# encoding: utf-8

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string
import re

signos_puntuacion = string.punctuation + '¿¡'

# remover signos de puntuación
def remove_punctuation ( text ):
    return re.sub('[%s]' % re.escape(signos_puntuacion), ' ', text)


def proc_text(text):
    s = remove_punctuation(text)
    ls = word_tokenize(s)
    
    # remover stop words
    sw = set(stopwords.words('spanish'))
    ls = filter(lambda x: x not in sw, ls)

    # lematizar
    stemmer = SnowballStemmer('spanish')
    ls = map(lambda x: stemmer.stem(x), ls)
    return ls


if __name__ == "__main__":
    s = u"""
    Hóla Adolf Hitlera (Braunau am Inn, 20 de abril de 1889-Berlín, 30 de abril de 1945) fue el Führer —presidente— y canciller de Alemania entre 1933 y 1945. Llevó al poder al Partido Nacionalsocialista Obrero Alemán o Partido Nazi,b y lideró un régimen totalitario durante el periodo conocido como Tercer Reich o Alemania nazi. Además, fue quien dirigió a Alemania durante la Segunda Guerra Mundial, iniciada por él con el propósito principal de cumplir sus planes expansionistas en Europa.
Hitler se afilió al Partido Obrero Alemán, precursor del Partido Nazi, en 1919, y se convirtió en líder de este en 1921. En 1923, tras el pronunciamiento en la cervecería Bürgerbräukeller de Múnich, Hitler intentó una insurrección, conocida como el Putsch de Múnich, tras cuyo fracaso fue condenado a cinco años de prisión. Durante su estancia en la cárcel redactó la primera parte de su libro Mi lucha (en alemán, Mein Kampf), en el cual expone su ideología junto con elementos autobiográficos. Liberado ocho meses después, en 1924, Hitler consiguió obtener creciente apoyo popular mediante la exaltación del pangermanismo, el antisemitismo y el anticomunismo, sirviéndose de su talento oratorio apoyado por la eficiente propaganda nazi y las concentraciones de masas cargadas de simbolismo.
        """

    print proc_text(s)

