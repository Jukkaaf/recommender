from collaborative import bookInfo

def publisherWeight(recommenderBooks, selectedBook):
    for book in recommenderBooks:
        if recommenderBooks[book]['Publisher'] == selectedBook['Publisher']:
            recommenderBooks[book]['Score'] = recommenderBooks[book]['Score'] * float(1.7)
    return recommenderBooks

def bookSimilarityWeight(recommenderBooks, selectedBook):
    return recommenderBooks