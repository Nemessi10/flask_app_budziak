from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from . import events_bp
from .forms import SportEventForm
from .models import SportEvent

@events_bp.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    form = SportEventForm()
    if form.validate_on_submit():
        event = SportEvent(
            name=form.name.data,
            description=form.description.data,
            date=form.date.data,
            category_id=form.category_id.data,
            owner_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('events.events'))

    events = SportEvent.query.filter_by(owner_id=current_user.id).order_by(SportEvent.date).all()
    return render_template('events.html', form=form, events=events)

@events_bp.route('/events/<int:event_id>')
@login_required
def event_details(event_id):
    event = SportEvent.query.get_or_404(event_id)
    if event.owner_id != current_user.id:
        flash('Access denied!', 'danger')
        return redirect(url_for('events.events'))
    return render_template('event_details.html', event=event)

@events_bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = SportEvent.query.get_or_404(event_id)
    if event.owner_id != current_user.id:
        flash('Access denied!', 'danger')
        return redirect(url_for('events.events'))

    form = SportEventForm(obj=event)
    if form.validate_on_submit():
        event.name = form.name.data
        event.description = form.description.data
        event.date = form.date.data
        event.category_id = form.category_id.data
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('events.event_details', event_id=event.id))

    return render_template('edit_event.html', form=form, event=event)

@events_bp.route('/events/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    event = SportEvent.query.get_or_404(event_id)
    if event.owner_id != current_user.id:
        flash('Access denied!', 'danger')
        return redirect(url_for('events.events'))

    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('events.events'))
