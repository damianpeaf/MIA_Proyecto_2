"""

STANDARD STRUCTURE:

{
  "carpeta alvaro": {
    "mia": {
      "_files": [
        {
          "file_name": "yanosale",
          "file_contents": "asfasfasfsda si sale"
        }
      ]
    },
    "_files": [
      {
        "file_name": "prueba 2",
        "file_contents": "Este es el contenido del archivo 2"
      }
    ]
  }
}

"""

"""

OWN STRUCTURE:

[
    {
        "type": "directory",
        "name": "otra",
        "content": [
            {
                "type": "directory",
                "name": "lol",
                "content": [
                    {
                        "type": "file",
                        "name": "no.txt",
                        "content": ""
                    }
                ]
            },
            {
                "type": "file",
                "name": "si.txt",
                "content": ""
            }
        ]
    },
    {
        "type": "file",
        "name": "prueba1.txt",
        "content": "Este es el contenido del archivo 1"
    }
]

"""


def convert_to_own(standard_struct):

    own_struct = []

    for folder_name, folder_content in standard_struct.items():

        if folder_name == '_files':
            for file in folder_content:
                own_struct.append({
                    'type': 'file',
                    'name': file['file_name'],
                    'content': file['file_contents']
                })
        else:
            own_struct.append({
                'type': 'directory',
                'name': folder_name,
                'content': convert_to_own(folder_content)
            })

    return own_struct


def convert_to_standard(own_struct):

    standard_struct = {}

    for item in own_struct:

        if item['type'] == 'file':
            if '_files' not in standard_struct:
                standard_struct['_files'] = []
            standard_struct['_files'].append({
                'file_name': item['name'],
                'file_contents': item['content']
            })
        else:
            standard_struct[item['name']] = convert_to_standard(item['content'])

    return standard_struct
