import os
#determinar tamanho do arquivo.file

def show_file_size(size):
    kb= size/1024
    mb= size/1024
    print('The file size in -')
    print('Bytes: {}'.format(size))
    print("Kilobytes (KB): {0:.2f}".format(kb))
    print("Megabytes (MB): {0:.2f}".format(mb))

    file_path = r"C:\Users\Lucas®\OneDrive\Área de Trabalho\CursoJS"

    size= os.stat(file_path).st_size
    show_file_size



