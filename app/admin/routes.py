from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.admin import bp
from app.models import User, ParkingLot, ParkingSpot, Reservation
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_lots = ParkingLot.query.count()
    total_spots = ParkingSpot.query.count()
    available_spots = ParkingSpot.query.filter_by(status='A').count()
    total_users = User.query.filter_by(is_admin=False).count()
    active_reservations = Reservation.query.filter_by(status='active').count()
    parking_lots = ParkingLot.query.all()
    
    return render_template('admin/dashboard.html',
                         total_lots=total_lots,
                         total_spots=total_spots,
                         available_spots=available_spots,
                         total_users=total_users,
                         active_reservations=active_reservations,
                         parking_lots=parking_lots)

@bp.route('/parking-lots')
@login_required
@admin_required
def parking_lots():
    lots = ParkingLot.query.all()
    return render_template('admin/parking_lots.html', lots=lots)

@bp.route('/parking-lot/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_parking_lot():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        address = request.form.get('address')
        pin_code = request.form.get('pin_code')
        price = float(request.form.get('price'))
        max_spots = int(request.form.get('max_spots'))
        
        lot = ParkingLot(
            name=name,
            prime_location_name=location,
            address=address,
            pin_code=pin_code,
            price_per_hour=price,
            maximum_spots=max_spots
        )
        db.session.add(lot)
        db.session.commit()
        
        # Create parking spots
        for i in range(max_spots):
            spot = ParkingSpot(lot_id=lot.id, spot_number=i+1)
            db.session.add(spot)
        db.session.commit()
        
        flash('Parking lot created successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/new_parking_lot.html')

@bp.route('/parking-lot/edit/<int:lot_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    
    if request.method == 'POST':
        lot.name = request.form.get('name')
        lot.prime_location_name = request.form.get('location')
        lot.address = request.form.get('address')
        lot.pin_code = request.form.get('pin_code')
        lot.price_per_hour = float(request.form.get('price'))
        new_max_spots = int(request.form.get('max_spots'))
        
        # Update number of spots if changed
        if new_max_spots != lot.maximum_spots:
            if new_max_spots > lot.maximum_spots:
                # Add new spots
                for i in range(lot.maximum_spots, new_max_spots):
                    spot = ParkingSpot(lot_id=lot.id, spot_number=i+1)
                    db.session.add(spot)
            else:
                # Remove excess spots if they're not occupied
                spots_to_remove = ParkingSpot.query.filter_by(
                    lot_id=lot.id,
                    status='A'
                ).order_by(ParkingSpot.spot_number.desc()).limit(
                    lot.maximum_spots - new_max_spots
                ).all()
                
                if len(spots_to_remove) < (lot.maximum_spots - new_max_spots):
                    flash('Cannot reduce spots - some are currently occupied.', 'error')
                    return redirect(url_for('admin.edit_parking_lot', lot_id=lot.id))
                
                for spot in spots_to_remove:
                    db.session.delete(spot)
            
            lot.maximum_spots = new_max_spots
        
        db.session.commit()
        flash('Parking lot updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/edit_parking_lot.html', lot=lot)

@bp.route('/parking-lot/delete/<int:lot_id>')
@login_required
@admin_required
def delete_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    
    # Check if any spots are occupied
    occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').first()
    if occupied_spots:
        flash('Cannot delete parking lot - some spots are currently occupied.', 'error')
        return redirect(url_for('admin.dashboard'))
    
    db.session.delete(lot)
    db.session.commit()
    
    flash('Parking lot deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/users.html', users=users)

@bp.route('/reservations')
@login_required
@admin_required
def reservations():
    reservations = Reservation.query.order_by(Reservation.start_time.desc()).all()
    return render_template('admin/reservations.html', reservations=reservations) 