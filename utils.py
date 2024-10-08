def try_key(input,*keys):
    try:
        result = input
        for elem in keys:
            result = result[elem]
        return result
    except:
        return None
