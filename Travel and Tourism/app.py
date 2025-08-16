from flask import Flask, render_template, request, redirect, url_for, flash
import cx_Oracle
from datetime import datetime


app = Flask(__name__)

app.config['SECRET_KEY'] = 'dbms'

# Database connection settings
DB_USERNAME = 'system'
DB_PASSWORD = 'system'
DB_DSN = 'localhost:1521/xe'  # TNS or EZConnect format like host:port/service_name

def get_db_connection():
    return cx_Oracle.connect(DB_USERNAME, DB_PASSWORD, DB_DSN)

@app.route('/')
def index():
    return render_template('index.html')

# Route to add a new user
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        userid = request.form['userid']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phonenumber = request.form['phonenumber']

        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert the user into the Users table
        cursor.execute("""
            INSERT INTO Users (Userid, Username, Password, Email, Phonenumber)
            VALUES (:userid, :username, :password, :email, :phonenumber)
        """, userid=userid, username=username, password=password, email=email, phonenumber=phonenumber)

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('view_users'))

    return render_template('add_user.html')

# Route to view all users with search functionality
@app.route('/view_users', methods=['GET', 'POST'])
def view_users():
    search_query = request.form.get('search_query', '').lower()
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch all users and filter them based on the search query
    if search_query:
        cursor.execute("""
            SELECT * FROM Users
            WHERE LOWER(Username) LIKE :search_query
            OR LOWER(Email) LIKE :search_query
            OR Phonenumber LIKE :search_query
        """, search_query=f'%{search_query}%')
    else:
        cursor.execute("SELECT * FROM Users")
    
    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('view_users.html', users=users)

# Route to update a user's details
@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch the user details to populate the form
    cursor.execute("SELECT * FROM Users WHERE Userid = :userid", (user_id,))
    user = cursor.fetchone()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phonenumber = request.form['phonenumber']

        # Update user details in the database
        cursor.execute("""
            UPDATE Users
            SET Username = :username, Password = :password, Email = :email, Phonenumber = :phonenumber
            WHERE Userid = :userid
        """, username=username, password=password, email=email, phonenumber=phonenumber, userid=user_id)

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('view_users'))

    cursor.close()
    connection.close()
    
    return render_template('update_user.html', user=user)

# Route to delete a user
@app.route('/delete_user/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Delete user from the database
    cursor.execute("DELETE FROM Users WHERE Userid = :userid", (user_id,))

    connection.commit()
    cursor.close()
    connection.close()

    flash('User has been deleted successfully!', 'success')
    return redirect(url_for('view_users'))

# Route to add a new destination
@app.route('/add_destination', methods=['GET', 'POST'])
def add_destination():
    if request.method == 'POST':
        destinationid = request.form['destinationid']
        destination_name = request.form['destination_name']
        country = request.form['country']
        rating = request.form['rating']

        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert the destination into the Destinations table
        cursor.execute("""
            INSERT INTO Destinations (Destinationid, DestinationName, Country, Rating)
            VALUES (:destinationid, :destination_name, :country, :rating)
        """, destinationid=destinationid, destination_name=destination_name, country=country, rating=rating)

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('view_destinations'))

    return render_template('add_destination.html')


# Route to add a new Trip

@app.route('/add_trip', methods=['GET', 'POST'])
def add_trip():
    if request.method == 'POST':
        tripid=request.form['tripid']
        destinationid=request.form['destinationid']
        userid=request.form['userid']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        maxparticipants = request.form['maxparticipants']

        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert the destination into the Destinations table
        cursor.execute("""
         INSERT INTO Trips (Tripid, Destinationid, Userid, startdate, enddate, maxparticipants)
            VALUES (:tripid, :destinationid, :userid, TO_DATE(:startdate, 'YYYY-MM-DD'), TO_DATE(:enddate, 'YYYY-MM-DD'), :maxparticipants)
            """, tripid=tripid, destinationid=destinationid, userid=userid, startdate=startdate, enddate=enddate, maxparticipants=maxparticipants)


        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('view_trips'))

    return render_template('add_trip.html')

# Route to delete a trip
@app.route('/delete_trip/<int:trip_id>', methods=['GET'])
def delete_trip(trip_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Delete user from the database
    cursor.execute("DELETE FROM Trips WHERE tripid = :tripid", (trip_id,))

    connection.commit()
    cursor.close()
    connection.close()

    flash('Trip has been deleted successfully!', 'success')
    return redirect(url_for('view_trips'))


# Route to add a new payment
@app.route('/add_payment', methods=['GET', 'POST'])
def add_payment():
    if request.method == 'POST':
        paymentid = request.form['paymentid']
        booking_id = request.form['booking_id']
        amount = request.form['amount']
        payment_date = request.form['payment_date']
        payment_method = request.form['payment_method']
        status = request.form['status']

        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert the payment into the Payments table
        cursor.execute("""
            INSERT INTO Payments (PaymentID,BookingID, Amount, PaymentDate, PaymentMethod, Status)
            VALUES (:paymentid,:booking_id, :amount, TO_DATE(:payment_date, 'YYYY-MM-DD'), :payment_method, :status)
        """, paymentid=paymentid,booking_id=booking_id, amount=amount, payment_date=payment_date, payment_method=payment_method, status=status)

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('view_payments'))

    return render_template('add_payment.html')

# Route to view all payments
@app.route('/view_payments')
def view_payments():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch all payments
    cursor.execute("""
        SELECT p.PaymentID, p.Amount, p.PaymentDate, p.PaymentMethod, b.BookingID, p.status
        FROM Payments p
        JOIN Bookings b ON p.BookingID = b.BookingID
    """)
    payments = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('view_payments.html', payments=payments)

# Route to update a payment details
@app.route('/update_payment/<int:payment_id>', methods=['GET', 'POST'])
def update_payment(payment_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch the user details to populate the form
    cursor.execute("SELECT * FROM Payments WHERE Paymentid = :paymentid", (payment_id,))
    payment = cursor.fetchone()

    if request.method == 'POST':
        bookingid= request.form['bookingid']
        amount= request.form['amount']
        paymentdate = request.form['paymentdate']
        paymentmethod=request.form['paymentmethod']
        status=request.form['status']

        # Update payment details in the database
        cursor.execute("""
            UPDATE Payments
            SET BookingID = :bookingid, Amount = :amount, PaymentDate = TO_DATE(:paymentdate, 'YYYY-MM-DD'), Paymentmethod = :Paymentmethod, Status = :status
            WHERE Paymentid = :paymentid
        """, bookingid=bookingid,amount=amount, paymentdate=paymentdate, paymentmethod=paymentmethod, status=status, paymentid=payment_id)

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('view_payments'))

    cursor.close()
    connection.close()
    
    return render_template('update_payment.html', payment=payment)

# Route to add a new booking
@app.route('/add_booking', methods=['GET', 'POST'])
def add_booking():
    if request.method == 'POST':
        booking_id = request.form['booking_id']
        userid = request.form['userid']
        tripid= request.form['tripid']
        booking_date = request.form['booking_date']
        status = request.form['status']
        price = request.form['price']

        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert the booking into the bookings table
        cursor.execute("""
            INSERT INTO Bookings (BookingID, UserID, TripID, BookingDate, Status, Price)
            VALUES (:booking_id, :userid, :tripid, TO_DATE(:booking_date, 'YYYY-MM-DD'), :status, :price)
        """,booking_id=booking_id, userid=userid, tripid=tripid, booking_date=booking_date, status=status, price=price)

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('view_bookings'))

    return render_template('add_booking.html')

# Route to view all bookings
@app.route('/view_bookings')
def view_bookings():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch all bookings
    cursor.execute("""
        SELECT b.BookingID, u.UserName, b.Tripid, b.Bookingdate, b.status,b.price
        FROM Bookings b
        JOIN Users u ON u.UserID = b.UserID
    """)
    bookings = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('view_bookings.html', bookings=bookings)



# Route to add a new review
@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        reviewid = request.form['reviewid']
        user_id = request.form['user_id']
        destination_id = request.form['destination_id']
        rating = request.form['rating']
        review_date = request.form['review_date']

        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert the review into the Reviews table
        cursor.execute("""
            INSERT INTO Reviews (Reviewid,UserID, DestinationID, Rating, ReviewDate)
            VALUES (:reviewid,:user_id, :destination_id, :rating, TO_DATE(:review_date, 'YYYY-MM-DD'))
        """, reviewid=reviewid,user_id=user_id, destination_id=destination_id, rating=rating, review_date=review_date)

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('view_reviews'))

    return render_template('add_review.html')

# Route to view all reviews
@app.route('/view_reviews')
def view_reviews():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch all reviews
    cursor.execute("""
        SELECT r.ReviewID, r.Rating, r.ReviewDate, u.Username, d.DestinationName
        FROM Reviews r
        JOIN Users u ON r.UserID = u.UserID
        JOIN Destinations d ON r.DestinationID = d.DestinationID
    """)
    reviews = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('view_reviews.html', reviews=reviews)

# Route to view all trips
@app.route('/view_trips')
def view_trips():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch all reviews
    cursor.execute("""
         SELECT t.tripid, t.destinationid, d.DestinationName,t.userid,t.startdate ,t.enddate, t.maxparticipants
        FROM Trips t
        JOIN Destinations d ON t.DestinationID = d.DestinationID
    """)
    trips = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('view_trips.html', trips=trips)

# Route to update a trip details
@app.route('/update_trip/<int:trip_id>', methods=['GET', 'POST'])
def update_trip(trip_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch the trip details to populate the form
    cursor.execute("SELECT * FROM Trips WHERE Tripid = :tripid", (trip_id,))
    trip = cursor.fetchone()

    if request.method == 'POST':
        destinationid = request.form['destinationid']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        maxparticipants = request.form['maxparticipants']

        # Update trip details in the database
        cursor.execute("""
            UPDATE Trips
            SET  Destinationid= :destinationid, Startdate=TO_DATE(:startdate,'YYYY-MM-DD'), Enddate = TO_DATE(:enddate,'YYYY-MM-DD'), Maxparticipants= :maxparticipants
            WHERE tripid = :tripid
        """,  destinationid=destinationid, startdate=startdate, enddate=enddate, maxparticipants=maxparticipants, tripid=trip_id)

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('view_trips'))

    cursor.close()
    connection.close()
    
    return render_template('update_trip.html', trip=trip)


# Route to add a new guide
@app.route('/add_guide', methods=['GET', 'POST'])
def add_guide():
    if request.method == 'POST':
        guideid=request.form['guideid']
        name = request.form['name']
        experience = request.form['experience']
        language = request.form['language']
        destination_id = request.form['destination_id']

        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert the guide into the Guides table
        cursor.execute("""
            INSERT INTO Guides (GuideID,Name, Experience, Language, DestinationID)
            VALUES (:guideid,:name, :experience, :language, :destination_id)
        """, guideid=guideid,name=name, experience=experience, language=language, destination_id=destination_id)

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('view_guides'))

    return render_template('add_guide.html')

@app.route('/view_guides', methods=['GET', 'POST'])
def view_guides():
    search_query = request.args.get('search', '')  # Get the search term from the URL query parameter
    
    connection = get_db_connection()
    cursor = connection.cursor()

    # SQL query to fetch guides, with search condition
    if search_query:
        # Use the LIKE operator for case-insensitive search
        cursor.execute("""
            SELECT g.GuideID, g.Name, g.Experience, g.Language, d.DestinationName
            FROM Guides g
            JOIN Destinations d ON g.DestinationID = d.DestinationID
            WHERE g.Name LIKE :search_term OR g.Language LIKE :search_term OR d.DestinationName LIKE :search_term
        """, {'search_term': f'%{search_query}%'})
    else:
        # No search query, fetch all guides
        cursor.execute("""
            SELECT g.GuideID, g.Name, g.Experience, g.Language, d.DestinationName
            FROM Guides g
            JOIN Destinations d ON g.DestinationID = d.DestinationID
        """)

    guides = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('view_guides.html', guides=guides)


# Route to view all destinations
@app.route('/view_destinations')
def view_destinations():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch all guides
    cursor.execute("""
        SELECT DestinationID, DestinationName, Country, Rating
        FROM Destinations """)
    destinations = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('view_destinations.html', destinations=destinations)

# Route to update a user's details
@app.route('/update_guide/<int:guide_id>', methods=['GET', 'POST'])
def update_guide(guide_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch the user details to populate the form
    cursor.execute("SELECT * FROM Guides WHERE Guideid = :guideid", (guide_id,))
    guide = cursor.fetchone()

    if request.method == 'POST':
       # username = request.form['username']
        experience = request.form['experience']
        language = request.form['language']
       # phonenumber = request.form['phonenumber']

        # Update guide details in the database
        cursor.execute("""
            UPDATE Guides
            SET  Experience = :experience, Language = :language
            WHERE Guideid = :guideid
        """,  experience=experience, language=language, guideid=guide_id)

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('view_guides'))

    cursor.close()
    connection.close()
    
    return render_template('update_guide.html', guide=guide)

# Route to delete a guide
@app.route('/delete_guide/<int:guide_id>', methods=['GET'])
def delete_guide(guide_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Delete user from the database
    cursor.execute("DELETE FROM Guides WHERE guideid = :guideid", (guide_id,))

    connection.commit()
    cursor.close()
    connection.close()

    flash('Guide has been deleted successfully!', 'success')
    return redirect(url_for('view_guides'))



if __name__ == '__main__':
    app.run(debug=True)
