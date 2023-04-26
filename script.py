import base64
import io
import re

with open('withImages.txt', 'r') as file:
    ct = 0
    for line in file:
        ct+=1
        print(ct)
        line = line.strip()
        if not line:
            continue

        # parse pk
        pk_unfilt = line.split('\t')[0]
        pk_match = re.match(r'(.+?)(\d+)', pk_unfilt)
        primarykey = int(pk_match.group(2))



        # parse b64
        json_data = line.split('\t')[1]
        json_data_dict = eval(json_data)

        alt_name = json_data_dict['Alt']

        content_type = json_data_dict['ContentType']
        just_b64_data = json_data_dict['Content']

        data = {
            "ContentType": content_type,
            "Content": just_b64_data
        }

        content_type, encoded_data = data["Content"].split(",", 1)
        encoded_bytes = encoded_data.encode("utf-8")
        decoded_bytes = base64.b64decode(encoded_bytes)

        # file ext
        media_type, *params = content_type.split(':')[-1].split(';')
        fileext = media_type.split('/')[-1]

        with io.BytesIO(decoded_bytes) as buffer:
            with open(f'{str(primarykey)}.{fileext}', "wb") as file:
                file.write(buffer.getbuffer())

