from flask import Flask,render_template
from flask import request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
ratingData_pt = pickle.load(open('ratingData_pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['Number_Of_Ratings'].values),
                           rating=list(popular_df['Average_Ratings'].values)
                           )


@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def getRecommendation():
        user_input = request.form.get('user_input')
        index = np.where(ratingData_pt.index == user_input)[0][0]
        similarBooks = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
        recommendedBooks = []
        for book in similarBooks:
            bookData = []
            temp_book_df = books[books['Book-Title'] == ratingData_pt.index[book[0]]]
            bookData.extend(temp_book_df.drop_duplicates('Book-Title')['Book-Title'].values)
            bookData.extend(temp_book_df.drop_duplicates('Book-Title')['Book-Author'].values)
            bookData.extend(temp_book_df.drop_duplicates('Book-Title')['Image-URL-M'].values)

            recommendedBooks.append(bookData)
        return render_template('recommend.html',recommendedBooks=recommendedBooks)

if __name__ == '__main__':
    app.run(debug=True)