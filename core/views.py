# encoding: utf-8

import operator
import time

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

from core.models import *
from utils.proc_text import *


@csrf_exempt
def index(request):
    t0_total = time.time()
    search = request.GET.get('search') or ''
    page = request.GET.get('page') or 1
    page = int(page)
    if search == '':
        return render(request, "index.html")
    search_data = {
        'lexemas': {
            'encontrados': [],
            'no_encontrados': []
        },
        'tiempo': {}
    }
    
    # Obtener lexemas del servidor nosql
    t0 = time.time()
    lexemas = list(Lexema.batch_get(set(proc_text(search))))
    for lex in lexemas:
        if lex.lexema in search:
            search_data['lexemas']['encontrados'].append(lex)
        else:
            search_data['lexemas']['no_encontrados'].append(lex)
    search_data['tiempo']['get_lexemas'] = round(time.time() - t0, 5)

    if len(lexemas) == 0:
        return render(request, "no_results.html", {
            'search': search,
            'search_data': search_data,
            'reason': 'Las palabras escogidas no existen en el corpus',
            'possible_fix': 'Use otras palabras en su búsqueda'
        })

    # Encontrar los documentos comunes a todos los lexemas
    t0 = time.time()
    docs_sets = []
    for lex in lexemas:
        docs_sets.append(set(lex.documentos))
    docs_comunes = set.intersection(*docs_sets)
    search_data['total_resultados'] = len(docs_comunes)
    search_data['tiempo']['docs_comunes'] = round(time.time() - t0, 5)

    if len(docs_comunes) == 0:
        return render(request, "no_results.html", {
            'search': search,
            'search_data': search_data,
            'reason': 'No hay noticias que tengan todas las palabras',
            'possible_fix': 'Busque las palabras una por una'
        })

    # Encontrar relevancia de los documentos comunes
    t0 = time.time()
    doc_rel = dict(zip(docs_comunes, [1]*len(docs_comunes)))
    for lex in lexemas:
        for doc, rel in zip(lex.documentos, lex.tfidf):
            if doc_rel.has_key(doc):
                doc_rel[doc] *= rel

    # Ordenar tuplas (documento, relevancia) por 'relevancia' invertida
    sorted_doc_rel = sorted(doc_rel.items(), key=lambda x: (x[1], x[0]), reverse=True)
    search_data['tiempo']['relevancia'] = round(time.time() - t0, 5)

    # Obtener documentos de esta pagina
    t0 = time.time()
    paginator = Paginator(sorted_doc_rel, 10)
    try:
        pagina = paginator.page(page)  # pagina: sorted_doc_rel_paginator
    except PageNotAnInteger:
        pagina = paginator.page(1)
    except EmptyPage:
        pagina = paginator.page(paginator.num_pages)

    docs = Documento.batch_get([d for d, r in pagina])
    docs = list(docs)
    for d in docs:
        d.rel = doc_rel[d.id]
    docs.sort(key=lambda x: (x.rel, x.id), reverse=True)

    search_data['tiempo']['get_documentos'] = round(time.time() - t0, 5)
    search_data['tiempo']['total'] = round(time.time() - t0_total, 5)

    return render(request, "search_result.html", context={
            'search': search,
            'search_data': search_data,
            'docs': docs,
            'pagina': pagina
        })
