"""Supplier purchase order tracker for a stores department.

Places orders with suppliers, marks deliveries as received, notifies the
warehouse and cleans up fulfilled orders.
"""

import logging
import sqlite3

logging.basicConfig(level=logging.INFO, format="%(message)s")


def create_connection():
    """Create an in-memory database containing the orders table."""
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, supplier TEXT, item TEXT, quantity INTEGER, received INTEGER, remarks TEXT)")
    return connection


def place_order(connection, supplier, item, quantity):
    """Insert a new, not-yet-received order and return its id."""
    cursor = connection.execute("INSERT INTO orders (supplier, item, quantity, received) VALUES (?, ?, ?, 0)", (supplier, item, quantity))
    return cursor.lastrowid


def mark_received(connection, order_id, remarks):
    """Mark an order as received and store the receiving remarks."""
    connection.execute(
        "UPDATE orders SET received = 1, remarks = ? WHERE id = ?",
        (remarks, order_id),
    )


def notify_warehouse(supplier):
    """Notify the warehouse about a supplier delivery."""
    logging.info("notifying warehouse about %s", supplier)


def cleanup(connection):
    """Delete fulfilled orders; log the error if the delete fails."""
    try:
        with connection:
            connection.execute("DELETE FROM orders WHERE received = 1")
    except sqlite3.Error as err:
        logging.error("cleanup failed: %s", err)


def pending_count(connection):
    """Return the number of orders that have not been received yet."""
    return connection.execute(
        "SELECT COUNT(*) FROM orders WHERE received = 0"
    ).fetchone()[0]


def main():
    """Run a short demonstration of the order tracker."""
    connection = create_connection()
    order_total = 0
    for supplier, item, quantity in (
        ("Acme Steel", "rods", 40),
        ("Bolt Co", "bolts", 500),
    ):
        place_order(connection, supplier, item, quantity)
        order_total += quantity
    mark_received(connection, 1, "ok")
    notify_warehouse("Acme")
    print(pending_count(connection), order_total)
    cleanup(connection)


if __name__ == "__main__":
    main()