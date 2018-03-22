def is_sentence(source):
    if source[-1] == '.':
        return True

    words = source.split(' ')
    if len(words) > 2:
        return True
    else:
        return False
