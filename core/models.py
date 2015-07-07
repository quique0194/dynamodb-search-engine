from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, JSONAttribute


class Lexema(Model):
    """
    A DynamoDB Lexema
    """
    class Meta:
        table_name = "Lexemas"
    lexema = UnicodeAttribute(hash_key=True)
    documentos = JSONAttribute(default='[]') # inverse index
    idf = NumberAttribute(default=0)


class Documento(Model):
    """
    A DynamoDB Documento
    """
    class Meta:
        table_name = "Documentos"
    id = NumberAttribute(hash_key=True)
    fecha = UnicodeAttribute(default='')
    titulo = UnicodeAttribute(default='')
    noticia = UnicodeAttribute(default='')
    url = UnicodeAttribute(default='')
    tf = JSONAttribute(default='{}')


if __name__ == '__main__':
    pass
    # Lexema.create_table(read_capacity_units=10, write_capacity_units=10)
    # Documento.create_table(read_capacity_units=15, write_capacity_units=15)

    # docs = [1,2,3]
    # lexema = Lexema("holas", documentos=docs, idf=1.2)
    # lexema.save()

    # try:
    #     lexema = Lexema.get("holas")
    #     print lexema.lexema
    #     print type(lexema.documentos)
    #     print lexema.documentos
    #     # print json.loads(lexema.documentos)
    #     print lexema.idf
    # except Lexema.DoesNotExist:
    #     print("Lexema does not exist")
    
