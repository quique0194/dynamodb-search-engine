from django.shortcuts import render
from django.http import HttpResponse

from core.models import *
from utils.proc_text import *

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

    elif request.method == 'POST':
        search = request.POST.get('search')
        lexemas = []
        for lex in proc_text(search):
            print lex
            try:
                lexema = Lexema.get(unicode(lex))
                lexemas.append(lexema)
            except Lexema.DoesNotExist:
                return render(request, "no_results.html", {
                    'search': search,
                    'msg': 'No existe el lexema ' + lex}
                )

        if len(lexemas) == 0:
            return render(request, "no_results.html", {'search': search})

        # doc_ids = None
        # for lex in lexemas:
        #     if doc_ids is None:
        #         doc_ids = set(lex.documentos)
        #     else:
        #         doc_ids = doc_ids & lex.documentos

        # doc_ids = list(doc_ids)

        doc_ids = lexemas[0].documentos[:10]
        docs = Documento.batch_get(doc_ids)
        docs = list(docs)

        context = {
            'lexemas': lexemas,
            'docs': docs,
            'search': search
        }
        return render(request, "search_result.html", context=context)

