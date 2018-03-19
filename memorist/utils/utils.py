def is_sentence(source):
    words = source.split(' ')
    if len(words) > 1:
        return True
    else:
        return False