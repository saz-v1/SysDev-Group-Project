document.addEventListener('DOMContentLoaded', function() {
    const trashIcons = document.querySelectorAll('.delete-menu-item');

    trashIcons.forEach(icon => {
        icon.addEventListener('click', function(event) {
            event.preventDefault(); 

            const menuId = icon.getAttribute('data-menu-id');
            deleteMenuItem(menuId);
        });
    });

    function deleteMenuItem(menuId) {
        fetch(`/delete_menu/${menuId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => {
            if (response.ok) {
                location.reload(); 
            } else {
                console.error('Error deleting menu item:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error deleting menu item:', error);
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const deleteLinks = document.querySelectorAll('.delete-reservation');

    deleteLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            
            const reservationId = this.getAttribute('data-reservation-id');
            
            if (confirm('Are you sure you want to delete this reservation?')) {
                fetch(`/delete_reservation/${reservationId}`, {
                    method: 'POST'
                })
                .then(response => {
                    if (response.ok) {
                        alert('Reservation deleted successfully!');
                        window.location.reload(); // Refresh the page after deletion
                    } else {
                        throw new Error('Failed to delete reservation.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Failed to delete reservation. Please try again.');
                });
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const deleteLinks = document.querySelectorAll('.delete-inventory');

    deleteLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            
            const inventoryId = this.getAttribute('data-inventory-id');
            
            if (confirm('Are you sure you want to delete this inventory item?')) {
                fetch(`/delete_inventory/${inventoryId}`, {
                    method: 'POST'
                })
                .then(response => {
                    if (response.ok) {
                        alert('Inventory item deleted successfully!');
                        window.location.reload(); // Refresh the page after deletion
                    } else {
                        throw new Error('Failed to delete inventory item.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Failed to delete inventory item. Please try again.');
                });
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const deleteLinks = document.querySelectorAll('.delete-staff-item');

    deleteLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            
            const staffId = this.getAttribute('data-staff-id');
            
            if (confirm('Are you sure you want to delete this staff member?')) {
                fetch(`/delete_staff/${staffId}`, {
                    method: 'POST'
                })
                .then(response => {
                    if (response.ok) {
                        alert('Staff member deleted successfully!');
                        window.location.reload(); // Refresh the page after deletion
                    } else {
                        throw new Error('Failed to delete staff member.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Failed to delete staff member. Please try again.');
                });
            }
        });
    });
});

document.getElementById('cancelOrderBtn').addEventListener('click', function() {
    window.location.href = "{{ url_for('index') }}";
});

