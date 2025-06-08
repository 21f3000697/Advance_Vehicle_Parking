from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.models import ParkingLot, ParkingSpot, Reservation

@bp.route('/')
def index():
    return render_template('main/index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    
    active_reservations = Reservation.query.filter_by(
        user_id=current_user.id,
        status='active'
    ).all()
    
    completed_reservations = Reservation.query.filter_by(
        user_id=current_user.id,
        status='completed'
    ).order_by(Reservation.end_time.desc()).limit(5).all()
    
    return render_template('main/dashboard.html',
                         active_reservations=active_reservations,
                         completed_reservations=completed_reservations)

@bp.route('/parking-lots')
@login_required
def parking_lots():
    lots = ParkingLot.query.all()
    return render_template('main/parking_lots.html', lots=lots)

@bp.route('/book-spot/<int:lot_id>', methods=['GET', 'POST'])
@login_required
def book_spot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    
    if request.method == 'POST':
        vehicle_number = request.form.get('vehicle_number')
        
        # Find first available spot
        available_spot = ParkingSpot.query.filter_by(
            lot_id=lot_id,
            status='A'
        ).first()
        
        if not available_spot:
            flash('No parking spots available in this lot.', 'error')
            return redirect(url_for('main.parking_lots'))
        
        # Create reservation
        reservation = Reservation(
            user_id=current_user.id,
            spot_id=available_spot.id,
            vehicle_number=vehicle_number
        )
        
        # Update spot status
        available_spot.status = 'O'
        
        db.session.add(reservation)
        db.session.commit()
        
        flash('Parking spot booked successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('main/book_spot.html', lot=lot)

@bp.route('/end-reservation/<int:reservation_id>')
@login_required
def end_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    
    if reservation.user_id != current_user.id:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Calculate total cost
    hours = (datetime.utcnow() - reservation.start_time).total_seconds() / 3600
    reservation.total_cost = hours * reservation.spot.lot.price_per_hour
    
    # Update reservation
    reservation.end_time = datetime.utcnow()
    reservation.status = 'completed'
    
    # Update spot status
    spot = reservation.spot
    spot.status = 'A'
    
    db.session.commit()
    
    flash('Parking spot released successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@bp.route('/reservation-history')
@login_required
def reservation_history():
    reservations = Reservation.query.filter_by(user_id=current_user.id).order_by(Reservation.start_time.desc()).all()
    return render_template('main/reservation_history.html', reservations=reservations)

@bp.route('/new-reservation')
@login_required
def new_reservation():
    return redirect(url_for('main.parking_lots')) 