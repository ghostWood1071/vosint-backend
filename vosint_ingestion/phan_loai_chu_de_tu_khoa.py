
from nlp.hieu.vosintv3_text_clustering_main.code_doan.src.update_chude import update_chude
from nlp.hieu.vosintv3_text_clustering_main.code_doan.src.create_db_chude import create_db_chude
from nlp.hieu.vosintv3_text_clustering_main.code_doan.src.create_db_linhvuc import create_db_linhvuc
from nlp.hieu.vosintv3_text_clustering_main.code_doan.src.update_linhvuc import update_linhvuc


print(create_db_chude())
print(update_chude())
print(create_db_linhvuc())
print(update_linhvuc())

from nlp.hieu.vosintv3_text_clustering_main.code_doan.src.create_db_object import create_db_object
from nlp.hieu.vosintv3_text_clustering_main.code_doan.src.update_object import update_object

create_db_object()
update_object()


